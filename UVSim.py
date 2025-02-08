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
                if instruction.startswith('+') or instruction.startswith('-') or instruction.isdigit():
                    #Store instructions in memory starting at address 00
                    self.memory[address] = int(instruction)

        #Initialize the program counter to 00 (starting execution at the first instruction)
        self.program_counter = 0

    #pass fetch a memory location, get the operation code
    def fetch_word(self, memory_index):
        #memory should be whatever the name of the variable that our 0-99 memory array is called. return memory at index.
        word = self.memory[memory_index]

        word_str = str(word)
        if len(word_str) == 4:
            #set operation code to the first two numbers, operand to the last two numbers.
            operation_code = int(word_str[:2])
            operand = int(word_str[2:4])
            #return operation code and operand
            return [operation_code, operand]
        else:
            operation_code = 99
            operand = 99
            return [operation_code, operand]

    def execute(self):
        #start at the first memory location, starting operation code is nothing, starting operand is nothing.
        #first two digits of word
        operation_code = 00
        #second two digits of word
        operand = 00
        #increment the counter unless branch function, which sets this to false
        increment_counter = True
        while operation_code != 43 or self.program_counter > 98:
            fetched_word = self.fetch_word(self.program_counter)
            operation_code = int(fetched_word[0])
            operand = int(fetched_word[1])

            #check if operation is equal to a relevant operation
            #relevant operations are 10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43
            match operation_code:
                case 10:
                    #Call READ
                    self.memory[operand] = int(input("Enter a number: "))
                case 11:
                    #Call WRITE
                    print(f"Output: {self.memory[operand]}")
                case 20:
                    #Call LOAD
                    self.accumulator = self.memory[operand]
                case 21:
                    #Call STORE
                    self.memory[operand] = self.accumulator
                case 30:
                    #Call ADD
                    self.accumulator += self.get_operand(operand)
                case 31:
                    #Call SUBTRACT
                    self.accumulator -= self.get_operand(operand)
                case 32:
                    #Call MULTIPLY
                    self.accumulator *= self.get_operand(operand)
                case 33:
                    #Call DIVIDE
                    divisor = self.get_operand(operand)
                    if divisor == 0:
                        print("ERROR: Division by zero. Execution halted.")
                        exit(1)
                    self.accumulator //= divisor
                case 40:
                    #Call BRANCH
                    self.program_counter = operand
                    increment_counter = False
                case 41:
                    #Call BRANCHNEG
                    if self.accumulator < 0:
                        self.program_counter = operand
                    increment_counter = False
                case 42:
                    #Call BRANCHZERO
                    if self.accumulator == 0:
                        self.program_counter = operand
                    increment_counter = False
                case 43:
                    #Call Halt function, but this code will stop executing anyways after halt because of while loop
                    print("Program halted.")
                    break
                case default:
                    print("Command not valid.")

            #increment program_counter if increment counter is true
            if increment_counter == True:
                self.program_counter += 1

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
