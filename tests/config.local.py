# Configuration for local testing on PC/Mac
DISPLAY = ':0'
FULLSCREEN = False  # Set to False for easier testing in windowed mode

# Window size for local testing (simulates your display)
# Set to None to use actual screen size, or specify dimensions
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 720

# Location settings (used for weather and sunrise/sunset times)
# Get your coordinates from: https://www.latlong.net/
LATITUDE = 51.0504   # Dresden, Germany (adjust to your city)
LONGITUDE = 13.7373  # Dresden, Germany (adjust to your city)

# Mock mode for testing on non-Raspberry Pi systems
MOCK_MODE = True  # Enable mock sensor data for local testing

# Update intervals (in milliseconds)
TEMP_UPDATE_INTERVAL = 5000      # Indoor sensor update interval
WEATHER_UPDATE_INTERVAL = 600000  # Outdoor weather update interval (10 minutes)
SUNRISE_SUNSET_UPDATE_INTERVAL = 3600000  # Update sunrise/sunset every hour

