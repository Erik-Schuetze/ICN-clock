# ICN Clock

A modern digital clock display with public transport departures and temperature monitoring.

## Features
- Large digital clock display with flashing colon
- DVB departure times for Dresden public transport (tram lines configurable)
- Inside temperature via HDC1080 sensor
- Outside temperature via wttr.in API
- Fullscreen display optimized for Raspberry Pi

## Important Note
The public transport feature only works in Dresden, Germany as it uses the [dvbpy library](https://github.com/offenesdresden/dvbpy) which is specific to Dresden's DVB (Dresdner Verkehrsbetriebe) system. To adapt this for other cities, you would need to implement a different transport API.

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

3. Configure your local settings:
```bash
cp config.sample.py config.py
# Edit config.py with your preferred settings
```

## Usage
```bash
python main.py
```

## Dependencies
- tkinter for GUI
- SDL_Pi_HDC1080 for temperature sensor
- dvbpy for Dresden public transport API (Dresden-only)
- requests for weather data

## Display Requirements
- Raspberry Pi with display
- X server running
- Piboto font family installed