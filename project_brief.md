# My agent: PlantCare Greenhouse Assistant

One-liner: A conversational agent that helps plant enthusiasts care for their indoor greenhouse with a catalog of house plants, watering schedules, generated plant diagnostics, and care advice.

Tool coverage:
- Memory: User plant preferences, home lighting conditions, and watering history
- Tools: Firestore plant catalog read/write, watering schedule calculator, live weather lookup for outdoor care
- Catalog/UI: House plants collection (rendered as A2UI cards and stock tables)
- Image gen: Custom plant health diagnostics and visual plant portraits using gemini-3.1-flash-lite-image
- Sandbox: Python calculation of soil moisture drop rates and customized fertilizer dosage

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch: code sandbox for calculations, Cloud Storage for media assets, FastAPI Cloud Run frontend
