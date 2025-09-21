import tkinter as tk
import os
import time
import SDL_Pi_HDC1080
import dvb
import requests
from config import *

os.environ['DISPLAY'] = DISPLAY

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
departure_labels = []

def update_departures():
    # Clear existing labels
    for label in departure_labels:
        label.destroy()
    departure_labels.clear()
    
    # Get new departures
    departures = dvb.monitor(STATION, TIME_OFFSET, NUM_RESULTS, CITY)
    
    # Create new labels
    y_offset = 65
    departure_font_size = 37
    for dep in departures:
        if dep['line'] in LINES_TO_SHOW:
            # Create line and direction label
            line_label = tk.Label(root, text=dep['line'], font=("Piboto Light", departure_font_size), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            line_label.place(x=screen_width-440, y=y_offset, anchor="e")
            departure_labels.append(line_label)
            direction_label = tk.Label(root, text=dep['direction'], font=("Piboto Thin", departure_font_size), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            direction_label.place(x=screen_width-425, y=y_offset, anchor="w")
            departure_labels.append(direction_label)
            
            # Create arrival time label with different style
            time_label = tk.Label(root, text=f"{dep['arrival']}m", font=("Piboto", departure_font_size), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            time_label.place(x=screen_width-40, y=y_offset, anchor="e")
            departure_labels.append(time_label)
            
            y_offset += 65  # Adjust spacing between departure rows
    
    # Schedule next update
    root.after(DEPARTURE_UPDATE_INTERVAL, update_departures)  # Update every 30 seconds

def create_date_labels():
    """Create and return labels for date display"""
    date_font_size = 50
    date_labels = {}
    
    # Create header labels
    date_labels['year_header'] = tk.Label(root, text="YEAR", font=("Piboto Thin", date_font_size), bg="white", fg="black")
    date_labels['month_header'] = tk.Label(root, text="MONTH", font=("Piboto Thin", date_font_size), bg="white", fg="black")
    date_labels['day_header'] = tk.Label(root, text="DAY", font=("Piboto Thin", date_font_size), bg="white", fg="black")
    
    # Create value labels
    date_labels['year_value'] = tk.Label(root, font=("Piboto Light", date_font_size), bg="white", fg="black")
    date_labels['month_value'] = tk.Label(root, text="MONTH", font=("Piboto Light", date_font_size), bg="white", fg="black")
    date_labels['day_value'] = tk.Label(root, text="DAY", font=("Piboto Light", date_font_size), bg="white", fg="black")
    
    # Create vertical dividers using Canvas
    divider_height = date_font_size * 2.4  # Height of the divider lines
    divider_y = screen_height/5*4 - date_font_size*1.2  # Top position aligned with headers

    # First divider (between year and month)
    divider1 = tk.Canvas(root, width=2, height=divider_height, bg="white", highlightthickness=0)
    divider1.create_line(1, 0, 1, divider_height, fill="black", width=2)
    divider1.place(x=screen_width/6*1.5-30-20, y=divider_y)
    date_labels['divider1'] = divider1

    # Second divider (between month and day)
    divider2 = tk.Canvas(root, width=2, height=divider_height, bg="white", highlightthickness=0)
    divider2.create_line(1, 0, 1, divider_height, fill="black", width=2)
    divider2.place(x=screen_width/6*2.5-30+30, y=divider_y)
    date_labels['divider2'] = divider2
    
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

def update_temperature():
    inside_temp = hdc1080.readTemperature()
    inside_hum = hdc1080.readHumidity()
    temp_label.config(text=f"{inside_temp:.1f}°C")
    hum_label.config(text=f"{inside_hum:.1f}%")
    root.after(TEMP_UPDATE_INTERVAL, update_temperature)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Add these lines to prevent exiting fullscreen
root.overrideredirect(True)  # Removes window decorations and prevents window controls
root.configure(bg="white")

# Bind escape key to a do-nothing function to prevent default escape behavior
def do_nothing(event):
    return "break"
root.bind('<Escape>', do_nothing)

# Optional: Add a way to properly exit the application if needed
def quit_app(event):
    root.quit()
root.bind('<Control-q>', quit_app)  # Now Ctrl+Q will quit the app

# Create labels with specific positions
hour_label = tk.Label(root, font=("Piboto Light", 350), bg="white", fg="black")
hour_label.place(x=20, y=screen_height/2-160, anchor="w")

colon_label = tk.Label(root, text=":", font=("Piboto Light", 350), bg="white", fg="black")
colon_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="e")

minute_label = tk.Label(root, font=("Piboto Light", 350), bg="white", fg="black")
minute_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="w")

second_label = tk.Label(root, font=("Piboto Light", 70), bg="white", fg="black")
second_label.place(x=30+screen_width/3*2-90, y=screen_height/2, anchor="w")

# Create date labels
date_labels = create_date_labels()

temp_label = tk.Label(root, font=("Piboto Thin", 40), bg="white", fg="black")
temp_label.place(x=screen_width-420, y=screen_height-30, anchor="sw")

hum_label = tk.Label(root, font=("Piboto Thin", 40), bg="white", fg="black")
hum_label.place(x=screen_width-30, y=screen_height-30, anchor="se")

update_clock()
update_departures()
update_temperature()
root.mainloop()


