# PlantCare Greenhouse Suite 🌿 — All-in-One Botanical Solution

A production-ready conversational AI agent and web application built with Google Agent Development Kit (ADK) and deployed to **Google Cloud Run**.

---

## 🎨 User Interface Preview

![PlantCare Greenhouse Assistant UI](ui_screenshot.png)

---

## 🌐 Public Live Application

- **Live Public Web Suite (Google Cloud Run)**: [https://plantcare-frontend-597874512082.us-east4.run.app](https://plantcare-frontend-597874512082.us-east4.run.app)
- **GitHub Repository**: [https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse](https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse)

---

## 🌟 All-in-One Features & Tools (12 Botanical Tools)

1. **🪴 Catalog Management**: Cloud Firestore houseplant catalog (`list_plants`, `get_plant`, `add_plant`).
2. **🩺 Health Diagnostics**: Symptom root cause & care treatment plans (`diagnose_plant_health`).
3. **🪴 Soil Mix Recipe & Repotting**: Chunky aroid/succulent volume % breakdown (`get_soil_mix_recipe`).
4. **🌱 Seed & Stem Propagation**: Cutting nodes, moss substrates, & heat mat settings (`plan_propagation`).
5. **🐛 Pest Treatment Protocols**: Neem oil recipes & isolation schedules for spider mites/thrips (`lookup_pest_treatment`).
6. **🌞 Grow Light Timer Math**: LED DLI, PPFD height, & daily photoperiod hours (`calculate_grow_light_schedule`).
7. **🌡️ Climate & Sensor Telemetry**: Real-time greenhouse temp, humidity %, Lux, CO2, & soil pH (`get_greenhouse_climate_stats`).
8. **🚿 Smart Drip Irrigation**: Solenoid valve timers for greenhouse zones (`schedule_irrigation_task`).
9. **🧪 Liquid Fertilizer Dosage**: N-P-K dilution ratios for active growing vs dormant seasons (`calculate_fertilizer_dosage`).
10. **📊 Executive Operations Report**: Valuation ($), inventory count, & health index (`export_greenhouse_report`).
11. **🖼️ Imagen 3 Image Generation**: Realistic AI plant photo rendering (`generate_plant_image`).
12. **🧮 Server-Side Code Execution**: Python sandbox for soil moisture schedule calculations (`AgentEngineSandboxCodeExecutor`).

---

## 💡 Quick Sample Prompts

- 🪴 **Catalog**: *"List all plants currently in our greenhouse catalog and check watering schedules."*
- 🩺 **Diagnostics**: *"My Monstera has yellowing leaves with brown spots, please diagnose its health issue."*
- 🪴 **Soil Mix**: *"Calculate custom chunky soil mix recipe for a tropical aroid in an 8-inch pot."*
- 🌱 **Propagation**: *"Generate step-by-step stem cutting propagation plan for Monstera Deliciosa."*
- 🐛 **Pest Protocol**: *"Look up treatment protocol for spider mites on indoor houseplants."*
- 🌞 **Grow Light**: *"Calculate supplemental LED grow light hours for medium-light Monstera with 6 hours natural light."*
- 🚿 **Irrigation**: *"Schedule smart drip irrigation for Zone 1 for 15 minutes every 3 days."*
- 📊 **Executive Report**: *"Export an executive greenhouse inventory and health report summary."*
- 🖼️ **Imagen 3**: *"Generate an image of a vibrant Golden Pothos trailing house plant in bright sunlight."*

---

## 🖥️ Running as a Local Daemon Service

```bash
./start_daemon.sh   # Runs continuously on http://localhost:8080
./stop_daemon.sh    # Stops background service
```

---

## 🏗️ Architecture & Stack

- **Model Engine**: Gemini 2.5 Flash via Google Cloud Vertex AI (`google-genai`).
- **Catalog Database**: Native Cloud Firestore (`plants` collection).
- **Media Storage**: Public Google Cloud Storage Bucket (`gs://plantcare-media-qwiklabs-gcp-02-99845fbbae24`).
- **Code Execution**: `AgentEngineSandboxCodeExecutor` for safe server-side Python math execution.
- **Visual Interface**: FastAPI proxy with built-in A2UI card renderer.
- **Deployment**: Google Cloud Run in `us-east4`.
