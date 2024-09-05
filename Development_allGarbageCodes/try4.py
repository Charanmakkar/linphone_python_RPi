import subprocess
import time

# Start Linphone in CLI mode
linphone_process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
linphone_process.stdin.write("autoanswer enable\n")

def monitor_and_auto_answer():
    try:        
        # Continuously monitor Linphone output
        while True:
            output = linphone_process.stdout.readline()
            if output:
                print(output.strip())
                   
            # Check if the process has ended
            if linphone_process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        linphone_process.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")

# Start monitoring Linphone and auto-answer calls
monitor_and_auto_answer()
