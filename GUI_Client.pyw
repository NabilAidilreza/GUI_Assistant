from threading import Thread
from socket import *
import PySimpleGUI as sg
import threading
import os
import BackendManager
from SystemInfo import getPCInfo
from FileHandler import readFile
lock = threading.Lock()
## Initialization ##
sg.theme('DarkBlue2')
voice_input_status = 'Off'
PC_INFO = getPCInfo()
layout = [[sg.Text(f"{PC_INFO}",size=(40,10)),sg.VerticalSeparator(pad=None),sg.Text(
"Local Commands \n\
1. open, \n\
2. create, \n\
3. move \n\
Global Commands \n\
1. search \n\
2. get \n\
General Commands \n\
1. exit | escape \n\
2. help \n",size=(15,10))],
          [sg.Text("Enter a command:"),sg.Input(size=(30,1),do_not_clear=False),sg.Button('Enter',key="__ENTER__")],
          [sg.Text("Input:"),sg.Text(size=(25,1),key="_INPUT_")],
          [sg.Text("Output: ")],
          [sg.Text(size=(50,3), key='_OUTPUT_')],
          [sg.Text("Voice Settings")],
          [sg.Text('Voice Input: '),sg.Button('Voice On'),sg.Button('Voice Off')],
          [sg.Text('Voice Status: '+voice_input_status,key='_VOICE_')],
          [sg.Text(size=(20,1))],
          [sg.Button('Restart'), sg.Button('Quit'), sg.Button("Help")]]

window = sg.Window('DesktopHelper', layout,size=(500, 500))


def client():
    ### CILENT ###
    global t1
    global TEST
    global window
    # Start Up Cilent Socket #
    cilent_socket = socket()
    cilent_socket.connect(('127.0.0.1',12345))

    print('[ GUI AI Client ] \n')
    print('Successfully linked to PC Assistant Server \n')


    while True:
        lock.acquire()
        ## RECEIVING ##
        data = b''
        while b'\n' not in data:
            data += cilent_socket.recv(1024)
        received = data.decode().strip()
        lock.release() 
        ### SOCKET ###
        ## SENDING ##
        
        if received == "INPUT":
            TEST.resetCommand()
            #TEST.setClear()
            while TEST.getCommand() == "":
                pass
            cilent_socket.sendall(str(TEST.getCommand()).encode() + b'\n')
        elif received == "END":
            break
        elif "ENDCOMMAND" in received:
            received = received.replace("ENDCOMMAND","")
            TEST.setReply(received)
        else:
            TEST.setReply(received)
            TEST.resetCommand()
            while TEST.getCommand() == "":
                pass
            cilent_socket.sendall(str(TEST.getCommand()).encode() + b'\n')


    cilent_socket.close()
    print("CLIENT CLOSED")

class GUI:
    def __init__(self,command):
        self.command = ''
        self.reply = ''
    def getCommand(self):
        return self.command
    def resetCommand(self):
        self.command = ''
    def setReply(self,a):
        global window
        self.reply = a
        window['_OUTPUT_'].update(a)
    def setClear(self):
        global window
        window['_OUTPUT_'].update("")
    def gui(self):
        global window
        global voice_input_status
        key_state = 0
        while True:
            ## GUI ##
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                window.close()
                break
            if event == "Restart":
                os.startfile (r"C:\Users\School\Desktop\PCHelper.bat")
                window.close()
                break
            if event == 'Help':
                sg.popup_ok(readFile('help.txt'),title="Help")
            # Voice Enable #
            if event == 'Voice On':
                voice_input_status = 'On'
            if event == 'Voice Off':
                voice_input_status = 'Off'
            self.command = values[1]
            ## DISPLAY ##
            window['_VOICE_'].update('Voice Status: ' + voice_input_status)
            window['_INPUT_'].update(self.command)
        BackendManager.relevant_windows(BackendManager.close)
TEST = GUI('')
t1 = Thread(target = client)
t2 = Thread(target = TEST.gui)

t1.start()
t2.start()


    
