"""
Stability Monitoring Agent
==========================
Monitors altitude and speed for severe, sudden drops.
Stores a rolling history to detect rapid descent.
"""

_history_alt = []
_history_speed = []

def evaluate(altitude: float, speed: float) -> str:
    global _history_alt, _history_speed
    
    _history_alt.append(altitude)
    _history_speed.append(speed)
    
    if len(_history_alt) > 10:
        _history_alt.pop(0)
        _history_speed.pop(0)
        
    avg_alt = sum(_history_alt) / len(_history_alt)
    avg_speed = sum(_history_speed) / len(_history_speed)
    
    # Check if there is a rapid drop from the rolling average
    alt_drop = avg_alt - altitude
    speed_drop = avg_speed - speed
    
    if alt_drop > 500 and speed_drop > 20:
        return "HIGH"
    return "NORMAL"
