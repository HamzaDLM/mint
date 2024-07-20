"""
Main entry for Mint language
"""

import sys
from scanner import Scanner
from utils import print_colored


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
        print_colored(f"Running file {file_name}", "BLUE")
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read()
            self.run(source_code)
            if Mint.had_error:
                sys.exit(65)

    def run_prompt(self):
        print("Running prompt")
        while True:
            line = input("> ")
            if line is None:
                self.run(line)
                Mint.had_error = False

    def error(self, line: int, message: str):
        where = ""
        print(f"[line {line}] Error {where}: {message}")
        Mint.had_error = True

    def run(self, source_code: str):
        scanner = Scanner(source_code)
        _ = scanner.scanTokens()
        # print("Source code: \n", source_code)
        # print("Printing tokens:")
        # for token in tokens:
        #     print(token)


def main():
    mint = Mint()
    mint.initialize()


if __name__ == "__main__":
    main()
