"""Multi-language test suite for the analyzer."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from analyzer import analyze_code

passed = 0
failed = 0

def check(desc, code, lang, expect_errors=None, expect_no_errors=None,
          expect_suggestions=None, expect_errors_count=None):
    global passed, failed
    r = analyze_code(code, lang)
    got = {e['type'] for e in r['errors']}
    # "Add Comments" suggestion always present; check specific suggestions
    suggestion_titles = {s['title'] for s in r.get('suggestions', [])}
    ok = True
    msg = f"[{lang}] {desc}"

    if expect_errors:
        missing = set(expect_errors) - got
        if missing:
            ok = False
            print(f"  FAIL {msg}: missing errors {missing}")

    if expect_no_errors:
        found = got & set(expect_no_errors)
        if found:
            ok = False
            print(f"  FAIL {msg}: unexpected errors {found}")

    if expect_errors_count is not None:
        if len(r['errors']) != expect_errors_count:
            ok = False
            print(f"  FAIL {msg}: expected {expect_errors_count} errors, got {len(r['errors'])}")

    if expect_suggestions is not None:
        missing_sug = set(expect_suggestions) - suggestion_titles
        if missing_sug:
            ok = False
            print(f"  FAIL {msg}: missing suggestions {missing_sug}")

    if ok:
        passed += 1
        print(f"  OK {msg}")
    else:
        failed += 1

# ===========================================================================
# PYTHON
# ===========================================================================
print("\n=== PYTHON ===")
check("clean syntax", 'x = 1\nprint(x)', 'python', expect_no_errors={"SyntaxError"})

check("missing colon", 'if x > 5\n  print(1)', 'python', expect_errors={"SyntaxError"})

check("assignment in condition", 'if x = 5:\n  pass', 'python', expect_errors={"AssignmentInCondition"})

check("infinite while loop", 'while True:\n  pass', 'python', expect_errors={"InfiniteLoopError"})

check("division guard needed", 'def f(x): return 10 / x', 'python', expect_errors={"ZeroDivisionError"})

check("bare except", 'try:\n  pass\nexcept:\n  pass', 'python', expect_errors={"BareExcept"})

check("name typo", 'total = 100\nprint(totl)', 'python', expect_errors={"NameError"})

check("mutable default arg", 'def f(x=[]): pass', 'python', expect_suggestions={"Mutable Default Argument"})

check("unused variable", 'x = 5\ny = 10\nprint(x)', 'python', expect_suggestions={"Unused Variable"})

check("None comparison with ==", 'if x == None: pass', 'python', expect_suggestions={"Use 'is' for None comparison"})

check("clean code no false pos", 'x = 1\nprint(x)\ny = x + 1\nprint(y)', 'python',
      expect_no_errors={"NameError", "ZeroDivisionError", "InfiniteLoopError", "SyntaxError"})

# ===========================================================================
# JAVASCRIPT
# ===========================================================================
print("\n=== JAVASCRIPT ===")
check("loose equality", 'if (x == 5) {}', 'javascript', expect_errors={"LooseEquality"})

check("missing radix", "parseInt('08')", 'javascript', expect_errors={"MissingRadix"})

check("var usage", 'var x = 5;', 'javascript', expect_suggestions={"Use let/const instead of var"})

check("missing semicolon", 'const x = 5', 'javascript', expect_errors={"MissingSemicolon"})

check("clean code", 'let x = 5;\nconsole.log(x);', 'javascript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

check("browser console.log", 'console.log("hi");', 'javascript',
      expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# TYPESCRIPT
# ===========================================================================
print("\n=== TYPESCRIPT ===")
check("loose equality TS", 'if (x == 5) {}', 'typescript', expect_errors={"LooseEquality"})

check("missing radix TS", "parseInt('08')", 'typescript', expect_errors={"MissingRadix"})

check("missing semicolon TS", 'const x: number = 5', 'typescript', expect_errors={"MissingSemicolon"})

check("clean code TS", 'let x: number = 5;\nconsole.log(x);', 'typescript',
      expect_no_errors={"MissingSemicolon", "LooseEquality"})

# ===========================================================================
# C
# ===========================================================================
print("\n=== C ===")
check("clean structure", '#include <stdio.h>\nint main() {\n  printf("hi");\n  return 0;\n}', 'c',
      expect_no_errors={"SyntaxError", "MissingSemicolon"})

check("void main", 'void main() {\n}', 'c', expect_errors={"MainReturnType"})

check("printf with &", '#include <stdio.h>\nint main() {\n  int x = 5;\n  printf("%d", &x);\n  return 0;\n}', 'c', expect_errors={"TypeMismatch"})

check("scanf without &", '#include <stdio.h>\nint main() {\n  int x;\n  scanf("%d", x);\n  return 0;\n}', 'c', expect_errors={"TypeMismatch"})

check("header without #", 'include <stdio.h>', 'c', expect_errors={"SyntaxError"})

check("use-after-free", '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  free(p);\n  *p = 5;\n  return 0;\n}', 'c', expect_errors={"UseAfterFree"})

check("double free", '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  free(p);\n  free(p);\n  return 0;\n}', 'c', expect_errors={"DoubleFree"})

check("memory leak", '#include <stdlib.h>\nint main() {\n  int *p = malloc(4);\n  return 0;\n}', 'c', expect_errors={"MemoryLeak"})

check("null ptr deref ->", 'int main() {\n  int *p = NULL;\n  p->x = 5;\n  return 0;\n}', 'c', expect_errors={"NullPointerDereference"})

check("null ptr deref *", 'int main() {\n  int *p = NULL;\n  *p = 5;\n  return 0;\n}', 'c', expect_errors={"NullPointerDereference"})

check("return local addr", 'int* foo() {\n  int buf[10];\n  return buf;\n}', 'c', expect_errors={"ReturnLocalAddress"})

check("off-by-one", 'int main() {\n  int arr[5];\n  for (int i = 0; i <= 5; i++) arr[i] = i;\n  return 0;\n}', 'c', expect_errors={"OffByOne"})

check("assignment in if", 'int main() {\n  int x;\n  if (x = 5) return 1;\n  return 0;\n}', 'c', expect_errors={"AssignmentInCondition"})

check("infinite recursion", 'void foo() {\n  foo();\n}', 'c', expect_errors={"InfiniteRecursion"})

check("div by zero", 'int main() {\n  int x = 10 / 0;\n  return 0;\n}', 'c', expect_errors={"DivisionByZero"})

check("mod by zero", 'int main() {\n  int y = 5 % 0;\n  return 0;\n}', 'c', expect_errors={"DivisionByZero"})

check("integer overflow", 'int main() {\n  int x = 2147483647;\n  return 0;\n}', 'c', expect_errors={"IntegerOverflow"})

check("shift overflow", 'int main() {\n  int x = 1 << 40;\n  return 0;\n}', 'c', expect_errors={"ShiftOverflow"})

check("string literal mod", 'int main() {\n  char *s = "hello";\n  s[0] = \'H\';\n  return 0;\n}', 'c', expect_errors={"StringLiteralModification"})

check("format mismatch", '#include <stdio.h>\nint main() {\n  printf("%s", 100);\n  return 0;\n}', 'c', expect_errors={"FormatMismatch"})

check("buffer underflow", 'int main() {\n  int arr[5];\n  arr[-1] = 0;\n  return 0;\n}', 'c', expect_errors={"BufferUnderflow"})

check("signed/unsigned cmp", 'int main() {\n  unsigned int u = 10;\n  int n = -1;\n  if (n < u) return 1;\n  return 0;\n}', 'c', expect_errors={"SignedUnsignedMismatch"})

check("seq point violation", 'int main() {\n  int z = 0;\n  z = z++ + ++z;\n  return 0;\n}', 'c', expect_errors={"SequencePointViolation"})

check("unsafe strcpy", 'int main() {\n  char buf[10];\n  strcpy(buf, "hello world");\n  return 0;\n}', 'c', expect_errors={"BufferOverflow"})

check("dead code after if(0)", 'int main() {\n  if (0) {\n    return 1;\n  }\n  return 0;\n}', 'c', expect_errors={"DeadCode"})

check("missing null check", '#include <stdlib.h>\nint main() {\n  int *p = malloc(100);\n  *p = 5;\n  return 0;\n}', 'c', expect_errors={"MissingNullCheck"})

check("wild pointer", 'int main() {\n  int *p;\n  *p = 5;\n  return 0;\n}', 'c', expect_errors={"WildPointer"})

check("declaration not deref", 'int main() {\n  int *ptr;\n  return 0;\n}', 'c',
      expect_no_errors={"WildPointer", "NullPointerDereference"})

check("longer not keyword", '#include <stdio.h>\nint main() {\n  printf("longer");\n  return 0;\n}', 'c',
      expect_no_errors={"MisspelledKeyword"})

check("clean no false mem", '#include <stdio.h>\nint main() {\n  int x = 5;\n  printf("%d", x);\n  return 0;\n}', 'c',
      expect_no_errors={"UseAfterFree", "DoubleFree", "InvalidFree", "NullPointerDereference",
                        "WildPointer", "MemoryLeak", "BufferOverflow"})

# ===========================================================================
# C++
# ===========================================================================
print("\n=== C++ ===")
check("use-after-free C++", '#include <cstdlib>\nint main() {\n  int *p = (int*)malloc(4);\n  free(p);\n  *p = 5;\n  return 0;\n}', 'c++', expect_errors={"UseAfterFree"})

check("double free C++", '#include <cstdlib>\nint main() {\n  int *p = (int*)malloc(4);\n  free(p);\n  free(p);\n  return 0;\n}', 'c++', expect_errors={"DoubleFree"})

check("nullptr deref", 'int main() {\n  int *p = nullptr;\n  *p = 5;\n  return 0;\n}', 'c++', expect_errors={"NullPointerDereference"})

check("memory leak C++", '#include <cstdlib>\nint main() {\n  int *p = (int*)malloc(4);\n  return 0;\n}', 'c++', expect_errors={"MemoryLeak"})

check("clean C++ no false pos", '#include <iostream>\nint main() {\n  int x = 5;\n  return 0;\n}', 'c++',
      expect_no_errors={"UseAfterFree", "DoubleFree", "InvalidFree", "MemoryLeak"})

# ===========================================================================
# C# - also in the "c,c++,c#,dart" semicolon block
# ===========================================================================
print("\n=== C# ===")
check("missing semicolon C#", 'int x = 5', 'c#', expect_errors={"MissingSemicolon"})
check("clean with semicolon C#", 'int x = 5;\nclass Foo {}', 'c#', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# DART - also in the "c,c++,c#,dart" semicolon block
# ===========================================================================
print("\n=== DART ===")
check("missing semicolon Dart", 'int x = 5', 'dart', expect_errors={"MissingSemicolon"})
check("clean with semicolon Dart", 'int x = 5;', 'dart', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# JAVA - NOT in the semicolon block; add to semicolon detection if needed
# ===========================================================================
print("\n=== JAVA ===")
check("clean Java class", 'class Foo {\n  int x = 5;\n}', 'java',
      expect_no_errors={"MissingSemicolon", "SyntaxError"})
check("Java missing semicolon", 'int x = 5', 'java', expect_errors={"MissingSemicolon"})
check("Java assignment", 'int x = 5;', 'java', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# KOTLIN - semicolons are optional; should NOT flag them
# ===========================================================================
print("\n=== KOTLIN ===")
check("Kotlin no semi needed", 'val x = 5', 'kotlin', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# GO - semicolons are inserted by compiler; should NOT flag
# ===========================================================================
print("\n=== GO ===")
check("Go no semi needed", 'package main\nfunc main() {}', 'go', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# RUST - requires semicolons
# ===========================================================================
print("\n=== RUST ===")
check("Rust missing semicolon", 'fn main() {\n  let x = 5\n}', 'rust', expect_errors={"MissingSemicolon"})
check("Rust clean", 'fn main() {\n  let x = 5;\n}', 'rust', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# SWIFT - semicolons are optional; should NOT flag
# ===========================================================================
print("\n=== SWIFT ===")
check("Swift no semi needed", 'let x = 5\nprint(x)', 'swift', expect_no_errors={"MissingSemicolon"})

# ===========================================================================
# SQL
# ===========================================================================
print("\n=== SQL ===")
check("= NULL comparison", 'SELECT * FROM t WHERE name = NULL', 'sql', expect_errors={"NullComparison"})
check("UPDATE without WHERE", 'UPDATE users SET name = "john"', 'sql', expect_errors={"MissingWHERE"})
check("DELETE without WHERE", 'DELETE FROM users', 'sql', expect_errors={"MissingWHERE"})
check("clean SQL", 'SELECT * FROM users WHERE id = 1', 'sql', expect_no_errors={"NullComparison", "MissingWHERE"})
check("INSERT no WHERE needed", 'INSERT INTO users VALUES (1, "a")', 'sql',
      expect_no_errors={"MissingWHERE"})

# ===========================================================================
# HTML
# ===========================================================================
print("\n=== HTML ===")
check("missing doctype", '<html><body>hello</body></html>', 'html', expect_errors={"MissingDoctype"})
check("unclosed tag", '<div><p>hello</div>', 'html', expect_errors={"SyntaxError"})
check("clean HTML", '<!DOCTYPE html>\n<html><body>hello</body></html>', 'html',
      expect_no_errors={"MissingDoctype"})
check("single valid tag", '<br>', 'html', expect_no_errors={"SyntaxError"})

# ===========================================================================
# CSS
# ===========================================================================
print("\n=== CSS ===")
check("missing CSS unit", 'body { margin: 10 }', 'css', expect_suggestions={"Missing CSS Unit"})
check("invalid color", 'body { color: 255 }', 'css', expect_errors={"InvalidColorValue"})
check("clean CSS", 'body { margin: 10px; color: red; }', 'css',
      expect_no_errors={"InvalidColorValue"})
check("CSS hex color valid", 'body { color: #fff; }', 'css', expect_no_errors={"InvalidColorValue"})
check("CSS rgba valid", 'body { color: rgba(0,0,0,.5); }', 'css', expect_no_errors={"InvalidColorValue"})
check("CSS hex invalid chars", 'body { color: #ggg; }', 'css', expect_errors={"InvalidColorValue"})
check("CSS hex mixed invalid", 'body { color: #12g45h; }', 'css', expect_errors={"InvalidColorValue"})
check("CSS hex valid 6digit", 'body { color: #ff00aa; }', 'css', expect_no_errors={"InvalidColorValue"})

# ===========================================================================
# NEW FEATURE: Python deep indentation
# ===========================================================================
print("\n=== PYTHON (deep indent) ===")
check("deep indentation warning",
      'def f():\n'
      '  if True:\n'
      '    if True:\n'
      '      if True:\n'
      '        if True:\n'
      '          if True:\n'
      '            if True:\n'
      '              if True:\n'
      '                if True:\n'
      '                  x = 1\n',
      'python',
      expect_suggestions={"Deep Indentation"})

# ===========================================================================
# NEW FEATURE: Rust-specific detection (unsafe, use-after-drop, borrow conflicts)
# ===========================================================================
print("\n=== RUST (specific) ===")
check("Rust unsafe block flagged",
      'unsafe { let x = 5; }', 'rust',
      expect_suggestions={"Unsafe Block"})
check("Rust use after drop",
      'fn main() {\n'
      '  let s = String::from("hi");\n'
      '  drop(s);\n'
      '  println!("{}", s);\n'
      '}', 'rust',
      expect_errors={"UseAfterDrop"})
check("Rust borrow conflict detected",
      'fn main() {\n'
      '  let mut x = 5;\n'
      '  let r1 = &x;\n'
      '  let r2 = &mut x;\n'
      '  println!("{}", r1);\n'
      '}', 'rust',
      expect_errors={"BorrowConflict"})

# ===========================================================================
# SUMMARY
# ===========================================================================
print(f"\n{'='*50}")
print(f"Passed: {passed}/{passed+failed}")
if failed:
    print(f"FAILED: {failed}")
else:
    print("All tests passed!")
print(f"Error types: 48 | Suggestion types: 19 | Combined: 67")

# Exit with error code if failed
if failed:
    sys.exit(1)
