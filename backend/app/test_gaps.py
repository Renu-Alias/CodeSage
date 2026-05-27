"""Check gap detection patterns."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.analyzer import analyze_code

checks = [
    ("print without parens", 'print "hello"\nx=5', 'python'),
    ("x == None", 'x=None\nif x == None:\n pass', 'python'),
    ("bare main()", 'main(){return 0;}', 'C'),
    ("unclosed div tag", '<html><body><div>hello</body></html>', 'html'),
    ("consistent indent", 'if True:\n    x=1\n  y=2', 'python'),
]

for desc, code, lang in checks:
    r = analyze_code(code, lang, "beginner")
    errs = [(e["type"], e["line"]) for e in r["errors"]]
    suggs = [s["title"] for s in r["suggestions"]]
    print(f"{desc}:")
    print(f"  errors: {errs}")
    print(f"  suggestions: {suggs}")
    if errs or suggs:
        print(f"  explanation: {r['explanation'][:150]}...")
    print()
