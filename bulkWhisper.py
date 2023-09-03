import json
import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv

df = pd.DataFrame(columns=['filename', 'text'])
flagged_audio = pd.DataFrame(columns=['filename', 'text'])
keyword_df = pd.read_csv('radiospotter_keywords.csv')
keywords = keyword_df.iloc[:, 0].tolist()

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


# Function to load the current status from the JSON file
def load_status():
    try:
        with open('file_status.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to update the status in the JSON file
def update_status(filename, status):
    current_status = load_status()
    current_status[filename] = status
    with open('file_status.json', 'w') as f:
        json.dump(current_status, f)


def query(filename):
    # Load current status
    status = load_status().get(filename, "pending")
    
    # If already completed, skip
    if status == "completed":
        print(f"Skipping {filename}, already completed.")
        return
    
    try:
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            update_status(filename, "completed")

            text_response = response.json()['text']

            global df  # Declare df as global so we can modify it
            new_row = {'filename': filename, 'text': text_response}
            df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

            if any(keyword.lower() in text_response.lower() for keyword in keywords):
                global flagged_audio
                flagged_audio = pd.concat([flagged_audio, pd.DataFrame(new_row, index=[0])], ignore_index=True)

            time.sleep(2)

            return text_response
        else:
            print(f"Error processing {filename}, Status Code: {response.status_code}")
            update_status(filename, "error")
            return None

    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")
        update_status(filename, "error")
        return None


# Find files to work on
mp3_files = [f for f in os.listdir(".") if f.endswith('.mp3')]

for mp3_file in mp3_files:
    print(f"File: {mp3_file}")
    print(query(mp3_file))
    print("\n\n")
    df.to_csv('processed_texts.csv', index=False)
    flagged_audio.to_csv('flagged_texts.csv', index=False)  
print(df)
print(flagged_audio)