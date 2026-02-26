from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PollutionRecord(db.Model):
    __tablename__ = 'pollution_records'
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Pollutant values
    aqi = db.Column(db.Integer, nullable=False)
    pm25 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    no2 = db.Column(db.Float)
    co = db.Column(db.Float)
    o3 = db.Column(db.Float)
    so2 = db.Column(db.Float)
    
    category = db.Column(db.String(50), nullable=False)
    location_source = db.Column(db.String(20), default='Unknown')
    accuracy = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'aqi': self.aqi,
            'pm25': self.pm25,
            'pm10': self.pm10,
            'no2': self.no2,
            'co': self.co,
            'o3': self.o3,
            'so2': self.so2,
            'category': self.category,
            'location_source': self.location_source,
            'accuracy': self.accuracy,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
