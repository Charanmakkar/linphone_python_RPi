# import RPi.GPIO as GPIO           # import RPi.GPIO module  
# GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
# GPIO.setup(port_or_pin, GPIO.OUT) # set a port/pin as an output   
# GPIO.output(port_or_pin, 1)       # set port/pin value to 1/GPIO.HIGH/True  
# GPIO.output(port_or_pin, 0)       # set port/pin value to 0/GPIO.LOW/False  

# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
butPin = 17 # Broadcom pin 17 (P1 pin 11)

dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(butPin): # button is released
            print("PRESSED")
        else: # button is pressed:
            print("ok")
            time.sleep(0.075)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
