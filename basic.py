import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
from requests import get

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak text
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to listen and convert speech to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8  # Time to wait before recognizing
        r.energy_threshold = 300  # Adjusting the energy threshold for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.5)  # To handle background noise
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything.")
            return "none"
        except sr.UnknownValueError:
            speak("Sorry, I could not understand your speech.")
            return "none"
        except sr.RequestError:
            speak("Sorry, I couldn't connect to the Google recognition service.")
            return "none"
    return query.lower()

# Function to wish based on time of day
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis, How can I help you today?")

# Function to send an email
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-app-password')  # Replace with your email and app-specific password
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(e)

# Main function
if __name__ == '__main__':
    wish()
    while True:
        query = takecommand()

        # Check if a valid query is received
        if query == "none" or query.strip() == "":
            continue

        # Logic for different commands
        if "open notepad" in query:
            npath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to close the camera
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "C:\\Users\\kavya\\Music"
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia, {results}")

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open facebook" in query:
            webbrowser.open("https://facebook.com")

        elif "open instagram" in query:
            webbrowser.open("https://instagram.com")

        # Corrected Google search function
        elif "open google" in query:
            speak("What should I search on Google?")
            cm = takecommand().lower()
            if cm != "none" and cm.strip() != "":
                webbrowser.open(f"https://www.google.com/search?q={cm}")2
                speak(f"Searching for {cm} on Google.")
            else:
                speak("Sorry, I didn't catch the search query.")

        elif "send message" in query:
            kit.sendwhatmsg("+918287183583", "Hello!", datetime.datetime.now().hour, datetime.datetime.now().minute + 2)

        elif "play song on youtube" in query:
            kit.playonyt("Gasolina")

        elif "email to kavya" in query:
            try:
                speak("What should I say?")
                content = takecommand().lower()
                to = "ka4260@srmist.edu.in"
                sendEmail(to, content)
            except Exception as e:
                speak("Sorry, I couldn't send the email.")
                print(e)

        elif "thanks" in query:
            speak("Thank you for using Jarvis. Have a great day!")
            sys.exit()

        speak("Do you have any other tasks for me?")
