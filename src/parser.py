from dataclasses import dataclass
from typing import Any, Union

from mint_token import Token
from token_type import TokenType


@dataclass
class Expr:
    """Base class for expressions"""


@dataclass
class Binary(Expr):
    """Represents an operation that takes two operands, such as addition, subtraction, etc."""

    left: Expr
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    """Represents expressions grouped together, typically within parentheses, to enforce precedence."""

    expression: Expr


@dataclass
class Literal(Expr):
    """Represents fixed values like numbers, strings, booleans, etc."""

    value: Any


@dataclass
class Unary(Expr):
    """Represents an operation that takes a single operand, such as negation or logical NOT."""

    operator: Token
    right: Expr


def ast_printer(node: Expr | None) -> str:
    """Take a look at the parsed syntax tree"""
    match node:
        case Binary():
            return f"({node.operator.lexeme} {ast_printer(node.left)} {ast_printer(node.right)})"
        case Grouping():
            return f"(group {ast_printer(node.expression)})"
        case Literal():
            return "nil" if node.value is None else str(node.value)
        case Unary():
            return f"({node.operator.lexeme} {ast_printer(node.right)})"
        case _:
            raise TypeError("Unsupported type")


def test_ast_printer() -> None:
    expression = Binary(
        left=Unary(
            operator=Token(
                TokenType.MINUS,
                "-",
                None,
                1,
            ),
            right=Literal(value=123),
        ),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(
            expression=Literal(
                value=420.69,
            )
        ),
    )
    assert ast_printer(expression) == "(* (- 123) (group 420.69))"
    print("Result:", ast_printer(expression))


class ParseException(RuntimeError):
    pass


class Parser:
    current = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def parse(self) -> Union[Expr, None]:
        try:
            return self.expression()
        except Exception as pe: # ParseException as pe:
            print("PARSE EXCEPTION!!!!!!!", pe)
            return None

    def expression(self) -> Expr:
        print("expression")
        return self.equality()

    def equality(self) -> Expr:
        print("equality")
        expression = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            expression = Binary(
                left=expression,
                operator=self.previous(),
                right=self.comparison(),
            )

        return expression

    def comparison(self) -> Expr:
        print("comparison")
        expression = self.term()

        while self.match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            expression = Binary(
                left=expression,
                operator=self.previous(),
                right=self.term(),
            )

        return expression

    def term(self) -> Expr:
        print("term")
        expression = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            expression = Binary(
                left=expression, operator=self.previous(), right=self.factor()
            )

        return expression

    def factor(self) -> Expr:
        print("factor")
        expression = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            expression = Binary(
                left=expression,
                operator=self.previous(),
                right=self.unary(),
            )

        return expression

    def unary(self) -> Expr:
        print("unary")
        if self.match([TokenType.BANG, TokenType.MINUS]):
            return Unary(operator=self.previous(), right=self.unary())

        return self.primary()

    def primary(self) -> Expr:
        print("primary")
        if self.match([TokenType.FALSE]):
            return Literal(value=False)
        if self.match([TokenType.TRUE]):
            return Literal(value=True)
        if self.match([TokenType.NIL]):
            return Literal(value=None)
            
        print(f"currently: {self.previous()} {self.match([TokenType.NUMBER])}")
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            print("returning:", self.previous().literal)
            return Literal(value=self.previous().literal)

        if self.match([TokenType.LEFT_PAREN]):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return Grouping(expression=expression)

        raise self.error(self.peek(), "Expected expression")

    def match(self, types: list[TokenType]) -> bool:
        """Check if the current token matches any of the token types, if so consume the token and return True"""
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, type_: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == type_

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def consume(self, type_: TokenType, message: str) -> Union[Token, ParseException]:
        """Check if the next token is of the expected type, if so consume the token
        If next token is not what we expect, report an errror
        """
        if self.check(type_):
            return self.advance()

        return self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseException:
        self.print_error(token, message)

        return ParseException()

    def print_error(self, token: Token, message: str) -> None:
        """Show error to user"""
        if token.token_type == TokenType.EOF:
            print(f"{token.line} at end {message}")
        else:
            print(f"{token.line} at '{token.lexeme}' {message}")

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                break

            if self.peek().token_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                break

        self.advance()
