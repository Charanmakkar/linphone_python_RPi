import subprocess
import time
import tkinter as tk
from tkinter import messagebox

# Start Linphone in CLI mode
linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
linphone_process.stdin.write("autoanswer enable\n")

def monitor_and_auto_answer():
    try:        
        # Continuously monitor Linphone output
        while True:
            output = linphone_process.stdout.readline()
            # if output:
            #     print(output.strip())
                   
            # # Check if the process has ended
            # if linphone_process.poll() is not None:
            #     break
                
    except KeyboardInterrupt:
        linphone_process.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")

def make_call():
    sip_id = sip_input.get()
    print(sip_id)
    if sip_id:
        try:
            linphone_process.stdin.write(f"call {sip_id}\n")
            linphone_process.stdin.flush()
            messagebox.showinfo("Call Status", f"Calling {sip_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make the call: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter a SIP ID")

# Create the main Tkinter window
root = tk.Tk()
root.title("Linphone SIP Caller")

# Create a label and input field for SIP ID
tk.Label(root, text="Enter SIP ID:").pack(pady=10)
sip_input = tk.Entry(root, width=50)
sip_input.pack(pady=10)

# Create a button to initiate the call
call_button = tk.Button(root, text="Make Call", command=make_call)
call_button.pack(pady=20)

# Start monitoring Linphone and auto-answer calls in a separate thread
import threading
monitor_thread = threading.Thread(target=monitor_and_auto_answer, daemon=True)
monitor_thread.start()

# Start the Tkinter main loop
root.mainloop()
