from typing import Dict
from dataclasses import dataclass 
from src.mint_token import Token

class Expr:
    pass

@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping:
    expression: Expr

@dataclass
class Literal:
    value: Dict

@dataclass
class Unary:
    operator: Token
    right: Expr

