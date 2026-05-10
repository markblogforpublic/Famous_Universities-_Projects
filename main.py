from parser import parse
from expr import to_string
from simplify import simplify
from derivative import derive


def eval_command(cmd: str) -> str:
    cmd = cmd.strip()

    if cmd.lower() in ("quit", "exit", "q"):
        return None

    if not cmd:
        return ""

    if cmd.startswith("d/d"):
        parts = cmd.split("/")
        if len(parts) >= 2:
            var = parts[1].strip()
            expr_part = cmd.split("(", 1)
            if len(expr_part) >= 2 and expr_part[1].endswith(")"):
                expr = expr_part[1][:-1].strip()
                try:
                    parsed = parse(expr)
                    deriv = derive(parsed, var)
                    result = simplify(deriv)
                    return to_string(result)
                except Exception as e:
                    return f"Error: {e}"

    if cmd.startswith("simplify(") and cmd.endswith(")"):
        expr = cmd[9:-1].strip()
        try:
            parsed = parse(expr)
            result = simplify(parsed)
            return to_string(result)
        except Exception as e:
            return f"Error: {e}"

    try:
        parsed = parse(cmd)
        result = simplify(parsed)
        return to_string(result)
    except Exception as e:
        return f"Error: {e}"


def main():
    print("=" * 50)
    print("  符号计算与代数系统")
    print("  Symbolic Computation System")
    print("=" * 50)
    print()
    print("用法:")
    print("  输入表达式直接计算: x^2 + 2*x")
    print("  求导: d/dx(x^2 + 2*x)")
    print("  化简: simplify(2*x + 4 - x + 2)")
    print("  退出: quit, exit, q")
    print()
    print("-" * 50)

    while True:
        try:
            cmd = input("> ")
            result = eval_command(cmd)
            if result is None:
                print("再见!")
                break
            if result:
                print(result)
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()