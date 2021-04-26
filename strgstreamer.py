import os
import subprocess

from gpiozero import Button, LED
from time import sleep
from signal import pause

button = Button(18)
led = LED(17)
running = False
def toggle_process():
    global running
    if (running is True):
        os.system("pkill -f gst-launch-1.0")
        led.off()
        running = not running
        print("STOPPED")
        sleep(1)
    elif (running is False):
        print("Pressed")
        subprocess.Popen(["bash","-c","gst-launch-1.0 --gst-debug=3 v4l2src device=/dev/video0 ! image/jpeg,width=1280,height=720,framerate=30/1 ! jpegparse ! jpegdec ! omxh264enc ! video/x-h264 ! h264parse ! queue ! mux. alsasrc device=hw:2,0 ! audioconvert ! voaacenc bitrate=128000 ! queue ! flvmux streamable=true name=mux ! rtmpsink location=rtmp://192.168.2.25:1935/live/pi"])
        running = not running
        led.on()
        print("STARTED")
        sleep(1)

button.when_pressed = toggle_process
pause()
