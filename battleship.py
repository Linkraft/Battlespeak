import sys, pygame, time, os, random, uuid
import speech_recognition as sr
from gtts import gTTS
from tempfile import TemporaryFile
from array import *
from random import randint

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

bg_img = pygame.image.load('assets/Intro-BG.png')
gridImg = pygame.image.load('assets/grid.png')
fiveBoat = pygame.image.load('assets/fiveBoatV.png')
fourBoat = pygame.image.load('assets/fourBoatV.png')
threeBoat1 = pygame.image.load('assets/threeBoat1V.png')
threeBoat2 = pygame.image.load('assets/threeBoat2V.png')
twoBoat = pygame.image.load('assets/twoBoatV.png')

boatArray = [fiveBoat, fourBoat, threeBoat1, threeBoat2, twoBoat]
sizeBoatArray = [5, 4, 3, 3, 2]
stopGameArray = ["stop", "stop game", "stop the game", \
                "end", "end game", "end the game", \
                "quit", "quit game", "quit the game"]
startGameArray = ["start", "start game", "start the game", \
                "begin", "begin game", "begin the game", \
                "play", "play game", "play the game"]
letterArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

global userShips, opponentShips, playerHits, opponentHits
#temporary placement of opponent battleships
opponentShips = [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
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

def waitOptions():
    waitArray = ["Hang on a minute.", "Wait just a second.", "Hold on, please.", "Give me a second.", "Hang on just a second."]
    option = randint(0,4);
    say(waitArray[option]);

def confirmOptions():
    confirmArray = ["Okay, I'm ready. What's your command?", "Alright! What is your command?", "Okay. What's your command?"]
    option = randint(0,2);
    say(confirmArray[option]);

def recognize_speech():
    while True:
        with mic as source:
            waitOptions()
            r.adjust_for_ambient_noise(source)
            confirmOptions()
            audio = r.listen(source)
            try:
                print(r.recognize_google(audio))
                command = r.recognize_google(audio)
                break
            except sr.RequestError:
                say("The Google API didn't work for some reason")
                say("Make sure this computer is connected to the Internet")
            except sr.UnknownValueError:
                say("I didn't quite catch that. Please try again!")
    return command

def sayIntro():
    say("Welcome to Battlespeak!\
            This is a voice-controlled version of the popular\
            board game Battleship. To play, you must give commands\
            to the program with your voice. Please note that voice\
            commands take time to process, so please be patient\
            when waiting to input a command or when waiting for recognition.")

def sayCommands():
    say("Here are the list of commands available to you:")
    say("To tell the program what coordinates you would like\
            to bomb, please say the coordinates in this form:")
    say("D1")
    say("where, D1, would be replaced with your desired coordinates")
    say("Finally, to begin the game, you can tell me to start or begin the game")

def validateCoordinates(command):
    while True:
        #input checks
        #check for speech recognition error where I1 is recognized always as "I won"
        if command == "I won":
            command = "I1"
            break

        #fixes errors like I4 = "I-4"
        command = command.replace('-', '')

        #check for errors like B4 = "before" or A2 = "82"
        if len(command) > 3 or command[0].isdigit():
            say("I don't understand that. Please try again more slowly!")
            command = recognize_speech()
            continue
        #check for errors like F7 = "ff7"
        elif not command[1].isdigit():
            say("That command is invalid. Please try again more slowly!")
            command = recognize_speech()
            continue

        #fixes errors like H8 = "h8"
        command = command.capitalize()

        #fixes error where recognition thinks "F" sounds like "S" very often
        if command[0] == 'S':
            command = command.replace('S', 'F')
            print("changed")

        #check for errors if the user says something like "K4"
        if command[0] not in letterArray:
            say("That letter is not valid. Please try a different letter or try again more slowly!")
            command = recognize_speech()
            continue
        break
    return command


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
        say("Would you like this boat to be horizontal or vertical?")

        with mic as source:
            waitOptions()
            r.adjust_for_ambient_noise(source)
            confirmOptions()
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.RequestError:
            say("The Google API didn't work for some reason")
            say("Make sure this computer is connected to the Internet")
        except sr.UnknownValueError:
            say("I didn't quite catch that. Please try again!")
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
                say("Which square of the grid should the tip of this boat be placed?")
                command = ""
                with mic as source:
                    waitOptions()
                    r.adjust_for_ambient_noise(source)
                    confirmOptions()
                    audio = r.listen(source)

                try:
                    print(r.recognize_google(audio))
                    command = r.recognize_google(audio)
                except sr.RequestError:
                    say("The Google API didn't work for some reason")
                    say("Make sure this computer is connected to the Internet")
                except sr.UnknownValueError:
                    say("I didn't quite catch that. Please try again!")
                    continue

                if command in stopGameArray:
                    say("Thanks for playing!")
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
                    say("I don't understand that. Please try again more slowly!")
                    continue
                #check for errors like F7 = "ff7"
                elif not command[1].isdigit():
                    say("That command is invalid. Please try again more slowly!")
                    continue

                #fixes errors like H8 = "h8"
                command = command.capitalize()

                #fixes error where recognition thinks "F" sounds like "S" very often
                if command[0] == 'S':
                    command[0] = 'F'

                #check for errors if the user says something like "K4"
                if command[0] not in letterArray:
                    say("That letter is not valid. Please try a different letter or try again more slowly!")
                    continue

                print("Current orientation: ", orient)
                print("Current size of boat: ", sizeBoatArray[boatsPlaced])
                print("Current command: ", command)
                print("Checking if the position is allowed...")

                #check if the position is allowed, based on size and orientation of ship
                isAllowed = checkPosition(orient, sizeBoatArray[boatsPlaced], command)

                if isAllowed:
                    print("Allowed!")
                    boatMoveGraphics(boatArray[boatsPlaced], command)
                    say("Boat placed.")
                    valid = True
                else:
                    print("Not allowed!")
                    say("That position is not valid due to boat size and how your boat is oriented. Please try another space.")
                    valid = False

            #increment while loop if command was "horizontal" or "vertical"
            boatsPlaced += 1

        elif command in stopGameArray:
            say("Thanks for playing!")
            pygame.quit()
            sys.exit()
        else:
            say("I couldn't recognize that. Please try again.")

def boatMoveGraphics(boatImg, location):
    #blit the boatImg to the appropriate part of the screen based on location letter + number
    squareArray = [[28, 74, 116, 161, 204, 248, 292, 337, 380, 422], \
                   [57, 99, 139, 185, 228, 271, 315, 359, 403, 475]]

    #get the letter value as an int 0-9 and the number value as an int 0-9
    #letter is in ASCII form, so subtract 65 so that 'A' corresponds to 0
    letter = ord(location[0]) - 65
    number = int(location[1]) - 1

    xCoord = squareArray[0][letter]
    yCoord = squareArray[1][number]

    

    screen.blit(boatImg, [xCoord, yCoord])


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

def player_turn():
    say("Which coordinate would you like to bomb?")

    coordinate = recognize_speech()
    coordinate = validateCoordinates(coordinate)

    vertical = coordinate[:1]
    horizontal = coordinate[1:]

    if opponentShips[ord(vertical) - ord('A')][int(horizontal)] == 1:
        print('Hit!')
        opponentShips[ord(vertical) - ord('A')][int(horizontal)] = 'X'
        say("Congratulations! You scored a hit!")
        playerHits += 1

    elif opponentShips[ord(vertical) - ord('A')][int(horizontal)] == 'X' or opponentShips[ord(vertical) - ord('A')][int(horizontal)] == '*':
        say("You have already bombed that spot. Please choose another")
        player_turn()
        return

    else:
        opponentShips[ord(vertical) - ord('A')][int(horizontal)] = '*'
        say("Sorry, your bomb did not land a hit")

def opponent_turn():
    horizontal = random.randint(0, 9)
    vertical = random.randint(0, 9)

    if userShips[vertical][horizontal] == '*' or userShips[vertical][horizontal] == 'X':
        opponent_turn()
        return

    elif userShips[vertical][horizontal] == '0':
        say("Your opponent chose coordinate " + vertical + horizontal + " and missed")
        userShips[vertical][horizontal] = '*'

    elif userShips[vertical][horizontal] == '1':
        say("Your opponent chose coordinate " + vertical + horizontal + " and hit")
        userShips[vertical][horizontal] = 'X'
        opponentHits += 1

def turn_loop():
    #clear the vertical space
    pygame.draw.rect(screen, blue, ((width // 2 - 40), 50, 80, 400))
    #clear the horizontal space
    pygame.draw.rect(screen, blue, ((width // 4 + 50), 500, 400, 100))
    pygame.display.update()

    playerHits = 0
    opponentHits = 0

    while True:
        player_turn()
        if playerHits == 17:
            say("Congratulations! You have sunk all the enemy ships.")
            break
        opponent_turn()
        if opponentHits == 17:
            say("Sorry, all your ships have been sunk.")
            break



def game_intro():
    screen.blit(bg_img, [0,0])

    largeFont = pygame.font.Font('freesansbold.ttf', 48)
    font = pygame.font.Font('freesansbold.ttf', 28)

    titleText = largeFont.render('Battlespeak', True, white)
    titleTextRect = titleText.get_rect()
    titleTextRect.center = (width // 2, height // 2)
    screen.blit(titleText, titleTextRect)

    pygame.display.update()

    sayIntro()
    validCommand = False
    while not validCommand:
        command = ""
        say("Would you like to hear the rules?")
        with mic as source:
            waitOptions()
            r.adjust_for_ambient_noise(source)
            confirmOptions()
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.RequestError:
            say("The Google API didn't work for some reason")
            say("Make sure this computer is connected to the Internet")
        except sr.UnknownValueError:
            say("I didn't quite catch that. Please try again!")

        if command == "yes":
            validCommand = True
            sayCommands()
        elif command == "no":
            validCommand = True
            say("Okay, I won't tell you the rules.")
        elif command in stopGameArray:
            say("Thanks for playing!")
            pygame.quit()
            sys.exit()

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        with mic as source:
            waitOptions()
            r.adjust_for_ambient_noise(source)
            confirmOptions()
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            command = r.recognize_google(audio)
        except sr.RequestError:
            say("The Google API didn't work for some reason")
            say("Make sure this computer is connected to the Internet")
        except sr.UnknownValueError:
            say("Whoops! You just spoke some nonsense. Try again!")

        if command in startGameArray:
            intro = False
            game_loop()
        elif command in stopGameArray:
            intro = False
            say("Thanks for playing!")
            pygame.quit()
            sys.exit()
        else:
            say("Sorry, that is not a valid response. Please try again.")

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


    pygame.display.update()

    #user places their boats
    placeBoats()

    say("All boats have been placed. Now it's time to start the game!")

    turn_loop()



if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    game_intro()
