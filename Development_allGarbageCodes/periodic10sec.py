import tkinter as tk
import threading
from datetime import datetime

# Function to perform the task every 10 seconds
def periodic_task():
    print("Task executed at:", datetime.now())
    # Schedule the next execution
    threading.Timer(10, periodic_task).start()

# Setup your Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Periodic Task App")

    label = tk.Label(root, text="Periodic Task Running...")
    label.pack(pady=20)

    # Start the periodic task
    periodic_task()

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
