import os
from google.cloud import firestore
from google.api_core.client_options import ClientOptions

# Hardcode project ID to avoid project number resolution issues in Agent Platform
PROJECT_ID = "qwiklabs-gcp-02-99845fbbae24"

def get_firestore_client():
    options = ClientOptions(quota_project_id=PROJECT_ID)
    return firestore.Client(project=PROJECT_ID, client_options=options)

def list_plants() -> list[dict]:
    """Retrieve all house plants in the greenhouse catalog from Firestore.
    
    Returns:
        List of dictionaries containing plant details (id, name, species, price, light_requirements, watering_interval_days, in_stock, description).
    """
    db = get_firestore_client()
    docs = db.collection("plants").stream()
    plants = []
    for doc in docs:
        plant_data = doc.to_dict()
        plants.append(plant_data)
    return plants

def get_plant(plant_id: str) -> dict:
    """Retrieve details for a specific house plant by its ID.
    
    Args:
        plant_id: Unique string identifier for the plant (e.g., 'monstera-01', 'fiddle-01').
        
    Returns:
        Dictionary with plant information if found, or an error message dict.
    """
    db = get_firestore_client()
    doc = db.collection("plants").document(plant_id).get()
    if doc.exists:
        return doc.to_dict()
    return {"error": f"Plant with ID '{plant_id}' not found."}

def add_plant(
    id: str,
    name: str,
    species: str,
    price: float,
    light_requirements: str,
    watering_interval_days: int,
    description: str
) -> dict:
    """Add a new house plant to the greenhouse catalog in Firestore.
    
    Args:
        id: Unique identifier for the plant (e.g. 'pothos-01').
        name: Common plant name (e.g. 'Golden Pothos').
        species: Botanical species name.
        price: Price in USD.
        light_requirements: Light condition recommendation.
        watering_interval_days: Recommended watering cycle frequency in days.
        description: Short overview of care and plant characteristics.
        
    Returns:
        Confirmation dictionary with saved plant record.
    """
    db = get_firestore_client()
    plant_data = {
        "id": id,
        "name": name,
        "species": species,
        "price": price,
        "light_requirements": light_requirements,
        "watering_interval_days": watering_interval_days,
        "in_stock": True,
        "stock_count": 10,
        "description": description
    }
    db.collection("plants").document(id).set(plant_data)
    return {"status": "success", "message": f"Added {name} to catalog.", "plant": plant_data}
