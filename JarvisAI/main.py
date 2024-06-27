import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import openai
import pyautogui
import time
from configuration import apikey

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

chatStr = ""
openai.api_key = apikey

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.UnknownValueError:
            error_message = "Google Speech Recognition could not understand audio"
            print(error_message)
            return "I didn't catch that. Please say that again."
        except sr.RequestError as e:
            error_message = f"Could not request results from Google Speech Recognition service; {e}"
            print(error_message)
            return "Service is down. Please try again later."
        except Exception as e:
            error_message = f"Some error occurred: {e}"
            print(error_message)
            return "Some error occurred. Sorry, Sir."

def chat(query):
    global chatStr
    chatStr += f"Aman: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"].strip()
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return error_message

def ai(prompt):
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        text += response_text
    except Exception as e:
        response_text = f"\nError: {e}"
        text += response_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    with open(filename, "w") as f:
        f.write(text)

    return response_text

if __name__ == '__main__':
    print('Starting Jarvis...')
    speak("Hello, I am Jarvis AI")
    sites = [
        ["youtube", "https://youtube.com"],
        ["google", "https://google.com"],
        ["amazon", "https://amazon.com"],
        ["netflix", "https://www.netflix.com/in/"]
    ]

    while True:
        query = takeCommand().lower()

        # Open websites
        if any(f"open {site[0]}" in query for site in sites):
            for site in sites:
                if f"open {site[0]}" in query:
                    speak(f"Opening {site[0]}, Sir...")
                    webbrowser.open(site[1])
                    break

        # Play music
        elif "open music" in query:
            musicPath = "C:\\Users\\adity\\Downloads\\DJ FKU - DELTA [NCS Release].mp3"
            speak("Playing music, Sir...")
            os.startfile(musicPath)

        # Tell the time
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strfTime}")

        # Open camera
        elif "open camera" in query:
            cameraPath = "C:\\Users\\adity\\OneDrive\\Desktop\\Camera.lnk"
            speak("Opening camera, Sir...")
            os.startfile(cameraPath)

        # AI responses
        elif "using artificial intelligence" in query:
            response_text = ai(prompt=query)
            speak("Generating AI response, Sir. Please check the Openai folder for the output.")

        # Quit Jarvis
        elif "jarvis quit" in query:
            speak("Goodbye, Sir.")
            exit()

        # Reset chat
        elif "reset chat" in query:
            chatStr = ""

        # Control Chrome with PyAutoGUI
        elif 'open chrome' in query:
            os.startfile("C:\\Users\\Public\\Desktop\\Google Chrome.lnk")
        elif 'maximize this window' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('x')
        elif 'google search' in query:
            query = query.replace("google search", "")
            pyautogui.hotkey('alt', 'd')
            pyautogui.write(f"{query}", interval=0.1)
            pyautogui.press('enter')
        elif 'youtube search' in query:
            query = query.replace("youtube search", "")
            pyautogui.hotkey('alt', 'd')
            time.sleep(1)
            pyautogui.press('tab', presses=4, interval=0.1)
            pyautogui.write(f"{query}", interval=0.1)
            pyautogui.press('enter')
        elif 'open new window' in query:
            pyautogui.hotkey('ctrl', 'n')
        elif 'open incognito window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
        elif 'minimize this window' in query:
            pyautogui.hotkey('alt', 'space')
            time.sleep(1)
            pyautogui.press('n')
        elif 'open history' in query:
            pyautogui.hotkey('ctrl', 'h')
        elif 'open downloads' in query:
            pyautogui.hotkey('ctrl', 'j')
        elif 'previous tab' in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        elif 'next tab' in query:
            pyautogui.hotkey('ctrl', 'tab')
        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')
        elif 'close window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'w')
        elif 'clear browsing history' in query:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")

        else:
            response = chat(query)
            speak(response)
