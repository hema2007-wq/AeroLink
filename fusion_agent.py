"""
Risk Fusion Agent
=================
Fuses outputs from all other agents into a single overall risk assessment.
"""

def evaluate(engine_risk: str, weather_risk: str, stability_risk: str, anomaly_score: float, anomaly_label: str) -> str:
    high_count = [engine_risk, weather_risk, stability_risk].count("HIGH")
    
    # Rule 1: CRITICAL
    if high_count >= 2 or (high_count == 1 and anomaly_label == "ANOMALY"):
        return "CRITICAL"
        
    # Rule 2: WARNING
    if high_count == 1 or anomaly_label == "ANOMALY":
        return "WARNING"
        
    # Default
    return "STABLE"
