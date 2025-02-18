import UVSim
import gui

def main():
    sim = UVSim.UVSim()
    #sim.load_program()
    #sim.execute()
    gui.application().run(SimGUI())

if __name__ == '__main__':
    main()
