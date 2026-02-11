# Copy this file to config.py and adjust values
DISPLAY = ':0'
FULLSCREEN = True
SUNSET = 22
SUNRISE = 6

# Window size (only used when FULLSCREEN = False)
# Uncomment and set to simulate specific display dimensions for testing
# WINDOW_WIDTH = 2560
# WINDOW_HEIGHT = 720

# Mock mode for testing on non-Raspberry Pi systems
MOCK_MODE = False  # Set to True to use mock sensor data

# Transport settings
STATION = 'Your Station Name'
CITY = 'Your City'
LINES_TO_SHOW = ['1', '2']  # Lines you want to monitor
TIME_OFFSET = 0
NUM_RESULTS = 10

# Temperature and humidity sensor settings
TEMP_UPDATE_INTERVAL = 10000
DEPARTURE_UPDATE_INTERVAL = 180000