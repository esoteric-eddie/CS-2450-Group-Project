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

    def load_file(self):
        """ Opens file dialog, sends file to Processor, and updates UI """
        filename = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text Files", "*.txt")])

        if filename:
            success = self.processor.load_file(filename)  # Load file via processor

            if success:
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, filename)

                # Update UI fields
                self.update_ui()
            else:
                self.out_output.config(state='normal')
                self.out_output.delete(0, tk.END)
                self.out_output.insert(0, "Error loading file")
                self.out_output.config(state='readonly')

    """ def update_ui(self):
         '''Updates all output fields with processor data '''
        self.pc_output.config(state='normal')
        self.pc_output.delete(0, tk.END)
        self.pc_output.insert(0, str(self.processor.get_pc()))
        self.pc_output.config(state='readonly')

        self.acc_output.config(state='normal')
        self.acc_output.delete(0, tk.END)
        self.acc_output.insert(0, str(self.processor.get_acc()))
        self.acc_output.config(state='readonly')

        self.out_output.config(state='normal')
        self.out_output.delete(0, tk.END)
        self.out_output.insert(0, self.processor.get_output())
        self.out_output.config(state='readonly')  """
        
        