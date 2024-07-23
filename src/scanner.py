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
        self.start = -1
        self.current = -1
        self.line = 1
        self.column = 1
        print("Source code:\n" + colorize(source, "GREEN"))

    def scanTokens(self):
        while not self.is_at_end():
            c = self.advance()
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
            # print(
            #     colorize(
            #         f"scanned: {c} line: {self.line} column: {self.column} current: {self.current}",
            #         "BLUE",
            #     )
            # )
            self.scanTokens()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_string(self):
        """Identify a string"""
        value = ""
        while self.peekNext() != '"':
            if self.peekNext() == "\n" or self.is_at_end():
                # if self.peekNext() == "\n":
                #     self.line += 1
                raise Exception(self.format_error("Unterminated string"))
            value += self.source[self.current + 1]
            self.advance()

        self.advance()  # consume the last "
        self.addToken(TokenType.STRING, value)

    def scan_number(self):
        """Identify a number"""
        value = ""
        while self.peekNext().isdigit() or self.peekNext() == ".":
            # raise Exception(self.format_error("Incomplete number"))
            value += self.source[self.current + 1]
            self.advance()

        self.addToken(TokenType.NUMBER, value)

    def scan_identifier(self):
        """Identify an identifier / reserved word"""
        while self.peekNext().isalnum():
            self.advance()

        value = self.source[self.start + 1 : self.current + 1]
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
        if self.is_at_end() or (self.source[self.current + 1] != expected):
            return False
        self.column += 1
        self.current += 1
        return True

    def addToken(self, token_type, literal=None):
        text = self.source[self.start + 1 : self.current + 1]
        print("Adding token:", Token(token_type, text, literal, self.line))
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self):
        """Move forward in the source"""
        if self.source[self.current] == "\n":
            self.column = 0
        self.column += 1
        self.current += 1
        # print(f"advancing from {self.current} which is {self.source[self.current]}")
        return self.source[self.current]

    def is_at_end(self):
        """Check if we're at the end of source"""
        return (self.current + 1) >= len(self.source)

    def format_error(self, text: str = ""):
        """Display the error and point to it in the snippet of code"""
        error_snippet = self.source.split("\n")[self.line - 1]
        content_length = f"{self.line} | "
        pointer = " " * (self.column + len(content_length) - 1) + colorize("^-- Here", "FAIL")
        split_line = colorize("\n==========================================\n", "FAIL")

        return f"{split_line}{colorize('Error: ' + text, 'FAIL')}\nUnexpected '{self.source[self.current]}' at line {colorize(str(self.line), 'FAIL')}, column {colorize(str(self.column), 'FAIL')}\n{content_length}{error_snippet}\n{pointer}{split_line}"
