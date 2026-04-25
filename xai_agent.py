"""
XAI Explanation Agent
=====================
Explains *why* the alert was triggered.
Uses statistical z-scores against a baseline to highlight which sensors deviated the most,
combined with explicit sub-agent risk flags.
"""
import pandas as pd

_baseline = {}

def initialize_xai(csv_path: str):
    global _baseline
    try:
        df = pd.read_csv(csv_path).head(100)
        features = ['altitude', 'speed', 'engine_temp', 'wind_speed', 'vibration', 'fuel_flow', 'cabin_pressure']
        for col in features:
            _baseline[col] = {
                'mean': df[col].mean(),
                'std': df[col].std() + 1e-5 # avoid division by zero
            }
    except Exception as e:
        pass

def evaluate(alt: float, speed: float, temp: float, wind: float, vib: float, fuel: float, cabin: float,
             engine_risk: str, weather_risk: str, stability_risk: str, anomaly_label: str, overall_risk: str) -> str:
                 
    if overall_risk == "STABLE":
        return "All telemetry within expected operational margins."
        
    explanations = []
    
    if engine_risk == "HIGH":
        explanations.append("Elevated engine temperature or vibration.")
    if weather_risk == "HIGH":
        explanations.append("High wind speed detected (turbulence).")
    if stability_risk == "HIGH":
        explanations.append("Unstable altitude/speed correlation (rapid descent).")
        
    # Find statistically anomalous features via local Z-scores
    if _baseline:
        vals = {
            'altitude': alt, 'speed': speed, 'engine_temp': temp, 
            'wind_speed': wind, 'vibration': vib, 'fuel_flow': fuel, 'cabin_pressure': cabin
        }
        z_scores = {k: abs(v - _baseline[k]['mean']) / _baseline[k]['std'] for k, v in vals.items()}
        sorted_features = sorted(z_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Only list features with a significant deviation > 2.0 sigmas
        top_deviations = [f"{k.replace('_', ' ')}" for k, z in sorted_features if z > 2.0]
        if top_deviations:
            explanations.append(f"Statistical anomalies found in: {', '.join(top_deviations[:2])}.")
            
    if not explanations and anomaly_label == "ANOMALY":
        explanations.append("Unsupervised ML model detected unknown multi-variate anomaly.")

    return " ".join(explanations)
