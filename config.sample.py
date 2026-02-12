# Copy this file to config.py and adjust values
DISPLAY = ':0'
FULLSCREEN = True

# Location settings (used for weather and sunrise/sunset times)
# Get your coordinates from: https://www.latlong.net/
LATITUDE = 51.0504   # Dresden, Germany (adjust to your city)
LONGITUDE = 13.7373  # Dresden, Germany (adjust to your city)

# Window size (only used when FULLSCREEN = False)
# Uncomment and set to simulate specific display dimensions for testing
# WINDOW_WIDTH = 2560
# WINDOW_HEIGHT = 720

# Mock mode for testing on non-Raspberry Pi systems
MOCK_MODE = False  # Set to True to use mock sensor data

# Update intervals (in milliseconds)
TEMP_UPDATE_INTERVAL = 10000     # Indoor sensor update interval
WEATHER_UPDATE_INTERVAL = 600000  # Outdoor weather update interval (10 minutes)
SUNRISE_SUNSET_UPDATE_INTERVAL = 3600000  # Update sunrise/sunset every hour
