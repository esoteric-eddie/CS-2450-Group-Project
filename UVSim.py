class UVSim:
    def __init__(self):
        """Initialize the UVSim virtual machine."""
        # Step 1: Initialize the Virtual Machine
        self.memory = [0] * 100        #Define memory as an array of 100 integers, initialized to zero
        self.accumulator = 0           #Create an accumulator register to store intermediate calculations
        self.program_counter = 0       #Define a program counter (PC) to keep track of the current instruction address
        self.instruction_register = 0  #Set up an instruction register (IR) to hold the instruction being executed

    def load_program(self):
        """Load a BasicML program from a file into memory."""
        # Step 2: Read the Input Program
        filename = input("Enter the name of the input file: ")  #Prompt the user for an input file containing BasicML instructions
        
        with open(filename, 'r') as file:
            for address, line in enumerate(file):
                #Ensure instructions are properly formatted (four-digit signed decimal)
                instruction = line.strip()
                if len(instruction) <= 5 and (instruction.startswith('+') or instruction.startswith('-') or instruction.isdigit()):
                    #Store instructions in memory starting at address 00
                    self.memory[address] = int(instruction)
        
        #Initialize the program counter to 00 (starting execution at the first instruction)
        self.program_counter = 0

# Test the implementation
if __name__ == "__main__":
    # Create and test UVSim
    uvsim = UVSim()
    uvsim.load_program()
    
    # Display results
    print("\nProgram loaded into memory:")
    print("Memory (first 10 locations):", uvsim.memory[:10])
    print("Program Counter:", uvsim.program_counter)
    print("Accumulator:", uvsim.accumulator)
    print("Instruction Register:", uvsim.instruction_register)