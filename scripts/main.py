from src import UVSim
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