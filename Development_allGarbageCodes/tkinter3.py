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
ip_label.pack(anchor='w', pady=(5, 0), padx=10)  # Left-align label with some space before the entry

ip_entry = tk.Entry(root)
ip_entry.pack(pady=(0, 10), padx=10)  # Extra space after the label and before the entry

# Port Label and Entry
port_label = tk.Label(root, text="Port:")
port_label.pack(anchor='w', pady=(5, 0), padx=10)  # Left-align label with some space before the entry

port_entry = tk.Entry(root)
port_entry.pack(pady=(0, 10), padx=10)  # Extra space after the label and before the entry

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
