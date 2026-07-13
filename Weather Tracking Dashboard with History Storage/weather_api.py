import requests
from config import GEO_URL, WEATHER_URL

def get_current_weather(city_name: str) -> dict:
    """
    Fetches real-time weather metrics using the public Open-Meteo API.
    Resolves city names to coordinates dynamically via the Geocoding API.
    """
    geo_params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        # Step 1: Resolve City Name to Coordinates
        geo_response = requests.get(GEO_URL, params=geo_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if "results" not in geo_data or not geo_data["results"]:
            print(f"\nError: City '{city_name}' not found. Please verify spelling.")
            return {}
            
        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        resolved_name = f"{location['name']}, {location.get('country', '')}"
        
        # Step 2: Query Weather Data using Coordinates
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "models": "best_match"
        }
        
        weather_response = requests.get(WEATHER_URL, params=weather_params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        
        # Map WMO World Meteorological Organization weather codes to human-readable text
        wmo_codes = {
            0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing Rime Fog", 51: "Light Drizzle", 53: "Moderate Drizzle",
            55: "Dense Drizzle", 61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
            71: "Slight Snow", 73: "Moderate Snow", 75: "Heavy Snow", 77: "Snow Grains",
            80: "Slight Rain Showers", 81: "Moderate Rain Showers", 82: "Violent Rain Showers",
            85: "Slight Snow Showers", 86: "Heavy Snow Showers", 95: "Thunderstorm"
        }
        code = current.get("weather_code", 0)
        condition = wmo_codes.get(code, "Unknown Conditions")

        return {
            "city": resolved_name,
            "temperature": round(current["temperature_2m"], 1),
            "humidity": current["relative_humidity_2m"],
            "condition": condition,
            "wind_speed": round(current["wind_speed_10m"], 1)
        }

    except requests.exceptions.ConnectionError:
        print("\nNetwork Error: Unable to connect to the weather service.")
    except requests.exceptions.RequestException as e:
        print(f"\nUnexpected Error: {e}")
        
    return {}