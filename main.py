import tkinter as tk
import os
import time
import SDL_Pi_HDC1080
import dvb
from config import *

os.environ['DISPLAY'] = DISPLAY
bg_color = "black"
fg_color = "white"

# Initialize sensor with error handling
try:
    hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
    sensor_available = True
except OSError as e:
    print(f"Failed to initialize temperature sensor: {e}")
    hdc1080 = None
    sensor_available = False

departure_labels = []

def update_departures():
    # Clear existing labels
    for label in departure_labels:
        label.destroy()
    departure_labels.clear()
    
    # Get new departures
    departures = dvb.monitor(STATION, TIME_OFFSET, NUM_RESULTS, CITY)[:7]
    
    # Create new labels
    y_offset = 70
    line_spacing = 70
    departure_font_size = 40
    for dep in departures:
        if dep['line'] in LINES_TO_SHOW:
            # Create line and direction label
            line_label = tk.Label(root, text=dep['line'], font=("Piboto Light", departure_font_size), bg=bg_color, fg=fg_color)
            line_label.place(x=screen_width-440, y=y_offset, anchor="e")
            departure_labels.append(line_label)
            direction_label = tk.Label(root, text=dep['direction'], font=("Piboto Thin", departure_font_size-5), bg=bg_color, fg=fg_color)
            direction_label.place(x=screen_width-425, y=y_offset, anchor="w")
            departure_labels.append(direction_label)
            
            # Create arrival time label with different style
            time_label = tk.Label(root, text=f"{dep['arrival']}m", font=("Piboto", departure_font_size), bg=bg_color, fg=fg_color)
            time_label.place(x=screen_width-40, y=y_offset, anchor="e")
            departure_labels.append(time_label)
            
            y_offset += line_spacing
    
    # Schedule next update
    root.after(DEPARTURE_UPDATE_INTERVAL, update_departures)

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
    divider1.place(x=screen_width/6*1.5-30-20, y=divider_y)

    # Second divider (between month and day)
    divider2 = tk.Canvas(root, width=2, height=divider_height, bg=bg_color, highlightthickness=0)
    divider2.create_line(1, 0, 1, divider_height, fill=fg_color, width=2)
    divider2.place(x=screen_width/6*2.5-30+30, y=divider_y)
    
    # Position header labels
    date_labels['year_header'].place(x=screen_width/6-30, y=screen_height/5*4-date_font_size, anchor="center")
    date_labels['month_header'].place(x=screen_width/6*2-30, y=screen_height/5*4-date_font_size, anchor="center")
    date_labels['day_header'].place(x=screen_width/6*3-30, y=screen_height/5*4-date_font_size, anchor="center")
    
    # Position value labels
    date_labels['year_value'].place(x=screen_width/6-30, y=screen_height/5*4+date_font_size, anchor="center")
    date_labels['month_value'].place(x=screen_width/6*2-30, y=screen_height/5*4+date_font_size, anchor="center")
    date_labels['day_value'].place(x=screen_width/6*3-30, y=screen_height/5*4+date_font_size, anchor="center")
    
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
        inside_temp = hdc1080.readTemperature()
        inside_hum = hdc1080.readHumidity()
        inside_co2 = 0  # Placeholder for CO2 value
        temp_label.config(text=f"{inside_temp:.1f}°C")
        hum_label.config(text=f"{inside_hum:.1f}%")
        hum_label.config(text=f"{inside_co2:.0f}ppm")
    except Exception as e:
        temp_label.config(text="00°C")
        hum_label.config(text="00%")
        co2_label.config(text="0000ppm")
        print(f"Temperature sensor error: {e}")
    
    root.after(TEMP_UPDATE_INTERVAL, update_air_data)

def update_color_scheme():
    hour = time.strftime("%H")
    # Flash the colon
    if int(hour)< SUNSET and int(hour) >= SUNRISE:
        fg_color = "black"
        bg_color = "white"
        root.configure(bg=bg_color)
        hour_label.configure(bg=bg_color, fg=fg_color)
        minute_label.configure(bg=bg_color, fg=fg_color)
        second_label.configure(bg=bg_color, fg=fg_color)
        colon_label.configure(bg=bg_color, fg=fg_color)
        temp_label.configure(bg=bg_color, fg=fg_color)
        hum_label.configure(bg=bg_color, fg=fg_color)
        co2_label.configure(bg=bg_color, fg=fg_color)
        for label in departure_labels:
            label.configure(bg=bg_color, fg=fg_color)
        for key, label in date_labels.items():
            label.configure(bg=bg_color, fg=fg_color)
    else:
        fg_color = "white"
        bg_color = "black"
        root.configure(bg=bg_color)
        hour_label.configure(bg=bg_color, fg=fg_color)
        minute_label.configure(bg=bg_color, fg=fg_color)
        second_label.configure(bg=bg_color, fg=fg_color)
        colon_label.configure(bg=bg_color, fg=fg_color)
        temp_label.configure(bg=bg_color, fg=fg_color)
        hum_label.configure(bg=bg_color, fg=fg_color)
        co2_label.configure(bg=bg_color, fg=fg_color)
        for label in departure_labels:
            label.configure(bg=bg_color, fg=fg_color)
        for key, label in date_labels.items():
            label.configure(bg=bg_color, fg=fg_color)
    root.after(900000, update_color_scheme)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.configure(bg=bg_color)
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

# Create labels with specific positions
hour_label = tk.Label(root, font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
hour_label.place(x=20, y=screen_height/2-160, anchor="w")

colon_label = tk.Label(root, text=":", font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
colon_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="e")

minute_label = tk.Label(root, font=("Piboto Light", 350), bg=bg_color, fg=fg_color)
minute_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="w")

second_label = tk.Label(root, font=("Piboto Light", 70), bg=bg_color, fg=fg_color)
second_label.place(x=30+screen_width/3*2-90, y=screen_height/2, anchor="w")

# Create date labels
date_labels = create_date_labels()

temp_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
temp_label.place(x=screen_width/6*4.5-30, y=screen_height/5*4+50, anchor="center")

hum_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
hum_label.place(x=screen_width/6*5-30, y=screen_height/5*4+50, anchor="center")

co2_label = tk.Label(root, font=("Piboto Thin", 40), bg=bg_color, fg=fg_color)
co2_label.place(x=screen_width/6*5.6-30, y=screen_height/5*4+50, anchor="center")

update_clock()
update_departures()
update_air_data()
update_color_scheme()
root.mainloop()


