import sys, pygame, time, os
import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from array import *

# Initialize Pygame
pygame.init()
pygame.time.Clock() # Initialize the clock

# Initialize screen resolution
size = width, height = 1020, 600
screen = pygame.display.set_mode(size)

# Initalize colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
pale_blue = 118, 142, 181
blue = 81, 120, 181
dark_blue = 53, 88, 143

def say(speech):
    try:
        tts = gTTS(text=speech, lang='en', slow=False)
        pygame.mixer.init()
        sf = TemporaryFile()
        tts.write_to_fp(sf)
        sf.seek(0)
        pygame.mixer.music.load(sf)
        pygame.mixer.music.play()
        print(speech) # For debugging purposes
        # Now wait for the sound clip to end
        while (pygame.mixer.music.get_busy()):
            continue
    except Exception:
        raise

def main():
    screen.fill(pale_blue)    
    largeFont = pygame.font.Font('freesansbold.ttf', 48)
    font = pygame.font.Font('freesansbold.ttf', 28)

    titleText = largeFont.render('Battlespeak', True, white)
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (width // 2, height // 2)
    screen.blit(titleText, titleTextRect)

    pygame.display.update()
    while True:
        say("My name is how I like to spell it!")
        say("My name is Jordan!")


if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index = 1)
    main()