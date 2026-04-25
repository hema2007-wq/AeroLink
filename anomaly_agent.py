"""
Anomaly Prediction Agent
========================
Uses Isolation Forest (unsupervised ML) to predict abnormal flight states.
"""
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

_model = None
_features = ['altitude', 'speed', 'engine_temp', 'wind_speed', 'vibration', 'fuel_flow', 'cabin_pressure']

def initialize_model(csv_path: str):
    """
    Fits the Isolation Forest on the first 100 rows to establish a 'normal' baseline.
    """
    global _model
    try:
        df = pd.read_csv(csv_path)
        # Use entire dataset as baseline to prevent random-walk drift false positives
        baseline_df = df[_features]
        
        _model = IsolationForest(n_estimators=100, contamination=0.15, random_state=42)
        _model.fit(baseline_df)
    except Exception as e:
        logging.error(f"Failed to initialize Anomaly Agent: {e}")

def evaluate(alt: float, speed: float, temp: float, wind: float, vib: float, fuel: float, cabin: float):
    if _model is None:
        return 0.0, "NORMAL"
        
    X = pd.DataFrame([[alt, speed, temp, wind, vib, fuel, cabin]], columns=_features)
    
    # 1 for inlier, -1 for outlier
    prediction = _model.predict(X)[0]
    
    # Get anomaly score and scale it for the dashboard
    raw_score = -_model.score_samples(X)[0] 
    
    # Normal raw_scores are typically around 0.45-0.55. Anomalies are > 0.60.
    # Map raw score to a [0, 1] range
    mapped_score = min(max((raw_score - 0.45) / 0.2, 0.0), 1.0)
    
    # Only assign ANOMALY if it's statistically significant
    label = "ANOMALY" if prediction == -1 and mapped_score > 0.65 else "NORMAL"
    return float(mapped_score), label
