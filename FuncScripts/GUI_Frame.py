import PySimpleGUI as sg
import wikipedia

## Initialization ##
sg.theme('DarkBlue2')
voice_input_status = 'On'
reply = ''
layout = [[sg.Text('Voice Input: '),sg.Button('Voice On'),sg.Button('Voice Off')],
          [sg.Text('Voice Status: '+voice_input_status,key='_VOICE_')],
          [sg.Text("Enter a command:"),sg.Input(),sg.Button('Enter')],
          [sg.Text("Input:"),sg.Text(size=(25,1),key="_INPUT_")],
          [sg.Text("Output: ")],
          [sg.Text(size=(25,3), key='_OUTPUT_')],
          [sg.Button('Restart'), sg.Button('Quit')]]

window = sg.Window('DesktopHelper', layout)


################################################################################# GUI ###################################################################################

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        window.close()
        break
    if event == 'Restart':
        window.close()
        break
    # Voice Enable #
    if event == 'Voice On':
        voice_input_status = 'On'
    if event == 'Voice Off':
        voice_input_status = 'Off'

    ## DISPLAY ##
    window['_VOICE_'].update('Voice Status: ' + voice_input_status)
    window['_OUTPUT_'].update(reply)
    window['_INPUT_'].update(values[0])
##import PySimpleGUI as sg
##
### ----------- Create the 3 layouts this Window will display -----------
##layout1 = [[sg.Text('This is layout 1 - It is all Checkboxes')],
##           *[[sg.CB(f'Checkbox {i}')] for i in range(5)]]
##
##layout2 = [[sg.Text('This is layout 2')],
##           [sg.Input(key='-IN-')],
##           [sg.Input(key='-IN2-')]]
##
##layout3 = [[sg.Text('This is layout 3 - It is all Radio Buttons')],
##           *[[sg.R(f'Radio {i}', 1)] for i in range(8)]]
##
### ----------- Create actual layout using Columns and a row of Buttons
##layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
##          [sg.Button('Cycle Layout'), sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('Exit')]]
##
##window = sg.Window('Swapping the contents of a window', layout)
##
##layout = 1  # The currently visible layout
##while True:
##    event, values = window.read()
##    print(event, values)
##    if event in (None, 'Exit'):
##        break
##    if event == 'Cycle Layout':
##        window[f'-COL{layout}-'].update(visible=False)
##        layout = layout + 1 if layout < 3 else 1
##        window[f'-COL{layout}-'].update(visible=True)
##    elif event in '123':
##        window[f'-COL{layout}-'].update(visible=False)
##        layout = int(event)
##        window[f'-COL{layout}-'].update(visible=True)
##window.close()
