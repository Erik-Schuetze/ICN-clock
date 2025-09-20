# ICN Clock

A digital clock display with DVB departure times and temperature monitoring.

## Features
- Digital clock display
- DVB departure times for tram lines 7 and 12
- Inside temperature via HDC1080 sensor
- Outside temperature via wttr.in API
- Fullscreen display optimized for Raspberry Pi

## Installation
1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Dependencies
- tkinter for GUI
- SDL_Pi_HDC1080 for temperature sensor
- dvb for Dresden public transport API
- requests for weather data