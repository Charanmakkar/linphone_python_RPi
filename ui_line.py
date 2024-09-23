# import tkinter as tk
# from tkinter import ttk

# # Create the main window
# root = tk.Tk()
# root.title("Tkinter UI with Split Line")

# # Create the first frame for the upper part
# frame_top = tk.Frame(root)
# frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# # Create a Text widget in the upper part
# text_box_top = tk.Text(frame_top, height=10, width=50)
# text_box_top.pack(pady=20, padx=20)

# # Insert some initial text in the top part
# text_box_top.insert(tk.END, "This is the upper part of the UI.")

# # Add a separator (splitting line) between the two sections
# separator = ttk.Separator(root, orient='horizontal')
# separator.pack(fill=tk.X, pady=10)

# # Create the second frame for the bottom part
# frame_bottom = tk.Frame(root)
# frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# # Create a Text widget in the bottom part
# text_box_bottom = tk.Text(frame_bottom, height=10, width=50)
# text_box_bottom.pack(pady=20, padx=20)

# # Insert some initial text in the bottom part
# text_box_bottom.insert(tk.END, "This is the lower part of the UI.")

# # Run the main loop
# root.mainloop()


import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Tkinter UI with Split Line")

# Add a separator (splitting line) between the two sections
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, pady=10)

# Run the main loop
root.mainloop()
