import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('espeak')
engine.setProperty('voice', voices[173].id)
engine.setProperty('rate', 150)     # setting up new voice rate
engine.setProperty('volume', 1.0)    # setting up volume level  between 0 and 1

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
 
 
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Bom Dia!")
 
    elif hour>=12 and hour<18:
        speak("Boa Tarde!")   
 
    else:
        speak("Boa Noite!")  
 
    speak("Eu sou o Genius e será um prazer te apoiar. Por favor, me diga como posso ajudar.")       
 
def takeCommand():
    #It takes microphone input from the user and returns string output
 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.pause_threshold = 1
        audio = r.listen(source)
 
    try:
        print("Compreendendo...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
 
    except Exception as e:
        # print(e)    
        print("Diga novamente, por favor...")  
        return "None"
    return query
 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('e-mail', 'yourpassword')  # Use your actual email and password
    # Note: For Gmail, you may need to allow "less secure apps" or use an app password.
    # If you have 2FA enabled, use an app password instead of your regular password.
    # For security, consider using environment variables or a secure vault for credentials.
    server.sendmail('e-mail', to, content)
    server.close()
 
if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
 
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Procurando na Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("De acordo com a Wikipedia")
            print(results)
            speak(results)
 
        elif 'abrir youtube' in query:
            webbrowser.open("youtube.com")
 
        elif 'abrir google' in query:
            webbrowser.open("google.com")
 
        elif 'abrir chatgpt' in query:
            webbrowser.open("chatgpt.com")   
 
 
        elif 'tocar música' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
 
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Brenda, agora são {strTime}")
 
        elif 'open code' in query:
            codePath = r"C:\Users\brend\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(codePath)
 
        elif 'email to friend' in query:
            try:
                speak("O que você gostaria de dizer?")
                content = takeCommand()
                to = "yourfriendEmail@gmail.com"   
                sendEmail(to, content)
                speak("Email enviado!")
            except Exception as e:
                print(e)
                speak("Desculpe. Não consegui enviar esse e-mail.")    
