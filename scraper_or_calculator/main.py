import argparse

def calculate(op: str, a: float, b: float) -> float:
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b
    raise ValueError("Invalid operation.")

def main():
    parser = argparse.ArgumentParser(description="Simple CLI calculator")
    parser.add_argument("--op", required=True, choices=["add", "sub", "mul", "div"],
                        help="Operation: add, sub, mul, div")
    parser.add_argument("--a", required=True, type=float, help="First number")
    parser.add_argument("--b", required=True, type=float, help="Second number")
    args = parser.parse_args()

    try:
        result = calculate(args.op, args.a, args.b)
        print(result)
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
