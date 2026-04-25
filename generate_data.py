"""
Generate Synthetic Flight Sensor Data
=====================================
Generates realistic multi-sensor telemetry for flight tracking.
Includes normal states and injected realistic anomaly patterns.
"""
import os
import numpy as np
import pandas as pd

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "flight_data.csv")

def generate_data(n_rows=500):
    np.random.seed(42)
    
    # helper for random walk
    def smooth_walk(start, n, step_scale, clip_min, clip_max):
        vals = [start]
        for i in range(1, n):
            # drift towards center slightly to prevent extreme drift
            drift = (start - vals[-1]) * 0.01
            delta = np.random.normal(drift, step_scale)
            v = np.clip(vals[-1] + delta, clip_min, clip_max)
            vals.append(v)
        return np.array(vals)

    # 1. Base telemetry (Normal Flight)
    altitude = smooth_walk(32000, n_rows, 50, 10000, 40000)
    speed = smooth_walk(450, n_rows, 5, 200, 600)
    engine_temp = smooth_walk(600, n_rows, 3, 400, 950)
    wind_speed = smooth_walk(15, n_rows, 2, 0, 150)
    vibration = smooth_walk(0.2, n_rows, 0.02, 0.0, 1.0)
    fuel_flow = smooth_walk(2500, n_rows, 20, 1000, 4000)
    cabin_pressure = smooth_walk(10.9, n_rows, 0.05, 8.0, 12.0)

    # Correlate some variables
    speed += (altitude - np.mean(altitude)) * 0.01
    engine_temp += (speed - np.mean(speed)) * 0.2
    vibration += (engine_temp - 600) * 0.001

    # 2. Inject Anomalies
    
    # Anomaly 1: Engine Overheating & Vibration rising (Rows 150-180)
    for i in range(150, 181):
        engine_temp[i] += (i - 150) * 8 # gradually rises
        vibration[i] += (i - 150) * 0.02
        fuel_flow[i] += (i - 150) * 15 # burns more fuel

    # Anomaly 2: Turbulence Spike (Rows 300-320)
    for i in range(300, 321):
        wind_speed[i] += np.random.uniform(40, 80)
        vibration[i] += np.random.uniform(0.1, 0.3)
        altitude[i] += np.random.uniform(-300, 300) # choppy altitude

    # Anomaly 3: Rapid descent / Instability (Rows 400-420)
    for i in range(400, 421):
        altitude[i] -= (i - 400) * 300
        speed[i] -= (i - 400) * 10
        cabin_pressure[i] += np.random.uniform(0.1, 0.4) # pressure fluctuations

    # 3. Add noise to everything to simulate sensors
    altitude += np.random.normal(0, 10, n_rows)
    speed += np.random.normal(0, 2, n_rows)
    engine_temp += np.random.normal(0, 2, n_rows)
    wind_speed += np.random.normal(0, 1, n_rows)
    vibration += np.random.normal(0, 0.01, n_rows)
    fuel_flow += np.random.normal(0, 5, n_rows)
    cabin_pressure += np.random.normal(0, 0.02, n_rows)

    # 4. Assemble Dataframe
    df = pd.DataFrame({
        "timestamp": np.arange(1, n_rows + 1),
        "altitude": np.round(altitude, 1),
        "speed": np.round(speed, 1),
        "engine_temp": np.round(engine_temp, 1),
        "wind_speed": np.round(wind_speed, 1),
        "vibration": np.round(vibration, 4),
        "fuel_flow": np.round(fuel_flow, 1),
        "cabin_pressure": np.round(cabin_pressure, 2)
    })

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[OK] Generated {n_rows} rows of telemetry data -> {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
