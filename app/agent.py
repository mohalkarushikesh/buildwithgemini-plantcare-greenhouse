import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.tools import (
    list_plants,
    get_plant,
    add_plant,
    diagnose_plant_health,
    calculate_fertilizer_dosage,
    get_greenhouse_climate_stats,
)
from app.image_tool import generate_plant_image
from app.a2ui_utils import a2ui_callback

MODEL = "gemini-2.5-flash"
PROJECT_ID = "qwiklabs-gcp-02-99845fbbae24"
LOCATION = "us-east4"

async def generate_memories_callback(callback_context: CallbackContext):
    """Callback after turn execution to persist important details into long-term Memory Bank."""
    await callback_context.add_session_to_memory()
    return None

instruction = """You are PlantCare Greenhouse Assistant, an expert AI botanist and greenhouse catalog supervisor.

Your mission is to assist plant enthusiasts, greenhouse managers, and customers with:
1. Catalog Management: Search, list, inspect, and add indoor plants in the Firestore catalog using `list_plants`, `get_plant`, and `add_plant`.
2. Plant Health Diagnostics: Diagnose plant symptoms, leaf spot issues, or watering stress using `diagnose_plant_health`.
3. Climate & Environmental Telemetry: Check real-time greenhouse temperature, humidity, and Lux light intensity with `get_greenhouse_climate_stats`.
4. Fertilizer & Water Calculations: Compute liquid fertilizer N-P-K dilutions and soil moisture requirements using `calculate_fertilizer_dosage` or Python code execution.
5. Visual Plant Generation: Generate images of plants using `generate_plant_image` when requested. Return the generated public image URL.
6. Personalized Memory: Remember user preferences, plant collection details, and watering schedules across sessions.

Always maintain a warm, knowledgeable, and helpful tone. Format responses neatly with markdown tables, bullet points, and highlight key metrics.
"""

code_executor = AgentEngineSandboxCodeExecutor(
    project=PROJECT_ID,
    location=LOCATION,
)

root_agent = Agent(
    name="plantcare_greenhouse",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        list_plants,
        get_plant,
        add_plant,
        diagnose_plant_health,
        calculate_fertilizer_dosage,
        get_greenhouse_climate_stats,
        generate_plant_image,
        PreloadMemoryTool(),
    ],
    code_executor=code_executor,
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
