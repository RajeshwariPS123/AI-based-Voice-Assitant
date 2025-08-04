from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("What can I do for you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except Exception:
            print("Say that again, please...")
            return "None"
    return query.lower()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find information on that topic.")

        elif 'open google' in query:
            speak("what should I search ?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")
            results = wikipedia.summary(qry, sentences=2)
            speak(results)
        
        elif 'print' in query:
            speak("what should i print") 
            query = takeCommand().lower()
            pyautogui.write(f"{query}")

        elif 'close google' in query:
            os.system("taskkill /f /im msedge.exe")

        elif "calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("ready")
                print("Listning...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string=r.recognize_google(audio)
            print(my_string)

            def get_operator_fn(op):
                return {
                    '+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    'divided' : operator.__truediv__,
                }[op]
 
            def eval_bianary_expr(op1,oper, op2):
                op1,op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak("your result is")
            speak(eval_bianary_expr(*(my_string.split())))

        elif "scroll down" in query:
            pyautogui.scroll(500)

        elif "scroll up" in query:
            pyautogui.scroll(-500)

        elif "drag window to the right" in query:
            pyautogui.moveTo(46, 31, 2)
            pyautogui.dragRel(1857, 31, 2)

        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

        elif 'open youtube' in query:
            speak("What would you like to watch?")
            qrry = takeCommand()
            kit.playonyt(qrry)

        elif 'play music' in query:
            music_dir = 'C:\\Music'  
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No music found in the folder.")

        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'what is my ip address' in query:
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                speak(f"Your IP address is {ipAdd}")
            except Exception:
                speak("Unable to fetch IP address at the moment.")

        elif 'volume up' in query:
            for _ in range(10):
                pyautogui.press("volumeup")

        elif 'volume down' in query:
            for _ in range(10):
                pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")

        elif "go to sleep" in query:
            speak("Alright, switching off.")
            sys.exit()

        elif "capture" in query:
            speak("Tell me a name for the file.")
            name = takeCommand()
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot saved.")

        elif 'open chrome' in query:
            chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            if os.path.exists(chrome_path):
                os.startfile(chrome_path)
            else:
                speak("Chrome is not installed in the specified path.")

        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")