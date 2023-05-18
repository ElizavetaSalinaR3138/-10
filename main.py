import time
import pyttsx3
import requests
import speech_recognition as sr
import webbrowser
from speech_recognition import UnknownValueError

engine = pyttsx3.init()
newVoiceRate = 130

voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)

rec = sr.Recognizer()

def welcome_speech():
    engine.say('Hello, I am a voice assistant.')
    engine.say('I can give you some information on almost any words.')
    engine.runAndWait()

def listen_():
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source)
        print('Listening to you...')
        voice = rec.listen(source)
        try:
            time.sleep(1.5)
            command = rec.recognize_google(voice, language="en-GB")
            return command
        except UnknownValueError:
            talk_("Could not recognize your speech.")
            return 'Request error'

def talk_(say):
    engine.say(say)
    engine.runAndWait()

def commands():
    talk_('I can give you the meaning, pronunciation,'
         ' transcription or  an example or open the source webpage')
    talk_('What do you want?')
    try:
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
            print('Waiting for the command...')
            voice = rec.listen(source)
            try:
                time.sleep(1.5)
                command = rec.recognize_google(voice)
                print(command)
            except UnknownValueError:
                command = 'Request error'
        if 'webpage' in command:
            return 1
        if 'pronunciation' in command:
            return 2
        if 'example' in command:
            return 4
        if 'transcription' in command:
            return 5
        if 'Request error' in command:
            return 10
    except:
        pass

def Voice_assistent(request_):
    url = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + rqst)
    s = url.json()
    iss = commands()
    match iss:
        case 5:
            if s[0].get('phonetic') != "None":
                print('phonetic : %s' % s[0].get('phonetic'))
            else:
                talk_('This information is not available.')
        case 2:
            if s[0].get('phonetics')[0].get('audio') != 'None':
                webbrowser.open_new_tab((s[0].get('phonetics')[0]).get('audio'))
            else:
                talk_('I can\'t find pronunciation recording')
        case 1:
            try:
                webbrowser.open_new_tab(s[0].get('sourceUrls')[0])
            except:
                talk_('I  can\'t find source URL')
        case 4:
            if s[0].get('meanings')[0].get('definitions')[0].get('example') != 'None':
                print('example : %s' % s[0].get('meanings')[0].get('definitions')[0].get('example'))
            else:
                talk_('I  don\'t have an example')
        case _:
            talk_('Request error, please try again')

request_ = ''
welcome_speech()

while True:
    speech = listen_()
    print(speech)
    if 'find a' in speech:
        request_ = speech.split(' ')[-1]
        Voice_assistent(request_)
    elif 'find an' in speech:
        request_ = speech.split(' ')[-1]
        Voice_assistent(request_)
    elif 'exit' in speech:
        quit()
    if request_ == '':
        talk_(f'Did not recognize the word. Please repeat the request again.')
        continue
