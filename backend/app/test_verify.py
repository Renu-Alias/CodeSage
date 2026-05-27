"""
Comprehensive test of CodeSage analyzer.py — ALL error detection patterns.
"""
import sys, re
sys.path.insert(0, "backend/app")
from analyzer import analyze_code

passed = 0
failed = 0
total_checks = 0

def check(description, condition, detail=""):
    global passed, failed, total_checks
    total_checks += 1
    if condition:
        passed += 1
        print(f"  PASS: {description}")
    else:
        failed += 1
        print(f"  FAIL: {description}  {detail}")

def check_err(description, errors, field, expected):
    check(description, any(e.get(field) == expected for e in errors),
          f"(expected {field}={expected!r}, got {[(e.get('type'), e.get('message')) for e in errors]})")

def count_err_by_type(errors, etype):
    return sum(1 for e in errors if e.get("type") == etype)

# ============================================================================
# 1. PYTHON
# ============================================================================
print("\n=== PYTHON CHECKS ===")

# 1a. Missing colon
res = analyze_code("def hello()\n    pass", "python")
check("Missing colon detected",
      any("missing colon" in e.get("message","").lower()
          or "colon" in e.get("message","").lower()
          or "expected ':'" in e.get("message","")
          for e in res["errors"]))
# The syntax might be caught by AST as SyntaxError with "expected ':'"
check("Missing colon has fix", ":" in res.get("fixed_code", ""))

# 1b. Division by zero
res = analyze_code("def f(x):\n    return 10 / x", "python")
check_err("Division by zero detected", res["errors"], "type", "ZeroDivisionError")
check("Div by zero has fix", "if" in res.get("fixed_code", ""))

# 1c. Infinite loop (while True without break)
res = analyze_code("while True:\n    pass", "python")
check_err("Infinite loop detected", res["errors"], "type", "InfiniteLoopError")

# 1d. Unclosed bracket
res = analyze_code("x = [1, 2, 3\nprint(x)", "python")
check("Unclosed bracket detected",
      any("never closed" in e.get("message","").lower()
          for e in res["errors"]))

# 1e. Assignment in condition (= vs ==)
res = analyze_code("if x = 5:\n    print(x)", "python")
# May be caught by AST or regex
found_assignment = any("assignment" in e.get("type","").lower()
                       or "=" in e.get("message","") and "==" in e.get("message","")
                       for e in res["errors"])
found_syntax = any("SyntaxError" in e.get("type","")
                   for e in res["errors"])
check("Assignment in condition detected (or SyntaxError)",
      found_assignment or found_syntax)

# 1f. Name typo (variable misspelling)
res = analyze_code("total = 100\nprint(tota)", "python")  # 'tota' vs 'total'
check("Name typo detected",
      any("tota" in e.get("message","") or "NameError" in e.get("type","")
          for e in res["errors"]))

# 1g. Bare except
res = analyze_code("try:\n    pass\nexcept:\n    pass", "python")
check_err("Bare except detected", res["errors"], "type", "BareExcept")

# 1h. Mutable default argument
res = analyze_code("def f(x=[]):\n    return x", "python")
check("Mutable default suggested",
      any("Mutable" in s.get("title","") or "default" in s.get("message","").lower()
          for s in res["suggestions"]))

# 1i. Unclosed string
res = analyze_code("x = 'hello\nprint(x)", "python")
check("Unclosed string detected",
      any("never closed" in e.get("message","").lower()
          or "unterminated" in e.get("message","").lower()
          for e in res["errors"]))

# ============================================================================
# 2. JAVASCRIPT
# ============================================================================
print("\n=== JAVASCRIPT CHECKS ===")

# 2a. Missing semicolon
res = analyze_code("let x = 5\nconst y = 10", "javascript")
check_err("Missing semicolon detected (JS)", res["errors"], "type", "MissingSemicolon")
check("Missing semicolon has fix", ";" in res.get("fixed_code", ""))

# 2b. Loose equality (== vs ===)
res = analyze_code("if (x == 5) {\n  console.log('ok')\n}", "javascript")
check_err("Loose equality detected", res["errors"], "type", "LooseEquality")

# 2c. parseInt without radix
res = analyze_code("let x = parseInt('08')\nconsole.log(x)", "javascript")
check_err("Missing radix detected", res["errors"], "type", "MissingRadix")

# 2d. var usage suggestion
res = analyze_code("var x = 5\nconsole.log(x)", "javascript")
check("var usage suggested",
      any("var" in s.get("title","").lower()
          for s in res["suggestions"]),
      str(res["suggestions"]))

# ============================================================================
# 3. C/C++
# ============================================================================
print("\n=== C/C++ CHECKS ===")

# 3a. Typo header
res = analyze_code("#include <stdiio.h>\nint main() { return 0; }", "c")
check("Typo header detected",
      any("Did you mean" in e.get("message","") or "stdio.h" in e.get("message","").lower()
          for e in res["errors"]),
      str(res["errors"]))
check("Typo header has fix", "stdio.h" in res.get("fixed_code", ""))

# 3b. printf without stdio.h
res = analyze_code("int main() { printf(\"hello\"); return 0; }", "c")
check_err("printf without stdio.h detected", res["errors"], "type", "SyntaxError")

# 3c. printf(&var) — using address where value expected
res = analyze_code("#include <stdio.h>\nint main() { int x = 5; printf(\"%d\", &x); return 0; }", "c")
check("printf(&var) detected",
      any("printf" in e.get("message","") and "address" in e.get("message","").lower()
          for e in res["errors"]),
      str(res["errors"]))

# 3d. scanf without & — missing address
res = analyze_code("#include <stdio.h>\nint main() { int x; scanf(\"%d\", x); return 0; }", "c")
check("scanf missing & detected",
      any("scanf" in e.get("message","") and "address" in e.get("message","").lower()
          for e in res["errors"]),
      str(res["errors"]))

# 3e. void main
res = analyze_code("void main() {\n  printf(\"hi\");\n}", "c")
check_err("void main detected", res["errors"], "type", "MainReturnType")
check("void main has fix", "int main" in res.get("fixed_code", ""))

# 3f. = in conditions
res = analyze_code("int main() {\n  int x = 5;\n  if (x = 5) { return 0; }\n  return 0;\n}", "c")
check("= in condition detected (C)",
      any("assignment" in e.get("type","").lower() or "=" in e.get("message","")
          for e in res["errors"]),
      str(res["errors"]))

# 3g. Missing semicolons in C
res = analyze_code("int main() {\n  int x = 5\n  return 0\n}", "c")
check_err("Missing semicolon detected (C)", res["errors"], "type", "MissingSemicolon")

# 3h. Uninitialized variable
res = analyze_code("int main() {\n  int x;\n  return 0;\n}", "c")
check("Uninitialized variable suggested",
      any("Uninitialized" in s.get("title","")
          for s in res["suggestions"]))

# ============================================================================
# 4. SQL
# ============================================================================
print("\n=== SQL CHECKS ===")

# 4a. DELETE without WHERE
res = analyze_code("DELETE FROM users", "sql")
check_err("DELETE without WHERE detected", res["errors"], "type", "MissingWHERE")

# 4b. UPDATE without WHERE
res = analyze_code("UPDATE users SET name = 'x'", "sql")
check_err("UPDATE without WHERE detected", res["errors"], "type", "MissingWHERE")

# 4c. NULL = comparison
res = analyze_code("SELECT * FROM users WHERE name = NULL", "sql")
check_err("NULL comparison detected", res["errors"], "type", "NullComparison")

# ============================================================================
# 5. HTML
# ============================================================================
print("\n=== HTML CHECKS ===")

res = analyze_code("<html><head></head><body></body></html>", "html")
check_err("Missing doctype detected", res["errors"], "type", "MissingDoctype")

# ============================================================================
# 6. CSS
# ============================================================================
print("\n=== CSS CHECKS ===")

res = analyze_code("div {\n  width: 100\n}", "css")
check("Missing CSS unit suggested",
      any("Missing" in s.get("title","") and "Unit" in s.get("title","")
          for s in res["suggestions"]),
      str(res["suggestions"]))

# ============================================================================
# 7. DEMO SNIPPETS
# ============================================================================
print("\n=== DEMO SNIPPET CHECKS ===")

DEMO_AVERAGE = "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
DEMO_LOOP = "def calculate_total(prices):\n    total = 0\n    for i in range(len(prices)):\n        tax = i * price # Error here\n        total += p\n    return total"

res = analyze_code(DEMO_AVERAGE, "python")
check("Demo average returns errors", len(res["errors"]) > 0)
check("Demo average has ZeroDivisionError",
      any("ZeroDivisionError" in e.get("type","") for e in res["errors"]))
check("Demo average has explanation", len(res.get("explanation","")) > 0)
check("Demo average has fixed_code", "if not numbers" in res.get("fixed_code",""))

res = analyze_code(DEMO_LOOP, "python")
check("Demo loop returns errors", len(res["errors"]) > 0)
check("Demo loop has NameError",
      any("NameError" in e.get("type","") for e in res["errors"]))
check("Demo loop has explanation", len(res.get("explanation","")) > 0)
check("Demo loop has fixed_code", "for price in prices" in res.get("fixed_code",""))

# ============================================================================
# 8. FIXED CODE VERIFICATION
# ============================================================================
print("\n=== FIXED CODE VERIFICATION ===")

# Missing colon fix
res = analyze_code("def hello()\n    pass", "python")
fc = res.get("fixed_code","")
check("Missing colon fix: line ends with colon",
      any(l.strip().startswith("def") and l.strip().endswith(":") for l in fc.split("\n")))

# Division by zero fix
res = analyze_code("def f(x):\n    return 10 / x", "python")
fc = res.get("fixed_code","")
check("Div by zero fix: has guard",
      "if " in fc and "!= 0" in fc)

# Missing semicolon fix (JS)
res = analyze_code("let x = 5\nconst y = 10", "javascript")
fc = res.get("fixed_code","")
check("JS semicolon fix: lines end with ;",
      fc.strip().endswith(";"))

# void main fix (C)
res = analyze_code("void main() {\n  return 0;\n}", "c")
fc = res.get("fixed_code","")
check("C void main fix: int main",
      "int main" in fc)

# Typo header fix (C)
res = analyze_code("#include <stdiio.h>\nint main() { return 0; }", "c")
fc = res.get("fixed_code","")
check("C typo header fix: stdio.h",
      "#include <stdio.h>" in fc or "<stdio.h>" in fc)

# printf without stdio.h fix (C)
res = analyze_code("int main() { printf(\"hello\"); return 0; }", "c")
fc = res.get("fixed_code","")
check("C printf+stdio.h fix: includes stdio.h",
      "include <stdio.h>" in fc)

# ============================================================================
# SUMMARY
# ============================================================================
print(f"\n{'='*60}")
print(f"RESULTS: {passed}/{total_checks} passed, {failed}/{total_checks} failed")
if failed:
    print("SOME TESTS FAILED")
    sys.exit(1)
else:
    print("ALL TESTS PASSED!")
    sys.exit(0)
