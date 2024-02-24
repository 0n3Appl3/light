# https://github.com/studioimaginaire/phue
# https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar
# https://github.com/formazione/Azure-ttk-theme

from tkinter.font import BOLD
from phue import Bridge
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import sounddevice as sd
import numpy as np
import threading

# The bridge the application will access to control lights
b = Bridge('192.168.0.211')
# This line is called only used once to register with the Philips Hue Bridge
# b.connect()
# Obtain the list of all lights connected to the Philips Hue bridge
lights = b.get_light_objects("list")

# Stores all light names for the combobox
light_names = []
# The two light sync colour options
variant_one = 40000
variant_two = 65000
# Stores the lowest colour the lights can display
hue = variant_one
# Keep track of the light the user selected
light = ""
# Has a light sync session started
started = False
# Keyword to stop light sync
STOP = "stop"
# Stores the keyword of the button that was pressed
flag = ""

# Add all light names to the array
for l in lights:
    light_names.append(l.name)

def print_sound(indata, frames, time, status):
    global hue
    # Calculate the volume of microphone input
    volume_norm = np.linalg.norm(indata) * 10
    print("|" * int(volume_norm))
    volume.set(int(volume_norm) * 2)

    # Light hue is closer to red the louder the volume
    colour = hue - (int(volume_norm)  * 2000)
    if (colour < 1): colour = 1

    # Set hue value
    light.hue = colour

def start():
    global started
    # Keep syncing until the stop button is pressed
    while not (flag == STOP):
        with sd.InputStream(callback = print_sound):
            sd.sleep(1000)
    started = False
        

def check_if_running():
    global light, started, flag

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

    if started:
        messagebox.showinfo("Note", "Light sync session is already running.")
        return

    if not x.is_alive():
        # Start light sync
        x.start()
        started = True

def change_colour():
    global hue
    # Change hue value based on checkbutton state
    if (colour_setting.get() == 0):
        hue = variant_one
    else:
        hue = variant_two

def which_button(button_press):
    # Store the keyword of the pressed button
    global flag
    flag = button_press
    print(flag)

def setup_gui():
    global volume, colour_setting, combobox

    # Start creation of the GUI
    master = Tk()
    master.title("Light Sync")
    master.geometry("250x280")
    volume = IntVar()
    colour_setting = IntVar()

    # Set the GUI theme
    style = ttk.Style(master)
    master.tk.call("source", "azure dark.tcl")
    style.theme_use('azure')

    # Sound volume visualiser
    progress = ttk.Progressbar(master, value=0, length=250, variable=volume, mode='determinate')
    progress.place(x=0, y=-8)

    # Title
    title = Label(master, text="Light", font=("Helvetica", 36, BOLD))
    title.place(x=10, y=15)

    # Subtitle
    subtitle = Label(master, text="Visualising sound volume")
    subtitle.place(x=10, y=65)

    # Combobox for selecting a light bulb
    combobox = Combobox(master, state="readonly", width=15, values=light_names)
    combobox.place(x=15, y=110)
    combobox.set(light_names[0])

    # Toggle between two different colour modes
    switch = ttk.Checkbutton(master, text="Enable alternate colours", variable=colour_setting, style="Switch", offvalue=0, onvalue=1, command=change_colour)
    switch.place(x=15, y=160)

    # Starts the light sync
    start_button = ttk.Button(master, text="Start", width=9, command=check_if_running)
    start_button.place(x=15, y=235)

    # Stops the light sync
    stop_button = ttk.Button(master, text="Stop", width=9, command=lambda m="stop": which_button(m))
    stop_button.place(x=130, y=235)

if __name__ == "__main__":
    setup_gui()
    mainloop()