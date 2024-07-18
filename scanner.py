from mint_token import Token
from token_type import TokenType
from mint import Mint

class Scanner:
    # TODO: source is bytes or str?
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while not self.is_at_end():
            c = self.advance()
            match c:
                case '(': 
                    self.addToken(TokenType.LEFT_PAREN)
                case ')': 
                    self.addToken(TokenType.RIGHT_PAREN)
                case '{':   
                    self.addToken(TokenType.LEFT_BRACE)
                case '}': 
                    self.addToken(TokenType.RIGHT_BRACE)
                case ',': 
                    self.addToken(TokenType.COMMA)
                case '.':   
                    self.addToken(TokenType.DOT)
                case '-': 
                    self.addToken(TokenType.MINUS)
                case '+': 
                    self.addToken(TokenType.PLUS)
                case ';': 
                    self.addToken(TokenType.SEMICOLON)
                case '*': 
                    self.addToken(TokenType.STAR) 
                case '!':
                    self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
                case '=':
                    self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
                case '<':
                    self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
                case '>':
                    self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
                case '#': # Comment
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                case '/':
                    self.addToken(TokenType.SLASH)
                case ' ':
                    pass 
                case '\r':
                    pass 
                case '\t':
                    pass
                case '\n':
                    self.line += 1
                 
                case _:
                    Mint().error(line=self.line, message="Unexpected character.")

            self.start = self.current
            self.scanTokens()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def match(self, expected: str):
        if self.is_at_end() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def addToken(self, token_type, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self):
        """Move forward in the source"""
        self.current += 1
        return self.source[self.current]

    def is_at_end(self):
        """Check if we're at the end of source"""
        return self.current >= len(self.source)
