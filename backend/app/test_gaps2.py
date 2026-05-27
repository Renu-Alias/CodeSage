"""Test unclosed HTML tag detection."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.analyzer import analyze_code

tests = [
    ("properly closed", '<html><body><div>hello</div></body></html>', []),
    ("unclosed div", '<html><body><div>hello</body></html>', ["Unclosed"]),
    ("unclosed div 2", '<!DOCTYPE html>\n<html><body><div>hello\n</body></html>', ["Unclosed"]),
    ("unclosed span", '<div><span>hi</div>', ["Unclosed"]),
    ("bare main()", 'main(){\nreturn 0;\n}', ["MainReturnType"]),
    ("void main", 'void main(){\nreturn 0;\n}', ["MainReturnType"]),
]

for desc, code, expected_types in tests:
    r = analyze_code(code, "html" if "html" in code or "DOCTYPE" in code else "C", "beginner")
    got = {e["type"] for e in r["errors"]}
    ok = all(et in desc for et in expected_types)  # simple check
    err_list = [(e["type"], e["line"]) for e in r["errors"]]
    print(f"[{'OK' if ok else 'MISS'}] {desc}: {err_list}")
