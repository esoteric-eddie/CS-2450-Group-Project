import pg as gui
import UVSim

class SimGUI(gui.window):
    def __init__(self):
        super().__init__("Simple GUI", size=(400,300))
        self.sim = UVSim.UVsim() #Initializes UVSim within GUI window

        self.input_label = gui.Label(self, "Enter text file:")
        self.input_field = gui.TextField(self)
