import tkinter as tk
import time
import SDL_Pi_HDC1080

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

def update_clock():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    temp = hdc1080.readTemperature()
    label.config(text=f"{now}\n{temp:.1f}°C")
    root.after(1000, update_clock)

root = tk.Tk()
root.configure(bg="white")
root.attributes("-fullscreen", True)

label = tk.Label(root, font=("Helvetica", 48), bg="white", fg="black")
label.pack(expand=True)

update_clock()
root.mainloop()
