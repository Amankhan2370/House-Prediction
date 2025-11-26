# Hyderabad House Price Predictor

AI-powered real estate price estimation platform for Hyderabad properties with 91.45% accuracy.

## Features

- **AI-Powered Predictions**: Machine Learning model with 91.45% accuracy
- **14 Premium Areas**: Coverage of Hyderabad's top real estate locations
- **4 Property Types**: Apartment, Independent House, Villa, Penthouse
- **Modern UI**: Professional grey and cream color scheme
- **Fully Responsive**: Works seamlessly on all devices
- **Real-time Predictions**: Instant price estimates

## Tech Stack

**Frontend:**
- React.js
- Axios
- CSS

**Backend:**
- Flask
- Scikit-learn (Random Forest Regressor)
- Pandas, NumPy

**ML Model:**
- Random Forest Regressor
- Feature Engineering (Label Encoding, Standard Scaling)
- 2000+ data points

## Model Performance

- **R² Score**: 0.9145 (91.45% accuracy)
- **MAE**: ₹3.5L (Mean Absolute Error)
- **RMSE**: ₹5.2L (Root Mean Squared Error)

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```

Backend runs on `http://localhost:5001`

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## Areas Covered

Hitech City, Gachibowli, Banjara Hills, Jubilee Hills, Kondapur, Madhapur, Himayatnagar, Begumpet, Manikonda, Nanakramguda, Financial District, Kukatpally, Miyapur, Hafeezpet

## License

MIT License
