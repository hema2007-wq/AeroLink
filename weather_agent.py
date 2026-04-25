"""
Weather Monitoring Agent
========================
Monitors wind speed for extreme turbulence.
Returns HIGH risk if wind speeds are dangerous.
"""

def evaluate(wind_speed: float) -> str:
    WIND_WARNING = 40.0
    
    if wind_speed > WIND_WARNING:
        return "HIGH"
    return "NORMAL"
