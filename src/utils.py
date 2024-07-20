"""
Utilities module
"""


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(message: str, color: str):
    color_code = getattr(Colors, color.upper(), Colors.ENDC)
    print(f"{color_code}{message}{Colors.ENDC}")


def format_colored(message: str, color: str) -> str:
    color_code = getattr(Colors, color.upper(), Colors.ENDC)
    return f"{color_code}{message}{Colors.ENDC}"
