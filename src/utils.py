"""
Utilities module
"""

from enum import Enum


class Colors(Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message: str, color: Colors):
    print(f"{color.value}{message}{Colors.ENDC.value}")


def colorize(message: str, color: Colors) -> str:
    return f"{color.value}{message}{Colors.ENDC.value}"
