#!/usr/bin/env python

"""
Python Code             : Emergency Calling Booth - Linphone / Linphonec with Python with RPI with GUI
Project Done for        : Naman Bhatnagar


File Version            : 1.0.1
Date of Last Modified   : 24 Sept 2024
Time of Last Modified   : 01:01 AM

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
import subprocess, sys
import time, traceback, threading
import tkinter as tk
from tkinter import messagebox, ttk
import RPi.GPIO as gpio  # importing Lib for GPIOs in RPI

# Lib for Audio with TKinter
import pygame

# Initialize pygame mixer for sound playback
pygame.mixer.init()


# Fixed Variables
fixed_sip_ids = ["100", "102", "104"]  # List of server IPs

# Global variables
current_server_index = 0
call_timeout = 10  # Timeout for unanswered calls (in seconds)
call_active = False  # Variable to track call status
CallAllServers = False  # Flag to track if we are calling all servers
check_receivedCall = True

# AUDIO FILE PATHs
fixed_audio_path = "/home/pi/audios/"
AUDIO_FILE_1 = fixed_audio_path + "1.mp3"
AUDIO_FILE_2 = fixed_audio_path + "2.mp3"


# GPIO Setup
pushButton = 21
gpio.setmode(gpio.BCM)
gpio.setup(pushButton, gpio.IN, pull_up_down=gpio.PUD_UP)

try:
    # Start Linphone in CLI mode
    linphone_process = subprocess.Popen(['/home/pi/linphone-sdk/build-raspberry/linphone-sdk/desktop/bin/linphonec'], 
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                        text=True, bufsize=1)
    linphone_process.stdin.write("autoanswer enable\n")
    linphone_process.stdin.write("register sip:pi@192.168.1.2 sip:192.168.1.2\n")

    # Function to check registration status
    def check_registration():
        try:
            linphone_process.stdin.write("register\n")
            linphone_process.stdin.flush()

            while True:
                output = linphone_process.stdout.readline().strip().lower()
                if output:
                    # print(output)

                    # Update the call status based on Linphone output
                    if "registered" in output:
                        print("SIP Account is registered.")
                        return True
                    else:
                        print("SIP Account is not registered.")
                        return False

                # Check if the process has ended
                if linphone_process.poll() is not None:
                    break

        except Exception as e:
            print(f"Error checking registration: {e}")
            return False
        
    def make_call_single():
        """ Function to make a call to the SIP ID entered in the input box. """
        global call_active

        # Get the SIP ID from the input box
        sip_id = sip_input.get()
        print(sip_id)
        if not sip_id:
            messagebox.showerror("Input Error", "Please enter a valid SIP ID.")
            return

        # if not check_registration():
        #     print("Not registered. Halting the process.")
        #     return

        print(f"Making a call to SIP ID: {sip_id}")

        try:
            linphone_process.stdin.write(f"call {sip_id}\n")
            linphone_process.stdin.flush()
            call_active = True
            update_call_status(2)  # Call is ringing
        except Exception as e:
            print(f"Error making call to {sip_id}: {e}")
            messagebox.showerror("Error", f"Failed to make the call to {sip_id}: {e}")


    def monitor_and_auto_answer():
        global call_active, CallAllServers, check_receivedCall
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
                        CallAllServers = True
                        
                        
                    elif "established" in output:
                        print("Call is established.")
                        update_call_status(1)
                        call_active = True
                        CallAllServers = False
                        check_receivedCall = True

                # Check if the process has ended
                if linphone_process.poll() is not None:
                    break

        except KeyboardInterrupt:
            linphone_process.terminate()
        except Exception as e:
            print(f"An error occurred: {e}")

    def make_call_gpio(channel=None):  # Accept an optional argument for GPIO event
        global call_active, current_server_index, CallAllServers

        # Check registration status before proceeding
        # if not check_registration():
        #     print("Not registered in terminal only.")
        #     return

        print(">>> make_CALL_gpio")

        # Reset index and CallAllServers flag when GPIO is triggered
        current_server_index = 0
        CallAllServers = True

        # Start calling the first server
        call_next_server()

    def call_next_server():
        global current_server_index, CallAllServers, call_active, check_receivedCall

        if CallAllServers:
            # If there are still SIP IDs to call
            if (current_server_index < len(fixed_sip_ids)) and (CallAllServers == True):
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
                print("All servers have been called OR Call attended")
                # messagebox.showinfo("Call Status", "All servers were tried. No response.")

                current_server_index = 0
                
                if check_receivedCall == True:
                    print("Connected")
                    CallAllServers = False
                else:
                    CallAllServers = False
                    print("No response from any.")

                    # Play Audio file
                    print("-> NO ANSWER AUDIO FILE")
                    play_audio(AUDIO_FILE_1)

        else:
            # FORCE Hault
            terminate_call()

    # def check_call_status():
    #     global call_active, current_server_index, CallAllServers

    #     # If the call is still not active, terminate it and call the next server
    #     if not call_active:
    #         print("Call inactive. Moving to next server.")
    #         terminate_call()
    #         current_server_index += 1
    #         call_next_server()
    #     else:
    #         print("Call is active, no need to call the next server.")

    def check_call_status():
        global call_active, current_server_index, CallAllServers, check_receivedCall

        if (CallAllServers):
            # Terminate the current call and move to the next server, even if the call is active
            print("Terminating the current call and moving to the next server.")

            # Terminate the current call
            terminate_call()
            
            # Move to the next SIP ID in the list
            current_server_index += 1
            
            # Call the next server in the list
            call_next_server()
        else:
            print("Call connected, NO need to switch client")
        
    

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
        proxy_id = proxy_sipId.get()
        proxy_server = proxy_sipAddr.get()
        if proxy_id and proxy_server:
            linphone_process.stdin.write(f"register {proxy_id} {proxy_server}\n")
            linphone_process.stdin.flush()
            messagebox.showinfo("Proxy Status", f"Proxy {proxy_id} added.")
        else:
            messagebox.showwarning("Input Error", "Please enter a proxy to add.")

    # def add_proxy():
    #     proxy = proxy_input.get()
    #     if proxy:
    #         linphone_process.stdin.write(f"proxy add {proxy}\n")
    #         linphone_process.stdin.flush()
    #         messagebox.showinfo("Proxy Status", f"Proxy {proxy} added.")
    #     else:
    #         messagebox.showwarning("Input Error", "Please enter a proxy to add.")

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
    
    # Function to retrieve and store the proxy list
    def get_proxy_list():
        try:
            # Send the proxy list command
            linphone_process.stdin.write("proxy list\n")
            linphone_process.stdin.flush()

            # Read the output and store the proxies in a list
            proxy_list = []
            while True:
                output = linphone_process.stdout.readline().strip()
                if "No proxies defined" in output:
                    print("No proxies found.")
                    break
                elif output.startswith("proxy:"):
                    # Parse and store each proxy
                    proxy_info = output.split("proxy: ")[1]
                    proxy_list.append(proxy_info)
                elif "linphonec>" in output:  # Stop reading when command prompt appears
                    break

            print("Proxy List: ", proxy_list)
            return proxy_list

        except Exception as e:
            print(f"Error retrieving proxy list: {e}")
            return []

    # Function to simulate GPIO press via UI button
    def gpio_test_button_click():
        global CallAllServers, check_receivedCall
        print(">>> GPIO TEST BUTTON")
        CallAllServers = True
        check_receivedCall = False
        make_call_gpio()  # Call the same function triggered by GPIO pin

    def play_audio(AudioFilePath = "/home/pi/audios/1.mp3"):
    # Load and play the audio file
        try:
            pygame.mixer.music.load(AudioFilePath)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing audio file: {e}")

    def stop_audio():
        # Stop the audio if it's playing
        pygame.mixer.music.stop()

    def on_closing():
        try:
            # Stop linphone subprocess if running
            if linphone_process.poll() is None:  # Check if the subprocess is still running
                linphone_process.terminate()  # Terminate the Linphone process
                linphone_process.wait()  # Wait for the process to finish

            print("Application is closing. Clean up complete.")
            
        except Exception as e:
            print(f"Error while closing: {e}")
        
        # Properly close the tkinter window
        root.destroy()
        
        # Exit the program
        sys.exit()


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
    call_button = tk.Button(root, text="Make Call", command=make_call_single)
    call_button.pack(pady=10)

    # Create a button to terminate the call
    terminate_button = tk.Button(root, text="Terminate Call", command=terminate_call)
    terminate_button.pack(pady=10)

    # Call status indicator
    status_label = tk.Label(root, text="Call Inactive", bg="red", width=20)
    status_label.pack(pady=10)

    # GPIO Test button
    gpio_test_button = tk.Button(root, text="GPIO TEST Button", command=gpio_test_button_click)
    gpio_test_button.pack(pady=20)

    # Add a separator (splitting line) between the two sections
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill=tk.X, pady=2)
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill=tk.X, pady=2)
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill=tk.X, pady=2)

    tk.Label(root, text="SETTINGS - under progress").pack(pady=10)

    # tk.Label(root, text="sip:192.168.1.2").pack(pady=10)
    proxy_sipAddr = tk.Entry(root, width=50)
    proxy_sipAddr.insert(0, "sip:192.168.1.2")
    proxy_sipAddr.pack(pady=10)

    # tk.Label(root, text="sip:username@192.168.1.2").pack(pady=10)
    proxy_sipId = tk.Entry(root, width=50)
    proxy_sipId.insert(0, "sip:username@192.168.1.2")
    proxy_sipId.pack(pady=10)

    # Buttons for proxy management
    add_proxy_button = tk.Button(root, text="Register Device", command=add_proxy)
    add_proxy_button.pack(pady=10)

    ## Input for proxy
    # proxy_input = tk.Entry(root, width=50)
    # proxy_input.insert(0, "do not touch me...")
    # proxy_input.pack(pady=10)

    # remove_proxy_button = tk.Button(root, text="Remove Proxy", command=remove_proxy)
    # remove_proxy_button.pack(pady=5)

    list_proxies_button = tk.Button(root, text="Read Current Config", command=list_proxies)
    list_proxies_button.pack(pady=5)

    # Start monitoring Linphone and auto-answer calls in a separate thread
    monitor_thread = threading.Thread(target=monitor_and_auto_answer, daemon=True)
    monitor_thread.start()

    # Bind the close event (X button) to the on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the Tkinter main loop
    root.mainloop()

except Exception as e:
    with open('/home/pi/script_error_gpio.log', 'a') as f:
        f.write(f"Error: {e}\n")
        f.write("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))


# register sip:101@192.168.1.29 pi 101
# register sip:102@192.168.1.2 sip:192.168.1.2
# register sip:101@192.168.1.2 sip:192.168.1.2
# proxy add sip:192.168.1.29 sip:101@192.168.1.29 101 
