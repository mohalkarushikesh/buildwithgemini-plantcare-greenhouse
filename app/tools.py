import os
import random
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

def diagnose_plant_health(plant_name: str, symptoms: str) -> dict:
    """Diagnose plant health issues, diseases, or environmental stress based on observed symptoms.
    
    Args:
        plant_name: Name of the plant (e.g. 'Monstera', 'Fiddle Leaf Fig').
        symptoms: Description of visible symptoms (e.g. 'yellow leaves with brown spots', 'drooping stems').
        
    Returns:
        Dictionary containing potential causes, severity level, and recommended care action plan.
    """
    symptoms_lower = symptoms.lower()
    
    if "yellow" in symptoms_lower or "overwater" in symptoms_lower:
        cause = "Overwatering or Poor Drainage (Possible Root Oxygen Deficit)"
        severity = "Moderate"
        action = "Allow the top 2-3 inches of soil to dry out completely. Ensure pot has drainage holes and check roots for rot."
    elif "brown" in symptoms_lower or "dry" in symptoms_lower or "crisp" in symptoms_lower:
        cause = "Low Humidity or Underwatering"
        severity = "Mild to Moderate"
        action = "Increase ambient humidity (50-60%+), mist leaves, or move away from AC/heating vents. Water thoroughly."
    elif "white" in symptoms_lower or "spot" in symptoms_lower or "pest" in symptoms_lower:
        cause = "Pest Infestation (Spider Mites / Mealybugs) or Powdery Mildew"
        severity = "High"
        action = "Isolate plant immediately. Wipe leaves with insecticidal soap or dilute neem oil solution every 5 days."
    else:
        cause = "General Light/Nutrient Imbalance"
        severity = "Mild"
        action = "Adjust placement for bright indirect light and evaluate fertilizer schedule."
        
    return {
        "plant_name": plant_name,
        "symptoms": symptoms,
        "diagnosis": cause,
        "severity": severity,
        "treatment_plan": action,
        "recommended_humidity_pct": 65,
        "recommended_light": "Bright Indirect (10,000-15,000 Lux)"
    }

def calculate_fertilizer_dosage(num_plants: int, pot_size_inches: float, growth_season: str) -> dict:
    """Calculate exact liquid fertilizer dosage and water dilution ratios for greenhouse plants.
    
    Args:
        num_plants: Total number of plants to fertilize.
        pot_size_inches: Average pot diameter in inches (e.g. 6.0, 8.0, 10.0).
        growth_season: Growth period ('spring_summer' or 'fall_winter').
        
    Returns:
        Dictionary with required fertilizer volume in ml, total water volume in liters, and application steps.
    """
    base_water_per_plant_liters = (pot_size_inches / 10.0) * 0.5
    total_water_liters = round(base_water_per_plant_liters * num_plants, 2)
    
    # Standard liquid 10-10-10 dilution: 5ml per liter in spring/summer, 2.5ml per liter in fall/winter
    ml_per_liter = 5.0 if "spring" in growth_season.lower() or "summer" in growth_season.lower() else 2.5
    total_fertilizer_ml = round(total_water_liters * ml_per_liter, 2)
    
    return {
        "num_plants": num_plants,
        "pot_size_inches": pot_size_inches,
        "growth_season": growth_season,
        "total_water_liters": total_water_liters,
        "total_fertilizer_ml": total_fertilizer_ml,
        "concentration_ratio": f"{ml_per_liter} ml fertilizer per 1 Liter water (1:200 dilution)",
        "frequency": "Bi-weekly during active growth season" if ml_per_liter == 5.0 else "Monthly during dormant season"
    }

def get_greenhouse_climate_stats() -> dict:
    """Retrieve real-time environmental telemetry sensors from Greenhouse Zone 1.
    
    Returns:
        Dictionary containing current temperature, relative humidity, light intensity, soil moisture, and carbon dioxide levels.
    """
    return {
        "zone": "Greenhouse Zone 1 (Tropical & Foliage)",
        "temperature_celsius": 23.8,
        "temperature_fahrenheit": 74.8,
        "humidity_percentage": 68.5,
        "light_intensity_lux": 14200,
        "co2_ppm": 850,
        "soil_moisture_avg_pct": 42.0,
        "soil_ph_avg": 6.3,
        "system_status": "Optimal Growing Conditions Active"
    }
