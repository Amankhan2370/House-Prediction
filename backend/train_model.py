import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Generate synthetic Hyderabad house price data
def generate_hyderabad_data(n_samples=1000):
    """Generate realistic synthetic data for Hyderabad house prices"""
    np.random.seed(42)
    
    # Hyderabad popular areas
    areas = ['Hitech City', 'Gachibowli', 'Banjara Hills', 'Jubilee Hills', 'Kondapur',
             'Madhapur', 'Himayatnagar', 'Begumpet', 'Manikonda',
             'Nanakramguda', 'Financial District', 'Kukatpally', 'Miyapur', 'Hafeezpet']
    
    property_types = ['Apartment', 'Independent House', 'Villa', 'Penthouse']
    
    data = []
    
    for _ in range(n_samples):
        area = np.random.choice(areas)
        property_type = np.random.choice(property_types)
        bhk = np.random.choice([1, 2, 3, 4, 5])
        sqft = np.random.randint(500, 5000)
        floor = np.random.randint(1, 15)
        age = np.random.randint(0, 30)
        
        # Base price calculation (realistic for Hyderabad)
        base_price = 3000  # per sqft base
        
        # Area multiplier (Hitech City, Gachibowli are expensive)
        area_multipliers = {
            'Hitech City': 1.8, 'Gachibowli': 1.7, 'Banjara Hills': 1.6,
            'Jubilee Hills': 1.5, 'Kondapur': 1.4, 'Madhapur': 1.4,
            'Himayatnagar': 1.3, 'Begumpet': 1.3, 'Manikonda': 1.2,
            'Nanakramguda': 1.3, 'Financial District': 1.6, 'Kukatpally': 1.1,
            'Miyapur': 1.1, 'Hafeezpet': 1.1
        }
        
        # Property type multiplier
        type_multipliers = {
            'Apartment': 1.0, 'Independent House': 1.5, 'Villa': 2.0, 'Penthouse': 2.5
        }
        
        # BHK multiplier
        bhk_multiplier = 1 + (bhk - 1) * 0.15
        
        # Floor multiplier (higher floors cost more)
        floor_multiplier = 1 + (floor - 1) * 0.02
        
        # Age depreciation
        age_multiplier = 1 - (age * 0.01)
        
        price_per_sqft = base_price * area_multipliers.get(area, 1.0) * \
                        type_multipliers.get(property_type, 1.0) * bhk_multiplier * \
                        floor_multiplier * age_multiplier
        
        # Add some randomness
        price_per_sqft *= np.random.uniform(0.9, 1.1)
        
        total_price = price_per_sqft * sqft
        
        # Round to nearest 10000
        total_price = round(total_price / 10000) * 10000
        
        data.append({
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
print("Generating Hyderabad house price dataset...")
df = generate_hyderabad_data(2000)

# Feature engineering
le_area = LabelEncoder()
le_type = LabelEncoder()

df['area_encoded'] = le_area.fit_transform(df['area'])
df['type_encoded'] = le_type.fit_transform(df['property_type'])

# Features
X = df[['area_encoded', 'type_encoded', 'bhk', 'sqft', 'floor', 'age']]
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
print("Training Random Forest model...")
model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
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
joblib.dump(le_area, 'le_area.pkl')
joblib.dump(le_type, 'le_type.pkl')

# Save area and type mappings for API
import json
area_mapping = {area: int(encoded) for area, encoded in zip(le_area.classes_, le_area.transform(le_area.classes_))}
type_mapping = {prop_type: int(encoded) for prop_type, encoded in zip(le_type.classes_, le_type.transform(le_type.classes_))}

with open('area_mapping.json', 'w') as f:
    json.dump(area_mapping, f, indent=2)

with open('type_mapping.json', 'w') as f:
    json.dump(type_mapping, f, indent=2)

print("\n✅ Model trained and saved successfully!")
print("Files saved:")
print("  - model.pkl")
print("  - scaler.pkl")
print("  - le_area.pkl")
print("  - le_type.pkl")
print("  - area_mapping.json")
print("  - type_mapping.json")
