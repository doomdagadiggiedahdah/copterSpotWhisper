import os
import json

# Function to initialize the status JSON file
def initialize_status(file_list):
    initial_status = {}
    for filename in file_list:
        initial_status[filename] = "pending"
    
    with open('file_status.json', 'w') as f:
        json.dump(initial_status, f)

# Sample code to get list of all audio files in a directory and initialize their status
audio_files = [f for f in os.listdir('.') if f.endswith('.mp3')]  # Replace '.' with the path to your directory containing audio files
initialize_status(audio_files)

