from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


class Expr(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass


@dataclass
class Number(Expr):
    value: float

    def __str__(self) -> str:
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)


@dataclass
class Variable(Expr):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Neg(Expr):
    expr: Expr

    def __str__(self) -> str:
        return f"(-{self.expr})"


@dataclass
class Add(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} + {self.right})"


@dataclass
class Sub(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} - {self.right})"


@dataclass
class Mul(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} * {self.right})"


@dataclass
class Div(Expr):
    left: Expr
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} / {self.right})"


@dataclass
class Pow(Expr):
    base: Expr
    exp: Expr

    def __str__(self) -> str:
        return f"({self.base} ^ {self.exp})"


def to_string(expr: Expr) -> str:
    if isinstance(expr, Number):
        return str(expr)
    elif isinstance(expr, Variable):
        return expr.name
    elif isinstance(expr, Neg):
        return f"-{to_string(expr.expr)}"
    elif isinstance(expr, Add):
        return f"{to_string(expr.left)} + {to_string(expr.right)}"
    elif isinstance(expr, Sub):
        return f"{to_string(expr.left)} - {to_string(expr.right)}"
    elif isinstance(expr, Mul):
        return f"{to_string(expr.left)} * {to_string(expr.right)}"
    elif isinstance(expr, Div):
        return f"{to_string(expr.left)} / {to_string(expr.right)}"
    elif isinstance(expr, Pow):
        return f"{to_string(expr.base)} ^ {to_string(expr.exp)}"
    return str(expr)