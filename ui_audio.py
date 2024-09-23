import tkinter as tk
import pygame

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Specify the path to your audio file
audio_file = "1.mp3"  # Change this to your audio file's path

def play_audio(AudioFilePath = "home/pi/audios/1.mp3"):
    # Load and play the audio file
    try:
        pygame.mixer.music.load(AudioFilePath)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing audio file: {e}")

def stop_audio():
    # Stop the audio if it's playing
    pygame.mixer.music.stop()

# Create the main Tkinter window
root = tk.Tk()
root.title("Audio Player")

# Create buttons
play_button = tk.Button(root, text="Play", command=play_audio)
play_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop", command=stop_audio)
stop_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
