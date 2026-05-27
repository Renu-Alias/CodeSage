"""Quick regression check after semicolon indent + explanation cleanup."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.analyzer import analyze_code

passed = 0; failed = 0
def t(desc, code, lang, checks):
    global passed, failed
    r = analyze_code(code, lang, "beginner")
    ok = True
    for key, val in checks.items():
        if key == "error_types":
            got = {e["type"] for e in r["errors"]}
            missing = set(val) - got
            if missing: ok = False; print(f"    missing errors: {missing}")
        elif key == "no_errors" and val and r["errors"]:
            ok = False; print(f"    expected 0 errors, got {len(r['errors'])}")
        elif key == "fixed_contains":
            for f in val:
                if f not in r["fixed_code"]: ok = False; print(f"    fixed missing: {f!r}")
        elif key == "fixed_not_contains":
            for f in val:
                if f in r["fixed_code"]: ok = False; print(f"    fixed should NOT contain: {f!r}")
    if ok: passed += 1
    else:
        failed += 1
        print(f"  FAIL {desc}: errors={[(e['type'], e['line']) for e in r['errors']]}")
        if "error_types" in checks: print(f"    expected: {checks['error_types']}")

print("Core checks...")
t("missing colon", "if x>5\n print(1)", "python", {"error_types": {"SyntaxError"}})
t("= vs ==", "if x=5:\n pass", "python", {"error_types": {"AssignmentInCondition"}})
t("infinite loop", "while True:\n pass", "python", {"error_types": {"InfiniteLoopError"}})
t("division guard", "return 10 / count", "python", {"error_types": {"ZeroDivisionError"}})
t("bare except", "except:\n pass", "python", {"error_types": {"BareExcept"}})
t("name typo", "total=100\nprint(totl)", "python", {"error_types": {"NameError"}})
t("JS == vs ===", "if(x==5){}", "javascript", {"error_types": {"LooseEquality"}})
t("JS parseInt", "parseInt('08')", "javascript", {"error_types": {"MissingRadix"}})
t("C void main", "void main(){\n}", "C", {"error_types": {"MainReturnType"}, "fixed_contains": {"int main"}})
t("C header typo", "#include <stdi.h>\nint main(){return 0;}", "C", {"fixed_contains": {"stdio.h"}})
t("C printf &x", "#include <stdio.h>\nint main(){int x=5;printf(\"%d\",&x);return 0;}", "C", {"fixed_not_contains": {"&x"}})
t("C scanf no &", "#include <stdio.h>\nint main(){int x;scanf(\"%d\",x);return 0;}", "C", {"fixed_contains": {"&x"}})
t("SQL = NULL", "SELECT * FROM t WHERE name = NULL", "sql", {"error_types": {"NullComparison"}})
t("HTML doctype", "<html><body>hello</body></html>", "html", {"error_types": {"MissingDoctype"}})
t("include without #", 'include <stdio.h>\nint main(){printf("hi");return 0;}', "C", {"error_types": {"SyntaxError"}, "fixed_contains": {"#include <stdio.h>"}})
t("include no semicolon", 'include <stdio.h>\nint main(){printf("hi");return 0;}', "C", {"fixed_not_contains": {"<stdio.h>;"}})

print(f"{passed}/{passed+failed} passed")
if failed: print(f"{failed} FAILED!")