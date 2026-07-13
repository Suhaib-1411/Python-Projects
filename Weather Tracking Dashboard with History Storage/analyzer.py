def filter_by_city(history: list, city_name: str) -> list:
    """Filters historical data by a specific city, case-insensitively."""
    return [entry for entry in history if entry["city"].lower() == city_name.lower()]

def calculate_analytics(city_records: list) -> dict:
    """Calculates summary statistics for a given list of city records."""
    if not city_records:
        return {}
        
    temps = [r["temperature"] for r in city_records]
    humidities = [r["humidity"] for r in city_records]
    
    return {
        "count": len(city_records),
        "avg_temp": round(sum(temps) / len(temps), 1),
        "max_temp": max(temps),
        "min_temp": min(temps),
        "avg_humidity": round(sum(humidities) / len(humidities), 1)
    }