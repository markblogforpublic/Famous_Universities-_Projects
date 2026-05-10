from expr import Expr, Number, Variable, Neg, Add, Sub, Mul, Div, Pow


def derive(expr: Expr, var: str) -> Expr:
    if isinstance(expr, Number):
        return Number(0)

    if isinstance(expr, Variable):
        return Number(1) if expr.name == var else Number(0)

    if isinstance(expr, Neg):
        return Neg(derive(expr.expr, var))

    if isinstance(expr, Add):
        return Add(derive(expr.left, var), derive(expr.right, var))

    if isinstance(expr, Sub):
        return Sub(derive(expr.left, var), derive(expr.right, var))

    if isinstance(expr, Mul):
        return Add(
            Mul(derive(expr.left, var), expr.right),
            Mul(expr.left, derive(expr.right, var))
        )

    if isinstance(expr, Div):
        return Div(
            Sub(
                Mul(derive(expr.left, var), expr.right),
                Mul(expr.left, derive(expr.right, var))
            ),
            Pow(expr.right, Number(2))
        )

    if isinstance(expr, Pow):
        if isinstance(expr.exp, Number):
            n = expr.exp.value
            return Mul(
                Mul(Number(n), Pow(expr.base, Number(n - 1))),
                derive(expr.base, var)
            )
        return Mul(
            Pow(expr.base, expr.exp),
            Mul(derive(expr.exp, var), Pow(expr.base, Sub(expr.exp, Number(1))))
        )

    return Number(0)


if __name__ == "__main__":
    from parser import parse
    from simplify import simplify
    from expr import to_string

    test_cases = [
        ("x^2 + 2*x", "x"),
        ("3*x^2 + 4*x + 5", "x"),
        ("x^3", "x"),
        ("sin(x)", "x"),
        ("x*y", "x"),
        ("(x + 1)^2", "x"),
        ("2*x - 3", "x"),
    ]

    for expr_str, var in test_cases:
        try:
            parsed = parse(expr_str)
            deriv = derive(parsed, var)
            simplified = simplify(deriv)
            print(f"d/d{var}({expr_str}) = {to_string(simplified)}")
        except Exception as e:
            print(f"d/d{var}({expr_str}) = Error: {e}")