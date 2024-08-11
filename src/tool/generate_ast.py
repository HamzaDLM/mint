import sys
from typing import Dict


def define_ast(output_dir: str, base_name: str, types: Dict):
    path = f"{output_dir}/{base_name.lower()}.py"

    with open(path, "w") as f:
        f.write(f"""from typing import Dict
from dataclasses import dataclass 
from src.mint_token import Token

class {base_name}:
    pass

""")

        for key, value in types.items():
            f.write(f"""@dataclass
class {key}:
    {value.replace(', ', '\n    ')}

""")


def main():
    if not len(sys.argv) > 1:
        raise Exception("Usage: generate_ast <output directory>")

    output_dir = f"src/{sys.argv[1]}"

    define_ast(
        output_dir,
        "Expr",
        {
            "Binary": "left: Expr, operator: Token, right: Expr",
            "Grouping": "expression: Expr",
            "Literal": "value: Dict",
            "Unary": "operator: Token, right: Expr",
        },
    )


if __name__ == "__main__":
    main()
