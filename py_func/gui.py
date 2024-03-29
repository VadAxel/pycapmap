########################################
# imports
########################################

import PySimpleGUI as sg
import os
from . import settings

########################################
# func
########################################

def start_graphic():
    
    sg.theme("DarkBlue14")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_directory,'..','images', 'logo.png')

    startup_layout = [
        [sg.Push(), sg.Image(logo_path), sg.Push()],
        [sg.Push(), sg.Text("Welcome to pycapmap!", font=("Helvetica", 30), text_color="white"), sg.Push()],
        [sg.Push(), sg.Button("Start - Plain", size=(14, 2), font=("Helvetica", 14, "bold")),sg.Button("Start - Extensive", size=(14, 2), font=("Helvetica", 14, "bold")), sg.Push()],
        [sg.Push(), sg.Button("Exit", size=(14, 2), font=("Helvetica", 14, "bold")), sg.Push()]
    ]
    screen_width, screen_height = sg.Window.get_screen_size()
    startup_window = sg.Window("pycapmap - Welcome", startup_layout, finalize=True,location=(0, 0), size=(screen_width, screen_height))    

    while True:
        startup_event, startup_values = startup_window.read()

        if startup_event == sg.WIN_CLOSED or startup_event == "Exit":
            exit()

        elif startup_event == "Start - Extensive":
            settings.extensive = True
            startup_window.close()
            break

        elif startup_event == "Start - Plain":
            startup_window.close()
            break