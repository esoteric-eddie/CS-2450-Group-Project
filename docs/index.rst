Overview:
UVSim is a virtual machine that executes a machine language called BasicML. The program
reads an input file containing BasicML instructions, loads them into memory, and executes them
line-by-line. The program interprets a 4 digit code into its corresponding instructions based on
an opcode and a specified register value.

User Stories:
1. As a computer science student, I want to use a virtual machine that uses simple
machine language instructions so that I can learn more about machine language.
2. As a user, I want to load and execute a BasicML program so that I can see the program
perform computations and display the result.

Use Cases:
1. Load Program from File
a. Actor(s): User
b. System:
    i. User enters the filename
    ii. The program reads the file and loads instructions into memory
    iii. The program counter is set to 0
c. Goal: Load a program from a file determined from user input

2. Fetch Word
a. Actor(s): UVSim
b. System:
    i. UVSim reads the memory at the current program counter (pc) location
    ii. It extracts the operation code and operand
    iii. The instruction is returned for execution
c. Goal: Fetch an instruction from memory to use in the program

3. READ InstrucKon
a. Actor(s): User, UVSim
b. System:
    i. UVSim prompts the user for input
    ii. The user enters a 4-digit number
    iii. UVSim stores the number in memory at the specified address
c. Goal: Execute a READ instruction from a file

4. WRITE InstrucKon
a. Actor(s): UVSim
b. System:
    i. UVSim fetches the value from the specified memory location
    ii. It prints the value to the console
c. Goal: Execute a WRITE instruction and print the value to the console

5. LOAD InstrucKon
a. Actor(s): UVSim
b. System:
    i. UVSim fetches a value from the specified memory location
    ii. It stores the value in the accumulator

6. STORE InstrucKon
a. Actor(s): UVSim
b. System:
    i. UVSim writes the value store in the accumulator variable to the specified
    memory location
c. Goal: Store the accumulator's value in a specified memory location

7. Arithmetic Operation (ADD, SUBTRACT, DIVIDE, MULTIPLY)
a. Actor(s): UVSim
b. System:
    i. UVSim fetches the operand from memory
    ii. It performs the specified arithmetic operation
    iii. The result is stored in the accumulator
c. Goal: Perform arithmetic operations on operands stored in a specified memory
location

8. Division by Zero
a. Actor(s): UVSim
b. System:
    i. UVSim retrieves the operand
    ii. If the operand is zero, it prints an error message and halts execution
c. Goal: Handle instances of division by zero

9. BRANCH Instruction
a. Actor(s): UVSim
b. System:
    i. UVSim evaluates the branch condition (positive, negative, or zero)
    ii. If the condition is met, it updates the program counter to the specified
    memory address
    iii. If not, it continues to the next instruction
c. Goal: Perform a branch instruction based on the accumulator's value

10. Halt the Program
a. Actor(s): UVSim
b. System:
    i. UVSim prints "Program halted."
    ii. Execution stops
c. Goal: Halt program after successful execution