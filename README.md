# Agentic AI-Based Real-Time Flight Safety Monitoring System

A proactive real-time aviation safety system designed to prevent flight accidents acting as a digital co-pilot. It combines Pathway real-time processing, Unsupervised Machine Learning, Explainable AI (XAI), and a multi-agent domain-specific architecture into a single intelligent product.

## Features
- **Multi-Agent Architecture**: Separate isolated agents handle Weather, Stability, and Engine mechanics independently.
- **Anomaly ML Extractor**: Employs an Isolation Forest to predict hidden correlative failures without hardcoded logic.
- **Streaming Pipeline**: Demonstrates stream-capable analysis loop handling data continuously.
- **XAI Integration**: Automatically analyzes standard deviation limits to explicitly explain what sensors triggered the failure and why.
- **Executive Dashboard**: A highly polished tactical UI providing critical systems info cleanly.

## Quickstart

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Generate the Test Mission File**
```bash
python generate_data.py
```
*Creates `data/flight_data.csv` comprising 500 ticks populated with realistic anomalies.*

3. **Run the Agentic Safety Core**
```bash
python main.py
```
*Starts evaluating streaming data row by row, resulting in `outputs/alerts_output.csv`.*

4. **Launch the Dashboard UI**
```bash
streamlit run dashboard.py
```

## Directory Structure
```
flight_safety_system/
├── data/                  # Generated synthetic logs
├── outputs/               # Evaluated analytical outputs
├── agents/                # The logic units processing telemetry
│   ├── engine_agent.py
│   ├── anomaly_agent.py
│   └── ...
├── generate_data.py       # Data creation script
├── main.py                # Main streaming event loop
├── dashboard.py           # Polished UI viewer
└── requirements.txt
```
