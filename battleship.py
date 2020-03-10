import speech_recognition as sr
import gtts, playsound, time, os
import sys, pygame
from array import *

#sprites from https://opengameart.org/content/battleships

pygame.init()
clock = pygame.time.Clock()

size = width, height = 1020, 600
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
pale_blue = 118, 142, 181
blue = 81, 120, 181
dark_blue = 53, 88, 143

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Battlespeak')

gridImg = pygame.image.load('assets/grid.png')
fiveBoat = pygame.image.load('assets/fiveBoat.png')
fourBoat = pygame.image.load('assets/fourBoat.png')
threeBoat1 = pygame.image.load('assets/threeBoat1.png')
threeBoat2 = pygame.image.load('assets/threeBoat2.png')
twoBoat = pygame.image.load('assets/twoBoat.png')

def speakText(speech, filename):
    file = filename + '.mp3'
    mp3 = gtts.gTTS(text=speech, lang='en', slow=False)
    mp3.save(file)
    playsound.playsound(file, True)
    os.remove(file)

def sayRules():
    speakText("Welcome to Battlespeak!\
            This is a voice-controlled version of the popular\
            board game Battleship. To play, you must give commands\
            to the program with your voice.", "f")
    sayCommands()

def sayCommands():
    speakText("Here are the list of commands available to you:", "a")
    speakText("To tell the program what coordinates you would like\
            to bomb, please say the coordinates in this form:", "b")
    speakText("Bomb D1", "c")
    speakText("where, D1, would be replaced with your desired coordinates", "a")
    speakText("Begin the game by saying start", "a")

def game_intro():
    screen.fill(pale_blue)

    largeFont = pygame.font.Font('freesansbold.ttf', 48)
    font = pygame.font.Font('freesansbold.ttf', 28)

    titleText = largeFont.render('Battlespeak', True, white)
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (width // 2, height // 2)
    screen.blit(titleText, titleTextRect)

    pygame.display.update()
    sayRules()

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        with mic as source:
            speakText("Hold on a moment","aa")
            r.adjust_for_ambient_noise(source)
            speakText("Now say your command:", "aaa")
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
            intro = False
            break
        except sr.RequestError:
            speakText("The Google API didn't work for some reason","ab")
            speakText("Make sure this computer is connected to the Internet", "ac")
        except sr.UnknownValueError:
            speakText("Whoops! You just spoke some nonsense. Try again!", "ad")

    if command == "start":
        game_loop()

def game_loop():
    screen.fill(blue)

    titleFont = pygame.font.Font('freesansbold.ttf', 20)

    ybText = titleFont.render('Your Board', True, white)
    ybTextRect = ybText.get_rect()
    ybTextRect.center = (width // 4, 20)

    obText = titleFont.render('Opponent Board', True, white)
    obTextRect = obText.get_rect()
    obTextRect.center = (750, 20)

    screen.blit(ybText, ybTextRect)
    screen.blit(obText, obTextRect)

    #temporary placement of opponent battleships
    opponentShips = [[0,1,1,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,1,1,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,1],
                    [0,0,1,1,1,1,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,0]]

    userShips = [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]]

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(gridImg, (15,40))
        screen.blit(gridImg, (570, 40))

        #user places their boats

        screen.blit(fiveBoat, (width // 2 - 10, 200))

        bpText = titleFont.render('Will your 5 boat be horizontal or vertical?', True, black)
        bpTextRect = bpText.get_rect()
        bpTextRect.center = (width // 2, height // 2 + 200)
        screen.blit(bpText, bpTextRect)





        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    game_intro()
