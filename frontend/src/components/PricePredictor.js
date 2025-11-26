import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/App.css';

const API_URL = 'http://localhost:5001';

function PricePredictor() {
  const [formData, setFormData] = useState({
    area: '',
    property_type: '',
    bhk: '',
    sqft: '',
    floor: '',
    age: ''
  });
  
  const [areas, setAreas] = useState([]);
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      axios.get(`${API_URL}/api/areas`),
      axios.get(`${API_URL}/api/property-types`)
    ]).then(([areasRes, typesRes]) => {
      setAreas(areasRes.data.areas);
      setPropertyTypes(typesRes.data.types);
    }).catch(err => {
      setError('Failed to load data. Make sure backend is running.');
      console.error(err);
    });
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
    setPrediction(null);
  };

  const handleRadioChange = (name, value) => {
    setFormData({
      ...formData,
      [name]: value
    });
    setError('');
    setPrediction(null);
  };

  const handleClear = () => {
    setFormData({
      area: '',
      property_type: '',
      bhk: '',
      sqft: '',
      floor: '',
      age: ''
    });
    setError('');
    setPrediction(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      const response = await axios.post(`${API_URL}/api/predict`, formData);
      setPrediction(response.data);
      setTimeout(() => {
        document.querySelector('.result-container')?.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'nearest' 
        });
      }, 100);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get prediction. Please check your inputs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getPropertyTypeIcon = (type) => {
    const icons = {
      'Apartment': '🏢',
      'Independent House': '🏠',
      'Villa': '🏡',
      'Penthouse': '🏰'
    };
    return icons[type] || '🏠';
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <div className="header-content">
          <h1>Hyderabad House Price Predictor</h1>
          <p className="header-subtitle">
            Get instant, AI-powered property valuations for Hyderabad's premium locations
          </p>
          <div className="header-stats">
            <div className="stat-item">
              <div className="stat-value">91.45%</div>
              <div className="stat-label">Accuracy</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">14</div>
              <div className="stat-label">Premium Areas</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">2K+</div>
              <div className="stat-label">Data Points</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">4</div>
              <div className="stat-label">Property Types</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Form Container */}
        <div className="form-container">
          <div className="form-header">
            <h2 className="form-title">Property Details</h2>
            <p className="form-subtitle">Enter your property information for an instant price estimate</p>
          </div>
          
          <form onSubmit={handleSubmit} className="prediction-form">
            {/* Location */}
            <div className="form-group">
              <label className="form-label">Location</label>
              <select
                name="area"
                value={formData.area}
                onChange={handleChange}
                required
                className="form-select"
              >
                <option value="">Select Area</option>
                {areas.map(area => (
                  <option key={area} value={area}>{area}</option>
                ))}
              </select>
            </div>

            {/* Property Type - Radio Buttons */}
            <div className="form-group">
              <label className="form-label">Property Type</label>
              <div className="radio-group">
                {propertyTypes.map(type => (
                  <div key={type} className="radio-option">
                    <input
                      type="radio"
                      id={`type-${type}`}
                      name="property_type"
                      value={type}
                      checked={formData.property_type === type}
                      onChange={(e) => handleRadioChange('property_type', e.target.value)}
                      className="radio-input"
                      required
                    />
                    <label htmlFor={`type-${type}`} className="radio-label">
                      {getPropertyTypeIcon(type)} {type}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            {/* BHK - Radio Buttons */}
            <div className="form-group">
              <label className="form-label">Bedrooms (BHK)</label>
              <div className="radio-group">
                {[1, 2, 3, 4, 5].map(bhk => (
                  <div key={bhk} className="radio-option">
                    <input
                      type="radio"
                      id={`bhk-${bhk}`}
                      name="bhk"
                      value={bhk}
                      checked={formData.bhk === String(bhk)}
                      onChange={(e) => handleRadioChange('bhk', e.target.value)}
                      className="radio-input"
                      required
                    />
                    <label htmlFor={`bhk-${bhk}`} className="radio-label">
                      {bhk}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            {/* Area and Floor */}
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Area (Square Feet)</label>
                <input
                  type="number"
                  name="sqft"
                  min="100"
                  step="50"
                  value={formData.sqft}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="e.g., 1200"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Floor Number</label>
                <input
                  type="number"
                  name="floor"
                  min="1"
                  max="20"
                  value={formData.floor}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="e.g., 3"
                />
              </div>
            </div>

            {/* Property Age */}
            <div className="form-group">
              <label className="form-label">Property Age (Years)</label>
              <input
                type="number"
                name="age"
                min="0"
                max="50"
                value={formData.age}
                onChange={handleChange}
                required
                className="form-input"
                placeholder="e.g., 5"
              />
            </div>

            {/* Buttons */}
            <div className="button-group">
              <button 
                type="button" 
                onClick={handleClear}
                className="clear-btn"
                disabled={loading}
              >
                Clear
              </button>
              <button 
                type="submit" 
                className="submit-btn submit-btn-main" 
                disabled={loading}
              >
                {loading ? 'Predicting...' : 'Get Price Estimate'}
              </button>
            </div>
          </form>
        </div>

        {/* Result Container */}
        <div className="result-container">
          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <div>
                <strong>Error:</strong> {error}
              </div>
            </div>
          )}

          {prediction && (
            <div className="prediction-result">
              <div className="price-display">
                <div className="price-label">Estimated Property Value</div>
                <div className="price-amount">{prediction.price_formatted}</div>
                <div className="price-per-sqft">
                  <span>📊</span>
                  {prediction.price_per_sqft_formatted}
                </div>
              </div>
              
              <div className="prediction-details">
                <div className="details-title">Property Information</div>
                <div className="detail-grid">
                  <div className="detail-card">
                    <div className="detail-label">Location</div>
                    <div className="detail-value">{prediction.input.area}</div>
                  </div>
                  
                  <div className="detail-card">
                    <div className="detail-label">Property Type</div>
                    <div className="detail-value">
                      {getPropertyTypeIcon(prediction.input.property_type)} {prediction.input.property_type}
                    </div>
                  </div>
                  
                  <div className="detail-card">
                    <div className="detail-label">Bedrooms</div>
                    <div className="detail-value">{prediction.input.bhk} BHK</div>
                  </div>
                  
                  <div className="detail-card">
                    <div className="detail-label">Built-up Area</div>
                    <div className="detail-value">{prediction.input.sqft.toLocaleString()} sqft</div>
                  </div>
                  
                  <div className="detail-card">
                    <div className="detail-label">Floor</div>
                    <div className="detail-value">Floor {prediction.input.floor}</div>
                  </div>
                  
                  <div className="detail-card">
                    <div className="detail-label">Property Age</div>
                    <div className="detail-value">{prediction.input.age} years</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {!prediction && !error && !loading && (
            <div className="placeholder">
              <div className="placeholder-icon">🏡</div>
              <div className="placeholder-title">Get Instant Price Estimate</div>
              <div className="placeholder-text">
                Fill in your property details to receive an AI-powered price prediction
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <div className="loading-title">Analyzing Property Data</div>
              <div className="loading-text">Our AI model is calculating the best estimate for you...</div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>Powered by AI</h4>
            <p>Advanced Machine Learning</p>
          </div>
          <div className="footer-section">
            <h4>Hyderabad Focused</h4>
            <p>14 Premium Areas</p>
          </div>
          <div className="footer-section">
            <h4>Instant Results</h4>
            <p>Real-time Predictions</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>Built for Hyderabad Real Estate • Powered by Machine Learning</p>
        </div>
      </div>
    </div>
  );
}

export default PricePredictor;