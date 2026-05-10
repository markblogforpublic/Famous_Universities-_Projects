from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    NUMBER = auto()
    VAR = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[str] = None

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type.name}, {self.value})"
        return f"Token({self.type.name})"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def read_number(self) -> str:
        result = ""
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return result

    def read_var(self) -> str:
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number())

            if self.current_char.isalpha():
                return Token(TokenType.VAR, self.read_var())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV)

            if self.current_char == '^':
                self.advance()
                return Token(TokenType.POW)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)

            raise ValueError(f"Unknown character: {self.current_char}")

        return Token(TokenType.EOF)

    def tokenize(self) -> list[Token]:
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


if __name__ == "__main__":
    lexer = Lexer("x^2 + 2*x")
    for token in lexer.tokenize():
        print(token)