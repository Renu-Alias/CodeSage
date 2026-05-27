"""New test cases for the C/C++ analyzer."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from analyzer import analyze_code

passed = 0
failed = 0

def check(desc, code, lang, expect_errors=None, expect_no_errors=None,
          expect_suggestions=None, expect_fixed_differs=False):
    global passed, failed
    r = analyze_code(code, lang)
    got = {e['type'] for e in r['errors']}
    ok = True

    if expect_errors:
        missing = set(expect_errors) - got
        if missing:
            ok = False
            print(f"  FAIL {desc}: missing errors {missing}")

    if expect_no_errors:
        found = got & set(expect_no_errors)
        if found:
            ok = False
            print(f"  FAIL {desc}: unexpected errors {found}")

    if expect_suggestions is not None:
        if len(r['suggestions']) != expect_suggestions:
            ok = False
            print(f"  FAIL {desc}: expected {expect_suggestions} suggestions, got {len(r['suggestions'])}")

    if expect_fixed_differs and r['fixed_code'].strip() == code.strip():
        ok = False
        print(f"  FAIL {desc}: fixed code identical to input")

    if ok:
        passed += 1
        print(f"  OK {desc}")
    else:
        failed += 1

# === CLEAN CODE ===
print("\n--- CLEAN CODE (no errors expected) ---")
check("clean C hello world",
      '#include <stdio.h>\nint main() {\n  printf("hello");\n  return 0;\n}',
      'c', expect_no_errors={"SyntaxError"})

check("clean C malloc + null check",
      '#include <stdlib.h>\nint main() {\n  int *p = malloc(10);\n  if (!p) return 1;\n  free(p);\n  return 0;\n}',
      'c', expect_no_errors={"MissingNullCheck", "MemoryLeak", "NullPointerDereference", "UseAfterFree", "DoubleFree"})

check("clean C++ new/delete",
      'int main() {\n  int* p = new int(5);\n  delete p;\n  return 0;\n}',
      'c++', expect_no_errors={"MemoryLeak", "NullPointerDereference"})

# === MEMORY ERRORS ===
print("\n--- MEMORY ERRORS ---")
check("use-after-free",
      '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  free(p);\n  *p = 5;\n  return 0;\n}',
      'c', expect_errors={"UseAfterFree"})

check("double free",
      '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  free(p);\n  free(p);\n  return 0;\n}',
      'c', expect_errors={"DoubleFree"})

check("memory leak",
      '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  return 0;\n}',
      'c', expect_errors={"MemoryLeak"})

check("invalid free (stack var)",
      'int main() {\n  int arr[10];\n  free(arr);\n  return 0;\n}',
      'c', expect_errors={"InvalidFree"})

check("malloc without null check",
      '#include <stdlib.h>\nint main() {\n  int *p = malloc(100);\n  *p = 5;\n  return 0;\n}',
      'c', expect_errors={"MissingNullCheck"})

check("null pointer dereference (->)",
      'int main() {\n  int *p = NULL;\n  p->x = 5;\n  return 0;\n}',
      'c', expect_errors={"NullPointerDereference"})

check("null pointer dereference (*)",
      'int main() {\n  int *p = NULL;\n  *p = 5;\n  return 0;\n}',
      'c', expect_errors={"NullPointerDereference"})

# === ARITHMETIC ERRORS ===
print("\n--- ARITHMETIC ERRORS ---")
check("division by literal zero",
      'int main() {\n  int x = 10 / 0;\n  return 0;\n}',
      'c', expect_errors={"DivisionByZero"})

check("modulo by literal zero",
      'int main() {\n  int y = 5 % 0;\n  return 0;\n}',
      'c', expect_errors={"DivisionByZero"})

check("integer overflow (literal INT_MAX)",
      'int main() {\n  int x = 2147483647;\n  return 0;\n}',
      'c', expect_errors={"IntegerOverflow"})

check("integer overflow (increment past max)",
      'int main() {\n  int x = 2147483640;\n  x = x + 1;\n  return 0;\n}',
      'c', expect_errors={"IntegerOverflow"})

check("shift overflow",
      'int main() {\n  int x = 1 << 40;\n  return 0;\n}',
      'c', expect_errors={"ShiftOverflow"})

# === POINTER ERRORS ===
print("\n--- POINTER ERRORS ---")
check("return local address",
      'int* foo() {\n  int buf[10];\n  return buf;\n}',
      'c', expect_errors={"ReturnLocalAddress"})

check("wild pointer",
      'int main() {\n  int *p;\n  *p = 5;\n  return 0;\n}',
      'c', expect_errors={"WildPointer"})

# === LOGIC ERRORS ===
print("\n--- LOGIC ERRORS ---")
check("assignment in condition",
      'int main() {\n  int x;\n  if (x = 5) return 1;\n  return 0;\n}',
      'c', expect_errors={"AssignmentInCondition"})

check("off-by-one loop",
      'int main() {\n  int arr[5];\n  for (int i = 0; i <= 5; i++) arr[i] = i;\n  return 0;\n}',
      'c', expect_errors={"OffByOne"})

check("infinite recursion",
      'void foo() {\n  foo();\n}',
      'c', expect_errors={"InfiniteRecursion"})

# === STRING/FORMAT ERRORS ===
print("\n--- STRING/FORMAT ERRORS ---")
check("string literal modification",
      'int main() {\n  char *s = "hello";\n  s[0] = \'H\';\n  return 0;\n}',
      'c', expect_errors={"StringLiteralModification"})

check("printf format mismatch (%s + int)",
      '#include <stdio.h>\nint main() {\n  printf("%s", 100);\n  return 0;\n}',
      'c', expect_errors={"FormatMismatch"})

# === UNDEFINED BEHAVIOR ===
print("\n--- UNDEFINED BEHAVIOR ---")
check("sequence point violation",
      'int main() {\n  int z = 0;\n  z = z++ + ++z;\n  return 0;\n}',
      'c', expect_errors={"SequencePointViolation"})

# === BUFFER ERRORS ===
print("\n--- BUFFER ERRORS ---")
check("buffer underflow",
      'int main() {\n  int arr[5];\n  arr[-1] = 0;\n  return 0;\n}',
      'c', expect_errors={"BufferUnderflow"})

check("unsafe strcpy",
      'int main() {\n  char buf[10];\n  strcpy(buf, "hello world");\n  return 0;\n}',
      'c', expect_errors={"BufferOverflow"})

# === SIGNED/UNSIGNED ===
print("\n--- SIGNED/UNSIGNED ---")
check("signed vs unsigned comparison",
      'int main() {\n  unsigned int u = 10;\n  int n = -1;\n  if (n < u) return 1;\n  return 0;\n}',
      'c', expect_errors={"SignedUnsignedMismatch"})

# === FALSE POSITIVE CHECKS ===
print("\n--- FALSE POSITIVE CHECKS ---")
check("'longer' in string not flagged as keyword",
      '#include <stdio.h>\nint main() {\n  printf("longer");\n  return 0;\n}',
      'c', expect_no_errors={"MisspelledKeyword"})

check("declaration not flagged as dereference",
      'int main() {\n  int *ptr;\n  return 0;\n}',
      'c', expect_no_errors={"WildPointer", "NullPointerDereference"})

# === FIXED CODE ===
print("\n--- FIXED CODE ---")
check("fixed code differs for assignment in condition",
      'int main() {\n  int x;\n  if (x = 5) return 1;\n  return 0;\n}',
      'c', expect_fixed_differs=True)

check("fixed code differs for off-by-one",
      'int main() {\n  int arr[5];\n  for (int i = 0; i <= 5; i++) arr[i] = i;\n  return 0;\n}',
      'c', expect_fixed_differs=True)

check("fixed code differs for void main",
      'void main() {\n}',
      'c', expect_fixed_differs=True)

# === C++ TESTS ===
print("\n--- C++ TESTS ---")
check("C++ use-after-free",
      '#include <cstdlib>\nint main() {\n  int *p = (int*)malloc(4);\n  free(p);\n  *p = 5;\n  return 0;\n}',
      'c++', expect_errors={"UseAfterFree"})

check("C++ double free",
      '#include <cstdlib>\nint main() {\n  int *p = (int*)malloc(4);\n  free(p);\n  free(p);\n  return 0;\n}',
      'c++', expect_errors={"DoubleFree"})

check("C++ null pointer dereference",
      'int main() {\n  int *p = nullptr;\n  *p = 5;\n  return 0;\n}',
      'c++', expect_errors={"NullPointerDereference"})

# === SUMMARY ===
print(f"\n{'='*40}")
print(f"Passed: {passed}/{passed+failed}")
if failed:
    print(f"FAILED: {failed}")
else:
    print("All tests passed!")
