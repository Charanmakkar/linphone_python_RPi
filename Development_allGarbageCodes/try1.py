import subprocess, time

# Function to execute a terminal command and capture the output
def run_command(command):
    try:
        # Run the command and capture the output and errors
        result = subprocess.run([command], shell=True, text=True, capture_output=True)
        
        # Print the output
        print("Output:")
        print(result.stdout)
        
        # Print any errors
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example: Running the 'ls' command
run_command("linphonec")
# time.sleep(1)
# run_command("call 104")


