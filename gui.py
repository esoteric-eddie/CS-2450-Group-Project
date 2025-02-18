import tkinter as tk
import UVSim

class SimGUI:
    def __init__(self,master):
        self.master = master
        master.title("UVSim")

        self.label = tk.Label(master, text="Test!")
        self.label.pack()

        self.close_button = tk.Button(master, text="close", command=master.quit)
        self.close_button.pack

        
        