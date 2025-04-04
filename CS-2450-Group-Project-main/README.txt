# CS-2450-Group-Project
# UVSim

## Description
UVSim is a command-line application that simulates a basic virtual machine to execute programs written in BasicML.

## Prerequisites
- Programming Language: Python 3.8+

## Running the Application
1. Open a terminal or command prompt.
2. Navigate to the setup.py
3. type: [pip install -e .] just what is in the brackets, not the brackets, into the terminal
    - It is up to the user if they want to install in a virtual envrionment, but it is recommended.
5. Run the program using: python3 scripts/main.py  
6. The program will display a text box to enter or browse for a file name containing BasicML instructions. Once you have your file selected, hit the load button.
    - Each instruction in the file should be a four-digit signed decimal number (Example: +1010), each on new line.
7. Once you have loaded your file, hit the run button. The simulator will then execute the program, processing each instruction.
    - Memory locations can be edited by double-clicking and cut, copy, paste can be used by right-clicking
    - Color theme can be changed by using the 'Choose Theme' button. Your color theme changes will be saved.
