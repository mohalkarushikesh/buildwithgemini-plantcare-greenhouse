FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir uvicorn fastapi google-auth httpx "a2a-sdk>=0.3.0" google-adk google-genai google-cloud-firestore google-cloud-storage pillow

COPY . .

ENV PORT=8080
ENV GOOGLE_GENAI_USE_VERTEXAI=true
ENV GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-02-99845fbbae24
ENV GOOGLE_CLOUD_LOCATION=us-east4
ENV PYTHONPATH=/app

CMD ["python", "frontend/main.py"]
