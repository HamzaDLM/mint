"""
Main entry for Mint language
"""

import sys
from parser import Parser, ast_printer, evaluate 
from scanner import Scanner
from utils import Colors, colorize, print_colored


class Mint:
    had_error = False

    def initialize(self):
        if len(sys.argv) > 2:
            print("Usage: Mint [script]")
            sys.exit(65)
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

    def run_file(self, file_name: str):
        # TODO: handle IO exceptions and add type hint
        print_colored(f"Running file {file_name}", Colors.BLUE)
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read()
            self.run(source_code)
            if Mint.had_error:
                sys.exit(65)

    def run_prompt(self):
        print("Mint 0.0.1-beta.1 Prompt")
        while True:
            line = input(colorize("$> ", Colors.GREEN))
            if line == "exit()":
                sys.exit(65)
            if line:
                self.run(line + "\n")
                Mint.had_error = False

    def error(self, line: int, message: str):
        where = ""
        print(f"[line {line}] Error {where}: {message}")
        Mint.had_error = True

    def run(self, source_code: str):
        scanner = Scanner(source_code)
        tokens = scanner.scanTokens()
        print("======== TOKENS ===============") 
        for token in tokens:
            print_colored(str(token), Colors.WARNING)

        parser = Parser(tokens=tokens)
        expressions = parser.parse()
        print("======== EXPRESSIONS ==========") 
        if expressions is not None:
            for expression in expressions:
                print(ast_printer(expression), colorize(str(expression), Colors.WARNING))
        
        print("======== EVALUATE ==========") 
        if expressions is not None:
            for expression in expressions:
                print(evaluate(expression))

def main():
    mint = Mint()
    mint.initialize()


if __name__ == "__main__":
    main()
