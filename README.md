# PlantCare Greenhouse Assistant 🌿

A production-ready conversational AI agent and web application built with Google Agent Development Kit (ADK) and deployed to **Google Cloud Run**.

---

## 🎨 User Interface Preview

![PlantCare Greenhouse Assistant UI](ui_screenshot.png)

---

## 🌐 Public Live Application

- **Live Public Web App (Google Cloud Run)**: [https://plantcare-frontend-597874512082.us-east4.run.app](https://plantcare-frontend-597874512082.us-east4.run.app)
- **GitHub Repository**: [https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse](https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse)

---

## ✨ Features & Tools

1. **🪴 Greenhouse Catalog Management**: Real-time Cloud Firestore integration (`list_plants`, `get_plant`, `add_plant`).
2. **🩺 Plant Health Diagnostics**: Instant disease, pest, and watering diagnosis (`diagnose_plant_health`).
3. **🌡️ Climate & Environmental Telemetry**: Real-time greenhouse sensor tracking for temp, humidity %, Lux light, CO2, and soil pH (`get_greenhouse_climate_stats`).
4. **🧪 Fertilizer & Liquid Dosage Math**: Calculates N-P-K fertilizer dilutions based on pot size and growth season (`calculate_fertilizer_dosage`).
5. **🖼️ Imagen 3 Image Generation**: Creates realistic visual imagery of healthy indoor plants (`generate_plant_image`).
6. **🧮 Server-Side Code Execution**: Executes Python code for soil moisture schedules via `AgentEngineSandboxCodeExecutor`.
7. **💡 Interactive Quick Chips & Typing Animations**: Enhanced UI with click-to-run prompt chips and smooth typing indicators.

---

## 💡 Sample Questions & Prompts

### 🪴 1. Catalog Inspection & Watering Schedules
> *"List all plants currently in our greenhouse catalog and check watering schedules."*

---

### 🩺 2. Plant Health Diagnostics
> *"My Monstera has yellowing leaves with brown spots, please diagnose its health issue."*

---

### 🌡️ 3. Greenhouse Climate Telemetry
> *"Check real-time greenhouse climate telemetry stats."*

---

### 🧪 4. Fertilizer Dilution Calculations
> *"Calculate fertilizer dosage for 15 plants in 8-inch pots for spring/summer."*

---

### 🖼️ 5. Visual Diagnostics & Imagen Generation
> *"Generate a high-quality visual photo of a healthy Monstera Deliciosa plant thriving in bright indirect sunlight."*

---

## 🖥️ Running as a Local Daemon Service

You can run the web application continuously in the background on your local workstation.

### Start Daemon Service
```bash
./start_daemon.sh
```
*App will run continuously on `http://localhost:8080` (or `http://0.0.0.0:8080`).*

### Stop Daemon Service
```bash
./stop_daemon.sh
```

---

## 🏗️ Architecture & Stack

- **Model Engine**: Gemini 2.5 Flash via Google Cloud Vertex AI (`google-genai`).
- **Catalog Database**: Native Cloud Firestore (`plants` collection).
- **Media Storage**: Public Google Cloud Storage Bucket (`gs://plantcare-media-qwiklabs-gcp-02-99845fbbae24`).
- **Code Execution**: `AgentEngineSandboxCodeExecutor` for safe server-side Python math execution.
- **Visual Interface**: FastAPI proxy with built-in A2UI card renderer.
- **Deployment**: Google Cloud Run in `us-east4`.
