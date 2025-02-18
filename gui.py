import tkinter as tk
import UVSim

class SimGUI:
    def __init__(self,root):
        self.root = root
        root.title("UVSim")
        self.processor = UVSim.UVSim()

 # Input Field (File Name)
        self.input_label = tk.Label(root, text="Enter text file:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.input_field = tk.Entry(root, width=40)
        self.input_field.grid(row=0, column=1, padx=10, pady=5)

        # Load Button
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.grid(row=0, column=2, padx=10, pady=5)

        # Program Counter Output
        self.pc_label = tk.Label(root, text="Program Counter:")
        self.pc_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.pc_output = tk.Entry(root, width=30, state='readonly')
        self.pc_output.grid(row=1, column=1, padx=10, pady=5)

        # Accumulator Output
        self.acc_label = tk.Label(root, text="Accumulator:")
        self.acc_label.grid(row=2, column=0, padx=10, pady=5)
        
        self.acc_output = tk.Entry(root, width=30, state='readonly')
        self.acc_output.grid(row=2, column=1, padx=10, pady=5)

        # Output Message
        self.out_label = tk.Label(root, text="Output:")
        self.out_label.grid(row=3, column=0, padx=10, pady=5)
        
        self.out_output = tk.Entry(root, width=40, state='readonly')
        self.out_output.grid(row=3, column=1, padx=10, pady=5, columnspan=2)

    #needs a method to find a file and load it into UVSim.py Either call it load_file to be comaptible with the previous code or change my previous code

    #needs a method to update UI as processing is occuring
        
        