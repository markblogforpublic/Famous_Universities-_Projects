from lexer import Lexer, Token, TokenType
from expr import Expr, Number, Variable, Neg, Add, Sub, Mul, Div, Pow


class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def error(self, expected: str):
        raise ValueError(f"Expected {expected}, got {self.current_token}")

    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type.name)

    def parse(self) -> Expr:
        return self.parse_expr()

    def parse_expr(self) -> Expr:
        result = self.parse_term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = Add(result, self.parse_term())
            else:
                self.eat(TokenType.MINUS)
                result = Sub(result, self.parse_term())
        return result

    def parse_term(self) -> Expr:
        result = self.parse_factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            if self.current_token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result = Mul(result, self.parse_factor())
            else:
                self.eat(TokenType.DIV)
                result = Div(result, self.parse_factor())
        return result

    def parse_factor(self) -> Expr:
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return Neg(self.parse_factor())
        return self.parse_exponent()

    def parse_exponent(self) -> Expr:
        result = self.parse_atom()
        if self.current_token.type == TokenType.POW:
            self.eat(TokenType.POW)
            result = Pow(result, self.parse_factor())
        return result

    def parse_atom(self) -> Expr:
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.value)
            self.eat(TokenType.NUMBER)
            return Number(value)
        elif self.current_token.type == TokenType.VAR:
            name = self.current_token.value
            self.eat(TokenType.VAR)
            return Variable(name)
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.parse_expr()
            self.eat(TokenType.RPAREN)
            return result
        else:
            self.error("number, variable, or '('")


def parse(text: str) -> Expr:
    parser = Parser(text)
    return parser.parse()


if __name__ == "__main__":
    from expr import to_string
    test_exprs = [
        "x^2 + 2*x",
        "(x + 1)^2",
        "3*x + 5",
        "-x^2 + 2*x - 1"
    ]
    for expr in test_exprs:
        result = parse(expr)
        print(f"{expr} -> {to_string(result)}")