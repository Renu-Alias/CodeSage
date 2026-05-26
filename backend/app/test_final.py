import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.analyzer import analyze_code

def test(name, code, lang, expect_errors=None, expect_suggestions=None):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    r = analyze_code(code, lang, "beginner")
    print(f"Errors: {len(r['errors'])} | Suggestions: {len(r['suggestions'])}")
    for e in r["errors"]:
        print(f"  ERR [{e['type']}] L{e['line']}: {e['message'][:100]}")
    for s in r["suggestions"]:
        print(f"  SUG [{s['title']}] L{s['line']}: {s['message'][:100]}")
    print("\nFixed code:")
    print(r["fixed_code"])
    print("\nExplanation snippet:")
    lines = r["explanation"].split("\n")
    for l in lines[:15]:
        print(l)
    if expect_errors is not None and len(r["errors"]) != expect_errors:
        print(f"  *** FAIL: expected {expect_errors} errors, got {len(r['errors'])}")
    if expect_suggestions is not None and len(r["suggestions"]) != expect_suggestions:
        print(f"  *** FAIL: expected {expect_suggestions} suggestions, got {len(r['suggestions'])}")
    if "### What each line does" in r["explanation"]:
        idx = r["explanation"].index("### What each line does")
        snippet = r["explanation"][idx:idx+400]
        if "stdo.h" in snippet:
            print("  *** FAIL: 'What each line does' still shows original buggy code!")
    return r

# Test 1: printf with &var
r1 = test("printf with &var",
    '#include <stdio.h>\nint main() {\n  int x = 5;\n  printf("%d", &x);\n  return 0;\n}',
    "C", expect_errors=1)

# Test 2: scanf without &
r2 = test("scanf without &",
    '#include <stdio.h>\nint main() {\n  int x;\n  scanf("%d", x);\n  return 0;\n}',
    "C", expect_errors=1)

# Test 3: C code with stdo.h typo (no dup stdio, shows fixed code in explanation)
r3 = test("C with stdo.h typo",
    '#include <stdo.h>\n\nint main() {\n  int numbers[] = {1, 2, 3, 4, 5};\n  int total = 5;\n \n  printf("%d", total);\n  return 0;\n}',
    "C", expect_errors=1)

# Test 4: Python missing colon with fix
r4 = test("Python missing colon",
    "x = 5\nif x > 5\n    print('big')",
    "python", expect_errors=1)

# Test 5: JS missing semicolons
r5 = test("JS missing semicolons",
    "let x = 5\nconst y = 10",
    "javascript", expect_errors=2)

# Test 6: Python div by zero
r6 = test("Python div by zero",
    "result = 10 / count",
    "python", expect_errors=1)

# Test 7: Correct C code (no errors)
r7 = test("Correct C code",
    "#include <stdio.h>\n\nint main() {\n  printf(\"hello\");\n  return 0;\n}",
    "C", expect_errors=0)

print("\n\n=== ALL TESTS DONE ===")
