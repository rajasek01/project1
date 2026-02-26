import requests
import os
from flask import current_app

def get_realtime_pollution(lat, lon):
    """
    Fetches real-time air pollution data from OpenWeatherMap API.
    """
    api_key = current_app.config['OPENWEATHERMAP_API_KEY']
    if api_key == 'YOUR_OPEN_WEATHER_API_KEY' or not api_key:
        # Graceful handling for missing API key/fallback to mock data
        return get_mock_pollution_data(lat, lon)
        
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract parameters
            components = data['list'][0]['components']
            aqi = data['list'][0]['main']['aqi'] # note: OWM AQI is 1-5, we might need to map it to the requested 0-300+ scale or use our own calculation
            
            # For demonstration, we'll map components to a custom AQI or just return them
            return {
                'aqi': aqi * 50, # Rough mapping for demonstration if using OWM scale
                'pm2_5': components.get('pm2_5'),
                'pm10': components.get('pm10'),
                'no2': components.get('no2'),
                'co': components.get('co'),
                'o3': components.get('o3'),
                'so2': components.get('so2'),
                'source': 'OpenWeatherMap'
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def fetch_nasa_earthdata(lat, lon):
    """
    Placeholder for NASA Earthdata API.
    Usually requires Earthdata login and handling specific product formats.
    """
    # Placeholder for actual implementation
    return {"source": "NASA Earthdata", "info": "Detailed satellite imagery/AOD data"}

# Local fallback for common locations (works even without API key)
LOCAL_LOCATIONS = {
    'india': (20.5937, 78.9629),
    'usa': (37.0902, -95.7129),
    'uk': (55.3781, -3.4360),
    'tamil nadu': (11.1271, 78.6569),
    'tamilnadu': (11.1271, 78.6569),
    'delhi': (28.6139, 77.2090),
    'london': (51.5074, -0.1278),
    'new york': (40.7128, -74.0060),
    'beijing': (39.9042, 116.4074),
    'tokyo': (35.6762, 139.6503),
    'mumbai': (19.0760, 72.8777),
    'paris': (48.8566, 2.3522),
    'berlin': (52.5200, 13.4050),
    'chennai': (13.0827, 80.2707),
    'bangalore': (12.9716, 77.5946)
}

def geocode_location(query):
    """
    Converts a location name to coordinates using OpenWeatherMap Geocoding API.
    Includes normalization, fallback for better regional support, and a local mock dictionary.
    """
    api_key = current_app.config['OPENWEATHERMAP_API_KEY']
    has_api_key = api_key != 'YOUR_OPEN_WEATHER_API_KEY' and bool(api_key)
    
    # 1. Normalize query
    clean_query = query.strip().lower()
    if not clean_query:
        return None, "Empty Query"

    print(f"[GEOCODE] Searching for: '{clean_query}' (API Key: {'Present' if has_api_key else 'Missing'})")

    # 2. Local Fallback Search (Immediate)
    if clean_query in LOCAL_LOCATIONS:
        print(f"[GEOCODE] [LOCAL_FALLBACK] Match found for '{clean_query}'")
        return LOCAL_LOCATIONS[clean_query], "Local Fallback"

    if not has_api_key:
        print(f"[GEOCODE] [WARNING] API Key missing and no local match for '{clean_query}'")
        return None, "API Key Missing & No Local Match"

    # 3. Attempt API lookup
    def fetch_coords(q):
        print(f"[GEOCODE] [API_REQ] Querying OWM: {q}")
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={q}&limit=1&appid={api_key}"
        try:
            response = requests.get(url, timeout=5)
            print(f"[GEOCODE] [API_RES] Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data:
                    return (data[0]['lat'], data[0]['lon']), None
            return None, f"API Error: {response.status_code}"
        except Exception as e:
            return None, f"Network Error: {str(e)}"

    # First attempt
    coords, err = fetch_coords(clean_query)
    
    # 4. Fallback: If fails, try with ", India" appended
    if not coords and ", india" not in clean_query:
        print(f"[GEOCODE] [FALLBACK] Retrying with India suffix...")
        coords, err = fetch_coords(f"{clean_query}, india")

    return coords, err

def get_mock_pollution_data(lat, lon):
    """
    Returns mock data for testing and demonstration when API keys are missing.
    """
    import random
    return {
        'aqi': random.randint(30, 250),
        'pm2_5': round(random.uniform(5, 100), 2),
        'pm10': round(random.uniform(10, 150), 2),
        'no2': round(random.uniform(10, 80), 2),
        'co': round(random.uniform(200, 1000), 2),
        'o3': round(random.uniform(20, 120), 2),
        'so2': round(random.uniform(2, 50), 2),
        'source': 'Mock Satellite System'
    }
