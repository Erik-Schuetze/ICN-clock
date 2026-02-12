import tkinter as tk
import os
import time
import sys
import requests
from datetime import datetime

# Add lib directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from sensor_wrapper import I2cConnection, LinuxI2cTransceiver, Scd4xI2cDevice
from config import *

os.environ['DISPLAY'] = DISPLAY

# Global variables for weather and sunrise/sunset
outdoor_temp = None
sunrise_hour = 6  # Default fallback values
sunset_hour = 22

def fetch_weather():
    """Fetch current outdoor temperature from Open-Meteo API"""
    global outdoor_temp
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m"
        response = requests.get(url, timeout=10)
        data = response.json()
        outdoor_temp = data['current']['temperature_2m']
        print(f"Updated outdoor temperature: {outdoor_temp}°C")
    except Exception as e:
        print(f"Failed to fetch weather: {e}")
        outdoor_temp = None

def fetch_sunrise_sunset():
    """Fetch sunrise and sunset times from Open-Meteo API"""
    global sunrise_hour, sunset_hour
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=sunrise,sunset&timezone=auto"
        response = requests.get(url, timeout=10)
        data = response.json()

        # Get today's sunrise and sunset
        sunrise_str = data['daily']['sunrise'][0]  # Format: "2024-01-01T07:30"
        sunset_str = data['daily']['sunset'][0]    # Format: "2024-01-01T16:45"

        # Extract hour from ISO format
        sunrise_hour = int(sunrise_str.split('T')[1].split(':')[0])
        sunset_hour = int(sunset_str.split('T')[1].split(':')[0])

        print(f"Updated sunrise: {sunrise_hour}:00, sunset: {sunset_hour}:00")
    except Exception as e:
        print(f"Failed to fetch sunrise/sunset: {e}")
        # Keep using the current values as fallback

# Initialize sensor with error handling
try:
    # Initialize I²C bus (bus=1 is default on Pi) using the library's transceiver adapter
    transceiver = LinuxI2cTransceiver("/dev/i2c-1")
    i2c = I2cConnection(transceiver)
    scd4x = Scd4xI2cDevice(i2c)

    scd4x.stop_periodic_measurement()
    scd4x.reinit()
    time.sleep(5)

    scd4x.start_periodic_measurement()
    time.sleep(5)

    sensor_available = True
except OSError as e:
    print(f"Failed to initialize temperature sensor: {e}")
    scd4x = None
    sensor_available = False


def create_date_labels():
    """Create and return labels for date display"""
    date_font_size = 50
    date_labels = {}
    
    # Create header labels
    date_labels['year_header'] = tk.Label(root, text="YEAR", font=("Piboto Thin", date_font_size), bg=bg_color, fg=fg_color)
    date_labels['month_header'] = tk.Label(root, text="MONTH", font=("Piboto Thin", date_font_size), bg=bg_color, fg=fg_color)
    date_labels['day_header'] = tk.Label(root, text="DAY", font=("Piboto Thin", date_font_size), bg=bg_color, fg=fg_color)
    
    # Create value labels
    date_labels['year_value'] = tk.Label(root, font=("Piboto Light", date_font_size), bg=bg_color, fg=fg_color)
    date_labels['month_value'] = tk.Label(root, text="MONTH", font=("Piboto Light", date_font_size), bg=bg_color, fg=fg_color)
    date_labels['day_value'] = tk.Label(root, text="DAY", font=("Piboto Light", date_font_size), bg=bg_color, fg=fg_color)
    
    # Create vertical dividers using Canvas
    divider_height = date_font_size * 2.4  # Height of the divider lines
    divider_y = screen_height/5*4 - date_font_size*1.2  # Top position aligned with headers

    # First divider (between year and month)
    divider1 = tk.Canvas(root, width=2, height=divider_height, bg=bg_color, highlightthickness=0)
    divider1.create_line(1, 0, 1, divider_height, fill=fg_color, width=2)
    divider1.place(x=screen_width/6*1.5-15-20, y=divider_y)

    # Second divider (between month and day)
    divider2 = tk.Canvas(root, width=2, height=divider_height, bg=bg_color, highlightthickness=0)
    divider2.create_line(1, 0, 1, divider_height, fill=fg_color, width=2)
    divider2.place(x=screen_width/6*2.5-15+30, y=divider_y)
    
    # Position header labels
    date_labels['year_header'].place(x=screen_width/6-15, y=screen_height/5*4-date_font_size, anchor="center")
    date_labels['month_header'].place(x=screen_width/6*2-15, y=screen_height/5*4-date_font_size, anchor="center")
    date_labels['day_header'].place(x=screen_width/6*3-15, y=screen_height/5*4-date_font_size, anchor="center")
    
    # Position value labels
    date_labels['year_value'].place(x=screen_width/6-15, y=screen_height/5*4+date_font_size, anchor="center")
    date_labels['month_value'].place(x=screen_width/6*2-15, y=screen_height/5*4+date_font_size, anchor="center")
    date_labels['day_value'].place(x=screen_width/6*3-15, y=screen_height/5*4+date_font_size, anchor="center")
    
    return date_labels

def update_clock():
    # Get current time and date
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    
    # Update time labels
    hour_label.config(text=hour)
    minute_label.config(text=minute)
    second_label.config(text=second)
    
    # Update date labels
    date_labels['year_value'].config(text=year)
    date_labels['month_value'].config(text=month)
    date_labels['day_value'].config(text=day)

    # Flash the colon
    if int(second) % 2 == 0:
        colon_label.config(fg="black")
    else:
        colon_label.config(fg="white")
    
    root.after(1000, update_clock)

def update_air_data():
    if not sensor_available:
        # Skip sensor reading if initialization failed
        temp_label.config(text="00°C")
        hum_label.config(text="00%")
        co2_label.config(text="0000ppm")
        root.after(TEMP_UPDATE_INTERVAL, update_air_data)
        return

    try:
        co2, temp, rh = scd4x.read_measurement()
        temp_label.config(text=f"{temp.degrees_celsius:.0f}°C")
        hum_label.config(text=f"{rh.percent_rh:.0f}%")
        co2_label.config(text=f"{co2.co2}ppm")
    except Exception as e:
        temp_label.config(text="00°C")
        hum_label.config(text="00%")
        co2_label.config(text="0000ppm")
        print(f"Temperature sensor error: {e}")
    
    root.after(TEMP_UPDATE_INTERVAL, update_air_data)

def update_outdoor_temp():
    """Update outdoor temperature display"""
    fetch_weather()
    if outdoor_temp is not None:
        outdoor_temp_label.config(text=f"{outdoor_temp:.0f}°C")
    else:
        outdoor_temp_label.config(text="--°C")

    root.after(WEATHER_UPDATE_INTERVAL, update_outdoor_temp)

def update_sunrise_sunset():
    """Update sunrise and sunset times"""
    fetch_sunrise_sunset()
    root.after(SUNRISE_SUNSET_UPDATE_INTERVAL, update_sunrise_sunset)

def get_color_scheme():
    hour = int(time.strftime("%H"))
    if hour < sunset_hour and hour >= sunrise_hour:
        fg_color = "black"
        bg_color = "white"
    else:
        fg_color = "white"
        bg_color = "black"
    return fg_color, bg_color

def update_color_scheme():
    fg_color, bg_color = get_color_scheme()
    root.configure(bg=bg_color)
    hour_label.configure(bg=bg_color, fg=fg_color)
    minute_label.configure(bg=bg_color, fg=fg_color)
    second_label.configure(bg=bg_color, fg=fg_color)
    colon_label.configure(bg=bg_color, fg=fg_color)
    temp_label.configure(bg=bg_color, fg=fg_color)
    hum_label.configure(bg=bg_color, fg=fg_color)
    co2_label.configure(bg=bg_color, fg=fg_color)
    outdoor_temp_label.configure(bg=bg_color, fg=fg_color)
    for key, label in date_labels.items():
        label.configure(bg=bg_color, fg=fg_color)
    root.after(900000, update_color_scheme)

root = tk.Tk()

# Handle window sizing based on configuration
if FULLSCREEN:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
else:
    # Use custom window size if specified, otherwise use screen size
    screen_width = getattr(sys.modules['config'], 'WINDOW_WIDTH', root.winfo_screenwidth())
    screen_height = getattr(sys.modules['config'], 'WINDOW_HEIGHT', root.winfo_screenheight())
    root.geometry(f"{screen_width}x{screen_height}")

fg_color, bg_color = get_color_scheme()
root.configure(bg=bg_color)

# Only go fullscreen if configured
if FULLSCREEN:
    # replace immediate fullscreen with a guarded delayed call
    def ensure_fullscreen(retries=5, delay_ms=1000):
        try:
            root.update_idletasks()
            root.attributes("-fullscreen", True)
            # verify: if window still small, try again
            if root.winfo_width() < screen_width - 50 and retries > 0:
                root.after(delay_ms, lambda: ensure_fullscreen(retries-1, delay_ms))
        except Exception:
            if retries > 0:
                root.after(delay_ms, lambda: ensure_fullscreen(retries-1, delay_ms))

    ensure_fullscreen()
else:
    # Windowed mode - set title for easier window management
    root.title("ICN Clock - Test Mode")

# Create labels with specific positions
hour_label = tk.Label(root, font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
hour_label.place(x=30, y=screen_height/2-145, anchor="w")

colon_label = tk.Label(root, text=":", font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
colon_label.place(x=40+screen_width/3, y=screen_height/2-145, anchor="e")

minute_label = tk.Label(root, font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
minute_label.place(x=40+screen_width/3, y=screen_height/2-145, anchor="w")

second_label = tk.Label(root, font=("Piboto Light", 80), bg=bg_color, fg=fg_color)
second_label.place(x=40+screen_width/3*2-80, y=screen_height/2, anchor="w")

# Create date labels
date_labels = create_date_labels()

temp_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
temp_label.place(x=screen_width-40, y=screen_height/5*1, anchor="e")

hum_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
hum_label.place(x=screen_width-40, y=screen_height/5*2, anchor="e")

co2_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
co2_label.place(x=screen_width-40, y=screen_height/5*3, anchor="e")

outdoor_temp_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
outdoor_temp_label.place(x=screen_width-40, y=screen_height/5*4, anchor="e")

update_clock()
update_air_data()
update_outdoor_temp()
update_sunrise_sunset()
update_color_scheme()
root.mainloop()


