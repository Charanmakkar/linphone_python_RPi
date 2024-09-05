import subprocess, time

# Function to start Linphone and make a call
def make_call(sip_address):
    try:
        # Start Linphone in the background
        linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        
        # Send commands to Linphone
        linphone_process.stdin.write(f"call {sip_address}\n")
        print(sip_address)
        # linphone_process.stdin.flush()

        # Capture and print the output
        output, error = linphone_process.communicate()
        # print("Output:")
        # print(output)
        # if error:
        #     print("Error:")
        #     print(error)

        print(linphone_process)

        return linphone_process
    
    except Exception as e:
        print(f"An error occurred: {e}")

def terminate_call(linphone_process):
    try:
        # Send commands to Linphone
        linphone_process.stdin.write("terminate\n")
        # linphone_process.stdin.flush()

        # Capture and print the output
        output, error = linphone_process.communicate()
        print("Output:")
        print(output)
        if error:
            print("Error:")
            print(error)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example: Call a SIP address
linphone_process = make_call("104")
time.sleep(4)
terminate_call(linphone_process)


