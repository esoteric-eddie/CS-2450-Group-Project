import pytest
from UVSim import UVSim

test_memory = [+1007,+1008,+2007,+3008,+2109,+1109,+4300,+0000,+0000,+0000,-99999]

# -------- UVSIM TESTS --------
@pytest.fixture
def uvsim():
    """ Create instance of UVSim before each test """
    return UVSim()

def test_memory(uvsim):
    """ Check if memory is initialize correctly """
    assert len(uvsim.memory) == 100
    assert all(value == 0 for value in uvsim.memory)

def test_registers(uvsim):
    """ Check if registers initialize correctly """
    assert uvsim.accumulator == 0
    assert uvsim.program_counter == 0
    assert uvsim.instruction_register == 0

def test_load_file(monkeypatch, tmp_path, uvsim):
    """ Create a test file to check if files are read correctly """
    # Create temp file with instructions
    test_file = tmp_path / "test_program.txt"
    test_file.write_text("+1007\n+2008\n+3109\n+4300\n")

    # Mock user input to give filename
    monkeypatch.setattr('builtins.input', lambda _: str(test_file))

    uvsim.load_program()

    # Check if memory loaded correctly
    assert uvsim.memory[:4] == [1007, 2008, 3109, 4300]
    assert uvsim.program_counter == 0

# -------- FUNCTION TESTS --------
def test_fetch_word():
    pass

def test_execution():
    pass

def test_invalid_opcode():
    pass

# -------- OPERATION TESTS --------
def test_load():
    pass

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