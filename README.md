# ICN Clock

## Features
- Large digital clock display with flashing colon
- **Outdoor temperature** from Open-Meteo weather API (no API key required)
- Temperature, humidity, and CO2 monitoring via Sensirion SCD4x sensor
- **Automatic sunrise/sunset detection** based on your location
- Day/night color scheme switching
- Fullscreen display optimized for Raspberry Pi
- **Mock mode for local testing on any PC/Mac**

## 📁 Project Structure

```
ICN-clock/
├── main.py              # Main application (START HERE for production)
├── config.py            # Your configuration
├── config.sample.py     # Configuration template
├── requirements.txt     # Python dependencies
├── start.sh             # Production startup script
│
├── lib/                 # Core modules (used by main.py)
│   ├── sensor_wrapper.py    # Auto-selects real/mock sensor
│   ├── mock_sensor.py       # Mock sensor implementation
│   └── SDL_Pi_HDC1080.py    # Legacy sensor (if needed)
│
├── tests/               # Testing tools (for local development)
│   ├── demo_sensor.py       # Quick sensor test
│   ├── test_local.py        # Full app test runner
│   └── config.local.py      # Test configuration
│
└── docs/                # Documentation
    ├── QUICKSTART.md        # Quick start guide
    ├── TESTING.md           # Testing documentation
    └── IMPLEMENTATION.md    # Technical details
```


## Display Requirements (Production)
- Raspberry Pi with display
- X server running
- **Piboto font family** (recommended for optimal display)

### Installing Piboto Font

The application uses the Piboto font family for optimal display on Raspberry Pi. Install it with:

```bash
# Download the font files
git clone https://github.com/thunderbird-1990/fonts-piboto.git
cd fonts-piboto

# Install fonts system-wide
sudo mkdir -p /usr/share/fonts/truetype/piboto
sudo cp ttf/*.ttf /usr/share/fonts/truetype/piboto/

# Update font cache
sudo fc-cache -fv

## 🚀 Quick Start

### For Production (Raspberry Pi)
```bash
python3 main.py
```

### For Local Testing (Mac/PC)
```bash
# Quick sensor demo (30 seconds)
python3 tests/demo_sensor.py

# Full application test
python3 tests/test_local.py
```

## 📖 Documentation

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 30 seconds
- **[docs/TESTING.md](docs/TESTING.md)** - Complete testing guide
- **[docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** - Technical details

## Installation

### For Production (Raspberry Pi)

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings:
```bash
cp config.sample.py config.py
# Edit config.py with your preferences
```

4. Run the application:
```bash
python3 main.py
# or use the startup script
./start.sh
```

### For Local Development (Mac/PC)

1. Copy the test config (already has MOCK_MODE enabled):
```bash
cp tests/config.local.py config.py
```

2. Run tests:
```bash
python3 tests/demo_sensor.py
```

## Configuration

Key settings in `config.py`:

```python
MOCK_MODE = False        # Set to True for local testing
FULLSCREEN = True        # Set to False for windowed mode
LATITUDE = 51.0504       # Your location latitude (for weather & sunrise/sunset)
LONGITUDE = 13.7373      # Your location longitude
```

**Getting your coordinates:**
1. Visit https://www.latlong.net/
2. Enter your city name
3. Copy the latitude and longitude values to your config.py

## Dependencies
- **tkinter** - GUI framework (included with Python)
- **requests** - HTTP library for weather API calls
- **sensirion-i2c-driver** - Real sensor (Raspberry Pi only, optional)
- **sensirion-i2c-scd** - Real sensor (Raspberry Pi only, optional)

## Weather Data
Uses the free **Open-Meteo API** (https://open-meteo.com/) for:
- Current outdoor temperature
- Automatic sunrise and sunset times based on your location
- No API key required!

## Display Requirements (Production)
- Raspberry Pi with display
- X server running
- Piboto font family installed (optional, falls back to available fonts)

## License & Credits

This project displays environmental sensor data using the Sensirion SCD4x sensor.
