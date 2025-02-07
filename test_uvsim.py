import pytest
from UVSim import UVSim

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
    assert "HALT" in captured.out
    assert uvsim.program_counter == 0

def test_execute_invalid_opcode(uvsim, capsys):
    """ Test if invalid opcodes output message """
    pass
    # uvsim.memory[0] = 9999
    # uvsim.execute()

    # captured = capsys.readouterr()
    # assert "Not an operation code" in captured.out

# -------- OPERATION TESTS --------
def test_store():
    pass

def test_add():
    pass

def test_subtract():
    pass

def test_multiply():
    pass

def test_divide():
    pass

def test_divide_by_zero():
    pass

def test_branch():
    pass

def test_branch_negative():
    pass

def test_branch_zero():
    pass

def test_halt():
    pass

# -------- TEST FILE TESTS --------
test_file = [+1009,+1010,+2009,+3110,+4107,+1109,+4300,+1110,+4300,+0000,+0000,-99999]