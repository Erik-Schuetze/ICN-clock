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
    for dep in departures:
        if dep['line'] in LINES_TO_SHOW:
            # Create line and direction label
            line_label = tk.Label(root, text=dep['line'], font=("Piboto Light", 40), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            line_label.place(x=screen_width-435, y=y_offset, anchor="e")
            departure_labels.append(line_label)
            direction_label = tk.Label(root, text=dep['direction'], font=("Piboto Thin", 40), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            direction_label.place(x=screen_width-420, y=y_offset, anchor="w")
            departure_labels.append(direction_label)
            
            # Create arrival time label with different style
            time_label = tk.Label(root, text=f"{dep['arrival']}m", font=("Piboto", 40), bg=BACKGROUND_COLOR, fg=FONT_COLOR)
            time_label.place(x=screen_width-40, y=y_offset, anchor="e")
            departure_labels.append(time_label)
            
            y_offset += 75  # Adjust spacing between departure rows
    
    # Schedule next update
    root.after(DEPARTURE_UPDATE_INTERVAL, update_departures)  # Update every 30 seconds

def update_clock():
    # Get current time and date
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    
    # Update labels
    hour_label.config(text=hour)
    minute_label.config(text=minute)
    second_label.config(text=second)
    year_label.config(text=f"YEAR\n{year}")
    month_label.config(text=f"MONTH\n{month}")
    day_label.config(text=f"DAY\n{day}")

    # Flash the colon
    if int(second) % 2 == 0:
        colon_label.config(fg="black")
    else:
        colon_label.config(fg="white")
    
    root.after(1000, update_clock)

def get_outside_temp():
    try:
        response = requests.get(f'https://wttr.in/{WEATHER_CITY}?format=%t')
        if response.status_code == 200:
            # Remove plus sign and convert to float
            temp_str = response.text.strip().replace('+', '').replace('°C', '')
            return float(temp_str)
    except:
        return None
    return None

def update_inside_temperature():
    inside_temp = hdc1080.readTemperature()
    in_temp_label.config(text=f"{inside_temp:.0f}°C")

    root.after(TEMP_UPDATE_INTERVAL, update_inside_temperature)

def update_outside_temperature():
    outside_temp = get_outside_temp()
    if outside_temp is not None:
        out_temp_label.config(text=f"{outside_temp:.0f}°C")
    else:
        out_temp_label.config(text="N/A")
    root.after(WEATHER_UPDATE_INTERVAL, update_outside_temperature)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.configure(bg="white")
root.attributes("-fullscreen", True)

# Create labels with specific positions
hour_label = tk.Label(root, font=("Piboto Light", 370), bg="white", fg="black")
hour_label.place(x=30, y=screen_height/2-150, anchor="w")

colon_label = tk.Label(root, text=":", font=("Piboto Light", 370), bg="white", fg="black")
colon_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="e")

minute_label = tk.Label(root, font=("Piboto Light", 370), bg="white", fg="black")
minute_label.place(x=30+screen_width/3, y=screen_height/2-150, anchor="w")

second_label = tk.Label(root, font=("Piboto Light", 80), bg="white", fg="black")
second_label.place(x=30+screen_width/3*2-80, y=screen_height/2, anchor="w")

year_label = tk.Label(root, font=("Piboto Light", 50), bg="white", fg="black")
year_label.place(x=screen_width/6-30, y=screen_height/6*5, anchor="center")

month_label = tk.Label(root, font=("Nunito Light", 50), bg="white", fg="black")
month_label.place(x=screen_width/6*2-30, y=screen_height/6*5, anchor="center")

day_label = tk.Label(root, font=("Nunito Light", 50), bg="white", fg="black")
day_label.place(x=screen_width/6*3-30, y=screen_height/6*5, anchor="center")

in_temp_label = tk.Label(root, font=("Piboto Light", 40), bg="white", fg="black")
in_temp_label.place(x=screen_width-160, y=screen_height-105, anchor="sw")

in_temp2_label = tk.Label(root, font=("Piboto Thin", 40), bg="white", fg="black")
in_temp2_label.place(x=screen_width-160, y=screen_height-105, anchor="se")
in_temp2_label.config(text=f"INSIDE: ")

out_temp_label = tk.Label(root, font=("Piboto Light", 40), bg="white", fg="black")
out_temp_label.place(x=screen_width-160, y=screen_height-30, anchor="sw")

out_temp2_label = tk.Label(root, font=("Piboto Thin", 40), bg="white", fg="black")
out_temp2_label.place(x=screen_width-160, y=screen_height-30, anchor="se")
out_temp2_label.config(text=f"OUTSIDE: ")

update_clock()
update_departures()
update_inside_temperature()
update_outside_temperature()
root.mainloop()


