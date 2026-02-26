def get_pollution_info(aqi):
    """
    Classifies the pollution level based on the AQI.
    Returns a dictionary with the level and indicator color.
    """
    if 0 <= aqi <= 50:
        return {"level": "Good", "color": "Green"}
    elif 51 <= aqi <= 100:
        return {"level": "Moderate", "color": "Yellow"}
    elif 101 <= aqi <= 150:
        return {"level": "Unhealthy (Sensitive)", "color": "Orange"}
    elif 151 <= aqi <= 200:
        return {"level": "Unhealthy", "color": "Red"}
    elif 201 <= aqi <= 300:
        return {"level": "Very Unhealthy", "color": "Purple"}
    elif aqi > 300:
        return {"level": "Hazardous", "color": "Maroon"}
    else:
        return {"level": "Unknown", "color": "Grey"}

# Optional: Add a simple RandomForest classifier placeholder if the user wants to train on custom data later
def predict_pollution_category(features):
    # This is a rule-based mock for the ML logic as per the "Rule-based AI logic OR Optional ML model" instruction
    # features could be [pm25, pm10, no2, co, o3, so2]
    # For now, we use the rule-based approach derived from AQI
    pass
