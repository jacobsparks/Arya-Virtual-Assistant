import speech_recognition as sr 
import time 
import random
import webbrowser 
from gtts import gTTS 
import playsound 
import os 
import subprocess as sp

def arya_voice(voice):
    tts = gTTS(text=voice, lang ='en')
    mp3_file = 'arya-' + str(random.randint(1,1000)) + '.mp3'
    tts.save(mp3_file)
    playsound.playsound(mp3_file)
    print(voice)
    os.remove(mp3_file)

def get_user_speech():
    with sr.Microphone() as source:
        audio = sr.Recognizer().listen(source)
        voice = ''
        try:
            voice = sr.Recognizer().recognize_google(audio)
        except sr.UnknownValueError:
            arya_voice('Sorry, I didn\'t get that.')
        except sr.RequestError:
            arya_voice('Sorry, my speech service seems to be offline.')
        return voice

def arya_response(voice):
    if 'what is your name' in voice or 'what\'s your name' in voice:
        arya_voice('My name is Arya.')
    if 'Aria what time is it' in voice:
        time.ctime()
        arya_voice('The current time is ' + str(time.strftime('%I %M%p %Z')))
    if 'Aria what is the date' in voice:
        arya_voice('The current date is ' + str(time.strftime('%B %d %Y')))
    if 'Aria search' in voice:
        arya_voice('What would you like to search for?')
        search = get_user_speech()
        webbrowser.get().open('https://google.com/search?q=' + search)
        arya_voice('Sure thing. Here is what I found for ' + search)
    if 'Aria find location' in voice:
        arya_voice('Okay. Please specify a location')
        location = get_user_speech()
        webbrowser.get().open('https://www.google.com/maps/search/' + location)
        arya_voice('Sure thing. Locating ' + location)
    if 'Aria open command ipconfig' in voice:
        arya_voice('Opening ipconfig')
        os.system('start cmd /k ipconfig')
    if 'Aria exit' in voice:
        arya_voice('Goodbye.')
        exit()


arya_voice('What can I do for you?')
while True:
    voice = get_user_speech()
    arya_response(voice)
