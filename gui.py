import tkinter as tk
import UVSim

class SimGUI:
    def __init__(self,root):
        self.root = root
        root.title("UVSim")
        self.processor = UVSim.UVSim()

        # Grid config
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=2)
        root.rowconfigure(5, weight=1)

        # Input Field (File Name)
        self.input_label = tk.Label(root, text="Enter text file:")
        self.input_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        self.input_field = tk.Entry(root, width=40)
        self.input_field.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Load Button (Keep in column 2)
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.grid(row=1, column=1, padx=10, pady=5)

        # Program Counter Output
        self.pc_label = tk.Label(root, text="Program Counter:")
        self.pc_label.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="w")

        self.pc_output = tk.Entry(root, width=30, state='readonly')
        self.pc_output.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Accumulator Output
        self.acc_label = tk.Label(root, text="Accumulator:")
        self.acc_label.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="w")

        self.acc_output = tk.Entry(root, width=30, state='readonly')
        self.acc_output.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Output Message
        self.out_label = tk.Label(root, text="Output:")
        self.out_label.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="w")

        self.out_output = tk.Entry(root, width=40, state='readonly')
        self.out_output.grid(row=4, column=1, padx=5, pady=5, sticky="w", columnspan=1)
        

        #User input value
        self.input_entry = tk.Label(root, text="Input:")
        self.input_entry.grid(row=5, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.input_val = tk.Entry(root, width=40)
        self.input_val.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Run button
        self.run_btn = tk.Button(root, text="Run", command=self.run)
        self.run_btn.grid(row=6, column=1, padx=10, pady=5)
        
        # Memory locations
        self.memory_label = tk.Label(root, text="Memory:")
        self.memory_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.memory_frame = tk.Frame(root)
        self.memory_frame.grid(row=1, column=2, rowspan=6, padx=15, pady=5, sticky="nsew")

        self.memory_listbox = tk.Listbox(self.memory_frame, width=50, height=10)
        self.memory_scroll = tk.Scrollbar(self.memory_frame, orient=tk.VERTICAL)

        self.memory_listbox.config(yscrollcommand=self.memory_scroll.set)
        self.memory_scroll.config(command=self.memory_listbox.yview)

        self.memory_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.memory_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Double click to edit
        self.memory_listbox.bind("<Double-Button-1>", self.edit_memory)

        # Load memory on start
        self.load_memory()
        
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
                self.load_memory()

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

    def load_memory(self):
        """ Load memory into listbox """
        self.memory_listbox.delete(0, tk.END)
        for index, value in enumerate(self.processor.memory):
            self.memory_listbox.insert(tk.END, f"{index:02}: {value}")

    def edit_memory(self, event):
        """ Edit memory on double click """
        selected_index = self.memory_listbox.curselection()
        if not selected_index:
            return
        
        index = selected_index[0]
        old_value = self.processor.memory[index]

        # Popup window for edit
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Memory")

        tk.Label(edit_window, text=f"Edit memory at location {index}:").grid(row=0, column=0, padx=10, pady=5)
        entry = tk.Entry(edit_window)
        entry.insert(0, str(old_value))
        entry.grid(row=0, column=1, padx=10, pady=5)

        def save_memory():
            try:
                new_value = int(entry.get())
                if -9999 <= new_value <= 9999:
                    self.processor.memory[index] = new_value
                    self.load_memory()
                    edit_window.destroy()
                else:
                    tk.Label(edit_window, text="Invalid value", fg="red").grid(row=1, column=1, padx=10, pady=5)
            except ValueError:
                tk.Label(edit_window, text="Enter a valid integer", fg="red").grid(row=1, column=1, padx=10, pady=5)

        save_button = tk.Button(edit_window, text="Save", command=save_memory)
        save_button.grid(row=2, column=1, padx=10, pady=5)

    def run(self):
        """Execute the loaded program and update GUI."""
        try:
            self.processor.execute()  # Run the simulation
            self.update_pc()  # Update program counter in UI
            self.update_accumulator()  # Update accumulator in UI
            self.load_memory()  # Refresh memory listbox
            self.update_output("Execution completed.")
        except Exception as e:
            self.update_output(f"Execution Error: {str(e)}")

    

        
