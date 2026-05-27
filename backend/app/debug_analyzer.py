import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import analyzer

code = """#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int) * 5);
    free(ptr);
    ptr[0] = 100;
    free(ptr);
    return 0;
}"""
result = analyzer.analyze_code(code, 'c')

print("=== ERRORS ===")
for e in result['errors']:
    print(f"  Line {e['line']}: [{e['type']}]")

# Now check what vars are tracked
print("\n=== Check freed_vars ===")
lines = code.split('\n')
stack_vars = {}
malloc_vars = {}
freed_vars = set()
fn_params = set()

for idx, line in enumerate(lines):
    stripped = line.strip()
    free_match = __import__('re').search(r'\bfree\s*\(\s*(\w+)\s*\)', stripped)
    if free_match:
        freed_vars.add(free_match.group(1))

print(f"freed_vars: {freed_vars}")

# Check UseAfterFree
for freed_name in freed_vars:
    for idx, line in enumerate(lines):
        line_num = idx + 1
        code_only = analyzer._strip_c_line(line)
        if freed_name in code_only and 'free' not in code_only:
            free_occurrences = [li for li, l in enumerate(lines) if __import__('re').search(r'\bfree\s*\(\s*' + __import__('re').escape(freed_name) + r'\s*\)', l)]
            if free_occurrences:
                last_free_line = free_occurrences[-1] + 1
                print(f"  freed={freed_name}, line={line_num}, last_free={last_free_line}, after={line_num > last_free_line}")
                if line_num > last_free_line:
                    if __import__('re').search(r'\b' + __import__('re').escape(freed_name) + r'\b', code_only):
                        print(f"    Would flag: UseAfterFree for {freed_name} on line {line_num}")
