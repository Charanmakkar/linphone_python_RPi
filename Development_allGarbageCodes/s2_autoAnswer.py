import subprocess

# Function to start Linphone and make a call
def make_call(sip_address):
    try:
        linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send command to make a call
        linphone_process.stdin.write(f"call {sip_address}\n")
        linphone_process.stdin.flush()

        # Capture and print the output
        output, error = linphone_process.communicate()
        print("Output:")
        print(output)
        if error:
            print("Error:")
            print(error)

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to hang up a call
def hangup_call():
    try:
        linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        linphone_process.stdin.write("terminate\n")
        linphone_process.stdin.flush()

        output, error = linphone_process.communicate()
        print("Output:")
        print(output)
        if error:
            print("Error:")
            print(error)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to send a message
def send_message(sip_address, message):
    try:
        linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        linphone_process.stdin.write(f"chat {sip_address}\n")
        linphone_process.stdin.write(f"{message}\n")
        linphone_process.stdin.flush()

        output, error = linphone_process.communicate()
        print("Output:")
        print(output)
        if error:
            print("Error:")
            print(error)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to monitor Linphone output and auto-answer incoming calls
def monitor_and_auto_answer():
    linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            output = linphone_process.stdout.readline()
            if output == '' and linphone_process.poll() is not None:
                break
            if output:
                print(output.strip())
                
                # Auto-answer incoming calls
                if "Incoming call" in output:
                    print("Auto-answering the call...")
                    linphone_process.stdin.write("answer\n")
                    linphone_process.stdin.flush()

    except KeyboardInterrupt:
        linphone_process.terminate()

# Example usage:
# Uncomment the following line to monitor Linphone and auto-answer calls

monitor_and_auto_answer()
