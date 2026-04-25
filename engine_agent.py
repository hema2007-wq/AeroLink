"""
Engine Monitoring Agent
=======================
Monitors engine temperature and vibration.
Returns HIGH risk if temperature is extreme or vibration is excessive.
"""

def evaluate(engine_temp: float, vibration: float) -> str:
    # Thresholds
    TEMP_WARNING = 750.0
    VIB_WARNING = 0.5

    if engine_temp > TEMP_WARNING or vibration > VIB_WARNING:
        return "HIGH"
    return "NORMAL"
