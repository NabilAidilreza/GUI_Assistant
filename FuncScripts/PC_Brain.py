import os
import subprocess
import shutil

import datetime
from time import ctime,sleep

from selenium import webdriver

from gtts import gTTS # google text to speech

import urllib.request
import urllib.parse
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import requests
import webbrowser

import pyttsx3
import playsound # to play saved mp3 file 
import speech_recognition as sr

#engine = pyttsx3.init()
curr_vid_url = ''

### AI SPEECH ###

##def record(ask = False):
##    listener = sr.Recognizer()
##    voice_data = ''
##    with sr.Microphone() as source:
##        print("Listening...")
##        listener.pause_threshold = 1
##        listener.adjust_for_ambient_noise(source)
##        audio = listener.listen(source)
##    try:
##        print("Recognizing...")
##        voice_data = listener.recognize_google(audio)
##        keyword = voice_data.lower
##        return keyword
##    except sr.UnknownValueError:
##        respond('Sorry, I did not get that')
##        sleep(1)
##        record(ask)
##    except sr.RequestError:
##        respond('Sorry, my speech service is down')
##        sleep(1)
##        record(ask)
##
##def respond(audio):
##    num=0
##    print(audio)
##    num += 1
##    response=gTTS(text=audio, lang='en')
##    file = str(num)+".mp3"
##    response.save(file)
##    playsound.playsound(file, True)
##    os.remove(file)
##    engine.say(audio)
##    engine.runAndWait()

def process(command):
    # Check if command is None
    if command:
        # Print Input
        command = command.lower()
        #print('Input: ' + str(command))
        # Search Function
        if 'search' in command:
            SEARCH()       
        elif 'open' in command:
            OPEN()
        elif 'create' in command:
            CREATE()
        elif 'move' in command:
            MOVE()
        elif 'exit' in command or 'escape' in command:
            exit()
        else:
            print('ERROR')
    else:
        print('Command not entered.')
        

def SEARCH():
    reply = 'What are you searching for?: '
    search_term = input(reply)
    print('Search Term is: ' + search_term)
    reply = 'On which search engine / site do I search this?: '
    site = str(input(reply)).lower()
    
    print('Processing...')
        
    if 'youtube' in site or 'yt' in site:
        # Search and play first yt video found #
        if len(search_term) == 0:
            return
        word_list = search_term.split()
        reply_string = ''
        if len(word_list) == 1:
            reply_string = word_list[0]
        else:
            reply_string = '+'.join(word_list)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_reply=" + reply_string)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        curr_vid_url = url
        print('Searching for ' + search_term + ' on Youtube \n')
        webbrowser.get().open(url)
        print("Playing first video on search term: " + search_term + ' on YouTube\n')
    else:
        # Search the term on a search engine #
        reply = "Is it a location?(Y/N): "
        answer  = input(reply)
        if answer.upper() == "Y":
            location = search_term
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            print('Here is the location of ' + location)
        else:
            snippet = ''
            if site in ['google','bing','searchencrypt']:
                snippet = 'search?q='
            elif site in ['duckduckgo']:
                snippet = '?q='
            else:
                snippet = 'search?q='
                site = 'google'
            url = f'https://{site}.com/{snippet}' + search_term
            print(f'Searching for ' + search_term + ' on ' + site)
            webbrowser.get().open(url)
            print('Here is what I found for ' + search_term)

def OPEN():
    options = ['website','game']
    print('Options: ')
    for i in range(len(options)):
        print(str(i) + '. ' + options[i])
    reply = 'What would you like to open?: '
    item = input(reply)
    if 'website' in item:
        # Opens first website found #
        ### PYTHON SELENIUM SCRIPT LINK ##
        pass
    if 'game' in item:
        options = ['Steam']
        print('Options: ')
        for i in range(len(options)):
            print(str(i+1) + '. ' + options[i])
        reply = 'What software would you like to open?'
        software = input(reply)
        if 'Genshin Impact' in software or 'game' in software:
            print('Opening chosen software now...')
            os.startfile (r"C:\Program Files\Genshin Impact\launcher.exe")

def CREATE():
    options = ['file','folder']
    print('Options: ')
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    reply = 'What do you want to create?: '
    item = input(reply)
    if 'file' in item:
        reply = 'What is the name of the file?: '
        name = input(reply)
        open(f'{name}.txt','w').close()
        reply = 'What is the file extension? (default:txt): '
        ext = input(reply)
        os.rename(f'{name}.txt',f'{name}.{ext}')
        print('A new file has been created under the same directory')
    if 'folder' in item:
        reply = 'What is the folder name?: '
        name = input(reply)
        curr_dir = os.getcwd()
        #parent_dir = os.path.dirname(curr_dir)
        path = os.path.join(curr_dir,name)
        os.mkdir(path)
        print("A new folder '% s' has been created" % path)

def MOVE():
    options = ['file','folder']
    print('Options: ')
    for i in range(len(options)):
        print(str(i+1) + '. ' + options[i])
    reply = 'What do you want to move?: '
    item = input(reply)
    if 'file' in item:
        reply = 'Name of file?: '
        file_name = input(reply)
        reply = 'Destination folder? (Directory Address C:): '
        dest_folder = input(reply)
        src_folder = os.getcwd()
        shutil.move(src_folder + "\\" + file_name, dest_folder + "\\" + file_name)
    if 'folder' in item:
        reply = 'Source folder? (Directory Address C:): '
        filename = input(reply)
        reply = 'Destination folder? (Directory Address C:): '
        dest_folder = input(reply)
        src_folder = os.getcwd()
        shutil.move(src_folder, dest_folder)

        
def run_assistant():
    while True:
        command = input('Enter a command: ')
        process(command)

print('Booting Up Assistant... \n')
print('Commands \n  \
   Local Commands \n \
      1. open, \n \
      2. create, \n \
      3. move \n \
    Global Commands \n \
      1. search \n \
    ... \n \
... \n')

run_assistant()





