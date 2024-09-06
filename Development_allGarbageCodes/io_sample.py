#!/usr/bin/python

import RPi.GPIO as gpio
from subprocess import call
import time
import subprocess
import os


gpio.setmode(gpio.BCM)
gpio.setup(5, gpio.IN, pull_up_down = gpio.PUD_UP)
os.environ['PATH'] = '/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin'

subprocess.Popen(["sudo -u pi linphonecsh init -a -C -c /home/pi/.linphonerc -d 6 -l /tmp/log.txt"])

def doorbell(channel):


    subprocess.Popen(["linphonecsh dial **9"])
    
gpio.add_event_detect(5, gpio.FALLING, callback=doorbell, bouncetime=300)

while 1:
    time.sleep(360)