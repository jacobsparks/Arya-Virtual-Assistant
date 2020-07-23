import speech_recognition as sr #Use to get user speech
import time 
import random #Use for mp3_file string & num guessing game
import webbrowser
from gtts import gTTS #Use to turn string into voice
import playsound #use to play mp3_file
import os #Use to exit program
import subprocess as sp #Use for command line prompts
from twilio.rest import Client #Use to send texts 

def get_user_speech():
    with sr.Microphone() as source: 
        audio = sr.Recognizer().listen(source) 
        voice = ''
        try:
            voice = sr.Recognizer().recognize_google(audio) 
        except sr.UnknownValueError:
            arya_voice('Sorry, I didn\'t get that.')
        except sr.RequestError:
            arya_voice('Sorry, it seems as though I am offline.')
        return voice


def arya_voice(voice):
    tts = gTTS(text=voice, lang ='en')
    mp3_file = 'arya-' + str(random.randint(1,1000)) + '.mp3'
    tts.save(mp3_file)
    playsound.playsound(mp3_file)
    print(voice)
    os.remove(mp3_file)

def arya_tasks(voice):
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
    if 'Aria run command ipconfig' in voice:
        arya_voice('Running ipconfig')
        os.system('start cmd /k ipconfig')
    if 'Aria text my phone' in voice:
        arya_voice('Will do. What would you like it to say?')
        account_sid = '********************'
        auth_token = '************************'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+13343784883',
            body=get_user_speech(),
            to='************'
        )
        arya_voice('Text successfully sent. What would you like me to do now?')
    if 'Aria let\'s play a number guessing game' in voice:
        arya_voice('Okay. Lets do it. You\'re going down! Pick a number between 1 and 20. You get 5 tries.')
        num = random.randint(1, 20)
        tries = 0
        while tries < 5:
            guess = get_user_speech()
            tries = tries + 1
            if int(guess) > num:
                arya_voice('Nope. Too high.')
            elif int(guess) < num:
                arya_voice('Nope. Too low.')
            else:
                break
        if int(guess) == num:
            arya_voice('Congrats. You win. What else can I do for you?')
        else:
            arya_voice('You\'ve tried too many times. You lose! What else can I do for you?')
    if 'Aria exit' in voice:
        arya_voice('Goodbye.')
        exit()

arya_voice('Hey! What can I do for you?')
while True:
    voice = get_user_speech()
    arya_response(voice)
