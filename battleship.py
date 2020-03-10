import speech_recognition as sr
import gtts, playsound, time, os

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
    speakText("where D1 would be replaced with your desired coordinates", "a")


if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    sayRules()

    while True:
        with mic as source:
            speakText("Hold on a moment","aa")
            r.adjust_for_ambient_noise(source)
            speakText("Now say your command:", "aaa")
            audio = r.listen(source)

        try:
            print(r.recognize_google(audio))
            break
        except sr.RequestError:
            speakText("The Google API didn't work for some reason","ab")
            speakText("Make sure this computer is connected to the Internet", "ac")
        except sr.UnknownValueError:
            speakText("Woops! You just spoke some nonsense. Try again!", "ad")
