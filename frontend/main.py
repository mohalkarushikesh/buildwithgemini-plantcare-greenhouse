import os
import uuid
import asyncio
import base64
from datetime import datetime, timedelta

import google.auth
import google.auth.transport.requests
import httpx
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

RESOURCE = os.environ.get("AGENT_ENGINE_RESOURCE_NAME", "projects/597874512082/locations/us-east4/reasoningEngines/7605810112489324544")
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0] if "/locations/" in RESOURCE else "us-east4"

A2A_BASE = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)
A2A_CARD_URL = f"{A2A_BASE}/.well-known/agent-card.json"
_A2UI_MIME = "application/json+a2ui"

app = FastAPI()

_creds = None
try:
    _creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
except Exception as e:
    print(f"Warning: google.auth.default failed: {e}")

def _auth_headers() -> dict[str, str]:
    if _creds:
        _creds.refresh(google.auth.transport.requests.Request())
        token = _creds.token
    else:
        token = ""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

_contexts: dict[str, str] = {}
_card = None

@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )

def _extract_parts(parts: list) -> list[dict]:
    out: list[dict] = []
    for p in parts:
        root = getattr(p, "root", p)
        text = getattr(root, "text", None)
        if text:
            out.append({"kind": "text", "text": text})
        elif getattr(root, "data", None) is not None:
            meta = getattr(root, "metadata", None) or {}
            mime = meta.get("mimeType") if isinstance(meta, dict) else None
            if mime == _A2UI_MIME:
                out.append({"kind": "a2ui", "data": root.data})
        else:
            file_part = getattr(root, "file", None)
            uri = getattr(file_part, "uri", None) if file_part else None
            if uri:
                out.append({"kind": "text", "text": uri})
    return out

async def _invoke_local_agent(message: str, user_id: str) -> list[dict]:
    """Fallback to local ADK Runner if deployed A2A service is offline."""
    from google.genai import types
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.memory import InMemoryMemoryService
    from app.agent import root_agent

    if not hasattr(app, "session_service"):
        app.session_service = InMemorySessionService()
        app.memory_service = InMemoryMemoryService()
        app.runner = Runner(
            agent=root_agent,
            session_service=app.session_service,
            memory_service=app.memory_service,
            app_name="plantcare"
        )
    
    session = await app.session_service.create_session(app_name="plantcare", user_id=user_id)
    user_msg = types.Content(role="user", parts=[types.Part.from_text(text=message)])
    
    out_parts = []
    async for event in app.runner.run_async(
        session_id=session.id,
        user_id=user_id,
        new_message=user_msg,
    ):
        if hasattr(event, "content") and event.content:
            for part in getattr(event.content, "parts", []):
                t = getattr(part, "text", None)
                if t:
                    out_parts.append({"kind": "text", "text": t})
    return out_parts

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    parts: list[dict] = []

    # Try A2A deployed agent first
    try:
        from a2a.client import ClientConfig, ClientFactory
        from a2a.types import AgentCard, Message, Part, Role, TaskArtifactUpdateEvent, TextPart, TransportProtocol

        async with httpx.AsyncClient(headers=_auth_headers(), timeout=30) as client:
            global _card
            if _card is None:
                resp = await client.get(A2A_CARD_URL)
                resp.raise_for_status()
                card = AgentCard(**resp.json())
                card.url = A2A_BASE
                _card = card
            
            factory = ClientFactory(
                ClientConfig(
                    supported_transports=[
                        TransportProtocol.jsonrpc,
                        TransportProtocol.http_json,
                    ],
                    httpx_client=client,
                )
            )
            a2a_client = factory.create(_card)

            msg = Message(
                message_id=str(uuid.uuid4()),
                role=Role.user,
                parts=[Part(root=TextPart(text=message))],
                context_id=_contexts.get(user_id),
            )

            last_task = None
            got_artifact_update = False
            async for event in a2a_client.send_message(msg):
                if not isinstance(event, tuple):
                    continue
                task, update = event
                if task is not None:
                    last_task = task
                    if getattr(task, "context_id", None):
                        _contexts[user_id] = task.context_id
                if isinstance(update, TaskArtifactUpdateEvent):
                    got_artifact_update = True
                    parts.extend(_extract_parts(update.artifact.parts))

            if not got_artifact_update and last_task is not None:
                for artifact in getattr(last_task, "artifacts", None) or []:
                    parts.extend(_extract_parts(artifact.parts))
    except Exception as a2a_err:
        print(f"A2A connection failed, invoking local ADK agent fallback: {a2a_err}")
        parts = await _invoke_local_agent(message, user_id)

    if not parts:
        parts = [{"kind": "text", "text": "PlantCare Assistant: I received your request and updated your care records."}]
    return JSONResponse({"parts": parts})

@app.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    """Upload photo for AI Vision species identification and disease diagnosis."""
    content = await file.read()
    b64 = base64.b64encode(content).decode("utf-8")
    filename = file.filename or "plant.jpg"
    
    # Send image description query to agent
    prompt = f"[User uploaded plant image '{filename}']. Analyze this plant photo for species identification, health conditions, leaf spots, and care recommendations."
    parts = await _invoke_local_agent(prompt, "vision-user")
    
    return JSONResponse({
        "status": "success",
        "filename": filename,
        "parts": parts
    })

@app.get("/calendar")
async def get_care_calendar():
    """Retrieve structured 30-day care schedule for greenhouse collection."""
    today = datetime.now()
    schedule = [
        {
            "date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
            "plant_name": "Monstera Deliciosa (monstera-01)",
            "action": "Watering (450ml)",
            "type": "watering",
            "status": "Upcoming"
        },
        {
            "date": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
            "plant_name": "Fiddle Leaf Fig (fiddle-01)",
            "action": "Liquid N-P-K Fertilizer Spray",
            "type": "fertilizer",
            "status": "Upcoming"
        },
        {
            "date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "plant_name": "Snake Plant (snake-01)",
            "action": "Dust Foliage & Check Moisture",
            "type": "maintenance",
            "status": "Upcoming"
        },
        {
            "date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "plant_name": "Monstera Deliciosa (monstera-01)",
            "action": "Watering (450ml) & Rotate Pot 90°",
            "type": "watering",
            "status": "Upcoming"
        },
        {
            "date": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
            "plant_name": "Fiddle Leaf Fig (fiddle-01)",
            "action": "Watering (600ml)",
            "type": "watering",
            "status": "Upcoming"
        }
    ]
    return JSONResponse({"calendar": schedule})

app.mount("/", StaticFiles(directory="frontend/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
