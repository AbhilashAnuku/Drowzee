import time

import pygame
from gtts import gTTS

def read_aloud(input_text):
    """Generates a sound file from input text"""
    tts = gTTS(text=input_text, lang='en-au', slow=False)
    title = 'story.mp3'
    tts.save(title)

async def foo(file_name):
    if file_name:
        await start_player(file_name)

def start_player(file_name):
    """Plays audio file using pygame mixer"""
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as message:
        print(message)
    pygame.mixer.quit()

sample_text = "wake up"
read_aloud(sample_text)
