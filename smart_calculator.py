import math
import re

# ─────────────────────────────────────────────
#  SmartCalc — The calculator students need
# ─────────────────────────────────────────────

HISTORY = []

# ── Helpers ──────────────────────────────────

def save_history(expression, result):
    HISTORY.append(f"  {expression} = {result}")
    if len(HISTORY) > 20:
        HISTORY.pop(0)

def show_history():
    if not HISTORY:
        print("\n  No history yet.\n")
    else:
        print("\n📜 Calculation History:")
        for item in HISTORY:
            print(item)
        print()

# ── 1. Basic Calculator ───────────────────────

def basic_calculator():
    print("\n📐 Basic Calculator")
    print("  Supports: + - * / ** // %")
    print("  Example: 3 * (4 + 2) ** 2")
    print("  Type 'back' to return.\n")

    while True:
        expr = input("  Enter expression: ").strip()
        if expr.lower() == "back":
            break
        try:
            # Only allow safe characters
            if re.search(r"[^0-9\s\+\-\*\/\(\)\.\%\*\s]", expr):
                raise ValueError("Invalid characters")
            result = eval(expr, {"__builtins__": {}})
            print(f"  = {result}\n")
            save_history(expr, result)
        except Exception:
            print("  ⚠️  Invalid expression. Try again.\n")

# ── 2. Unit Converter ────────────────────────

CONVERSIONS = {
    "length": {
        "km":  1000, "m": 1, "cm": 0.01, "mm": 0.001,
        "mile": 1609.34, "yard": 0.9144, "foot": 0.3048, "inch": 0.0254
    },
    "weight": {
        "kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495, "ton": 1000
    },
    "temperature": "special",
    "speed": {
        "km/h": 1, "m/s": 3.6, "mph": 1.60934, "knot": 1.852
    },
    "area": {
        "m2": 1, "km2": 1e6, "cm2": 0.0001, "ft2": 0.092903, "acre": 4046.86
    },
    "data": {
        "bit": 1, "byte": 8, "kb": 8000, "mb": 8e6, "gb": 8e9, "tb": 8e12
    },
}

def convert_temperature(value, from_unit, to_unit):
    to_celsius = {"c": lambda x: x, "f": lambda x: (x-32)*5/9, "k": lambda x: x-273.15}
    from_celsius = {"c": lambda x: x, "f": lambda x: x*9/5+32, "k": lambda x: x+273.15}
    if from_unit not in to_celsius or to_unit not in from_celsius:
        return None
    return from_celsius[to_unit](to_celsius[from_unit](value))

def unit_converter():
    print("\n📏 Unit Converter")
    cats = list(CONVERSIONS.keys())
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c.title()}")
    print("  Type 'back' to return.\n")

    choice = input("  Choose category: ").strip()
    if choice.lower() == "back":
        return
    try:
        cat = cats[int(choice) - 1]
    except (ValueError, IndexError):
        print("  Invalid choice.\n")
        return

    if cat == "temperature":
        print("  Units: C, F, K")
        try:
            val = float(input("  Value: "))
            fu = input("  From (C/F/K): ").strip().lower()
            tu = input("  To   (C/F/K): ").strip().lower()
            result = convert_temperature(val, fu, tu)
            if result is None:
                print("  ⚠️  Invalid units.\n")
            else:
                out = f"{val}{fu.upper()} → {round(result, 4)}{tu.upper()}"
                print(f"  = {round(result, 4)} {tu.upper()}\n")
                save_history(out, round(result, 4))
        except ValueError:
            print("  ⚠️  Invalid input.\n")
    else:
        units = CONVERSIONS[cat]
        print(f"  Units: {', '.join(units.keys())}")
        try:
            val = float(input("  Value: "))
            fu = input("  From: ").strip().lower()
            tu = input("  To:   ").strip().lower()
            if fu not in units or tu not in units:
                print("  ⚠️  Unknown unit.\n")
                return
            result = val * units[fu] / units[tu]
            out = f"{val} {fu} → {tu}"
            print(f"  = {round(result, 6)} {tu}\n")
            save_history(out, round(result, 6))
        except ValueError:
            print("  ⚠️  Invalid input.\n")

# ── 3. Equation Solver ───────────────────────

def solve_quadratic():
    print("\n🔢 Quadratic Equation Solver  (ax² + bx + c = 0)")
    try:
        a = float(input("  a = "))
        b = float(input("  b = "))
        c = float(input("  c = "))
        if a == 0:
            if b == 0:
                print("  Not an equation.\n")
            else:
                x = -c / b
                print(f"  Linear solution: x = {x}\n")
                save_history(f"{a}x²+{b}x+{c}=0", f"x={x}")
            return
        disc = b**2 - 4*a*c
        if disc > 0:
            x1 = (-b + math.sqrt(disc)) / (2*a)
            x2 = (-b - math.sqrt(disc)) / (2*a)
            print(f"  ✅ Two real roots: x₁ = {round(x1,4)}, x₂ = {round(x2,4)}\n")
            save_history(f"{a}x²+{b}x+{c}=0", f"x1={round(x1,4)}, x2={round(x2,4)}")
        elif disc == 0:
            x = -b / (2*a)
            print(f"  ✅ One root: x = {round(x,4)}\n")
            save_history(f"{a}x²+{b}x+{c}=0", f"x={round(x,4)}")
        else:
            real = -b / (2*a)
            imag = math.sqrt(-disc) / (2*a)
            print(f"  Complex roots: x = {round(real,4)} ± {round(imag,4)}i\n")
            save_history(f"{a}x²+{b}x+{c}=0", f"{round(real,4)}±{round(imag,4)}i")
    except ValueError:
        print("  ⚠️  Enter valid numbers.\n")

# ── 4. Statistics Calculator ─────────────────

def statistics_calc():
    print("\n📊 Statistics Calculator")
    raw = input("  Enter numbers separated by spaces or commas: ")
    try:
        nums = [float(x) for x in re.split(r"[,\s]+", raw.strip()) if x]
        if not nums:
            raise ValueError
        n = len(nums)
        total = sum(nums)
        mean = total / n
        sorted_nums = sorted(nums)
        mid = n // 2
        median = sorted_nums[mid] if n % 2 else (sorted_nums[mid-1] + sorted_nums[mid]) / 2
        variance = sum((x - mean)**2 for x in nums) / n
        std_dev = math.sqrt(variance)

        from collections import Counter
        freq = Counter(nums)
        max_freq = max(freq.values())
        modes = [k for k, v in freq.items() if v == max_freq]

        print(f"\n  Count   : {n}")
        print(f"  Sum     : {round(total, 4)}")
        print(f"  Mean    : {round(mean, 4)}")
        print(f"  Median  : {round(median, 4)}")
        print(f"  Mode    : {modes if max_freq > 1 else 'No mode'}")
        print(f"  Min     : {min(nums)}")
        print(f"  Max     : {max(nums)}")
        print(f"  Range   : {round(max(nums)-min(nums), 4)}")
        print(f"  Std Dev : {round(std_dev, 4)}")
        print(f"  Variance: {round(variance, 4)}\n")

        save_history(f"Stats({nums})", f"mean={round(mean,4)}, std={round(std_dev,4)}")
    except (ValueError, ZeroDivisionError):
        print("  ⚠️  Invalid input.\n")

# ── 5. Percentage Tools ──────────────────────

def percentage_tools():
    print("\n💯 Percentage Tools")
    print("  1. What is X% of Y?")
    print("  2. X is what % of Y?")
    print("  3. % increase / decrease")
    print("  4. Add / subtract tax or discount")
    print("  Type 'back' to return.\n")

    choice = input("  Choose: ").strip()

    try:
        if choice == "1":
            x = float(input("  X (percent): "))
            y = float(input("  Y (value): "))
            result = (x / 100) * y
            print(f"  {x}% of {y} = {round(result, 4)}\n")
            save_history(f"{x}% of {y}", round(result, 4))

        elif choice == "2":
            x = float(input("  X (part): "))
            y = float(input("  Y (whole): "))
            result = (x / y) * 100
            print(f"  {x} is {round(result, 2)}% of {y}\n")
            save_history(f"{x}/{y}*100", f"{round(result,2)}%")

        elif choice == "3":
            old = float(input("  Original value: "))
            new = float(input("  New value: "))
            change = ((new - old) / old) * 100
            direction = "increase" if change >= 0 else "decrease"
            print(f"  {round(abs(change), 2)}% {direction}\n")
            save_history(f"{old}→{new}", f"{round(change,2)}%")

        elif choice == "4":
            val = float(input("  Original value: "))
            pct = float(input("  Tax / Discount %: "))
            mode = input("  Add or subtract? (a/s): ").strip().lower()
            amount = (pct / 100) * val
            result = val + amount if mode == "a" else val - amount
            label = "After adding" if mode == "a" else "After subtracting"
            print(f"  {label} {pct}%: {round(result, 4)}\n")
            save_history(f"{val} ± {pct}%", round(result, 4))

        elif choice.lower() == "back":
            return
        else:
            print("  Invalid choice.\n")
    except (ValueError, ZeroDivisionError):
        print("  ⚠️  Invalid input.\n")

# ── 6. Number Tools ──────────────────────────

def number_tools():
    print("\n🔢 Number Tools")
    print("  1. Prime check")
    print("  2. Factorial")
    print("  3. Fibonacci sequence")
    print("  4. GCD & LCM")
    print("  5. Number base converter (decimal ↔ binary/hex/octal)")
    print("  Type 'back' to return.\n")

    choice = input("  Choose: ").strip()

    try:
        if choice == "1":
            n = int(input("  Number: "))
            if n < 2:
                print(f"  {n} is NOT prime.\n")
            elif all(n % i != 0 for i in range(2, int(math.sqrt(n))+1)):
                print(f"  ✅ {n} IS prime.\n")
            else:
                print(f"  ❌ {n} is NOT prime.\n")

        elif choice == "2":
            n = int(input("  Number (0–20): "))
            n = max(0, min(n, 20))
            result = math.factorial(n)
            print(f"  {n}! = {result}\n")
            save_history(f"{n}!", result)

        elif choice == "3":
            n = int(input("  How many terms? (1–30): "))
            n = max(1, min(n, 30))
            seq = [0, 1]
            while len(seq) < n:
                seq.append(seq[-1] + seq[-2])
            print(f"  {seq[:n]}\n")
            save_history(f"Fibonacci({n})", seq[n-1])

        elif choice == "4":
            a = int(input("  First number: "))
            b = int(input("  Second number: "))
            gcd = math.gcd(a, b)
            lcm = abs(a * b) // gcd
            print(f"  GCD = {gcd}, LCM = {lcm}\n")
            save_history(f"GCD/LCM({a},{b})", f"{gcd}/{lcm}")

        elif choice == "5":
            n = int(input("  Decimal number: "))
            print(f"  Binary : {bin(n)}")
            print(f"  Octal  : {oct(n)}")
            print(f"  Hex    : {hex(n).upper()}\n")
            save_history(f"Convert({n})", f"bin={bin(n)} hex={hex(n)}")

        elif choice.lower() == "back":
            return
        else:
            print("  Invalid choice.\n")
    except (ValueError, ZeroDivisionError):
        print("  ⚠️  Invalid input.\n")

# ── Main Menu ────────────────────────────────

def main():
    print("=" * 50)
    print("   🧮  SmartCalc — The Student Calculator")
    print("   Everything you need, one place.")
    print("=" * 50)

    menu = {
        "1": ("📐 Basic Calculator",      basic_calculator),
        "2": ("📏 Unit Converter",         unit_converter),
        "3": ("🔢 Quadratic Solver",       solve_quadratic),
        "4": ("📊 Statistics Calculator",  statistics_calc),
        "5": ("💯 Percentage Tools",       percentage_tools),
        "6": ("🔣 Number Tools",           number_tools),
        "7": ("📜 View History",           show_history),
    }

    while True:
        print("\nWhat do you need?")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        print("  8. Exit")

        choice = input("\nChoose: ").strip()
        if choice in menu:
            menu[choice][1]()
        elif choice == "8":
            print("\n✅ Goodbye! Keep calculating, keep learning! 🚀\n")
            break
        else:
            print("  Invalid choice. Enter a number 1–8.")

if __name__ == "__main__":
    main()
