from mint_token import Token
from token_type import TokenType
from utils import colorize

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        print("Source code raw:\n" + colorize(repr(source), "GREEN"))
        print("Source code:\n" + colorize(source, "GREEN"))

    def scanTokens(self):
        while not self.is_at_end():
            c = self.advance()
            print(
                colorize(
                    f"scan {repr(c)} start {self.start} current {self.current} line: {self.line}",
                    "WARNING",
                )
            )
            match c:
                case "(":
                    self.addToken(TokenType.LEFT_PAREN)
                case ")":
                    self.addToken(TokenType.RIGHT_PAREN)
                case "{":
                    self.addToken(TokenType.LEFT_BRACE)
                case "}":
                    self.addToken(TokenType.RIGHT_BRACE)
                case ",":
                    self.addToken(TokenType.COMMA)
                case ".":
                    self.addToken(TokenType.DOT)
                case "-":
                    self.addToken(TokenType.MINUS)
                case "+":
                    self.addToken(TokenType.PLUS)
                case ";":
                    self.addToken(TokenType.SEMICOLON)
                case "*":
                    self.addToken(TokenType.STAR)
                case "!":
                    self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
                case "=":
                    self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
                case "<":
                    self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
                case ">":
                    self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
                case "#":  # Comment
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                    self.line += 1
                case "/":
                    self.addToken(TokenType.SLASH)
                case " ":
                    pass
                case "\r":
                    pass
                case "\t":
                    pass
                case "\n":
                    self.line += 1
                case '"':
                    self.scan_string()
                case _:
                    if c.isdigit():
                        self.scan_number()
                    elif c.isalpha():
                        self.scan_identifier()
                    else:
                        raise Exception(self.format_error("Unexpected character"))

            self.start = self.current
            c = repr(c) if c in {"\n", "\r"} else c
            self.scanTokens()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n" :
                self.line += 1
            self.advance()

        if self.is_at_end():
            raise Exception(self.format_error("Unterminated string"))

        self.advance()  # consume the last "
        self.addToken(TokenType.STRING, self.source[self.start + 1 : self.current - 1])

    def scan_number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peekNext().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def scan_identifier(self):
        while self.peek().isalnum():
            self.advance()

        value = self.source[self.start : self.current]
        if value in KEYWORDS:
            self.addToken(KEYWORDS[value])
        else:
            self.addToken(TokenType.IDENTIFIER, value)

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str):
        if self.is_at_end() or (self.source[self.current] != expected):
            return False
        self.column += 1
        self.current += 1
        return True

    def addToken(self, token_type, literal=None):
        text = self.source[self.start : self.current]
        print("Adding token:", Token(token_type, text, literal, self.line))
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self):
        value = self.source[self.current]
        if value == "\n":
            self.column = 0
        self.column += 1
        self.current += 1
        # print(f"advancing from {self.current} which is {self.source[self.current]}")
        return value

    def is_at_end(self):
        return (self.current + 1) >= len(self.source)

    def format_error(self, text: str = ""):
        """Display the error and point to it in the snippet of code"""
        error_snippet = self.source.split("\n")[self.line - 1]
        content_length = f"{self.line} | "
        pointer = " " * (self.column + len(content_length) - 1) + colorize("^-- Here", "FAIL")
        split_line = colorize("\n==========================================\n", "FAIL")

        return f"{split_line}{colorize('Error: ' + text, 'FAIL')}\nUnexpected '{self.source[self.current]}' at line {colorize(str(self.line), 'FAIL')}, column {colorize(str(self.column), 'FAIL')}\n{content_length}{error_snippet}\n{pointer}{split_line}"
