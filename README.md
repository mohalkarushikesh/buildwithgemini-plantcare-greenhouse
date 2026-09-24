# PlantCare Greenhouse Assistant 🌿

A production-ready conversational AI agent and web application built with Google Agent Development Kit (ADK) and deployed to **Google Cloud Run**.

---

## 🌐 Public Live Application

- **Live Public App (Google Cloud Run)**: [https://plantcare-frontend-597874512082.us-east4.run.app](https://plantcare-frontend-597874512082.us-east4.run.app)
- **GitHub Repository**: [https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse](https://github.com/mohalkarushikesh/buildwithgemini-plantcare-greenhouse)

---

## 💡 Sample Questions & Prompts

Try asking the agent any of the following sample queries in the web chat:

### 1. 🪴 Catalog Management & Inspection
> *"List all plants currently in our greenhouse catalog and show the watering frequency for Monstera Deliciosa."*

### 2. 🎨 Visual Diagnostics & Imagen Generation
> *"Generate a high-quality visual photo of a healthy Monstera Deliciosa plant thriving in bright indirect sunlight."*

### 3. 🧮 Soil Moisture Calculations & Inventory Math
> *"We have 15 Monsteras requiring 450ml water twice a week, and 12 Snake Plants needing 200ml once a week. Calculate total monthly water consumption in liters using Python."*

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

## 🏗️ Architecture & Features

- **Model Engine**: Gemini 2.5 Flash via Google Cloud Vertex AI (`google-genai`).
- **Catalog Database**: Native Cloud Firestore (`plants` collection).
- **Media Storage**: Public Google Cloud Storage Bucket (`gs://plantcare-media-qwiklabs-gcp-02-99845fbbae24`).
- **Code Execution**: `AgentEngineSandboxCodeExecutor` for safe server-side Python math execution.
- **Visual Interface**: FastAPI proxy with built-in A2UI card renderer.
- **Deployment**: Google Cloud Run in `us-east4`.

---

## 🛠️ Local Development

### Requirements
- Python 3.11+
- `uv` package manager (`uv sync`)

### Test Chat Endpoint Locally
```bash
curl -s -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "List all plants in our catalog"}'
```
