from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import json
import os

app = Flask(__name__)
CORS(app)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and preprocessing objects
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
le_area = joblib.load(os.path.join(BASE_DIR, 'le_area.pkl'))
le_type = joblib.load(os.path.join(BASE_DIR, 'le_type.pkl'))

# Load mappings
with open(os.path.join(BASE_DIR, 'area_mapping.json'), 'r') as f:
    area_mapping = json.load(f)

with open(os.path.join(BASE_DIR, 'type_mapping.json'), 'r') as f:
    type_mapping = json.load(f)

# Get available areas and types
AVAILABLE_AREAS = list(le_area.classes_)
AVAILABLE_TYPES = list(le_type.classes_)

@app.route('/')
def home():
    return jsonify({
        "message": "Hyderabad House Price Prediction API",
        "status": "running"
    })

@app.route('/api/areas', methods=['GET'])
def get_areas():
    """Get list of available areas"""
    return jsonify({"areas": AVAILABLE_AREAS})

@app.route('/api/property-types', methods=['GET'])
def get_property_types():
    """Get list of available property types"""
    return jsonify({"types": AVAILABLE_TYPES})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict house price"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['area', 'property_type', 'bhk', 'sqft', 'floor', 'age']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        area = data['area']
        property_type = data['property_type']
        bhk = int(data['bhk'])
        sqft = float(data['sqft'])
        floor = int(data['floor'])
        age = int(data['age'])
        
        # Validate area
        if area not in AVAILABLE_AREAS:
            return jsonify({
                "error": f"Area '{area}' not available. Please choose from: {', '.join(AVAILABLE_AREAS)}"
            }), 400
        
        # Validate property type
        if property_type not in AVAILABLE_TYPES:
            return jsonify({
                "error": f"Property type '{property_type}' not available. Please choose from: {', '.join(AVAILABLE_TYPES)}"
            }), 400
        
        # Encode categorical features
        area_encoded = le_area.transform([area])[0]
        type_encoded = le_type.transform([property_type])[0]
        
        # Prepare features
        features = np.array([[area_encoded, type_encoded, bhk, sqft, floor, age]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # Calculate price per sqft
        price_per_sqft = prediction / sqft
        
        return jsonify({
            "predicted_price": round(prediction, 2),
            "price_per_sqft": round(price_per_sqft, 2),
            "price_formatted": f"₹{prediction:,.0f}",
            "price_per_sqft_formatted": f"₹{price_per_sqft:,.0f}/sqft",
            "input": {
                "area": area,
                "property_type": property_type,
                "bhk": bhk,
                "sqft": sqft,
                "floor": floor,
                "age": age
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Hyderabad House Price Prediction API...")
    print(f"Available areas: {', '.join(AVAILABLE_AREAS)}")
    print(f"API running on: http://localhost:5001")
    print(f"Available endpoints:")
    print(f"  - GET  http://localhost:5001/api/areas")
    print(f"  - GET  http://localhost:5001/api/property-types")
    print(f"  - POST http://localhost:5001/api/predict")
    print("")
    app.run(debug=True, host='0.0.0.0', port=5001)
