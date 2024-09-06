#!/usr/bin/env python

"""
Python Code             : Emergency Calling Booth - Linphone / Linphonec with Python with RPI with GUI
Project Done for        : Naman Bhatnagar


File Version            : 1.0.1
Date of Last Modified   : 06 Sept 2024
Time of Last Modified   : 12:18 PM

Developer               : Charanpreet Singh
Email                   : charanmakkar2@gmail.com
Git Repo Link           : https://github.com/Charanmakkar/linphone_python_RPi
my Github               : https://github.com/charanmakkar


/*
DESCRIPTION:
------------
linphone with Raspberry Pi 4 and Controlled with python
Voip calling using RPI + mic + speaker
Software controlled with Python based UI

linphone installed with instructions given at : https://wiki.linphone.org/xwiki/wiki/public/view/Linphone/Linphone%20and%20Raspberry%20Pi/

all above instructions are simply fied and mentioned in file in current repo: "readme instructions Linux.txt" 

**Calling can be done with GPIO also, 
so GPIO_5 of RPI is configured for the same
Push the Button, it should connect you to the server.
*/

"""

# all imports 
import subprocess, os
import time
import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as gpio                 # importing Lib for GPIOs in RPI

# Fixed Variables
# fixed_sip_id = username
fixed_sip_id = "104"

# GPIO Setup
gpio.setmode(gpio.BCM)
gpio.setup(5, gpio.IN, pull_up_down = gpio.PUD_UP)

# Start Linphone in CLI mode
linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
linphone_process.stdin.write("autoanswer enable\n")

call_active = False  # Variable to track call status

def monitor_and_auto_answer():
    global call_active
    try:        
        # Continuously monitor Linphone output
        while True:
            output = linphone_process.stdout.readline()
            if output:
                # print(output.strip())

                # Update the call status based on Linphone output
                if "ended" in output:
                    update_call_status(0)
                elif "ringing" in output:
                    update_call_status(2)
                elif "established" in output:
                    update_call_status(1)
                
                   
            # Check if the process has ended
            if linphone_process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        linphone_process.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")

def make_call():
    global call_active
    sip_id = sip_input.get()
    
    if call_active:
        terminate_call()

    if sip_id:
        try:
            linphone_process.stdin.write(f"call {sip_id}\n")
            linphone_process.stdin.flush()
            messagebox.showinfo("Call Status", f"Calling {sip_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make the call: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter a SIP ID")
    
def make_call_gpio():
    global call_active
    
    if call_active:
        terminate_call()

    try:
        linphone_process.stdin.write(f"call {fixed_sip_id}\n")
        linphone_process.stdin.flush()
        messagebox.showinfo("Call Status", f"Calling {fixed_sip_id}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to make the call: {e}")

def terminate_call():
    global call_active
    if call_active:
        try:
            linphone_process.stdin.write("terminate\n")
            linphone_process.stdin.flush()
            update_call_status(False)
            messagebox.showinfo("Call Status", "Call terminated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate the call: {e}")
    else:
        messagebox.showwarning("Call Status", "No active call to terminate")

def update_call_status(active):
    global call_active
    call_active = active
    if call_active == 1:
        status_label.config(text="Call Active", bg="green")
    elif(call_active == 2):
        status_label.config(text="ringing", bg="blue")
    elif(call_active == 0):
        status_label.config(text="Call Inactive", bg="red")

# Event added for 1 button to make a call
gpio.add_event_detect(5, gpio.FALLING, callback=make_call, bouncetime=300)

# Create the main Tkinter window
root = tk.Tk()
root.title("Linphone SIP Caller")

# Create a label and input field for SIP ID
tk.Label(root, text="Enter SIP ID:").pack(pady=10)
sip_input = tk.Entry(root, width=50)
sip_input.pack(pady=10)

# Create a button to initiate the call
call_button = tk.Button(root, text="Make Call", command=make_call)
call_button.pack(pady=10)

# Create a button to terminate the call
terminate_button = tk.Button(root, text="Terminate Call", command=terminate_call)
terminate_button.pack(pady=10)

# Call status indicator
status_label = tk.Label(root, text="Call Inactive", bg="red", width=20)
status_label.pack(pady=10)

# Start monitoring Linphone and auto-answer calls in a separate thread
import threading
monitor_thread = threading.Thread(target=monitor_and_auto_answer, daemon=True)
monitor_thread.start()

# Start the Tkinter main loop
root.mainloop()
