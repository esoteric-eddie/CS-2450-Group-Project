class UVSim:
    def __init__(self):
        """Initialize the UVSim virtual machine."""
        # Step 1: Initialize the Virtual Machine
        self.memory = [0] * 250  # Define memory as an array of 250 integers, initialized to zero
        self.accumulator = 0  # Create an accumulator register to store intermediate calculations
        self.program_counter = 0  # Define a program counter (PC) to keep track of the current instruction address
        self.instruction_register = 0  # Set up an instruction register (IR) to hold the instruction being executed
        self.out_of_bounds = 248

    def load_program(self, filename):
        """Load a BasicML program from a file into memory."""
        # Step 2: Read the Input Program

        with open(filename, 'r') as file:
            for address, line in enumerate(file):
                # Ensure instructions are properly formatted (four-digit signed decimal)
                instruction = line.strip()
                if instruction.startswith('+') or instruction.startswith('-') or instruction.isdigit():
                    # Store instructions in memory starting at address 00
                    self.memory[address] = int(instruction)

        # Initialize the program counter to 00 (starting execution at the first instruction)
        self.program_counter = 0

    def convert_file(self, filename):

        converted_lines = []

        with open(filename, 'r') as file:
            for address, line in enumerate(file):
                line = line.strip()
                if (len(line) != 5 and line != "-99999"):
                    print(line)
                    print(len(line))
                    raise Exception("File contains words longer than 5 digits and doesn't match the old file type.")
        
        with open(filename, 'r') as file:
            for address, line in enumerate(file):
                # Ensure instructions are properly formatted (four-digit signed decimal)
                instruction = line.strip()
                instruction = instruction[:1] + "0" + instruction[1:]
                instruction = instruction[:3] + "0" + instruction[3:]
                instruction += "\n"
                converted_lines.append(instruction)

        with open(filename, 'w') as file:
            file.writelines(converted_lines)

    # pass fetch a memory location, get the operation code
    def fetch_word(self, memory_index):
        # memory should be whatever the name of the variable that our 0-99 memory array is called. return memory at index.
        word = self.memory[memory_index]

        word_str = str(word)
        if len(word_str) == 5:
            # set operation code to the first two numbers, operand to the last two numbers.
            operation_code = int(word_str[:2])
            operand = int(word_str[2:5])
            # return operation code and operand
            return [operation_code, operand]
        else:
            operation_code = 99
            operand = 999
            return [operation_code, operand]

    def get_operand(self, operand):
        """Ensure operand is within valid memory range (0-99)."""
        if 0 <= operand < 249:
            return self.memory[operand]
        else:
            print(f"ERROR: Memory access out of bounds (Address: {operand}).")
            exit(1)  # Stop execution

    def execute(self, input_callback=None, step_mode=True):
        """ Execute one instruction at a time if step_mode is enabled. """

        if self.program_counter > self.out_of_bounds:
            return  # Prevent out-of-bounds execution

        fetched_word = self.fetch_word(self.program_counter)
        operation_code = int(fetched_word[0])
        operand = int(fetched_word[1])

        print(operation_code)

        match operation_code:
            case 10:  # READ instruction (pause execution); ensures user can enter values when prompted
                if input_callback:
                    input_callback(operand)  # Tell GUI to get input
                else:
                    try:
                        value = int(input("Enter a number: "))  # Get input from terminal
                    except ValueError:
                        print("ERROR: Invalid input. Please enter a valid number.")
                        return

                self.memory[operand] = value
            case 11:  # WRITE instruction
                print(f"Output: {self.memory[operand]}")

            case 20:  # LOAD
                self.accumulator = self.memory[operand]

            case 21:  # STORE
                self.memory[operand] = self.accumulator

            case 30:  # ADD
                self.accumulator += self.get_operand(operand)

            case 31:  # SUBTRACT
                self.accumulator -= self.get_operand(operand)

            case 32:  # MULTIPLY
                self.accumulator *= self.get_operand(operand)

            case 33:  # DIVIDE
                divisor = self.get_operand(operand)
                if divisor == 0:
                    raise ZeroDivisionError("ERROR: Division by zero. Execution halted.")
                self.accumulator //= divisor

            case 40:  # BRANCH
                self.program_counter = operand
                return  # Stop execution for next step

            case 41:  # BRANCHNEG
                if self.accumulator < 0:
                    self.program_counter = operand
                return

            case 42:  # BRANCHZERO
                if self.accumulator == 0:
                    self.program_counter = operand
                return

            case 43:  # HALT
                print("Program halted.")
                return  # Stop execution completely

            case _:
                raise ValueError("ERROR: Invalid command.")

        self.program_counter += 1  # Ensure PC always moves to the next instruction

        if step_mode:
            return  # Stop execution for GUI to continue


# Test the implementation
if __name__ == "__main__":
    # Create and test UVSim
    uvsim = UVSim()
    #uvsim.convert_file("tests/Test1.txt")
    uvsim.load_program("tests/Test3.txt")

    # Display results
    print("\nProgram loaded into memory:")
    print("Memory (first 10 locations):", uvsim.memory[:10])
    print("Program Counter:", uvsim.program_counter)
    print("Accumulator:", uvsim.accumulator)
    print("Instruction Register:", uvsim.instruction_register)

    # change GUI input to accept 6 digits
    # format the display in GUI to display a 0 in front of numbers