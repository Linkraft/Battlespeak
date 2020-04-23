import speech_recognition as sr
import gtts, playsound, time, os, random, uuid
import sys, pygame
from array import *
from random import randint
from gtts import gTTS
from tempfile import TemporaryFile

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
redx = pygame.image.load('assets/redx.png')
whitex = pygame.image.load('assets/whitex.png')

boatArray = [fiveBoat, fourBoat, threeBoat1, threeBoat2, twoBoat]
sizeBoatArray = [5, 4, 3, 3, 2]
stopGameArray = ["stop", "stop game", "stop the game", \
                "end", "end game", "end the game", \
                "quit", "quit game", "quit the game"]
startGameArray = ["start", "start game", "start the game", \
                "begin", "begin game", "begin the game", \
                "play", "play game", "play the game"]
letterArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

playerHits = 0
opponentHits = 0


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

def recognize_speech():
    while True:
        with mic as source:
            audio = r.listen(source)
            try:
                speech = r.recognize_google(audio)
                print(speech)
                command = speech
                break
            except sr.RequestError:
                say("The Google API didn't work for some reason")
                say("Make sure this computer is connected to the Internet")
            except sr.UnknownValueError:
                say("I didn't quite catch that. Please try again!")
    return command


def sayRules():
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
    say("where, D1, would be replaced with your desired coordinates.")
    say("To begin the game, you can tell me to start or begin the game. \
         Finally, if you want to stop playing at any time, you can tell me to end or quit the game.")

def validateCoordinates(command):
    while True:
        #input checks
        #check for speech recognition error where I1 is recognized always as "I won"
        if "I won" in command:
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
            say("I don't understand that. Please try again more slowly!")
            command = recognize_speech()
            continue

        #fixes errors like H8 = "h8"
        command = command.capitalize()

        #fixes error where recognition thinks "F" sounds like "S" very often
        if command[0] == 'S':
            command[0] = 'F'

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
        command = recognize_speech()
        
        if "horizontal" in command:
            command = "horizontal"
        elif "vertical" in command:
            command = "vertical"

        if command == "horizontal" or command == "vertical":
            orient = "horizontal"
            if command == "horizontal":
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

            valid = False
            while not valid:
                say("Which square of the grid should the tip of this boat be placed?")
                command = recognize_speech()
                command = validateCoordinates(command)
                if command in stopGameArray:
                    say("Thanks for playing!")
                    pygame.quit()
                    sys.exit()

                print("Current orientation: ", orient)
                print("Current size of boat: ", sizeBoatArray[boatsPlaced])
                print("Current command: ", command)
                print("Checking if the position is allowed...")

                #check if the position is allowed, based on size and orientation of ship
                isAllowed = checkPosition(orient, sizeBoatArray[boatsPlaced], command)

                if isAllowed:
                    print("Allowed!")
                    boatMoveGraphics(boatArray[boatsPlaced], command)
                    #clear the vertical space
                    pygame.draw.rect(screen, blue, ((width // 2 - 40), 50, 80, 400))
                    #clear the horizontal space
                    pygame.draw.rect(screen, blue, ((width // 4 + 50), 500, 400, 100))

                    pygame.display.update()
                    say("Boat placed.")
                    valid = True
                else:
                    print("Not allowed!")
                    valid = False

            #increment while loop if command was "horizontal" or "vertical"
            boatsPlaced += 1
            pygame.display.update()

        elif command in stopGameArray:
            say("Thanks for playing!")
            pygame.quit()
            sys.exit()
        else:
            say("I couldn't recognize that. Please try again.")

def boatMoveGraphics(boatImg, location):
    #blit the boatImg to the appropriate part of the screen based on location letter + number
    squareArray = [[57, 99, 139, 185, 228, 271, 315, 359, 403, 475], \
                    [28, 74, 116, 161, 204, 248, 292, 337, 380, 422]]

    #get the letter value as an int 0-9 and the number value as an int 0-9
    #letter is in ASCII form, so subtract 65 so that 'A' corresponds to 0
    letter = ord(location[0]) - 65
    number = 0

    #if the number coord is a single digit, find that digit
    if len(location) < 3:
        number = int(location[1]) - 1
    #else, it's a double digit which can only be 10 (9 when indexed in an array)
    else:
        number = 9

    xCoord = squareArray[1][number]
    yCoord = squareArray[0][letter]

    print("X coordinate is ", xCoord)
    print("Y coordinate is ", yCoord)

    screen.blit(boatImg, [xCoord, yCoord])

def placeHitMarker(player, location, hit):

    marker = whitex
    squareArray = [[57, 99, 139, 185, 228, 271, 315, 359, 403, 475], \
                    [28, 74, 116, 161, 204, 248, 292, 337, 380, 422]]

    #get the letter value as an int 0-9 and the number value as an int 0-9
    #letter is in ASCII form, so subtract 65 so that 'A' corresponds to 0
    letter = ord(location[0]) - 65
    number = 0

    #if the number coord is a single digit, find that digit
    if len(location) < 3:
        number = int(location[1]) - 1
    #else, it's a double digit which can only be 10 (9 when indexed in an array)
    else:
        number = 9

    xCoord = squareArray[1][number]
    yCoord = squareArray[0][letter]

    print("X coordinate is ", xCoord)
    print("Y coordinate is ", yCoord)

    if (player == True):
        xCoord += 570

    if (hit):
        marker = redx

    screen.blit(marker, [xCoord, yCoord])
    pygame.display.update()

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
                invalidMsg()
                return False
        elif size == 4:
            invalidArray = ['H', 'I', 'J']
            if letter in invalidArray:
                invalidMsg()
                return False
        elif size == 3:
            invalidArray = ['I', 'J']
            if letter in invalidArray:
                invalidMsg()
                return False
        #if size is 2
        else:
            if letter == 'J':
                invalidMsg()
                return False

    #if horiz, invalid numbers are (7-10 for 5boat), (8-10 for 4boat), (9-10 for 3boat), (10 for 2boat)
    else:
        if size == 5:
            if number > 6:
                invalidMsg()
                return False
            elif number <= 0:
                say("Your number must be between 1 and 10")
                return False
        elif size == 4:
            if number > 7:
                invalidMsg()
                return False
            elif number <= 0:
                say("Your number must be between 1 and 10")
                return False
        elif size == 3:
            if number > 8:
                invalidMsg()
                return False
            elif number <= 0:
                say("Your number must be between 1 and 10")
                return False

        #size == 2
        else:
            if number > 9:
                invalidMsg()
                return False
            elif number <= 0:
                say("Your number must be between 1 and 10")
                return False

    #if it reaches this part, the boat size and orientation is valid
    #Now check to see if the boat is being placed in a position that is already occupied
    isOccupied = False
    isValid = True

    #first, check the array to see if the spaces are occupied (1) or not (0)
    index1 = ord(letter[0]) - 65
    index2 = number - 1

    #start at userShips[index1][index2]
    #iterate through "size" times, so 0 to "size" - 1

    #check to see if all the spaces are clear before placing the ship
    for i in range(size):
        if userShips[index1][index2] == 1:
            say("There's already a boat there!")
            return False

            #update the indexes based on orientation
            #if vertical, we want to increment index1
            #if horizontal, we want to increment index2
        if orient == "vertical":
            index1 = index1 + 1
        else:
            index2 = index2 + 1

    #reset indices
    index1 = ord(letter[0]) - 65
    index2 = number - 1

    #place the ship (fill array space with 1's)
    for i in range(size):
        userShips[index1][index2] = 1
        isValid = True

            #update the indexes based on orientation
            #if vertical, we want to increment index1
            #if horizontal, we want to increment index2
        if orient == "vertical":
            index1 = index1 + 1
        else:
            index2 = index2 + 1

    return isValid

def invalidMsg():
    say("That position is not valid due to boat size and how your boat is oriented. Please try another space.")

def player_turn():
    global playerHits
    say("Which coordinate would you like to bomb?")

    coordinate = recognize_speech()
    coordinate = validateCoordinates(coordinate)

    vertical = coordinate[:1]
    horizontal = coordinate[1:]

    if opponentShips[ord(vertical) - ord('A')][int(horizontal)] == 1:
        print('Hit!')
        opponentShips[ord(vertical) - ord('A')][int(horizontal)] = 'X'
        say("Congratulations! You scored a hit!")
        placeHitMarker(True, coordinate, True)
        playerHits = playerHits + 1

    elif opponentShips[ord(vertical) - ord('A')][int(horizontal)] == 'X' or opponentShips[ord(vertical) - ord('A')][int(horizontal)] == '*':
        say("You have already bombed that spot. Please choose another")
        player_turn()
        return

    else:
        opponentShips[ord(vertical) - ord('A')][int(horizontal)] = '*'
        say("Sorry, your bomb did not land a hit")
        placeHitMarker(True, coordinate, False)


def opponent_turn():
    global opponentHits

    print('Opponent turn')

    horizontal = random.randint(0, 9)
    vertical = random.randint(0, 9)

    print(vertical)
    print(horizontal)

    print(userShips[vertical][horizontal])

    if userShips[vertical][horizontal] == '*' or userShips[vertical][horizontal] == 'X':
        opponent_turn()
        return

    elif userShips[vertical][horizontal] == 0:
        print('Opponent Miss')
        placeHitMarker(False, str(chr(vertical + 65)) + str(horizontal), False)
        say("Your opponent chose coordinate " + chr(vertical + 65) + str(horizontal) + " and missed")
        userShips[vertical][horizontal] = '*'

    elif userShips[vertical][horizontal] == 1:
        print('Opponent Hit')
        placeHitMarker(False, str(chr(vertical + 65)) + str(horizontal), True)
        say("Your opponent chose coordinate " + chr(vertical + 65) + str(horizontal) + " and hit")
        userShips[vertical][horizontal] = 'X'
        opponentHits += 1

def turn_loop():
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

    with mic as source:
            say("Please give the voice recognizer a moment to adjust to your ambient noise")
            r.adjust_for_ambient_noise(source)

    validCommand = False
    while validCommand != True:
        say("Would you like to hear the rules?")
        command = recognize_speech()
        if "yes" in command:
            validCommand = True
            sayRules()
        elif "no" in command:
            validCommand = True
            say("Okay, I won't tell you the rules.")
        elif command in stopGameArray:
            say("Thanks for playing!")
            pygame.quit()
            sys.exit()

    intro = True
    while intro:
        say("To begin the game, say start")
        command = recognize_speech()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

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
    #temporary placement of opponent battleships

    pygame.display.update()

    #user places their boats
    placeBoats()
    say("All boats have been placed. Now it's time to start the game!")
    turn_loop()

if __name__ == "__main__":
    r = sr.Recognizer()
    r.operation_timeout = 10
    mic = sr.Microphone(device_index=1)
    game_intro()
