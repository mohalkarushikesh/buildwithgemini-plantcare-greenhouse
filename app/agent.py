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
    schedule_irrigation_task,
    export_greenhouse_report,
    plan_propagation,
    get_soil_mix_recipe,
    calculate_grow_light_schedule,
    lookup_pest_treatment,
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

instruction = """You are PlantCare Greenhouse Assistant, an All-in-One AI Botanical & Greenhouse Suite.

You provide end-to-end plant care, greenhouse automation, and catalog solutions:
1. Catalog Management: Search, list, inspect, and add indoor plants in the Firestore catalog using `list_plants`, `get_plant`, and `add_plant`.
2. Health & Pest Treatment: Diagnose symptoms with `diagnose_plant_health` and look up organic pest protocols using `lookup_pest_treatment`.
3. Climate & Environmental Telemetry: Track real-time greenhouse sensors (temp, humidity, Lux, soil pH) with `get_greenhouse_climate_stats`.
4. Smart Drip Irrigation: Schedule automated solenoid valves using `schedule_irrigation_task`.
5. Soil Mix & Repotting Recipes: Calculate custom chunky soil mix volume breakdowns using `get_soil_mix_recipe`.
6. Propagation & Seed Planning: Create stem cutting & seed germination guides using `plan_propagation`.
7. Grow Light Photoperiod Math: Calculate LED supplemental light hours and DLI using `calculate_grow_light_schedule`.
8. Liquid Fertilizer Calculations: Compute N-P-K dilutions using `calculate_fertilizer_dosage` or Python code execution.
9. Executive Reporting: Export valuation, plant health index, and catalog summaries using `export_greenhouse_report`.
10. Visual Plant Generation: Generate images of plants using `generate_plant_image` when requested. Return the public image URL.
11. Personalized Memory: Remember user preferences, plant collection details, and care schedules across sessions.

Always maintain a warm, knowledgeable, and professional tone. Format responses neatly with markdown tables, bullet points, and key metrics.
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
        schedule_irrigation_task,
        export_greenhouse_report,
        plan_propagation,
        get_soil_mix_recipe,
        calculate_grow_light_schedule,
        lookup_pest_treatment,
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
