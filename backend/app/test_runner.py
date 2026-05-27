import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import analyzer

code = open(os.path.join(os.path.dirname(__file__), 'test_c_code.txt')).read()
result = analyzer.analyze_code(code, 'c')

print('=== ERRORS ===')
for e in result['errors']:
    print(f"  Line {e['line']}: [{e['type']}] {e['message'][:120]}")
print()
print('=== SUGGESTIONS ===')
for s in result['suggestions']:
    print(f"  Line {s['line']}: [{s['title']}] {s['message'][:120]}")
print()

orig = open(os.path.join(os.path.dirname(__file__), 'test_c_code.txt')).read()
if result['fixed_code'].strip() == orig.strip():
    print('WARNING: Fixed code is IDENTICAL to input!')
else:
    print('OK: Fixed code differs from input')
    
# Count
print(f"\nTotal errors: {len(result['errors'])}")
print(f"Total suggestions: {len(result['suggestions'])}")
