from subprocess import run
from string import digits


def get_int(string: str) -> int:
    digits_str = ''.join([char for char in string if char in digits])
    if digits_str == "":
        digits_str = "0"
    
    return int(digits_str)

def get_float(string: str) -> float:
    allowed_chars = digits + "."
    return float(''.join([char for char in string if char in allowed_chars]))

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = file.read()
        return content.strip()

def read_lines(file_path: str) -> list[str]:
    content = read_file(file_path)
    lines = content.split("\n")
    return [line.strip() for line in lines]
    
def search_line(lines: list[str], key: str, default: str = "") -> str:
    for line in lines:
        if key in line:
            return line
    return default

def exec_command(command: str) -> str:
    return run(command.split(" "), capture_output=True, text=True).stdout.strip()
