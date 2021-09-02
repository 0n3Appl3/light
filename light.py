# https://github.com/studioimaginaire/phue
# https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar

from tkinter.font import BOLD
from phue import Bridge
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sounddevice as sd
import numpy as np
import threading

# The bridge the application will access to control lights
b = Bridge('192.168.2.197')
# This line is called only used once to register with the Philips Hue Bridge
# b.connect()
# Obtain the list of all lights connected to the Philips Hue bridge
lights = b.get_light_objects("list")

# Stores all light names for the combobox
light_names = []
# Starting colour
hue = 1
# Keep track of the light the user selected
light = ""
# Keyword to stop light sync
stop = "stop"
# Stores the keyword of the button that was pressed
flag = ""

# Add all light names to the array
for l in lights:
    light_names.append(l.name)

def print_sound(indata, frames, time, status):
    # Lowest colour = minimum volume output
    hue = 40000

    # Calculate the volume of microphone input
    volume_norm = np.linalg.norm(indata) * 10
    print("|" * int(volume_norm))

    # Light hue is closer to red the louder the volume
    hue = hue - (int(volume_norm)  * 2000)
    if (hue < 1): hue = 1

    # Set hue value
    light.hue = hue

def start():
    # Keep syncing until the stop button is pressed
    while not (stop == flag):
        with sd.InputStream(callback = print_sound):
            sd.sleep(1000)
        

def check_if_running():
    global light
    global flag
    flag = ""

    # Create a new thread for starting light sync
    x = threading.Thread(target=start)
    
    # Set the light to what was selected in the combobox
    for l in lights:
        if (l.name == combobox.get()):
            light = l

    # The selected light needs to be turned on before continuing
    if not light.on:
        messagebox.showinfo("Note", "You need to turn on your light.")
        return

    if not x.is_alive():
        # Start light sync
        x.start()

def which_button(button_press):
    # Store the keyword of the pressed button
    global flag
    flag = button_press
    print(flag)

# Start creation of the GUI
master = Tk()
master.title("Light Sync")
master.geometry("200x200")

# Title
title = Label(master, text="Light", fg="#1a2152", font=("Helvetica", 36, BOLD))
title.place(x=10, y=10)

# Subtitle
subtitle = Label(master, text="Visualising sound volume")
subtitle.place(x=10, y=60)

# Combobox for selecting a light bulb
combobox = Combobox(master, width=15, values=light_names)
combobox.place(x=10, y=90)
combobox.set(light_names[0])

# Starts the light sync
start_button = Button(master, text="Start", width=9, command=check_if_running)
start_button.place(x=10, y=160)

# Stops the light sync
stop_button = Button(master, text="Stop", width=9, command=lambda m="stop": which_button(m))
stop_button.place(x=100, y=160)

# Show the GUI
mainloop()

