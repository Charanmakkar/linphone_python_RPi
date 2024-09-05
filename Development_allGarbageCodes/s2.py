import subprocess

# Function to start Linphone and make a call
def make_call(sip_address):
    try:
        linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(linphone_process)
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
        print(linphone_process)
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

# Function to monitor Linphone output in real-time
def monitor_linphone():
    linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(linphone_process)
    try:
        # Monitor output
        while True:
            output = linphone_process.stdout.readline()
            if output == '' and linphone_process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        linphone_process.terminate()

# Example usage:
# Uncomment the following lines to test each function

# Make a call to a SIP address
# make_call("sip:104@192.168.1.10")
# make_call("104")

# Hang up a call
# hangup_call()

# Send a message to a SIP address
# send_message("sip:username@sipserver.com", "Hello from Linphone!")

# Monitor Linphone in real-time
monitor_linphone()
