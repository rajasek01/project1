from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import Config
from models import db, PollutionRecord
from utils.satellite_api import get_realtime_pollution
from utils.pollution_classifier import get_pollution_info
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_data():
    city = request.form.get('city')
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    accuracy = request.form.get('accuracy')
    source = request.form.get('source', 'Manual')
    
    # Accuracy filtering (Reject > 500m for "GPS" source if provided)
    if source == 'GPS' and accuracy:
        try:
            acc_val = float(accuracy)
            if acc_val > 500: # Threshold for low accuracy
                return jsonify({"status": "error", "message": f"Accuracy too low ({acc_val}m). Please try again or enter city manually."}), 400
        except ValueError:
            pass

    # Better geocoding logic
    if not lat or not lon:
        source = 'Geocoding'
        if not city:
            return jsonify({"error": "No location provided"}), 400
            
        from utils.satellite_api import geocode_location
        coords, err = geocode_location(city)
        
        if coords:
            lat, lon = coords
            source = f"Geocoding ({err})" if err == "Local Fallback" else "Geocoding (API)"
            print(f"[GEOCODE] Resolved '{city}' to {lat}, {lon} via {source}")
        else:
            # Suggestion-based error handling
            message = f"Location '{city}' not recognized."
            if err == "API Key Missing & No Local Match":
                message = f"Location '{city}' not in local database and API Key is missing."
            
            suggestions = ["Check for spelling errors", "Try adding the state or country (e.g., 'Tamil Nadu, India')", "Provide an API key in .env for global search"]
            return jsonify({
                "status": "error", 
                "message": message,
                "suggestions": suggestions,
                "debug": err
            }), 400
    
    try:
        lat, lon = float(lat), float(lon)
        accuracy = float(accuracy) if accuracy else None
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid coordinates or accuracy format"}), 400

    # Logging trace
    print(f"[LOCATION TRACE] Source: {source}, Lat: {lat}, Lon: {lon}, Accuracy: {accuracy}m")

    data = get_realtime_pollution(lat, lon)
    if data:
        pollution_info = get_pollution_info(data['aqi'])
        
        # Save to database
        record = PollutionRecord(
            location=city or f"Coord: {lat:.4f}, {lon:.4f}",
            latitude=lat,
            longitude=lon,
            aqi=data['aqi'],
            pm25=data['pm2_5'],
            pm10=data['pm10'],
            no2=data['no2'],
            co=data['co'],
            o3=data['o3'],
            so2=data['so2'],
            category=pollution_info['level'],
            location_source=source,
            accuracy=accuracy
        )
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "data": data,
            "classification": pollution_info,
            "record_id": record.id
        })
    else:
        return jsonify({"status": "error", "message": "Failed to fetch data"}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    records = PollutionRecord.query.order_by(PollutionRecord.timestamp.desc()).limit(10).all()
    return jsonify([r.to_dict() for r in records])

@app.route('/history')
def history():
    records = PollutionRecord.query.order_by(PollutionRecord.timestamp.desc()).all()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
