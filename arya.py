#TODO: figure out how to open command line as administrator for "execute a command" task
#TODO: add email sending
#TODO: move tasks to seperate file, call functions as needed in main
#TODO: add calendar-keeping
#TODO: add shut down computer
#TODO: add YouTube searches

import speech_recognition
import time 
import random
import webbrowser
from gtts import gTTS 
import playsound 
import os
import subprocess as sp
from subprocess import call
from twilio.rest import Client
from bs4 import BeautifulSoup
import requests
import mysql.connector

def arya_voice(voice): #translates string into arya's voice, saves to mp3, plays mp3, deletes mp3
    tts = gTTS(text=voice, lang ='en')
    mp3 = 'arya.mp3'
    tts.save(mp3)
    playsound.playsound(mp3)
    print(voice)
    os.remove(mp3)

def get_speech(): #gets user input, converts to string, checks to see if input is valid or if service is offline
    with speech_recognition.Microphone() as source:
        user_input = speech_recognition.Recognizer().listen(source)
        voice = ''
        try:
            voice = speech_recognition.Recognizer().recognize_google(user_input)
        except speech_recognition.UnknownValueError:
            arya_voice('Sorry, I didn\'t get that.')
        except speech_recognition.RequestError:
            arya_voice('Sorry, it seems as though I am offline.')
        return voice

def arya_tasks(voice): #all of arya's functionality
    if 'what is your name' in voice or 'what\'s your name' in voice:
        arya_voice('My name is Arya')
    elif 'Aria what time is it' in voice:
        time.ctime()
        arya_voice('The current time is ' + str(time.strftime('%I %M%p %Z')))
    elif 'Aria what is the date' in voice:
        arya_voice('The current date is ' + str(time.strftime('%B %d %Y')))
    elif 'Aria search' in voice:
        arya_voice('What would you like to search for?')
        search = get_speech()
        webbrowser.get().open('https://google.com/search?q=' + search)
        arya_voice('Sure thing. Here is what I found for ' + search)
    elif 'Aria find location' in voice:
        arya_voice('Okay. Please specify a location')
        location = get_speech()
        webbrowser.get().open('https://www.google.com/maps/search/' + location)
        arya_voice('Sure thing. Locating ' + location)
    elif 'Aria execute a command' in voice:
        arya_voice('What command would you like to execute?')
        command = get_speech()
        if 'ipconfig' in command:
            os.system('start cmd /k ipconfig')
        elif 'netstat' in command:
            os.system('start cmd /k netstat')
        elif 'traceroute' in command:
            os.system('start cmd /k tracert')
        elif 'ping' in command:
            arya_voice('What destination would you like to ping?')
            destination = get_speech()
            print(destination)
            os.system('start cmd /k ping ' + destination.replace(' ', ''))
        elif 'driver query' in command:
            os.system('start cmd /k driverquery')
        elif 'task list' in command:
            os.system('start cmd /k tasklist')
        elif 'taskkill' in command:
            arya_voice('Okay. Do you want to kill the task based off of the process ID or image name?')
            dec = get_speech()
            if dec == 'process ID':
                arya_voice('Please give me the process ID')
                pid = get_speech()
                os.system('start cmd /k taskkill -pid ' + pid)
            elif dec == 'image name':
                arya_voice('Please give me the image name')
                img_name = get_speech()
                os.system('start cmd /k taskkill -im ' + img_name)
        elif 'system info' in command:
            os.system('start cmd /k systeminfo')
    elif 'Aria text my phone' in voice:
        arya_voice('Will do. What would you like it to say?')
        account_sid = '*************************'
        auth_token = '**************************'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+13343784883',
            body=get_speech(),
            to='+17066768585'
        )
        arya_voice('Text successfully sent. What would you like me to do now?')
    elif 'Aria let\'s play a number guessing game' in voice:
        arya_voice('Okay. Lets do it. You\'re going down! Pick a number between 1 and 20. You get 5 tries.')
        num = random.randint(1, 20)
        tries = 0
        while tries < 5:
            guess = get_speech()
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
    elif 'Aria translate a word to Pig Latin' in voice:
        arya_voice('Sure. What is the word?')
        word = get_speech()
        new_word = word[1:] + word[0] + 'ay'
        arya_voice(word +' in pig latin is ' + new_word)
    elif 'Aria look up a stock price' in voice:
        stock_scrape()
        while True:
            arya_voice('Do you want to lookup another ticker? Yes or no.')
            decision = get_speech()
            if 'yes' in decision:
                stock_scrape()
            else:
                arya_voice('Okay. What would you like me to do now?')
                break
    elif 'Aria enter test result' in voice:
        quality_db()
        arya_voice('The test result has been sent to the database.')
    elif 'Aria exit' in voice:
        arya_voice('Goodbye.')
        exit()
    
def stock_scrape():
    arya_voice('What ticker do you want me to find?')
    ticker = get_speech().replace(' ', '')
    url = 'https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser' )
    stock_price = soup.find('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}, {'data-reactid':'50'}).text
    dollar = stock_price[:-3]
    cents = stock_price[-2:]
    arya_voice('The current price of ' + ticker + ' is ' + dollar + " dollars and " + cents + " cents.")

def quality_db():
    arya_voice('Sure. Please give me a roll number.')
    roll = (int(get_speech().replace(' ', '')))
    arya_voice('Now give me a style number')
    style = (int(get_speech().replace(' ', '')))
    arya_voice('Now give me a color number')
    color = (int(get_speech().replace(' ', '')))
    arya_voice('What test was conducted?')
    test = get_speech()
    arya_voice('Did the test pass or fail?')
    result = get_speech()
    db = mysql.connector.connect(host='localhost', user='root', password='***********', database='testdatabase')
    cursor = db.cursor()
    sql = 'INSERT INTO qualitytest (RollNum, StyleNum, ColorNum, TestType, PassFail) VALUES (%s,%s,%s,%s,%s)'
    args = (roll, style, color, test, result)
    cursor.execute(sql, args)
    db.commit()
    return


arya_voice('Hey! What can I do for you?')
while True: #loops program
    voice = get_speech()
    print(voice)            #used for debugging
    arya_tasks(voice)
