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
fiveBoat = pygame.image.load('assets/fiveBoatV.png')
fourBoat = pygame.image.load('assets/fourBoatV.png')
threeBoat1 = pygame.image.load('assets/threeBoat1V.png')
threeBoat2 = pygame.image.load('assets/threeBoat2V.png')
twoBoat = pygame.image.load('assets/twoBoatV.png')

boatArray = [fiveBoat, fourBoat, threeBoat1, threeBoat2, twoBoat]
sizeBoatArray = [5, 4, 3, 3, 2]
stopGameArray = ["stop", "stop game", "end", "end game", "quit", "quit game"]
letterArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

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
    speakText("Finally, to begin the game, say start", "a")


def placeBoats():

    boatsPlaced = 0
    while boatsPlaced < 5:
        command = ""
        #fill in the empty areas with blue so that the boats don't blit on top of each other
        #rect parameters: Surface, color, Rect (x, y, width, height)
        pygame.draw.rect(screen, blue, ((width // 2 - 40), 50, 80, 400))
        pygame.draw.rect(screen, blue, ((width // 4 + 50), 500, 400, 100))
        #blit the boat to the screen
        screen.blit(boatArray[boatsPlaced], (width // 2 - 20, height // 2 - 100))
        pygame.display.update()
        speakText("Would you like this boat to be horizontal or vertical?", "a")

        with mic as source:
            speakText("Hold on a moment","aa")
            r.adjust_for_ambient_noise(source)
            speakText("Now say your command:", "aaa")
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.RequestError:
            speakText("The Google API didn't work for some reason","ab")
            speakText("Make sure this computer is connected to the Internet", "ac")
        except sr.UnknownValueError:
            speakText("I didn't quite catch that. Please try again!", "ad")
            continue

        orient = ""
        if command == "horizontal" or command == "vertical":
            if command == "horizontal":
                orient = "horizontal"
                #clear the vertical space
                pygame.draw.rect(screen, blue, ((width // 2 - 40), 50, 80, 400))
                #display the boat horizontally
                if boatsPlaced == 0:
                    boatArray[boatsPlaced] = pygame.image.load('assets/fiveBoatH.png')
                elif boatsPlaced == 1:
                    boatArray[boatsPlaced] = pygame.image.load('assets/fourBoatH.png')
                elif boatsPlaced == 2:
                    boatArray[boatsPlaced] = pygame.image.load('assets/threeBoat1H.png')
                elif boatsPlaced == 3:
                    boatArray[boatsPlaced] = pygame.image.load('assets/threeBoat2H.png')
                elif boatsPlaced == 4:
                    boatArray[boatsPlaced] = pygame.image.load('assets/twoBoatH.png')

                imgSize = boatArray[boatsPlaced].get_size()
                imgWidth = imgSize[0]
                screen.blit(boatArray[boatsPlaced], (width // 2 - (imgWidth // 2), height // 2 + 220))
                pygame.display.update()

            elif command == "vertical":
                orient = "vertical"

            valid = False
            while not valid:
                speakText("Which square of the grid should the tip of this boat be placed?", "bp")
                command = ""
                with mic as source:
                    speakText("Hold on a moment","aa")
                    r.adjust_for_ambient_noise(source)
                    speakText("Now say your command:", "aaa")
                    audio = r.listen(source)

                try:
                    print(r.recognize_google(audio))
                    command = r.recognize_google(audio)
                except sr.RequestError:
                    speakText("The Google API didn't work for some reason","ab")
                    speakText("Make sure this computer is connected to the Internet", "ac")
                except sr.UnknownValueError:
                    speakText("I didn't quite catch that. Please try again!", "ad")
                    continue

                if command in stopGameArray:
                    speakText("Goodbye!", "a")
                    pygame.quit()
                    sys.exit()

                #input checks
                #check for speech recognition error where I1 is recognized always as "I won"
                if command == "I won":
                    command = "I1"
                    break

                #fixes errors like I4 = "I-4"
                command = command.replace('-', '')

                #check for errors like B4 = "before" or A2 = "82"
                if len(command) > 3 or command[0].isdigit():
                    speakText("I don't understand that. Please try again more slowly!", "ad")
                    continue
                #check for errors like F7 = "ff7"
                elif not command[1].isdigit():
                    speakText("That command is invalid. Please try again more slowly!", "ad")
                    continue

                #fixes errors like H8 = "h8"
                command = command.capitalize()

                #fixes error where recognition thinks "F" sounds like "S" very often
                if command[0] == 'S':
                    command[0] = 'F'

                #check for errors if the user says something like "K4"
                if command[0] not in letterArray:
                    speakText("That letter isn't valid. Please try a different letter or try again more slowly!", "ad")
                    continue

                print("Current orientation: ", orient)
                print("Current size of boat: ", sizeBoatArray[boatsPlaced])
                print("Current command: ", command)
                print("Checking if the position is allowed...")

                #check if the position is allowed, based on size and orientation of ship
                isAllowed = checkPosition(orient, sizeBoatArray[boatsPlaced], command)

                if isAllowed:
                    print("Allowed!")
                    speakText("Boat placed.", "cm")
                    valid = True
                else:
                    print("Not allowed!")
                    speakText("That position isn't valid due to boat size and orientation. Please try another space.", "rm")
                    valid = False

            #increment while loop if command was "horizontal" or "vertical"
            boatsPlaced += 1

        elif command in stopGameArray:
            speakText("Goodbye!", "a")
            pygame.quit()
            sys.exit()
        else:
            speakText("I couldn't recognize that. Please try again.", "fr")

def checkPosition(orient, size, square):
    #first split the square var into letter and number
    letter = square[0]
    number = 0
    if len(square) == 2:
        number = int(square[1], 10)
    elif len(square) == 3:
        number = int(square[-2:], 10)

    #use orient, size, letter, and number to determine if boat is in valid position

    #if vertical, invalid letters are (G-J for 5boat), (H-J for 4boat), (I-J for 3boat), (J for 2boat)
    if orient == "vertical":
        if size == 5:
            invalidArray = ['G', 'H', 'I', 'J']
            if letter in invalidArray:
                return False
            else:
                return True
        elif size == 4:
            invalidArray = ['H', 'I', 'J']
            if letter in invalidArray:
                return False
            else:
                return True
        elif size == 3:
            invalidArray = ['I', 'J']
            if letter in invalidArray:
                return False
            else:
                return True
        #if size is 2
        else:
            if letter == 'J':
                return False
            else:
                return True
        #default return statement
        return False


    #if horiz, invalid numbers are (7-10 for 5boat), (8-10 for 4boat), (9-10 for 3boat), (10 for 2boat)
    else:
        if size == 5:
            if number > 6:
                return False
            elif number > 0:
                return True
        elif size == 4:
            if number > 7:
                return False
            elif number > 0:
                return True
        elif size == 3:
            if number > 8:
                return False
            elif number > 0:
                return True

        #size == 2
        else:
            if number > 9:
                return False
            elif number > 0:
                return True
        #default return statement
        return False


def game_intro():
    screen.fill(pale_blue)

    largeFont = pygame.font.Font('freesansbold.ttf', 48)
    font = pygame.font.Font('freesansbold.ttf', 28)

    titleText = largeFont.render('Battlespeak', True, white)
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (width // 2, height // 2)
    screen.blit(titleText, titleTextRect)

    pygame.display.update()


    validCommand = False
    while not validCommand:
        command = ""
        speakText("Would you like to hear the rules?", "a")
        with mic as source:
            speakText("Hold on a moment","aa")
            r.adjust_for_ambient_noise(source)
            speakText("Now say your command:", "aaa")
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.RequestError:
            speakText("The Google API didn't work for some reason","ab")
            speakText("Make sure this computer is connected to the Internet", "ac")
        except sr.UnknownValueError:
            speakText("I didn't quite catch that. Please try again!", "ad")

        if command == "yes":
            validCommand = True
            sayRules()
        elif command == "no":
            validCommand = True
        elif command in stopGameArray:
            speakText("Goodbye!", "a")
            pygame.quit()
            sys.exit()

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

    if command == "start" or command == "start game":
        game_loop()
    elif command in stopGameArray:
        speakText("Goodbye!", "a")
        pygame.quit()
        sys.exit()
    else:
        speakText("Sorry, that isn't a valid response. Please try again.", "fr")

def game_loop():
    #render the game screen with titles and boards
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

    screen.blit(gridImg, (15,40))
    screen.blit(gridImg, (570, 40))
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

    pygame.display.update()

    #user places their boats
    placeBoats()



if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    game_intro()
