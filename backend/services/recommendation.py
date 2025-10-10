from typing import Dict, Any, List
import os
import random

# In a real implementation, we'd call Google Maps Directions API and AQI APIs.
# Here we stub external calls but keep clear interfaces.

class ExternalApis:
    def __init__(self) -> None:
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.aqi_api_key = os.getenv("AQI_API_KEY", "")

    def fetch_routes(self, source: str, destination: str) -> List[Dict[str, Any]]:
        # Stubbed: simulate 3 route candidates with time (min) and distance (km)
        baseline = random.randint(12, 20)
        return [
            {"id": "fastest", "label": "Fastest Route", "timeMin": baseline, "distanceKm": round(random.uniform(3.5, 5.0), 1)},
            {"id": "balanced", "label": "Balanced Route", "timeMin": baseline + 3, "distanceKm": round(random.uniform(3.2, 4.8), 1)},
            {"id": "eco", "label": "Eco-Friendly Route", "timeMin": baseline + 7, "distanceKm": round(random.uniform(3.0, 4.2), 1)},
        ]

    def fetch_aqi_for_route(self, route_id: str) -> str:
        # Stubbed: return pollution level as a category
        return random.choice(["Low", "Medium", "High"])


def estimate_emissions_kg(distance_km: float, mode: str) -> float:
    # Very rough factors (kg CO2e per km)
    factors = {
        "walk": 0.0,
        "cycle": 0.0,
        "bus": 0.08,
        "metro": 0.04,
        "car": 0.18,
        "bike": 0.09,
    }
    factor = factors.get(mode, 0.18)
    return round(distance_km * factor, 3)


def green_score(distance_km: float, time_min: int, pollution_level: str, mode: str) -> int:
    # Base from mode: greener modes get higher base
    mode_base = {"walk": 60, "cycle": 55, "metro": 45, "bus": 40, "bike": 25, "car": 20}
    base = mode_base.get(mode, 20)

    # Penalty for distance/time; bonus for low pollution
    distance_penalty = max(0, (distance_km - 3.0) * 5)
    time_penalty = max(0, (time_min - 15) * 1.5)
    pollution_bonus = {"Low": 20, "Medium": 10, "High": 0}.get(pollution_level, 10)

    score = base + pollution_bonus - distance_penalty - time_penalty
    return max(0, min(100, int(round(score))))


def recommend_routes(source: str, destination: str) -> Dict[str, Any]:
    apis = ExternalApis()
    candidates = apis.fetch_routes(source, destination)

    # Evaluate several modes for each route; we'll output 3 representative options
    options: List[Dict[str, Any]] = []
    for route in candidates:
        pollution = apis.fetch_aqi_for_route(route["id"])
        distance = float(route["distanceKm"])
        time_min = int(route["timeMin"])

        modes = ["walk", "cycle", "bus", "metro", "car"]
        best_by_score = None
        for mode in modes:
            emission = estimate_emissions_kg(distance, mode)
            score = green_score(distance, time_min, pollution, mode)
            option = {
                "id": f"{route['id']}:{mode}",
                "label": route["label"],
                "mode": mode,
                "timeMin": time_min,
                "distanceKm": distance,
                "pollution": pollution,
                "emissionsKg": emission,
                "greenScore": score,
                "ecoPoints": int(round(score / 5)),
            }
            if not best_by_score or option["greenScore"] > best_by_score["greenScore"]:
                best_by_score = option
        if best_by_score:
            options.append(best_by_score)

    # Sort to highlight eco and balanced options
    options.sort(key=lambda o: (-o["greenScore"], o["timeMin"]))

    recommended = options[0] if options else None
    summary = {
        "source": source,
        "destination": destination,
        "recommended": recommended,
        "options": options[:3],
    }
    return summary
