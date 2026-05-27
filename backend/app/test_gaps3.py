"""Test all gap patterns with correct language."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.analyzer import analyze_code

tests = [
    ("properly closed html", '<html><body><div>hello</div></body></html>', "html", ["MissingDoctype"], "only doctype, no unclosed"),
    ("unclosed div", '<html><body><div>hello</body></html>', "html", ["SyntaxError"], "div left unclosed by wrong close"),
    ("unclosed span", '<div><span>hi</div>', "html", ["SyntaxError"], "span unclosed when div closed early"),
    ("bare main() C", 'main(){\nreturn 0;\n}', "C", ["MainReturnType"], "bare main detected"),
    ("void main C", 'void main(){\nreturn 0;\n}', "C", ["MainReturnType"], "void main detected"),
    ("== None Python", 'x=None\nif x == None:\n    pass', "python", ["Use 'is' for None"], "== None suggested as is None"),
    ("print without parens", 'print "hello"', "python", ["SyntaxError"], "print catches missing parens"),
]

for desc, code, lang, expected_types, note in tests:
    r = analyze_code(code, lang, "beginner")
    err_types = [e["type"] for e in r["errors"]]
    sug_titles = [s["title"] for s in r["suggestions"]]
    all_types = err_types + sug_titles
    ok = all(e in all_types for e in expected_types)
    status = "OK" if ok else "MISS"
    print(f"[{status}] {desc}: errors={err_types} suggestions={sug_titles}")
