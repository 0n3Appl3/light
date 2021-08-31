# https://github.com/studioimaginaire/phue
# https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar

from phue import Bridge
import sounddevice as sd
import numpy as np

b = Bridge('<ip of bridge>')
# This line is called only used once to register with the Philips Hue Bridge.
# b.connect()
lights = b.get_light_objects("list")

# Starting colour
hue = 1
light = ""
target_light = "Janna's Light strips"
duration = 200

for l in lights:
    if (l.name == target_light):
        light = l

def print_sound(indata, outdata, frames, time, status):
    hue = 25000
    volume_norm = np.linalg.norm(indata) * 10
    hue = hue - (int(volume_norm)  * 2500)
    print("|" * int(volume_norm))
    print(hue)
    if (hue < 1):
        hue = 1
    light.hue = hue # Set hue value

with sd.Stream(callback = print_sound):
    sd.sleep(duration * 1000)
