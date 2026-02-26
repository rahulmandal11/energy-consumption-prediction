from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Load model and scaler
MODEL_PATH = 'model/energy_prediction_model.pkl'
SCALER_PATH = 'model/feature_scaler.pkl'
DATA_PATH = 'data/sample_data.csv'

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
historical_data = pd.read_csv(DATA_PATH)
historical_data['Start time UTC'] = pd.to_datetime(historical_data['Start time UTC'])

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction based on input features"""
    try:
        data = request.get_json()

        # Extract features from request
        hour = int(data.get('hour', 12))
        dayofweek = int(data.get('dayofweek', 0))
        month = int(data.get('month', 1))
        dayofyear = int(data.get('dayofyear', 1))
        is_weekend = int(data.get('is_weekend', 0))
        quarter = int(data.get('quarter', 1))

        # Get lag features from historical data (last 24 hours)
        lag_features = historical_data.tail(24)['consumption'].values[::-1].tolist()

        # Calculate rolling statistics
        rolling_mean_24 = np.mean(historical_data.tail(24)['consumption'].values)
        rolling_std_24 = np.std(historical_data.tail(24)['consumption'].values)
        rolling_mean_168 = np.mean(historical_data.tail(168)['consumption'].values)

        # Create feature vector
        features = [hour, dayofweek, month, dayofyear, is_weekend, quarter] + \
                   lag_features + \
                   [rolling_mean_24, rolling_std_24, rolling_mean_168]

        # Scale features
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)

        # Make prediction
        prediction = model.predict(features_scaled)[0]

        return jsonify({
            'success': True,
            'prediction': float(prediction),
            'unit': 'MWh',
            'features': {
                'hour': hour,
                'dayofweek': dayofweek,
                'month': month,
                'is_weekend': bool(is_weekend)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/predict_date', methods=['POST'])
def predict_date():
    """Make prediction for a specific date and hour"""
    try:
        data = request.get_json()
        date_str = data.get('date')
        hour = int(data.get('hour', 12))

        # Parse date
        target_date = datetime.strptime(date_str, '%Y-%m-%d')

        # Extract features
        dayofweek = target_date.weekday()
        month = target_date.month
        dayofyear = target_date.timetuple().tm_yday
        is_weekend = 1 if dayofweek >= 5 else 0
        quarter = (month - 1) // 3 + 1

        # Get lag features from historical data
        lag_features = historical_data.tail(24)['consumption'].values[::-1].tolist()

        # Calculate rolling statistics
        rolling_mean_24 = np.mean(historical_data.tail(24)['consumption'].values)
        rolling_std_24 = np.std(historical_data.tail(24)['consumption'].values)
        rolling_mean_168 = np.mean(historical_data.tail(168)['consumption'].values)

        # Create feature vector
        features = [hour, dayofweek, month, dayofyear, is_weekend, quarter] + \
                   lag_features + \
                   [rolling_mean_24, rolling_std_24, rolling_mean_168]

        # Scale and predict
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        prediction = model.predict(features_scaled)[0]

        return jsonify({
            'success': True,
            'date': date_str,
            'hour': hour,
            'prediction': float(prediction),
            'unit': 'MWh',
            'day_name': target_date.strftime('%A')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/predict_day', methods=['POST'])
def predict_day():
    """Predict consumption for all 24 hours of a specific day"""
    try:
        data = request.get_json()
        date_str = data.get('date')

        # Parse date
        target_date = datetime.strptime(date_str, '%Y-%m-%d')

        predictions = []

        for hour in range(24):
            # Extract features
            dayofweek = target_date.weekday()
            month = target_date.month
            dayofyear = target_date.timetuple().tm_yday
            is_weekend = 1 if dayofweek >= 5 else 0
            quarter = (month - 1) // 3 + 1

            # Get lag features
            lag_features = historical_data.tail(24)['consumption'].values[::-1].tolist()

            # Rolling statistics
            rolling_mean_24 = np.mean(historical_data.tail(24)['consumption'].values)
            rolling_std_24 = np.std(historical_data.tail(24)['consumption'].values)
            rolling_mean_168 = np.mean(historical_data.tail(168)['consumption'].values)

            # Create feature vector
            features = [hour, dayofweek, month, dayofyear, is_weekend, quarter] + \
                       lag_features + \
                       [rolling_mean_24, rolling_std_24, rolling_mean_168]

            # Scale and predict
            features_array = np.array(features).reshape(1, -1)
            features_scaled = scaler.transform(features_array)
            prediction = model.predict(features_scaled)[0]

            predictions.append({
                'hour': hour,
                'consumption': float(prediction)
            })

        total_daily = sum([p['consumption'] for p in predictions])
        avg_hourly = total_daily / 24

        return jsonify({
            'success': True,
            'date': date_str,
            'day_name': target_date.strftime('%A'),
            'hourly_predictions': predictions,
            'total_daily': float(total_daily),
            'average_hourly': float(avg_hourly),
            'unit': 'MWh'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/statistics')
def statistics():
    """Get historical statistics"""
    try:
        stats = {
            'mean': float(historical_data['consumption'].mean()),
            'median': float(historical_data['consumption'].median()),
            'std': float(historical_data['consumption'].std()),
            'min': float(historical_data['consumption'].min()),
            'max': float(historical_data['consumption'].max()),
            'total_records': len(historical_data)
        }
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
