#!/usr/bin/env python

"""
Python Code             : Emergency Calling Booth - Linphone / Linphonec with Python with RPI with GUI
Project Done for        : Naman Bhatnagar
File Version            : 1.0.1
Date of Last Modified   : 15 Sept 2024
Time of Last Modified   : 12:18 PM

Developer               : Charanpreet Singh
Email                   : charanmakkar2@gmail.com
Git Repo Link           : https://github.com/Charanmakkar/linphone_python_RPi
my Github               : https://github.com/charanmakkar

Description:
------------
This project uses Linphone with Raspberry Pi 4 and is controlled via Python. It allows VoIP calling using a button press 
on GPIO or a button on the Python UI. The call will automatically try different SIP IDs if one does not respond within 
a timeout period.
"""

# Imports
import subprocess, os, time, traceback, threading
import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as gpio  # For GPIO handling in RPi

# Fixed Variables
fixed_sip_ids = ["100", "101", "104"]  # List of server IPs
current_server_index = 0  # Global variable to track the current server being called
call_timeout = 20  # Timeout for unanswered calls (in seconds)

# GPIO Setup
pushButton = 21
gpio.setmode(gpio.BCM)
gpio.setup(pushButton, gpio.IN, pull_up_down=gpio.PUD_UP)

# Start Linphone in CLI mode
linphone_process = subprocess.Popen(['/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin/linphonec'], 
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                    text=True, bufsize=1)
linphone_process.stdin.write("autoanswer enable\n")

CallAllServers = False
call_active = False  # Global variable to track the call status

def monitor_and_auto_answer():
    global call_active
    try:
        # Continuously monitor Linphone output
        while True:
            output = linphone_process.stdout.readline()
            if output:
                print(output.strip())

                # Update the call status based on Linphone output
                if "error" in output or "Call terminated" in output:
                    print("Call ended with error or termination.")
                    update_call_status(0)
                    call_active = False

                elif "ringing" in output:
                    print("Call is ringing.")
                    update_call_status(2)
                    
                elif "established" in output:
                    print("Call is established.")
                    update_call_status(1)
                    call_active = True

            # Check if the process has ended
            if linphone_process.poll() is not None:
                break

    except KeyboardInterrupt:
        linphone_process.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")

def make_call_gpio(channel=None):  # Accept an optional argument for GPIO event
    global call_active, current_server_index, CallAllServers

    print(">>> make_CALL_gpio")

    # Reset index and CallAllServers flag when GPIO is triggered
    current_server_index = 0
    CallAllServers = True

    # Start calling the first server
    call_next_server()

def call_next_server():
    global current_server_index, CallAllServers, call_active

    if CallAllServers:
        # If there are still SIP IDs to call
        if current_server_index < len(fixed_sip_ids):
            sip_id = fixed_sip_ids[current_server_index]

            print(f"Calling SIP ID: {sip_id}")
            sip_input.delete(0, tk.END)  # Clear existing input
            sip_input.insert(0, sip_id)  # Insert current SIP ID in input field

            try:
                # Make the actual call
                linphone_process.stdin.write(f"call {sip_id}\n")
                linphone_process.stdin.flush()
                call_active = True

                # Set a timeout to check call status and decide next action
                root.after(call_timeout * 1000, check_call_status)

            except Exception as e:
                print(f"Error making call to {sip_id}: {e}")
                messagebox.showerror("Error", f"Failed to make the call to {sip_id}: {e}")

        else:
            # If all servers have been tried, reset and stop calling
            print("All servers have been called. No response from any.")
            messagebox.showinfo("Call Status", "All servers were tried. No response.")
            current_server_index = 0
            CallAllServers = False
    else:
        terminate_call()

def check_call_status():
    global call_active, current_server_index, CallAllServers

    # If the call is still not active, terminate it and call the next server
    if not call_active:
        print("Call inactive. Moving to next server.")
        terminate_call()
        current_server_index += 1
        call_next_server()
    else:
        print("Call is active, no need to call the next server.")

def terminate_call():
    global call_active
    print(">>> TERMINATE")
    if call_active:
        try:
            linphone_process.stdin.write("terminate\n")
            linphone_process.stdin.flush()
            update_call_status(0)
            call_active = False
            time.sleep(2)
        except Exception as e:
            print("ERROR WITH TERMINATION: ", e)
    else:
        print(">>> Call is NOT active")

def update_call_status(active):
    global call_active
    call_active = active
    if call_active == 1:
        status_label.config(text="Call Active", bg="green")
    elif call_active == 2:
        status_label.config(text="Ringing", bg="blue")
    elif call_active == 0:
        status_label.config(text="Call Inactive", bg="red")

def add_proxy():
    proxy = proxy_input.get()
    if proxy:
        linphone_process.stdin.write(f"proxy add {proxy}\n")
        linphone_process.stdin.flush()
        messagebox.showinfo("Proxy Status", f"Proxy {proxy} added.")
    else:
        messagebox.showwarning("Input Error", "Please enter a proxy to add.")

def remove_proxy():
    proxy = proxy_input.get()
    if proxy:
        linphone_process.stdin.write(f"proxy remove {proxy}\n")
        linphone_process.stdin.flush()
        messagebox.showinfo("Proxy Status", f"Proxy {proxy} removed.")
    else:
        messagebox.showwarning("Input Error", "Please enter a proxy to remove.")

def list_proxies():
    linphone_process.stdin.write("proxy list\n")
    linphone_process.stdin.flush()

# Function to simulate GPIO press via UI button
def gpio_test_button_click():
    global CallAllServers
    print(">>> GPIO TEST BUTTON")
    CallAllServers = True
    make_call_gpio()  # Call the same function triggered by GPIO pin

# Event added for the physical button to make a call
gpio.add_event_detect(pushButton, gpio.FALLING, callback=make_call_gpio, bouncetime=300)

# Create the main Tkinter window
root = tk.Tk()
root.title("Linphone SIP Caller")

# Create a label and input field for SIP ID
tk.Label(root, text="Enter SIP ID:").pack(pady=10)
sip_input = tk.Entry(root, width=50)
sip_input.pack(pady=10)

# Create a button to initiate the call
call_button = tk.Button(root, text="Make Call", command=make_call_gpio)
call_button.pack(pady=10)

# Create a button to terminate the call
terminate_button = tk.Button(root, text="Terminate Call", command=terminate_call)
terminate_button.pack(pady=10)

# Call status indicator
status_label = tk.Label(root, text="Call Inactive", bg="red", width=20)
status_label.pack(pady=10)

# GPIO Test button
gpio_test_button = tk.Button(root, text="GPIO TEST Button", command=gpio_test_button_click)
gpio_test_button.pack(pady=10)

# Input for proxy
tk.Label(root, text="Enter Proxy:").pack(pady=10)
proxy_input = tk.Entry(root, width=50)
proxy_input.pack(pady=10)

# Buttons for proxy management
add_proxy_button = tk.Button(root, text="Add Proxy", command=add_proxy)
add_proxy_button.pack(pady=5)

remove_proxy_button = tk.Button(root, text="Remove Proxy", command=remove_proxy)
remove_proxy_button.pack(pady=5)

list_proxies_button = tk.Button(root, text="List Proxies", command=list_proxies)
list_proxies_button.pack(pady=5)

# Start monitoring Linphone and auto-answer calls in a separate thread
monitor_thread = threading.Thread(target=monitor_and_auto_answer, daemon=True)
monitor_thread.start()

# Start the Tkinter main loop
root.mainloop()
