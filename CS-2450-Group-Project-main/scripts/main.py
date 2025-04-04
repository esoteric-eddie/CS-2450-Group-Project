import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import gui
import tkinter as tk

def main():

    root = tk.Tk()
    # sim = UVSim.UVSim()
    # sim.load_program()
    # sim.execute()
    gui.SimGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()