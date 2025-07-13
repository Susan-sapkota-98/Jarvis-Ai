import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pyttsx3

openai.api_key = apikey

chat_history = []

# Initialize pyttsx3 once for better performance
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Sorry, I could not understand.", e)
            return ""

def chat(query):
    global chat_history
    chat_history.append({"role": "user", "content": query})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
        message = response["choices"][0]["message"]["content"]
        say(message)
        chat_history.append({"role": "assistant", "content": message})
        return message
    except Exception as e:
        print("OpenAI API error:", e)
        say("Sorry, I am having trouble reaching the AI service.")
        return ""

if __name__ == "__main__":
    say("Jarvis AI activated")
    print("Welcome to Jarvis A.I")

    while True:
        query = takeCommand()

        if not query:
            continue

        # Open websites commands
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]
        opened_site = False
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                opened_site = True
                break
        if opened_site:
            continue

        if "open music" in query.lower():
            # Update this path to a valid music file on your system
            musicPath = "/home/susan/Music/example.mp3"
            if os.path.exists(musicPath):
                os.system(f"xdg-open '{musicPath}'")
                say("Playing music")
            else:
                say("Music file not found")
            continue

        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {minute} minutes")
            continue

        elif "reset chat" in query.lower():
            chat_history = []
            say("Chat history has been cleared")
            continue

        elif "jarvis quit" in query.lower() or "exit" in query.lower():
            say("Shutting down Jarvis. Goodbye!")
            break

        else:
            print("Chatting with AI...")
            chat(query)
