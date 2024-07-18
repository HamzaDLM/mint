"""
Main entry for Mint language
"""
import sys
from scanner import Scanner

class Mint:
    had_error = False

    def main(self):
        if len(sys.argv) > 1:
            print("Usage: Mint [script]")
            sys.exit(65)
        elif len(sys.argv) == 1:
            self.run_file(sys.argv[0])
        else:
            self.run_prompt()

    def run_file(self, file_name: str):
        # TODO: handle IO exceptions and add type hint
        print(f'Running file {file_name}')
        with open(file_name, 'rb') as file:
            byte_array = file.read()
            self.run(byte_array)
            if Mint.had_error:
                sys.exit(65)

    def run_prompt(self):
        print("Running prompt")
        while True:
            line = input('> ')
            if line is None:
                self.run(line)
                Mint.had_error = False

    def error(self, line: int, message: str):
        where = ''
        print(f'[line {line}] Error {where}: {message}')
        Mint.had_error = True

    def run(self, byte_array):
        scanner = Scanner(byte_array)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)

if __name__ == '__main__':
    mint = Mint()
    mint.main()
