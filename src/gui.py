import tkinter as tk
from tkinter import ttk, colorchooser
import json
import os
from src import UVSim
from tkinter import filedialog

class SimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim")
        self.processor = UVSim.UVSim()

        self.tab_count = 0
        self.tabs = {}  # Track tab frames (by their name): tab name -> dictionary of widgets

        # Grid Config for Notebook
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # New Tab button
        self.new_tab_btn = ttk.Button(self.root, text="New Tab", command=self.add_new_tab, style="BlackText.TButton")
        self.new_tab_btn.grid(row=1, column=0, pady=10)

        # Start with one tab
        self.add_new_tab()

    def choose_color_scheme(self):
        """Opens a color picker for users to select primary and off colors."""
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        if not primary_color:
            return

        off_color = colorchooser.askcolor(title="Choose Off-Color")[1]
        if not off_color:
            return

        self.save_color_scheme(primary_color, off_color)


    def save_color_scheme(self, primary, off_color):
        """Saves the selected colors to a configuration file."""
        self.color_scheme = {"primary": primary, "off_color": off_color}
        with open("color_config.json", "w") as f:
            json.dump(self.color_scheme, f)
        self.apply_color_scheme()

    def load_color_scheme(self):
        """Loads the color scheme from a file or applies the default."""
        default_scheme = {
            "primary": "#4C721D",  # UVU dark green
            "off_color": "#FFFFFF"  # White
        }
        config_path = "color_config.json"

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    self.color_scheme = json.load(f)
            except json.JSONDecodeError:
                self.color_scheme = default_scheme
        else:
            self.color_scheme = default_scheme

        self.apply_color_scheme()

    def apply_color_scheme(self):
        primary = self.color_scheme.get("primary", "#4C721D")
        off_color = self.color_scheme.get("off_color", "#FFFFFF")

        style = ttk.Style()
        style.configure("TButton", background=primary, foreground=off_color)
        style.configure("TFrame", background=primary)
        style.configure("TLabel", background=primary, foreground=off_color)

        self.root.configure(bg=primary)

        # Apply ttk style changes
        style = ttk.Style()
        style.configure("TButton", background=primary, foreground=off_color)
        style.configure("TFrame", background=primary)
        style.configure("TLabel", background=primary, foreground=off_color)

    def browse_file(self):
        """Opens a file dialog and inserts the selected file path into the input field of the active tab."""
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            title="Select a program file",
            filetypes=filetypes,
            initialdir="."
        )

        if filename:
            widgets = self.get_current_tab_widgets()
            input_field = widgets["input_field"]
            input_field.delete(0, tk.END)
            input_field.insert(0, filename)


    # Method to find a file and load it into UVSim.py
    def load_file(self):
        """ Resets UVSim and loads a new program from the selected file (for the current tab). """
        widgets = self.get_current_tab_widgets()
        input_field = widgets["input_field"]
        processor = widgets["processor"]
        input_val = widgets["input_val"]
        enter_btn = widgets["enter_btn"]

        file = input_field.get().strip()

        if not file:
            self.update_output("No file name entered.")
            return

        try:
            # Reset UVSim instance for this tab
            processor = UVSim.UVSim()
            widgets["processor"] = processor

            # Try loading the file (with built-in validation)
            processor.load_program(file)

            # Update UI
            self.load_memory()
            self.update_pc()
            self.update_accumulator()
            self.update_output("Program loaded successfully.")

            input_val.config(state=tk.DISABLED)
            enter_btn.config(state=tk.DISABLED)
            input_val.delete(0, tk.END)

        except FileNotFoundError:
            self.update_output("Error: File not found.")
        except ValueError as ve:
            self.update_output(f"Error: {ve}")
        except Exception as e:
            self.update_output(f"Error: {str(e)}")



    # Methods to update UI as processing is occurring
    def update_pc(self):
        """ Updates the program counter display in the UI (for the current tab) """
        widgets = self.get_current_tab_widgets()
        pc_output = widgets["pc_output"]
        processor = widgets["processor"]

        pc_output.config(state='normal')
        pc_output.delete(0, tk.END)
        pc_output.insert(0, str(processor.program_counter))
        pc_output.config(state='readonly')
        self.root.update_idletasks()  # Ensure immediate UI refresh

    def update_accumulator(self):
        """ Updates the accumulator display in the UI. """
        widgets = self.get_current_tab_widgets()
        acc_output = widgets["acc_output"]
        processor = widgets["processor"]

        acc_output.config(state='normal')
        acc_output.delete(0, tk.END)
        acc_output.insert(0, str(processor.accumulator))
        acc_output.config(state='readonly')
        self.root.update_idletasks()  # Ensure immediate UI refresh

    def update_output(self, message):
        widgets = self.get_current_tab_widgets()
        out_output = widgets["out_output"]

        """ Update the output message field in GUI """
        out_output.config(state='normal')
        out_output.delete(0, tk.END)
        out_output.insert(0, message)
        out_output.config(state='readonly')



    def load_memory(self):
        """ Load memory into listbox (per-tab) """
        widgets = self.get_current_tab_widgets()
        memory_listbox = widgets["memory_listbox"]
        processor = widgets["processor"]

        memory_listbox.delete(0, tk.END)
        for index, value in enumerate(processor.memory):
            str_val = str(value)
            if value < 0:
                # For negative numbers, keep the minus sign and pad the rest
                formatted_value = '-' + str_val[1:].zfill(5)
            else:
                # For positive numbers, pad to 6 digits
                formatted_value = str_val.zfill(6)

            memory_listbox.insert(tk.END, f"{index:02}: {formatted_value}")

    def edit_memory(self, event):
        """ Edit memory on double click """
        widgets = self.get_current_tab_widgets()
        memory_listbox = widgets["memory_listbox"]
        processor = widgets["processor"]

        selected_index = memory_listbox.curselection()
        if not selected_index:
            return

        index = selected_index[0]
        old_value = processor.memory[index]

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
                    processor.memory[index] = new_value
                    self.load_memory()
                    edit_window.destroy()
                else:
                    tk.Label(edit_window, text="Invalid value", fg="red").grid(row=1, column=1, padx=10, pady=5)
            except ValueError:
                tk.Label(edit_window, text="Enter a valid integer", fg="red").grid(row=1, column=1, padx=10, pady=5)

        save_button = tk.Button(edit_window, text="Save", command=save_memory)
        save_button.grid(row=2, column=1, padx=10, pady=5)

    # CUT, COPY, PASTE FUNCTIONALITY
    def show_memory_menu(self, event):
        """ Right-click for menu in memory listbox"""
        try:
            self.memory_menu.post(event.x_root, event.y_root)
        except tk.TclError:
            pass

    def copy_memory(self, event=None):
        """Copy selected values"""
        widgets = self.get_current_tab_widgets()
        memory_listbox = widgets["memory_listbox"]

        selected_rows = memory_listbox.curselection()
        if selected_rows:
            memory_values = []
            for i in selected_rows:
                row_text = memory_listbox.get(i)
                parts = row_text.strip().split(": ")
                if len(parts) == 2:
                    value = parts[1].strip()
                    memory_values.append(value)
            copy_text = "\n".join(memory_values)

            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)
            self.root.update()

    def cut_memory(self):
        """ Cut selected values"""
        widgets = self.get_current_tab_widgets()
        memory_listbox = widgets["memory_listbox"]
        processor = widgets["processor"]

        selected_rows = memory_listbox.curselection()
        if selected_rows:
            # Get values only and put in list with newlines
            memory_values = []
            for i in selected_rows:
                row_text = memory_listbox.get(i)
                value = row_text.split(": ")[1]
                memory_values.append(value)
            copy_text = "\n".join(memory_values)

            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)
            self.root.update()

            # Set cut values to 0
            for i in selected_rows:
                processor.memory[i] = 0
            self.load_memory()

    def paste_memory(self):
        """ Paste clipboard into memory starting from first selected """
        widgets = self.get_current_tab_widgets()
        memory_listbox = widgets["memory_listbox"]
        processor = widgets["processor"]

        selected_rows = memory_listbox.curselection()
        if not selected_rows:
            self.update_output("No memory location selected.")
            return

        try:
            clipboard_text = self.root.clipboard_get().strip()
            new_values = clipboard_text.split("\n")

            # Convert valid numbers from clipboard
            numeric_values = []
            for value in new_values:
                try:
                    num = int(value.strip())
                    if -999999 <= num <= 999999:
                        numeric_values.append(num)
                except ValueError:
                    continue

            if not numeric_values:
                self.update_output("Clipboard contains no valid numbers.")
                return

            # Paste starting at first selected index
            start_index = selected_rows[0]
            for i, num in enumerate(numeric_values):
                memory_index = start_index + i
                if memory_index >= 250: # Stop if out of bounds
                    break
                processor.memory[memory_index] = num

            self.load_memory()  # Refresh UI

        except tk.TclError:
            self.update_output("Clipboard is empty or inaccessible.")


    def run(self):
        widgets = self.get_current_tab_widgets()
        processor = widgets["processor"]

        if processor.halted:
            self.update_output("Execution completed.")
            return

        try:
            processor.execute(input_callback=self.handle_read_instruction, step_mode=True)
            self.update_pc()
            self.update_accumulator()
            self.load_memory()

            if processor.halted:
                self.update_output("Execution completed.")
                return

            # Check next instruction — if it's a READ, stop here and wait for input
            next_instruction = processor.memory[processor.program_counter]
            opcodeHolder = str(next_instruction // 100)
            if int(opcodeHolder[:2]) == 10:
            #if next_instruction // 100 == 10:
                return  # Pause for input — do NOT schedule another self.run()

            self.update_output("Executing next instruction...")
            self.root.after(500, self.run)

        except Exception as e:
            self.update_output(f"Execution Error: {str(e)}")

    def process_user_input(self, event=None):
        widgets = self.get_current_tab_widgets()
        input_val = widgets["input_val"]
        enter_btn = widgets["enter_btn"]
        processor = widgets["processor"]

        """Processes user input and resumes execution"""
        user_input = input_val.get().strip()

        try:
            value = int(user_input)
            if not -999999 <= value <= 999999:
                raise ValueError
        except ValueError:
            self.update_output("Invalid input! Enter a signed six-digit number (e.g., +1234 or -5678).")
            return

        processor.memory[self.current_operand] = int(user_input)    # Store input in memory
        self.update_output(f"Stored {user_input} at memory[{self.current_operand}]. Resuming execution...")

        # Disable input field and button
        input_val.config(state=tk.DISABLED)
        enter_btn.config(state=tk.DISABLED)

        # Resume execution from the next instruction
        processor.program_counter += 1
        self.run()  # Continue execution

    def handle_read_instruction(self, operand):
        """Handles READ instruction by enabling input and pausing execution"""
        widgets = self.get_current_tab_widgets()
        input_val = widgets["input_val"]
        enter_btn = widgets["enter_btn"]

        self.current_operand = operand
        print(f"[GUI] Waiting for user input for memory[{operand}]")
        self.update_output(f"Enter a 6-digit number for memory location {operand}")

        # Enable input field and button
        input_val.config(state=tk.NORMAL)
        enter_btn.config(state=tk.NORMAL)
        input_val.delete(0, tk.END)
        input_val.focus_set()  # Focus on input field

    def convert_file_to_6_digit(self):
        """Calls UVSim to convert a selected legacy file to 6-digit format (for current tab)."""
        widgets = self.get_current_tab_widgets()
        input_field = widgets["input_field"]
        processor = widgets["processor"]

        file = input_field.get().strip()

        if not file:
            self.update_output("No file name entered to convert.")
            return

        try:
            processor.convert_file(file)
            self.update_output("File converted to 6-digit format successfully.")
        except Exception as e:
            self.update_output(f"Conversion Error: {str(e)}")

        self.load_file()

    def add_new_tab(self):
        self.tab_count += 1
        tab_title = f"Tab {self.tab_count}"

        # Create tab frame
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_title)
        # self.tabs[tab_title] = tab_frame  # Keeping track of tab names - prob don't need

        # New tab is seen by user
        self.notebook.select(tab_frame)

        # Customized frame
        self.create_tab(tab_frame, tab_title)

    def get_current_tab_widgets(self):
        tab_id = self.notebook.select()  # get current tab widget ID
        if not tab_id:
            raise Exception("No tab is currently selected.")

        tab_title = self.notebook.tab(tab_id, "text")  # get actual tab title like 'Tab 2'

        if tab_title not in self.tabs:
            raise KeyError(f"Tab title '{tab_title}' not found in self.tabs. Possibly closed.")

        return self.tabs[tab_title]

    def create_tab(self, frame, title):
        style = ttk.Style()
        style.configure("BlackText.TButton", foreground="black")    # Make sure button text is black

        # Frame for close button and color theme button
        frame_close = ttk.Frame(frame)
        frame_close.grid(row=0, column=0, padx=10, pady=0, sticky='nsew')

        # Close button still in outer tab frame
        #ttk.Button(frame_close, text="Close Current Tab", command=lambda: self.notebook.forget(frame), style="BlackText.TButton").grid(row=0, column=0)
        ttk.Button(frame_close, text="Close Current Tab", command=lambda: self.close_tab(frame), style="BlackText.TButton").grid(row=0, column=0)

        # Frame for left side
        frame_main_left = ttk.Frame(frame, padding=10)
        frame_main_left.grid(row=1, column=0, padx=0, pady=0, sticky='nsew')

        # Frame for right side
        frame_main_right = ttk.Frame(frame, padding=10)
        frame_main_right.grid(row=1, column=1, padx=0, pady=0, sticky='nsew')

        """ File Loader """
        # FRAME for File Loader and Browse Button
        frame_load_file = ttk.Frame(frame_main_left, padding=10, borderwidth=2, relief="groove")
        frame_load_file.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Input Label (enter text file)
        input_label = ttk.Label(frame_load_file, text="Enter text file:", foreground="black")
        input_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        # Input Field (enter text file)
        input_field = ttk.Entry(frame_load_file, width=30)
        input_field.grid(row=0, column=1, padx=4, pady=5, sticky='w')

        # Browse Button (enter text file)
        browse_button = ttk.Button(frame_load_file, text="Browse", command=self.browse_file, style="BlackText.TButton")
        browse_button.grid(row=0, column=2, padx=4, pady=5, sticky = 'w')

        # Load Button (enter text file)
        load_button = ttk.Button(frame_load_file, text="Load File", command=self.load_file, style="BlackText.TButton")
        load_button.grid(row=0, column=3, padx=5, pady=5)

        """ Run and Convert Buttons """
        # FRAME for Run Button and Convert Button
        frame_run = ttk.Frame(frame_main_left, padding=5)
        frame_run.grid(row=2, column=0, padx=170, pady=0, sticky='w')

        # Run Button
        run_btn = ttk.Button(frame_run, text="Run", command=self.run, style="BlackText.TButton")
        run_btn.grid(row=0, column=0, padx=5, pady=5)

        # Convert Button
        convert_btn = ttk.Button(frame_run, text="Convert to 6-Digit", command=self.convert_file_to_6_digit, style="BlackText.TButton")
        convert_btn.grid(row=0, column=1, padx=5, pady=5)

        """ PC and Accumulator Outputs """
        # FRAME for PC and Accumulator
        frame_pcacc_out = ttk.Frame(frame_main_left, padding=(85, 10, 85, 10), borderwidth=2, relief="groove")
        frame_pcacc_out.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Program Counter Label and Output
        pc_label = ttk.Label(frame_pcacc_out, text="Program Counter:", foreground="black")
        pc_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        pc_output = ttk.Entry(frame_pcacc_out, width=10, state='readonly')
        pc_output.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Accumulator Label and Output
        acc_label = ttk.Label(frame_pcacc_out, text="Accumulator:", foreground="black")
        acc_label.grid(row=0, column=3, padx=(10, 5), pady=5, sticky="w")
        acc_output = ttk.Entry(frame_pcacc_out, width=10, state='readonly')
        acc_output.grid(row=0, column=4, padx=5, pady=5, sticky="w")


        """ Output and Input Message Fields and Enter Button """
        # FRAME for In-Out Fields
        frame_inout = ttk.Frame(frame_main_left, padding=(0, 10, 0, 10))
        frame_inout.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # Output Message Field
        out_label = ttk.Label(frame_inout, text="Output:", foreground="black")
        out_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        out_output = ttk.Entry(frame_inout, width=50, state='readonly')
        out_output.grid(row=0, column=1, padx=5, pady=5, sticky="w", columnspan=1)

        # Input field (User input)
        out_label = ttk.Label(frame_inout, text="Input:", foreground="black")
        out_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        input_val = ttk.Entry(frame_inout, width=50)
        input_val.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        input_val.bind("<Return>", self.process_user_input)  # Bind Enter key

        # Enter Button (Initially Disabled)
        enter_btn = ttk.Button(frame_inout, text="Enter", command=self.process_user_input, state=tk.DISABLED, style="BlackText.TButton")
        enter_btn.grid(row=1, column=2, padx=5, pady=5)

        # Bind Enter Key to process_user_input
        input_val.bind("<Return>", self.process_user_input)  # Bind Enter key to input processing


        """Memory List Box"""
        #FRAME for Memory List Box
        frame_memory = ttk.Frame(frame_main_right, padding=10)
        frame_memory.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Memory locations
        memory_label = ttk.Label(frame_memory, text="Memory:", foreground="black")
        memory_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        memory_frame = ttk.Frame(frame_memory)
        memory_frame.grid(row=1, column=1, rowspan=6, padx=15, pady=5, sticky="nsew")

        memory_listbox = tk.Listbox(memory_frame, width=15, height=10, selectmode=tk.EXTENDED)
        memory_scroll = tk.Scrollbar(memory_frame, orient=tk.VERTICAL)

        memory_listbox.config(yscrollcommand=memory_scroll.set)
        memory_scroll.config(command=memory_listbox.yview)

        memory_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        memory_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Double click to edit
        memory_listbox.bind("<Double-Button-1>", self.edit_memory)

        # Context menu
        memory_menu = tk.Menu(self.root, tearoff=0)
        memory_menu.add_command(label="Cut", command=self.cut_memory)
        memory_menu.add_command(label="Copy", command=self.copy_memory)
        memory_menu.add_command(label="Paste", command=self.paste_memory)

        # Bind right-click to show context menu
        memory_listbox.bind("<Button-3>", self.show_memory_menu)

        # Use shortcuts for copy/paste
        self.root.bind('<Control-c>', self.copy_memory)
        memory_listbox.bind("<Control-c>", lambda e: self.copy_memory())
        memory_listbox.bind("<Control-x>", lambda e: self.cut_memory())
        memory_listbox.bind("<Control-v>", lambda e: self.paste_memory())


        """Color Theme Selector"""
        color_button = ttk.Button(frame_close, text="Choose Theme", command=self.choose_color_scheme, style="BlackText.TButton")
        color_button.grid(row=1, column=0, padx=10, pady=10)
        self.load_color_scheme()

        #Save widgets in a dict for this tab
        self.tabs[title] = {
            "input_field": input_field,
            "memory_listbox": memory_listbox,
            "pc_output": pc_output,
            "acc_output": acc_output,
            "out_output": out_output,
            "input_val": input_val,
            "enter_btn": enter_btn,
            "processor": UVSim.UVSim()
        }

        # Load memory on start
        self.load_memory()

    def close_tab(self, frame):
        """Removes the tab and its associated widgets from memory."""
        try:
            # Get the title of the tab being closed
            for tab_id in self.notebook.tabs():
                if self.notebook.nametowidget(tab_id) == frame:
                    tab_title = self.notebook.tab(tab_id, "text")
                    break
            else:
                raise Exception("Could not find tab title for frame.")

            # Remove tab from notebook and internal tabs dict
            self.notebook.forget(frame)
            if tab_title in self.tabs:
                del self.tabs[tab_title]

        except Exception as e:
            print(f"Error closing tab: {e}")



