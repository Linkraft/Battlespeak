import speech_recognition as sr
r = sr.Recognizer()

mic = sr.Microphone(device_index=1)

print(sr.Microphone.list_microphone_names())

while True:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print(r.recognize_google(audio))
        break
    except sr.RequestError:
        print("The Google API didn't work for some reason")
        print("Make sure this computer is connected to the Internet")
    except sr.UnknownValueError:
        print("Woops! You just spoke some nonsense. Try again!")
