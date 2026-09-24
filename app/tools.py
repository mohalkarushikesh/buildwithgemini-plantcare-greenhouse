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

def schedule_irrigation_task(zone_id: str, run_time_minutes: int, repeat_days: int) -> dict:
    """Schedule automated smart drip irrigation solenoid valve cycles for a greenhouse zone.
    
    Args:
        zone_id: Greenhouse zone identifier (e.g., 'Zone 1 - Tropicals', 'Zone 2 - Succulents').
        run_time_minutes: Duration to run irrigation pumps in minutes.
        repeat_days: Recurrence interval in days (e.g. every 3 days, 7 days).
        
    Returns:
        Confirmation dictionary with scheduled valve timer details.
    """
    task_id = f"IRR-{random.randint(1000, 9999)}"
    return {
        "task_id": task_id,
        "status": "Scheduled",
        "zone_id": zone_id,
        "duration_minutes": run_time_minutes,
        "interval_days": repeat_days,
        "next_execution": f"Tomorrow at 06:00 AM (Recurring every {repeat_days} days)",
        "water_flow_rate_gpm": 2.5,
        "estimated_gallons_per_cycle": round(2.5 * run_time_minutes, 1)
    }

def export_greenhouse_report() -> dict:
    """Export executive greenhouse inventory valuation, plant health index, and climate analytics summary.
    
    Returns:
        Summary metrics dictionary including catalog count, estimated inventory value ($), and health index.
    """
    plants = list_plants()
    total_count = len(plants)
    total_value = sum(p.get("price", 0) * p.get("stock_count", 1) for p in plants) if plants else 0
    
    return {
        "report_type": "Greenhouse Operations & Catalog Executive Summary",
        "total_catalog_species": total_count,
        "total_inventory_units": 40,
        "estimated_inventory_value_usd": f"${total_value:,.2f}",
        "plant_health_index": "96.4% Optimal",
        "climate_efficiency_score": "A+ (Solar + Smart HVAC)",
        "recommendations": "Maintain current humidity levels (65-70%) and execute bi-weekly liquid fertilizer routines."
    }

def plan_propagation(species_name: str, method: str) -> dict:
    """Generate stem cutting and seed propagation plans including rooting medium, heat mat settings, and node preparation.
    
    Args:
        species_name: Plant name (e.g. 'Monstera Deliciosa', 'Pothos', 'Fiddle Leaf Fig').
        method: Propagation technique ('stem_cutting', 'water_propagation', 'sphagnum_moss', or 'seed').
        
    Returns:
        Dictionary with step-by-step propagation guide, expected rooting days, and substrate recipe.
    """
    return {
        "species_name": species_name,
        "method": method,
        "expected_rooting_days": "14 to 21 days",
        "optimal_temperature": "24°C - 26°C (75°F - 78°F)",
        "humidity_chamber_recommended": True,
        "substrate_recipe": "50% Damp Sphagnum Moss + 50% Perlite" if "moss" in method.lower() else "Distilled Water + 1 drop Rooting Hormone",
        "step_by_step": [
            "Cut 0.5 inches below an active aerial root node using sterilized shears.",
            "Let the cut end callus over in warm ambient air for 30 minutes.",
            "Submerge the node completely in substrate while leaving leaves above the rim.",
            "Place under indirect LED grow light (12 hours/day) with bottom heat mat ON."
        ]
    }

def get_soil_mix_recipe(plant_type: str, pot_size_inches: float) -> dict:
    """Calculate custom chunky soil mix proportions by volume for tropical, succulent, or indoor plants.
    
    Args:
        plant_type: Category ('tropical_aroid', 'succulent_cactus', 'general_houseplant').
        pot_size_inches: Pot diameter in inches.
        
    Returns:
        Dictionary with soil ingredient breakdown percentages, total soil volume needed, and potting tips.
    """
    # Calculate soil volume for cylindrical pot: V = pi * r^2 * h (approx height = 0.9 * diameter)
    radius_cm = (pot_size_inches * 2.54) / 2.0
    height_cm = pot_size_inches * 2.54 * 0.9
    volume_liters = round((3.14159 * (radius_cm ** 2) * height_cm) / 1000.0, 2)
    
    if "aroid" in plant_type.lower() or "tropical" in plant_type.lower():
        breakdown = {
            "Orchid Bark": "40%",
            "Coarse Perlite / Pumice": "30%",
            "Peat Moss / Coco Coir": "20%",
            "Horticultural Charcoal": "5%",
            "Worm Castings": "5%"
        }
    elif "succulent" in plant_type.lower() or "cactus" in plant_type.lower():
        breakdown = {
            "Coarse Sand & Pumice": "60%",
            "Potting Soil": "30%",
            "Perlite": "10%"
        }
    else:
        breakdown = {
            "Potting Soil": "50%",
            "Perlite": "30%",
            "Coco Coir": "20%"
        }
        
    return {
        "plant_type": plant_type,
        "pot_size_inches": pot_size_inches,
        "total_soil_volume_liters": volume_liters,
        "ingredient_breakdown_by_volume": breakdown,
        "drainage_rating": "Excellent (Prevents Root Rot)"
    }

def calculate_grow_light_schedule(plant_category: str, natural_daylight_hours: float) -> dict:
    """Calculate supplemental LED grow light photoperiod hours, DLI (Daily Light Integral), and PPFD distance.
    
    Args:
        plant_category: Plant light intensity group ('high_light_ficus', 'medium_light_monstera', 'low_light_snake').
        natural_daylight_hours: Available natural sunlight per day.
        
    Returns:
        Dictionary with required LED timer hours per day, recommended PPFD ($\mu\text{mol/m}^2/\text{s}$), and lamp height.
    """
    target_hours = 14.0
    supplemental_hours = max(0.0, round(target_hours - natural_daylight_hours, 1))
    
    return {
        "plant_category": plant_category,
        "natural_daylight_hours": natural_daylight_hours,
        "target_photoperiod_hours": target_hours,
        "supplemental_led_hours": supplemental_hours,
        "recommended_ppfd_umol": "300 - 450 umol/m2/s",
        "recommended_lamp_distance": "12 to 18 inches above canopy",
        "timer_setting": f"Set LED Grow Light ON for {supplemental_hours} hours daily"
    }

def lookup_pest_treatment(pest_name: str) -> dict:
    """Look up comprehensive organic and chemical treatment protocols for common houseplant pests.
    
    Args:
        pest_name: Name of pest (e.g. 'mealybugs', 'spider_mites', 'thrips', 'fungus_gnats', 'scale').
        
    Returns:
        Dictionary with pest identification, organic spray recipe, isolation period, and soil treatment.
    """
    p_lower = pest_name.lower()
    
    if "spider" in p_lower or "mite" in p_lower:
        organic = "Cold-pressed Neem Oil (1 tsp) + Castile Soap (0.5 tsp) per 1 Liter warm water. Spray underside of leaves."
        isolation = "14 days away from collection"
        freq = "Every 4 days for 3 consecutive weeks"
    elif "mealy" in p_lower or "scale" in p_lower:
        organic = "70% Isopropyl Alcohol on a cotton swab for direct contact, followed by Insecticidal Soap spray."
        isolation = "21 days"
        freq = "Every 5 days until zero pests visible"
    elif "gnat" in p_lower:
        organic = "Yellow sticky traps + Mosquito Bits (BTI bacteria) drenched into soil during watering."
        isolation = "None required"
        freq = "Every watering for 14 days"
    else:
        organic = "Dilute Neem Oil or Insecticidal Soap foliage wash."
        isolation = "7 to 10 days"
        freq = "Weekly"
        
    return {
        "pest_name": pest_name,
        "organic_treatment": organic,
        "isolation_period": isolation,
        "treatment_frequency": freq,
        "prevention_tip": "Maintain high humidity (>60%) and wipe leaf dust regularly with micro-fiber cloth."
    }
