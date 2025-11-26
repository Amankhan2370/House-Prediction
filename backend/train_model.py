import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import json

# Indian cities with their major areas
CITIES_DATA = {
    'Mumbai': {
        'areas': ['Bandra', 'Andheri', 'Powai', 'Worli', 'Juhu', 'Malad', 'Goregaon', 'Borivali', 'Thane', 'Navi Mumbai'],
        'base_price': 15000,
        'multipliers': {'Bandra': 2.5, 'Worli': 2.3, 'Juhu': 2.2, 'Andheri': 1.8, 'Powai': 1.7, 'Malad': 1.3, 'Goregaon': 1.2, 'Borivali': 1.1, 'Thane': 1.0, 'Navi Mumbai': 0.9}
    },
    'Delhi': {
        'areas': ['Gurgaon', 'Noida', 'Dwarka', 'Rohini', 'Vasant Kunj', 'Saket', 'Greater Kailash', 'Lajpat Nagar', 'Connaught Place', 'Karol Bagh'],
        'base_price': 8000,
        'multipliers': {'Gurgaon': 2.0, 'Noida': 1.8, 'Vasant Kunj': 1.9, 'Saket': 1.8, 'Greater Kailash': 1.7, 'Dwarka': 1.4, 'Rohini': 1.2, 'Lajpat Nagar': 1.3, 'Connaught Place': 2.2, 'Karol Bagh': 1.1}
    },
    'Bangalore': {
        'areas': ['Koramangala', 'Indiranagar', 'Whitefield', 'Electronic City', 'Marathahalli', 'HSR Layout', 'JP Nagar', 'BTM Layout', 'Bannerghatta', 'Yelahanka'],
        'base_price': 6000,
        'multipliers': {'Koramangala': 1.8, 'Indiranagar': 1.7, 'Whitefield': 1.5, 'Electronic City': 1.3, 'Marathahalli': 1.4, 'HSR Layout': 1.6, 'JP Nagar': 1.5, 'BTM Layout': 1.2, 'Bannerghatta': 1.1, 'Yelahanka': 1.0}
    },
    'Hyderabad': {
        'areas': ['Hitech City', 'Gachibowli', 'Banjara Hills', 'Jubilee Hills', 'Kondapur', 'Madhapur', 'Himayatnagar', 'Begumpet', 'Manikonda', 'Nanakramguda'],
        'base_price': 4000,
        'multipliers': {'Hitech City': 1.8, 'Gachibowli': 1.7, 'Banjara Hills': 1.6, 'Jubilee Hills': 1.5, 'Kondapur': 1.4, 'Madhapur': 1.4, 'Himayatnagar': 1.3, 'Begumpet': 1.3, 'Manikonda': 1.2, 'Nanakramguda': 1.3}
    },
    'Chennai': {
        'areas': ['Adyar', 'Anna Nagar', 'T Nagar', 'OMR', 'Velachery', 'Porur', 'Tambaram', 'Chrompet', 'Guindy', 'Nungambakkam'],
        'base_price': 5000,
        'multipliers': {'Adyar': 1.7, 'Anna Nagar': 1.6, 'T Nagar': 1.8, 'OMR': 1.5, 'Velachery': 1.4, 'Porur': 1.3, 'Tambaram': 1.1, 'Chrompet': 1.2, 'Guindy': 1.4, 'Nungambakkam': 1.6}
    },
    'Pune': {
        'areas': ['Hinjewadi', 'Koregaon Park', 'Baner', 'Wakad', 'Viman Nagar', 'Kothrud', 'Hadapsar', 'Aundh', 'Magarpatta', 'Kharadi'],
        'base_price': 5500,
        'multipliers': {'Hinjewadi': 1.5, 'Koregaon Park': 1.8, 'Baner': 1.6, 'Wakad': 1.4, 'Viman Nagar': 1.5, 'Kothrud': 1.3, 'Hadapsar': 1.2, 'Aundh': 1.4, 'Magarpatta': 1.5, 'Kharadi': 1.4}
    },
    'Kolkata': {
        'areas': ['Salt Lake', 'New Town', 'Park Street', 'Ballygunge', 'Alipore', 'Behala', 'Howrah', 'Dum Dum', 'Rajarhat', 'Garia'],
        'base_price': 3500,
        'multipliers': {'Salt Lake': 1.6, 'New Town': 1.5, 'Park Street': 1.8, 'Ballygunge': 1.7, 'Alipore': 1.9, 'Behala': 1.2, 'Howrah': 1.1, 'Dum Dum': 1.2, 'Rajarhat': 1.4, 'Garia': 1.3}
    }
}

def generate_india_data(n_samples_per_city=500):
    """Generate realistic synthetic data for Indian cities house prices"""
    np.random.seed(42)
    
    property_types = ['Apartment', 'Independent House', 'Villa', 'Penthouse']
    data = []
    
    for city, city_info in CITIES_DATA.items():
        for _ in range(n_samples_per_city):
            area = np.random.choice(city_info['areas'])
            property_type = np.random.choice(property_types)
            bhk = np.random.choice([1, 2, 3, 4, 5])
            sqft = np.random.randint(500, 5000)
            floor = np.random.randint(1, 15)
            age = np.random.randint(0, 30)
            
            base_price = city_info['base_price']
            area_multiplier = city_info['multipliers'].get(area, 1.0)
            
            # Property type multiplier
            type_multipliers = {
                'Apartment': 1.0, 'Independent House': 1.5, 'Villa': 2.0, 'Penthouse': 2.5
            }
            
            # BHK multiplier
            bhk_multiplier = 1 + (bhk - 1) * 0.15
            
            # Floor multiplier
            floor_multiplier = 1 + (floor - 1) * 0.02
            
            # Age depreciation
            age_multiplier = 1 - (age * 0.01)
            
            price_per_sqft = base_price * area_multiplier * \
                            type_multipliers.get(property_type, 1.0) * bhk_multiplier * \
                            floor_multiplier * age_multiplier
            
            # Add randomness
            price_per_sqft *= np.random.uniform(0.9, 1.1)
            
            total_price = price_per_sqft * sqft
            total_price = round(total_price / 10000) * 10000
            
            data.append({
                'city': city,
                'area': area,
                'property_type': property_type,
                'bhk': bhk,
                'sqft': sqft,
                'floor': floor,
                'age': age,
                'price': total_price
            })
    
    return pd.DataFrame(data)

# Create dataset
print("Generating India house price dataset...")
df = generate_india_data(500)

# Feature engineering
le_city = LabelEncoder()
le_area = LabelEncoder()
le_type = LabelEncoder()

df['city_encoded'] = le_city.fit_transform(df['city'])
df['area_encoded'] = le_area.fit_transform(df['area'])
df['type_encoded'] = le_type.fit_transform(df['property_type'])

# Features including city
X = df[['city_encoded', 'area_encoded', 'type_encoded', 'bhk', 'sqft', 'floor', 'age']]
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
print("Training Random Forest model...")
model = RandomForestRegressor(n_estimators=150, max_depth=25, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"MAE: ₹{mae:,.0f}")
print(f"RMSE: ₹{np.sqrt(mse):,.0f}")
print(f"R² Score: {r2:.4f}")

# Save model and encoders
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(le_city, 'le_city.pkl')
joblib.dump(le_area, 'le_area.pkl')
joblib.dump(le_type, 'le_type.pkl')

# Save mappings
city_mapping = {city: int(encoded) for city, encoded in zip(le_city.classes_, le_city.transform(le_city.classes_))}
area_mapping = {area: int(encoded) for area, encoded in zip(le_area.classes_, le_area.transform(le_area.classes_))}
type_mapping = {prop_type: int(encoded) for prop_type, encoded in zip(le_type.classes_, le_type.transform(le_type.classes_))}

with open('city_mapping.json', 'w') as f:
    json.dump(city_mapping, f, indent=2)

with open('area_mapping.json', 'w') as f:
    json.dump(area_mapping, f, indent=2)

with open('type_mapping.json', 'w') as f:
    json.dump(type_mapping, f, indent=2)

# Save city-area mapping
city_area_mapping = {}
for city, city_info in CITIES_DATA.items():
    city_area_mapping[city] = city_info['areas']

with open('city_area_mapping.json', 'w') as f:
    json.dump(city_area_mapping, f, indent=2)

print("\n✅ Model trained and saved successfully!")
print("Files saved:")
print("  - model.pkl")
print("  - scaler.pkl")
print("  - le_city.pkl")
print("  - le_area.pkl")
print("  - le_type.pkl")
print("  - city_mapping.json")
print("  - area_mapping.json")
print("  - type_mapping.json")
print("  - city_area_mapping.json")
print(f"\n📊 Total cities: {len(CITIES_DATA)}")
print(f"📊 Total areas: {len(le_area.classes_)}")
print(f"📊 Total samples: {len(df)}")