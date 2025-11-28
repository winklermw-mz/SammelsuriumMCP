import requests

GEO_LOCATION_API = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"


def call_geo_api(location: str) -> dict:
    geo_res = requests.get(GEO_LOCATION_API, params={"name": location, "count": 1}).json()
    if "results" not in geo_res or len(geo_res["results"]) == 0:
        raise Exception(f"City '{location}' not found")
    coord = geo_res["results"][0]
    return {"lat": coord["latitude"], "lon": coord["longitude"]}

def call_weather_api(lat: int, lon: int) -> dict:
    weather_res = requests.get(WEATHER_API, {"latitude": lat, "longitude": lon, "current_weather": True}).json()
    if "current_weather" not in weather_res:
        raise Exception("No weather data available")
    return weather_res["current_weather"]

def get_weather_codes(code: str) -> dict:
    codes = {
        "0": "Clear sky",
        "1": "Mainly clear",
        "2": "Partly cloudy",
        "3": "Overcast",
        "45": "Fog",
        "48": "Depositing rime fog",
        "51": "Light drizzle",
        "53": "Moderate drizzle",
        "55": "Dense drizzle",
        "56": "Light freezing drizzle",
        "57": "Dense freezing drizzle",
        "61": "Slight rain",
        "63": "Moderate rain",
        "65": "Heavy rain",
        "66": "Light freezing rain",
        "67": "Heavy freezing rain",
        "71": "Slight snow fall",
        "73": "Moderate snow fall",
        "75": "Heavy snow fall",
        "77": "Snow grains",
        "80": "Slight rain showers",
        "81": "Moderate rain showers",
        "82": "Violent rain showers",
        "85": "Slight snow showers",
        "86": "Heavy snow showers",
        "95": "Thunderstorm (slight or moderate)",
        "96": "Thunderstorm with slight hail",
        "99": "Thunderstorm with heavy hail"
    }
    if code in codes:
        return codes[code]
    return "not specified"

def get_weather_forecast(location: str) -> dict:
    coord = call_geo_api(location)
    lat = coord["lat"]
    lon = coord["lon"]
    weather_data = call_weather_api(lat, lon)
    return {
        "location": location,
        "temperature": f"{weather_data["temperature"]} °C",
        "windspeed": f"{weather_data["windspeed"]} km/h",
        "time": weather_data["time"],
        "condition": get_weather_codes(str(weather_data["weathercode"]))
    }