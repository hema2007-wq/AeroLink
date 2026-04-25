"""
Advisory Agent
==============
Converts aggregated risks into actionable guidance for the pilot.
"""

def evaluate(overall_risk: str, engine_risk: str, weather_risk: str, stability_risk: str) -> str:
    messages = []
    
    if overall_risk == "CRITICAL":
        messages.append("⚠️ IMMEDIATE ACTION REQUIRED.")
        
    if engine_risk == "HIGH":
        messages.append("Reduce engine load and monitor temperature/vibration trend.")
        
    if weather_risk == "HIGH":
        messages.append("Change altitude/vector to avoid turbulence.")
        
    if stability_risk == "HIGH":
        messages.append("Arrest descent immediately; increase thrust.")
        
    if overall_risk == "WARNING" and not messages:
        messages.append("Monitor systems closely - anomalous behavior detected.")
        
    if overall_risk == "STABLE":
        messages.append("Systems nominal. Continue flight plan.")
        
    return " | ".join(messages)
