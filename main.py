"Joshua Eaton"
#test push for Jackson
#test dummy memory variable
memory = ["1013", "2014", "1415", "4344"]

#pass fetch a memory location, get the operation code
def fetch_word(memory_index):
    #memory should be whatever the name of the variable that our 0-99 memory array is called. return memory at index.
    word = memory[memory_index]
    #set operation code to the first two numbers, operand to the last two numbers.
    operation_code = word[:2]
    operand = word[2:4]
    #return operation code and operand
    return [operation_code, operand]

def exectue():
    #start at the first memory location, starting operation code is nothing, starting operand is nothing.
    #current location in memory
    program_counter = 0
    #first two digits of word
    operation_code = 00
    #second two digits of word
    operand = 00
    #increment the counter unless branch function, which sets this to false
    increment_counter = True
    while operation_code != 43:
        fetched_word = fetch_word(program_counter)
        operation_code = int(fetched_word[0])
        operand = int(fetched_word[1])

        #check if operation is equal to a relevant operation
        #relevant operations are 10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43
        match operation_code:
            case 10:
                #Call READ
                print("READ")
            case 11:
                #Call WRITE
                print("WRITE")
            case 20:
                #Call LOAD
                print("LOAD")
            case 20:
                #Call STORE
                print("STORE")
            case 30:
                #Call ADD
                print("ADD")
            case 31:
                #Call SUBTRACT
                print("SUBTRACT")
            case 32:
                #Call MULTIPLY
                print("MULTIPY")
            case 33:
                #Call DIVIDE
                print("DIVIDE")
            case 40:
                #Call BRANCH
                print("BRANCH")
                #increment_counter = False
            case 41:
                #Call BRANCHNEG
                print("BRANCHNEG")
                #increment_counter = False
            case 42:
                #Call BRANCHZERO
                print("BRANCHZERO")
                #increment_counter = False
            case 43:
                #Call Halt function, but this code will stop executing anyways after halt because of while loop
                print("HALT")
            case default:
                print("Not an operation code")

        #increment program_counter if increment counter is true
        if increment_counter == True:
            program_counter += 1

def main():
    exectue()

if __name__ == '__main__':
    main()
