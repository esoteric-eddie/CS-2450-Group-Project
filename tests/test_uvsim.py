import pytest
from src import UVSim

test_file1 = "Test1.txt"
test_file_memory = [+1007,+1008,+2007,+3008,+2109,+1109,+4300,+0000,+0000,+0000,-99999]

@pytest.fixture
def uvsim():
    """ Create instance of UVSim before each test """
    return UVSim()

# -------- UVSIM TESTS --------
def test_memory(uvsim):
    """ Check if memory initializes correctly """
    assert len(uvsim.memory) == 100
    assert all(value == 0 for value in uvsim.memory)

def test_registers(uvsim):
    """ Check if registers initialize correctly """
    assert uvsim.accumulator == 0
    assert uvsim.program_counter == 0
    assert uvsim.instruction_register == 0

# -------- METHOD TESTS --------
def test_load_file(uvsim, monkeypatch):
    """ Check if test file is read correctly """
    # Mock input to return test file
    monkeypatch.setattr("builtins.input", lambda _: str(test_file1))

    uvsim.load_program()

    assert uvsim.memory[:len(test_file_memory)] == test_file_memory

def test_fetch_word(uvsim):
    """ Test if memory is correctly broken into opcode and operand """
    uvsim.memory[0] = 2010
    opcode, operand = uvsim.fetch_word(0)
    
    assert opcode == 20
    assert operand == 10

def test_execute_halt(uvsim, capsys):
    """ Test if execution stops if opcode 43 """
    uvsim.memory[0] = 4300
    uvsim.execute()

    captured = capsys.readouterr()
    assert "Program halted." in captured.out
    assert uvsim.program_counter == 0

def test_execute_invalid_opcode(uvsim):
    """ Test if invalid opcodes are ignored """
    uvsim.memory[0] = 9999
    uvsim.memory[1] = 4300
    uvsim.execute()

def test_execute_no_halt(uvsim):
    """ Test if execution stops with no halt """
    uvsim.memory[0] = 9999
    uvsim.execute()

    assert uvsim.program_counter == 99

# -------- OPERATION TESTS --------
def test_store(uvsim):
    """ Test STORE operation """
    uvsim.accumulator = 42
    uvsim.memory[10] = 0

    uvsim.memory[0] = +2110  # STORE at memory address 10
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.memory[10] == 42

def test_store_same(uvsim):
    """ Test STORE operation on current location """
    uvsim.accumulator = 42
    uvsim.memory[0] = 0

    uvsim.memory[0] = +2100  # STORE at memory address 10
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.memory[0] == 42

def test_add(uvsim):
    """ Test ADD operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +3010  # ADD memory[10] to accumulator
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == 15

def test_add_neg(uvsim):
    """ Test ADD operation with negative value """
    uvsim.accumulator = -10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +3010  # ADD memory[10] to accumulator
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == -5

def test_subtract(uvsim):
    """ Test SUBTRACT operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +3110  # SUBTRACT memory[10] from accumulator
    uvsim.memory[1] = 4300

    uvsim.execute()

    assert uvsim.accumulator == 5

def test_subtract_neg(uvsim):
    """ Test SUBTRACT operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = -5

    uvsim.memory[0] = +3110  # SUBTRACT memory[10] from accumulator
    uvsim.memory[1] = 4300

    uvsim.execute()

    assert uvsim.accumulator == 15

def test_multiply(uvsim):
    """ Test MULTIPLY operation """
    uvsim.accumulator = 3
    uvsim.memory[10] = 4

    uvsim.memory[0] = +3210  # MULTIPLY memory[10] with accumulator
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == 12

def test_multiply_99(uvsim):
    """ Test MULTIPLY operation with a large number """
    uvsim.accumulator = 99
    uvsim.memory[10] = 99

    uvsim.memory[0] = +3210  # MULTIPLY memory[10] with accumulator
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == 9801

def test_divide(uvsim):
    """ Test DIVIDE operation """
    uvsim.accumulator = 20
    uvsim.memory[10] = 5

    uvsim.memory[0] = +3310  # DIVIDE accumulator by memory[10]
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == 4

def test_divide_float(uvsim):
    """ Test DIVIDE operation """
    uvsim.accumulator = 5
    uvsim.memory[10] = 2

    uvsim.memory[0] = +3310  # DIVIDE accumulator by memory[10]
    uvsim.memory[1] = 4300
    uvsim.execute()

    assert uvsim.accumulator == 2

def test_divide_by_zero(uvsim, capsys):
    """ Test DIVIDE by zero """
    uvsim.accumulator = 10
    uvsim.memory[10] = 0

    uvsim.memory[0] = +3310  # Attempt to divide by zero
    uvsim.memory[1] = 4300

    with pytest.raises(SystemExit):
        uvsim.execute()

    captured = capsys.readouterr()
    assert "ERROR: Division by zero" in captured.out

def test_branch(uvsim):
    """ Test BRANCH operation """
    uvsim.memory[0] = +4010  # BRANCH to memory address 10
    uvsim.memory[1] = 4300
    uvsim.memory[11] = 4300
    uvsim.execute()

    assert uvsim.program_counter == 11

def test_branch_negative(uvsim):
    """ Test BRANCHNEG operation """
    uvsim.accumulator = -1
    uvsim.memory[0] = +4110  # BRANCHNEG to memory[10]
    uvsim.memory[1] = 4300
    uvsim.memory[11] = 4300

    uvsim.execute()
    assert uvsim.program_counter == 11

def test_branch_zero(uvsim):
    """ Test BRANCHZERO operation """
    uvsim.accumulator = 0
    uvsim.memory[0] = +4210  # BRANCHZERO to memory[10]
    uvsim.memory[1] = 4300
    uvsim.memory[11] = 4300

    uvsim.execute()
    assert uvsim.program_counter == 11


# -------- TEST FILE TESTS --------
test_file = [+1009,+1010,+2009,+3110,+4107,+1109,+4300,+1110,+4300,+0000,+0000,-99999]