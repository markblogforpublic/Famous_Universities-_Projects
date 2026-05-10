from expr import Expr, Number, Variable, Neg, Add, Sub, Mul, Div, Pow


def simplify(expr: Expr) -> Expr:
    if isinstance(expr, Number):
        return expr

    if isinstance(expr, Variable):
        return expr

    if isinstance(expr, Neg):
        simplified = simplify(expr.expr)
        if isinstance(simplified, Number):
            return Number(-simplified.value)
        if isinstance(simplified, Neg):
            return simplified.expr
        return Neg(simplified)

    if isinstance(expr, Add):
        left = simplify(expr.left)
        right = simplify(expr.right)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
        if isinstance(left, Number) and left.value == 0:
            return right
        if isinstance(right, Number) and right.value == 0:
            return left
        return Add(left, right)

    if isinstance(expr, Sub):
        left = simplify(expr.left)
        right = simplify(expr.right)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        if isinstance(right, Number) and right.value == 0:
            return left
        return Sub(left, right)

    if isinstance(expr, Mul):
        left = simplify(expr.left)
        right = simplify(expr.right)
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
        if isinstance(left, Number):
            if left.value == 0:
                return Number(0)
            if left.value == 1:
                return right
        if isinstance(right, Number):
            if right.value == 0:
                return Number(0)
            if right.value == 1:
                return left
        return Mul(left, right)

    if isinstance(expr, Div):
        left = simplify(expr.left)
        right = simplify(expr.right)
        if isinstance(left, Number) and isinstance(right, Number):
            if right.value == 0:
                raise ValueError("Division by zero")
            return Number(left.value / right.value)
        if isinstance(right, Number) and right.value == 1:
            return left
        return Div(left, right)

    if isinstance(expr, Pow):
        base = simplify(expr.base)
        exp = simplify(expr.exp)
        if isinstance(exp, Number):
            if exp.value == 0:
                return Number(1)
            if exp.value == 1:
                return base
            if isinstance(base, Number):
                return Number(base.value ** exp.value)
        return Pow(base, exp)

    return expr


if __name__ == "__main__":
    from parser import parse
    from expr import to_string

    test_cases = [
        "0 + x",
        "1 * x",
        "0 * x",
        "x^1",
        "x^0",
        "x + 0",
        "(x + 1) + 2",
        "2 * x + 3 * x",
        "-(-x)",
        "x * 1 + 0"
    ]

    for expr in test_cases:
        parsed = parse(expr)
        result = simplify(parsed)
        print(f"{expr} -> {to_string(result)}")