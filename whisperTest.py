# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
import glob
#import vlc
#import playsound
from playsound import playsound

openai.api_key = os.environ.get('API_KEY')
if not openai.api_key:
    raise ValueError("No API key provided. Set the API_KEY environment variable.")


files = glob.glob('/home/mat/Documents/ProgramExperiments/copterSpotter/*.mp3')
#file_names = [os.path.basename(file) for file in files]

name = "./20230815_144229.mp3"

for i in files:
    audio_file= open(i, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("|" + i + " | " + transcript["text"] + "|")
    #player = vlc.MediaPlayer(i)
    for i in range(3):
        #player.play()
        playsound.playsound(i)
