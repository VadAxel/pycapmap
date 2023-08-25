########################################
# imports
########################################

import tkinter as tk
from tkinter import filedialog
import pyshark
import PySimpleGUI as sg
from .gui import *

########################################
# func
########################################

def choose_pcap_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[('PCAP files', '*.pcap'), ('All files', '*.*')],
        title='Choose a PCAP file'
    )

    return file_path

start_graphic()

capture = pyshark.FileCapture(choose_pcap_file(), display_filter='')


