import os
import subprocess
import shutil
import win32gui

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



### SERVER ###
from socket import *
from time import *
# Start Up Server Socket #
server_socket = socket()
server_socket.bind(('127.0.0.1',12345))
server_socket.listen()

# Establish Connection With Cilent #
print('Type Ctrl-F6 or close the shell to terminate the server.')
connection_socket, addr = server_socket.accept()
print('Connected to: ' + str(addr))

print('[ PC Assistant Server ] \n')
print('Successfully linked to GUI AI Client \n')

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
            pass
        else:
            connection_socket.sendall(b'WRONG COMMAND' + b'\n')
    else:
        connection_socket.sendall(b'COMMAND NOT SENT' + b'\n')
        
def SEARCH():
    reply = b'What are you searching for?: '
    connection_socket.sendall(reply + b'\n')
    search_term = WaitForReply()
    print('Search Term is: ' + search_term)
    reply = b'On which search engine / site do I search this? (e.g Youtube, Google, etc) '
    connection_socket.sendall(reply + b'\n')
    site = str(WaitForReply()).lower()
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
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + reply_string)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        curr_vid_url = url
        print('Searching for ' + search_term + ' on Youtube \n')
        webbrowser.get().open(url)
        reply = b"Playing first video on search term: " + search_term.encode() + b' on YouTube\n'
        connection_socket.sendall(reply + b" ENDCOMMAND" + b'\n')
    else:
        # Search the term on a search engine #
        reply = b"Is it a location?(Y/N): "
        connection_socket.sendall(reply + b'\n')
        answer = WaitForReply()
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
            reply = b'Here is what I found for ' + search_term.encode()
            connection_socket.sendall(reply + b" ENDCOMMAND" + b'\n')

def OPEN():
    options = ['website','game']
    option_string = ""
    option_string += 'Options: \n'
    for i in range(len(options)):
        option_string += str(i) + '. ' + options[i] + '\n'
    reply = option_string + 'What would you like to open?: '
    connection_socket.sendall(reply.encode() + b'\n')
    item = WaitForReply()
    if 'website' in item:
        # Opens first website found #
        ### PYTHON SELENIUM SCRIPT LINK ##
        pass
    if 'game' in item:
        options = ['Steam']
        option_string = ""
        option_string += 'Options: \n'
        for i in range(len(options)):
            option_string += str(i) + '. ' + options[i] + '\n'
        reply = option_string + 'What software would you like to open?'
        connection_socket.sendall(reply.encode() + b'\n')
        software = WaitForReply()
        if 'Genshin Impact' in software or 'game' in software:
            print('Opening chosen software now...')
            os.startfile (r"C:\Program Files\Genshin Impact\launcher.exe")

def CREATE():
    options = ['file','folder']
    option_string = ""
    option_string += 'Options: \n'
    for i in range(len(options)):
        option_string += str(i) + '. ' + options[i] + '\n'
    reply = option_string + 'What do you want to create?: '
    connection_socket.sendall(reply.encode() + b'\n')
    item = WaitForReply()
    if 'file' in item:
        reply = b'What is the name of the file?: '
        connection_socket.sendall(reply + b'\n')
        name = WaitForReply()
        open(f'{name}.txt','w').close()
        reply = b'What is the file extension? (default:txt): '
        connection_socket.sendall(reply + b'\n')
        ext = WaitForReply()
        os.rename(f'{name}.txt',f'{name}.{ext}')
        print('A new file has been created under the same directory')
    if 'folder' in item:
        reply = b'What is the folder name?: '
        connection_socket.sendall(reply + b'\n')
        name = WaitForReply()
        curr_dir = os.getcwd()
        #parent_dir = os.path.dirname(curr_dir)
        path = os.path.join(curr_dir,name)
        os.mkdir(path)
        print("A new folder '% s' has been created" % path)

def MOVE():
    options = ['file','folder']
    option_string = ""
    option_string += 'Options: \n'
    for i in range(len(options)):
        option_string += str(i) + '. ' + options[i] + '\n'
    reply = option_string + 'What do you want to move?: '
    connection_socket.sendall(reply.encode() + b'\n')
    item = WaitForReply()
    if 'file' in item:
        reply = b'Name of file?: '
        connection_socket.sendall(reply.encode() + b'\n')
        file_name = WaitForReply()
        reply = b'Destination folder? (Directory Address C:): '
        connection_socket.sendall(reply.encode() + b'\n')
        dest_folder = WaitForReply()
        src_folder = os.getcwd()
        shutil.move(src_folder + "\\" + file_name, dest_folder + "\\" + file_name)
    if 'folder' in item:
        reply = b'Source folder? (Directory Address C:): '
        connection_socket.sendall(reply.encode() + b'\n')
        filename = WaitForReply()
        reply = b'Destination folder? (Directory Address C:): '
        connection_socket.sendall(reply.encode() + b'\n')
        dest_folder = WaitForReply()
        src_folder = os.getcwd()
        shutil.move(src_folder, dest_folder)

def WaitForReply():
    data = b''
    while b'\n' not in data:
        data += connection_socket.recv(1024)
    return data.decode().strip()
def PrintWaitSeconds(num):
    for i in range(num,0,-1):
        sleep(1)
        print("Closing in " + str(i) + ' seconds')
### LOOP ###
while True:
    ### SENDING ###
    connection_socket.sendall(b'INPUT' + b'\n')
    print('WAITING FOR REPLY... \n')
    ### RECEIVING ###
    reply = WaitForReply()
    if reply in ['exit','escape']:
        connection_socket.sendall(b'END' + b'\n')
        PrintWaitSeconds(3)
        break
    process(reply)
server_socket.close()
print("SERVER CLOSED")
connection_socket.close()
