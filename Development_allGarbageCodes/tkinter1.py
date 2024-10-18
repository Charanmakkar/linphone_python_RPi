import tkinter as tk
from tkinter import messagebox

def submit():
    ip = ip_entry.get()
    port = port_entry.get()

    # Validation (optional)
    if not ip:
        messagebox.showwarning("Input Error", "Please enter a valid IP address.")
        return
    if not port.isdigit() or not (0 <= int(port) <= 65535):
        messagebox.showwarning("Input Error", "Please enter a valid port number (0-65535).")
        return

    # Display input or handle as needed
    messagebox.showinfo("Info", f"IP: {ip}\nPort: {port}")

# Create the main window
root = tk.Tk()
root.title("IP and Port Input")

# IP Label and Entry
ip_label = tk.Label(root, text="IP:")
ip_label.grid(row=0, column=0, padx=10, pady=10)

ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Port Label and Entry
port_label = tk.Label(root, text="Port:")
port_label.grid(row=1, column=0, padx=10, pady=10)

port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
