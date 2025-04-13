import pytest
from src.UVSim import UVSim

test_file1 = "tests/Test1.txt"
test_file_memory = [+10007, +10008, +20007, +30008, +21009, +11009, +43000, +00000, +00000, +00000]

@pytest.fixture
def uvsim():
    """ Create instance of UVSim before each test """
    return UVSim()

# -------- UVSIM TESTS --------
def test_memory(uvsim):
    """ Check if memory initializes correctly """
    assert len(uvsim.memory) == 250  # instead of 100
    assert all(value == 0 for value in uvsim.memory)

def test_registers(uvsim):
    """ Check if registers initialize correctly """
    assert uvsim.accumulator == 0
    assert uvsim.program_counter == 0
    assert uvsim.instruction_register == 0

# -------- METHOD TESTS --------
def test_load_file(uvsim):
    """ Check if test file is read correctly """
    for i, val in enumerate(test_file_memory):
        uvsim.memory[i] = val

    assert uvsim.memory[:len(test_file_memory)] == test_file_memory

def test_fetch_word(uvsim):
    """ Test if memory is correctly broken into opcode and operand """
    uvsim.memory[0] = 20010
    opcode, operand = uvsim.fetch_word(0)
    
    assert opcode == 20
    assert operand == 10

def test_execute_halt(uvsim, capsys):
    """ Test if execution stops if opcode 43 """
    initial_pc = uvsim.program_counter
    uvsim.memory[0] = +43000
    uvsim.execute(uvsim.fetch_word(0))
    assert uvsim.program_counter == initial_pc


def test_execute_invalid_opcode(uvsim):
    """ Test if invalid opcodes are ignored """
    uvsim.memory[0] = 99999
    uvsim.memory[1] = 43000

    with pytest.raises(ValueError, match="ERROR: Invalid command."):
        uvsim.execute()

def test_execute_no_halt(uvsim):
    """ Test if execution stops with no halt """
    uvsim.memory[0] = 99999

    with pytest.raises(ValueError, match="ERROR: Invalid command."):
        uvsim.execute()

# -------- OPERATION TESTS --------
def test_store(uvsim):
    """ Test STORE operation """
    uvsim.accumulator = 42
    uvsim.memory[10] = 0

    uvsim.memory[0] = +21010  # STORE at memory address 10
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.memory[10] == 42

def test_store_same(uvsim):
    """ Test STORE operation on current location """
    uvsim.accumulator = 42
    uvsim.memory[0] = 0

    uvsim.memory[0] = +21000  # STORE at memory address 10
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.memory[0] == 42

def test_add(uvsim):
    """ Test ADD operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +30010  # ADD memory[10] to accumulator
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == 15

def test_add_neg(uvsim):
    """ Test ADD operation with negative value """
    uvsim.accumulator = -10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +30010  # ADD memory[10] to accumulator
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == -5

def test_subtract(uvsim):
    """ Test SUBTRACT operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = 5

    uvsim.memory[0] = +31010  # SUBTRACT memory[10] from accumulator
    uvsim.memory[1] = 43000

    uvsim.execute()

    assert uvsim.accumulator == 5

def test_subtract_neg(uvsim):
    """ Test SUBTRACT operation """
    uvsim.accumulator = 10
    uvsim.memory[10] = -5

    uvsim.memory[0] = +31010  # SUBTRACT memory[10] from accumulator
    uvsim.memory[1] = 43000

    uvsim.execute()

    assert uvsim.accumulator == 15

def test_multiply(uvsim):
    """ Test MULTIPLY operation """
    uvsim.accumulator = 3
    uvsim.memory[10] = 4

    uvsim.memory[0] = +32010  # MULTIPLY memory[10] with accumulator
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == 12

def test_multiply_99(uvsim):
    """ Test MULTIPLY operation with a large number """
    uvsim.accumulator = 99
    uvsim.memory[10] = 99

    uvsim.memory[0] = +32010  # MULTIPLY memory[10] with accumulator
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == 9801

def test_divide(uvsim):
    """ Test DIVIDE operation """
    uvsim.accumulator = 20
    uvsim.memory[10] = 5

    uvsim.memory[0] = +33010  # DIVIDE accumulator by memory[10]
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == 4

def test_divide_float(uvsim):
    """ Test DIVIDE operation """
    uvsim.accumulator = 5
    uvsim.memory[10] = 2

    uvsim.memory[0] = +33010  # DIVIDE accumulator by memory[10]
    uvsim.memory[1] = 43000
    uvsim.execute()

    assert uvsim.accumulator == 2

def test_divide_by_zero(uvsim, capsys):
    """ Test DIVIDE by zero """
    uvsim.accumulator = 10
    uvsim.memory[10] = 0

    uvsim.memory[0] = +33010  # divide by zero
    uvsim.memory[1] = 43000

    with pytest.raises(ZeroDivisionError, match="ERROR: Division by zero"):
        uvsim.execute()

def test_branch(uvsim):
    """ Test BRANCH operation """
    uvsim.memory[0] = +40011  # BRANCH to memory address 11
    uvsim.memory[1] = 43000
    uvsim.memory[11] = 43000
    uvsim.execute()

    assert uvsim.program_counter == 11

def test_branch_negative(uvsim):
    """ Test BRANCHNEG operation """
    uvsim.accumulator = -1
    uvsim.memory[0] = +41011  # BRANCHNEG to memory[11]
    uvsim.memory[1] = 43000
    uvsim.memory[11] = 43000

    uvsim.execute()
    assert uvsim.program_counter == 11

def test_branch_zero(uvsim):
    """ Test BRANCHZERO operation """
    uvsim.accumulator = 0
    uvsim.memory[0] = +42011  # BRANCHZERO to memory[11]
    uvsim.memory[1] = 43000
    uvsim.memory[11] = 43000

    uvsim.execute()
    assert uvsim.program_counter == 11

def test_load_instruction(uvsim):
    """ Test LOAD operation """
    uvsim.memory[30] = 43021
    uvsim.memory[0] = 20030  # LOAD instruction
    uvsim.memory[1] = 43000

    uvsim.execute()

    assert uvsim.accumulator == 43021

# -------- USER INPUT TESTS --------
def test_read_instruction(uvsim, monkeypatch):
    """ Test READ instruction """
    input_value = "1234\n"  # test user input
    monkeypatch.setattr("builtins.input", lambda operand: input_value.strip())  # Strip newline

    uvsim.memory[0] = 10005  # READ into memory[5]
    uvsim.memory[1] = 43000

    uvsim.execute()

    assert uvsim.memory[5] == 1234, f"Expected 1234, but got {uvsim.memory[5]}"

def test_write_instruction(uvsim, capsys):
    """ Test WRITE instruction """
    uvsim.memory[20] = 56078
    uvsim.memory[0] = 11020  # WRITE instruction
    uvsim.memory[1] = 43000

    uvsim.execute()

    captured = capsys.readouterr()
    assert "Output: 56078" in captured.out