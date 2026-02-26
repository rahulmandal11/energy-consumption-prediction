# ⚡ Energy Consumption Prediction Using Machine Learning

A machine learning project for predicting hourly electricity consumption using historical time series data (2016-2021). Built with Gradient Boosting Regressor and deployed as an interactive Flask web application.

**Project Type:** Academic Assignment | Time Series Forecasting  
**Author:** Rahul  
**Location:** Ahmedabad, Gujarat, India  
**Date:** February 2026  

---

## 📋 Project Overview

This project demonstrates the application of supervised machine learning to energy consumption forecasting. The system predicts hourly electricity consumption in megawatt-hours (MWh) based on temporal features, historical lag values, and rolling statistics.

### Key Features
- **Gradient Boosting Regressor** trained on 52,966 hourly records
- **33 engineered features** (temporal + lag + rolling statistics)
- **R² = 0.9954** and **MAPE < 1%** on test set
- Interactive **Flask web application** with 3 prediction modes
- Comprehensive **Jupyter notebook** with EDA and training pipeline

---

## 🎯 Assignment Requirements

This project fulfills all required components:

1. ✅ **Model Selection**: Gradient Boosting chosen over ARIMA, Random Forest, and LSTM with justification
2. ✅ **Data Preprocessing**: EDA, feature engineering, chronological splitting, scaling
3. ✅ **Model Training**: Trained on historical data with hyperparameter tuning
4. ✅ **Model Evaluation**: RMSE, MAE, R², MAPE metrics with interpretation
5. ✅ **Insights**: Energy management applications and sustainability implications

---

## 📊 Results

| Metric | Validation | Test |
|--------|------------|------|
| RMSE   | 82.45 MWh  | 79.32 MWh |
| MAE    | 58.23 MWh  | 56.17 MWh |
| R²     | 0.9956     | 0.9954 |
| MAPE   | 0.59%      | 0.57% |

**Feature Importance:** Previous hour consumption (lag_1) accounts for 91.27% of predictive power.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/energy-consumption-prediction.git
cd energy-consumption-prediction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the notebook (optional - pre-trained model included)**
```bash
jupyter notebook notebooks/EDA_Analysis.ipynb
# Run all cells to train model from scratch
```

4. **Start the Flask application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

---

## 📁 Project Structure

```
energy-consumption-prediction/
│
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── notebooks/
│   └── EDA_Analysis.ipynb          # Data analysis & model training
│
├── templates/
│   └── index.html                  # Web interface
│
├── static/
│   ├── css/style.css               # Styling
│   └── js/script.js                # Frontend logic
│
├── model/
│   ├── energy_prediction_model.pkl # Trained model
│   └── feature_scaler.pkl          # Feature scaler
│
└── data/
    ├── energy_data.csv             # Original dataset (52,966 rows)
    └── sample_data.csv             # Recent 1,000 records for predictions
```

---

## 🔧 Technologies Used

- **Python 3.9+** - Programming language
- **scikit-learn** - Machine learning (Gradient Boosting)
- **pandas & numpy** - Data processing
- **Flask** - Web framework
- **matplotlib & seaborn** - Visualization
- **Chart.js** - Interactive charts
- **Jupyter** - Exploratory analysis

---

## 📈 Model Approach

### 1. Feature Engineering
- **Temporal features** (6): hour, day of week, month, quarter, day of year, weekend indicator
- **Lag features** (24): Previous 24 hours of consumption
- **Rolling statistics** (3): 24-hour mean/std, 168-hour (weekly) mean

### 2. Model Selection
**Gradient Boosting Regressor** chosen for:
- Handling non-linear patterns
- Feature importance interpretability
- Training efficiency
- Robustness to overfitting

### 3. Data Splitting
- **80% Training** (Dec 2015 - Aug 2020)
- **10% Validation** (Aug 2020 - Nov 2020)
- **10% Test** (Nov 2020 - Jan 2021)

Chronological split prevents data leakage.

---

## 🌐 Web Application

The Flask app provides three prediction modes:

1. **Quick Predict**: Manual input of temporal features
2. **Date Predict**: Select date and hour for prediction
3. **Full Day Predict**: Generate 24-hour forecast with chart

---

## 📊 Key Insights

### Peak Consumption Patterns
- **Peak hour:** 17:00 (5 PM) - 10,015 MWh
- **Lowest hour:** 01:00 (1 AM) - 8,465 MWh
- **Peak month:** January (winter heating)
- **Lowest month:** June (mild weather)
- **Weekdays:** 6.8% higher than weekends

### Energy Management Applications
1. **Demand Forecasting** - 24-hour load prediction
2. **Peak Load Management** - Demand response programs
3. **Grid Stability** - Supply-demand balancing
4. **Renewable Integration** - Optimized clean energy dispatch

---

## 📝 Report

Full academic report available: `Energy-Consumption-Report.docx`

Includes:
- Literature review
- Detailed methodology
- Results and evaluation
- Interpretation and insights
- Sustainability implications
- References (8 academic sources)

---

## 🎓 Learning Outcomes

This project demonstrates understanding of:
- Time series forecasting techniques
- Feature engineering for temporal data
- Gradient boosting algorithms
- Model evaluation and validation
- Production deployment with Flask
- Data visualization and interpretation

---

## ⚠️ Limitations

- Requires 168 hours of historical data for full features
- Does not incorporate weather data
- Trained on single geographic region
- May need retraining for long-term pattern shifts

---

## 🔮 Future Enhancements

- [ ] Incorporate weather data (temperature, humidity)
- [ ] Add holiday/special event features
- [ ] Implement online learning for concept drift
- [ ] Extend to multi-location forecasting
- [ ] Add confidence intervals to predictions
- [ ] Deploy with Docker containerization

---

## 📄 License

This project is created for academic purposes.

---

## 🙏 Acknowledgments

- Dataset: Hourly electricity consumption data (2016-2021)
- Assignment: Machine Learning course project
- Tools: scikit-learn, Flask, Chart.js communities

---

## 📧 Contact

**Rahul**  
Ahmedabad, Gujarat, India  
[GitHub Profile](https://github.com/rahulmandal11)

---

⭐ If you found this project helpful for learning, please give it a star!
