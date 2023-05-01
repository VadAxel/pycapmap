########################################
# imports
########################################

import pyshark
import tkinter as tk
from tkinter import filedialog

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

file = choose_pcap_file()

capture = pyshark.FileCapture(file, display_filter='')

