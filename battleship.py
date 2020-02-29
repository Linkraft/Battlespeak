import speech_recognition as sr

def printRules():
    print("     Welcome to Battlespeak!\n")
    print("This is a voice-controlled version of the popular")
    print("board game Battleship. To play, you must give commands")
    print("to the program with your voice.\n")
    printCommands()

def printCommands():
    print("Here are the list of commands available to you:")
    print("- To tell the program what coordinates you would like")
    print("  to bomb, please say the coordinates in this form:")
    print("                 \"Bomb D1\"")
    print("  where \"D1\" would be replaced with your desired coordinates")


if __name__ == "__main__":
    r = sr.Recognizer()

    mic = sr.Microphone(device_index=1)

    print(sr.Microphone.list_microphone_names())

    printRules()

    while True:
        with mic as source:
            print("Hold on a moment...")
            r.adjust_for_ambient_noise(source)
            print("Now say your command:")
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            break
        except sr.RequestError:
            print("The Google API didn't work for some reason")
            print("Make sure this computer is connected to the Internet")
        except sr.UnknownValueError:
            print("Woops! You just spoke some nonsense. Try again!")
