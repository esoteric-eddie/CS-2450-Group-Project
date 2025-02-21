import tkinter as tk
from src import UVSim

class SimGUI:
    def __init__(self, root):
        self.root = root
        root.title("UVSim")
        self.processor = UVSim.UVSim()

        self.current_operand = None  # Store the operand for READ operation

        # Grid config
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=2)
        root.rowconfigure(5, weight=1)

        """Frames"""
        #frame for file loader (Row 0)
        frame_lf = tk.Frame(root)
        frame_lf.grid(row=0, column=0, sticky='nsew', padx=10)
        frame_lf.columnconfigure(0, weight=1)
        frame_lf.rowconfigure(1, weight=1)

        # Frame for load and run buttons (Row 1)
        frame_btns = tk.Frame(root)
        frame_btns.grid(row=1, column=0, sticky='nsew', padx = 10)
        frame_btns.columnconfigure(0, weight=1)
        frame_btns.rowconfigure(1, weight=1)

        # Frame for PC and Accumulator (Row 2)
        frame_pca = tk.Frame(root)
        frame_pca.grid(row=2, column=0, sticky='nsew', padx=10)
        frame_pca.columnconfigure(0, weight=1)
        frame_pca.rowconfigure(1, weight=1)

        #Frame for Output/Input fields (Row 3)
        frame_inout = tk.Frame(root)
        frame_inout.grid(row=3, column=0, sticky='nsew', padx=10)
        frame_inout.columnconfigure(0, weight=1)
        frame_inout.rowconfigure(1, weight=1)

        # Frame for Enter Button (Row 4)
        frame_enter = tk.Frame(root)
        frame_enter.grid(row=4, column=0, sticky='nsew', padx=10)
        frame_enter.columnconfigure(0, weight=1)
        frame_enter.rowconfigure(1, weight=1)

        """Buttons"""
        # Load Button
        self.load_button = tk.Button(frame_btns, text="Load File", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=5, sticky="e")

        # Run Button
        self.run_btn = tk.Button(frame_btns, text="Run", command=self.run)
        self.run_btn.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Enter Button (Initially Disabled)
        self.enter_btn = tk.Button(frame_enter, text="Enter", command=self.process_user_input, state=tk.DISABLED)
        self.enter_btn.grid(row=0, column=1, padx=5, pady=5)

        """Input/Output Fields"""
        # Input Label (Enter text file)
        self.input_label = tk.Label(frame_lf, text="Enter text file:")
        self.input_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        # Input Field (enter text file)
        self.input_field = tk.Entry(frame_lf, width=35)
        self.input_field.grid(row=0, column=1, padx=4, pady=5, sticky="w")

        # Program Counter Output
        self.pc_label = tk.Label(frame_pca, text="Program Counter:")
        self.pc_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        self.pc_output = tk.Entry(frame_pca, width=10, state='readonly')
        self.pc_output.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Accumulator Output
        self.acc_label = tk.Label(frame_pca, text="Accumulator:")
        self.acc_label.grid(row=0, column=3, padx=(10, 5), pady=5, sticky="w")
        self.acc_output = tk.Entry(frame_pca, width=10, state='readonly')
        self.acc_output.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        # Output Message Field
        self.out_label = tk.Label(frame_inout, text="Output:")
        self.out_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        self.out_output = tk.Entry(frame_inout, width=35, state='readonly')
        self.out_output.grid(row=0, column=1, padx=5, pady=5, sticky="w", columnspan=1)

        # Input field (User input)
        self.out_label = tk.Label(frame_inout, text="Input:")
        self.out_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        self.input_val = tk.Entry(frame_inout, width=35)
        self.input_val.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.input_val.bind("<Return>", self.process_user_input)  # Bind Enter key

        """Memory List Box"""
        # Memory locations
        self.memory_label = tk.Label(root, text="Memory:")
        self.memory_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.memory_frame = tk.Frame(root)
        self.memory_frame.grid(row=1, column=1, rowspan=6, padx=15, pady=5, sticky="nsew")

        self.memory_listbox = tk.Listbox(self.memory_frame, width=15, height=10)
        self.memory_scroll = tk.Scrollbar(self.memory_frame, orient=tk.VERTICAL)

        self.memory_listbox.config(yscrollcommand=self.memory_scroll.set)
        self.memory_scroll.config(command=self.memory_listbox.yview)

        self.memory_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.memory_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Double click to edit
        self.memory_listbox.bind("<Double-Button-1>", self.edit_memory)

        # Load memory on start
        self.load_memory()

        # Bind Enter Key to process_user_input
        self.input_val.bind("<Return>", self.process_user_input)  # Bind Enter key to input processing


    # Method to find a file and load it into UVSim.py
    def load_file(self):
        """ Resets UVSim and loads a new program from the selected file. """
        file = self.input_field.get().strip()

        if not file:
            self.update_output("No file name entered.")
            return

        try:
            # Reset the UVSim instance
            self.processor = UVSim.UVSim()  # Create a fresh UVSim instance

            # Load new program into memory
            self.processor.load_program(file)

            # Reset UI fields
            self.update_pc()
            self.update_accumulator()
            self.load_memory()
            self.update_output(f"Program loaded successfully.")

            # Disable input field and Enter button
            self.input_val.config(state=tk.DISABLED)
            self.enter_btn.config(state=tk.DISABLED)
            self.input_val.delete(0, tk.END)  # Clear input box

        except FileNotFoundError:
            self.update_output("Error: File not found.")
        except Exception as e:
            self.update_output(f"Error: {str(e)}")

    # Methods to update UI as processing is occurring
    def update_pc(self):
        """ Updates the program counter display in the UI. """
        self.pc_output.config(state='normal')
        self.pc_output.delete(0, tk.END)
        self.pc_output.insert(0, str(self.processor.program_counter))
        self.pc_output.config(state='readonly')
        self.root.update_idletasks()  # Ensure immediate UI refresh

    def update_accumulator(self):
        """ Updates the accumulator display in the UI. """
        self.acc_output.config(state='normal')
        self.acc_output.delete(0, tk.END)
        self.acc_output.insert(0, str(self.processor.accumulator))
        self.acc_output.config(state='readonly')
        self.root.update_idletasks()  # Ensure immediate UI refresh

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
        """Starts execution step by step, ensuring UI updates correctly"""
        try:
            self.processor.execute(input_callback=self.handle_read_instruction, step_mode=True)
            self.update_pc()
            self.update_accumulator()
            self.load_memory()

            # Stop execution if HALT is reached or program is empty
            if self.processor.memory[self.processor.program_counter] == 4300 or self.processor.program_counter > 98:
                self.update_output("Execution completed.")
                return

            # Check if the next instruction is READ (10XX)
            next_instruction = self.processor.memory[self.processor.program_counter] // 100
            if next_instruction == 10:  # If next instruction is READ, wait for user input
                return  # Stop execution until input is provided

            # Continue executing after a short delay
            self.update_output("Executing next instruction...")
            self.root.after(500, self.run)

        except Exception as e:
            self.update_output(f"Execution Error: {str(e)}")

    def process_user_input(self, event=None):
        """Processes user input and resumes execution"""
        user_input = self.input_val.get().strip()

        if not user_input.isdigit() or len(user_input) != 4:
            self.update_output("Invalid input! Enter a four-digit number.")
            return

        self.processor.memory[self.current_operand] = int(user_input)  # Store input in memory
        self.update_output(f"Stored {user_input} at memory[{self.current_operand}]. Resuming execution...")

        # Disable input field and button
        self.input_val.config(state=tk.DISABLED)
        self.enter_btn.config(state=tk.DISABLED)

        # Resume execution from the next instruction
        self.processor.program_counter += 1
        self.run()  # Continue execution

    def handle_read_instruction(self, operand):
        """Handles READ instruction by enabling input and pausing execution"""
        self.current_operand = operand
        self.update_output(f"Enter a 4-digit number for memory[{operand}]:")

        # Enable input field and button
        self.input_val.config(state=tk.NORMAL)
        self.enter_btn.config(state=tk.NORMAL)
        self.input_val.delete(0, tk.END)
        self.input_val.focus_set()  # Focus on input field