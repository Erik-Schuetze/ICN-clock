# Configuration for local testing on PC/Mac
DISPLAY = ':0'
FULLSCREEN = False  # Set to False for easier testing in windowed mode

# Window size for local testing (simulates your display)
# Set to None to use actual screen size, or specify dimensions
WINDOW_WIDTH = 2560
WINDOW_HEIGHT = 720

SUNSET = 22
SUNRISE = 6

# Mock mode for testing on non-Raspberry Pi systems
MOCK_MODE = True  # Enable mock sensor data for local testing

# Transport settings
STATION = 'Tharandter Straße'
CITY = 'Dresden'
LINES_TO_SHOW = ['7', '12', '6']
TIME_OFFSET = 0  # minutes in future
NUM_RESULTS = 10

# Temperature and humidity sensor settings
TEMP_UPDATE_INTERVAL = 5000
DEPARTURE_UPDATE_INTERVAL = 120000

