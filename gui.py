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

        #User input value - needs an event added to it. 
        self.input_entry = tk.Label(root, text="Input:")
        self.input_entry.grid(row=4, column=0, padx=10, pady=5)
        self.input_val = tk.Entry(root, width=40)
        self.input_val.grid(row=4, column=1, padx=10, pady=5)
        
    # Method to find a file and load it into UVSim.py
    def load_file(self):
            """ Load inputed file into UVSim and update fields """
            file = self.input_field.get().strip()

            if not file:
                self.update_output("No file name entered.")
                return

            try:
                self.processor.load_program(file)

                # Update GUI fields
                self.update_pc()
                self.update_accumulator()
                self.update_output(f"Program loaded successfully.")

            except FileNotFoundError:
                self.update_output("Error: File not found.")
            except Exception as e:
                self.update_output(f"Error: {str(e)}")

    # Methods to update UI as processing is occuring
    def update_pc(self):
        """ Update the program counter field in GUI """
        self.pc_output.config(state='normal')
        self.pc_output.delete(0, tk.END)
        self.pc_output.insert(0, str(self.processor.program_counter))
        self.pc_output.config(state='readonly')

    def update_accumulator(self):
        """ Update the accumulator field in GUI """
        self.acc_output.config(state='normal')
        self.acc_output.delete(0, tk.END)
        self.acc_output.insert(0, str(self.processor.accumulator))
        self.acc_output.config(state='readonly')

    def update_output(self, message):
        """ Update the output message field in GUI """
        self.out_output.config(state='normal')
        self.out_output.delete(0, tk.END)
        self.out_output.insert(0, message)
        self.out_output.config(state='readonly')
        
        
