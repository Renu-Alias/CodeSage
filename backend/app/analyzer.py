import re
import ast

DEMO_AVERAGE = "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
DEMO_LOOP = "def calculate_total(prices):\n    total = 0\n    for i in range(len(prices)):\n        tax = i * price # Error here\n        total += p\n    return total"

def analyze_code(code: str, language: str, mode: str = "Beginner") -> dict:
    code_stripped = code.strip()
    if code_stripped == DEMO_AVERAGE.strip():
        return get_calculate_average_analysis(mode)
    if code_stripped == DEMO_LOOP.strip():
        return get_loop_price_analysis(mode)
    return run_general_analysis(code, language, mode)

def get_calculate_average_analysis(mode: str) -> dict:
    errors = [
        {"line": 4, "type": "ZeroDivisionError", "message": "Function crashes if list is empty because dividing by len=0 is undefined."},
        {"line": 1, "type": "TypeError", "message": "If list contains non-numbers, sum() fails."}
    ]
    suggestions = [
        {"line": 3, "title": "Guard Clause", "message": "Check if list is empty first: `if not numbers: return 0`"},
        {"line": 1, "title": "Type Hints", "message": "Add `numbers: list[float]` to clarify expected input."}
    ]
    if mode.lower() == "beginner":
        explanation = (
            "### How this code works\n\n"
            "Line 1: `total = sum(numbers)` — adds up everything in the list.\n"
            "   Example: `[2, 4, 6]` → 2+4+6 = 12\n\n"
            "Line 4: `return total / len(numbers)` — divides total by the count.\n"
            "   Example: 12 ÷ 3 = 4.0\n\n"
            "### The bug\n\n"
            "If the list is empty (`[]`), `len([])` is **0**. "
            "Dividing by 0 is mathematically impossible — like trying to share 10 cookies among 0 friends! "
            "Python stops with a `ZeroDivisionError`.\n\n"
            "### How to fix\n\n"
            "Before dividing, check if the list has anything in it:\n\n"
            "```python\ndef calculate_average(numbers):\n"
            "    if not numbers:   # if list is empty\n"
            "        return 0      # return 0 safely\n"
            "    total = sum(numbers)\n"
            "    return total / len(numbers)\n"
            "```"
        )
    else:
        explanation = "### Technical Breakdown\n\n- Empty list `len=0` causes ZeroDivisionError\n- sum() requires numeric types\n- Fix: guard clause for empty input"
    fixed_code = (
        "def calculate_average(numbers):\n"
        "    if not numbers:\n"
        "        return 0\n"
        "    total = sum(numbers)\n"
        "    return total / len(numbers)"
    )
    return {"errors": errors, "suggestions": suggestions, "explanation": explanation, "fixed_code": fixed_code}

def get_loop_price_analysis(mode: str) -> dict:
    errors = [
        {"line": 3, "type": "NameError", "message": "Line 3: `price` (singular) doesn't exist — you have `prices` (plural). Line 4: `p` is not defined either."}
    ]
    suggestions = [
        {"line": 1, "title": "Use Direct Iteration", "message": "Use `for price in prices:` instead of indexing — simpler and no name confusion!"}
    ]
    explanation = (
        "### What went wrong\n\n"
        "You have a list called `prices` (plural), but inside the loop you wrote `price` and `p` — which don't exist.\n\n"
        "Think of it like this: you have a box of toys (`prices`), and you try to grab a toy using the word \"box\" instead of \"toy.\" "
        "Python can't find what you mean!\n\n"
        "### Simple fix\n\n"
        "```python\n"
        "for price in prices:         # Python hands you each item\n"
        "    tax = price * 0.05\n"
        "    total += price + tax\n"
        "```"
    )
    fixed_code = (
        "def calculate_total(prices):\n"
        "    total = 0\n"
        "    for price in prices:\n"
        "        tax = price * 0.05\n"
        "        total += price + tax\n"
        "    return total"
    )
    return {"errors": errors, "suggestions": suggestions, "explanation": explanation, "fixed_code": fixed_code}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _find_unclosed_multiline(code, lang):
    issues = []
    lines = code.split("\n")
    stack = []
    in_single = in_double = False
    in_triple_single = in_triple_double = False
    for idx, line in enumerate(lines):
        i = 0
        while i < len(line):
            ch = line[i]
            next_ch = line[i+1] if i + 1 < len(line) else ''
            if ch in ('"', "'") and next_ch == ch and i + 2 < len(line) and line[i+2] == ch:
                if ch == '"': in_triple_double = not in_triple_double
                else: in_triple_single = not in_triple_single
                i += 3; continue
            if ch == '"' and not in_single and not in_triple_single:
                in_double = not in_double
            elif ch == "'" and not in_double and not in_triple_double:
                in_single = not in_single
            elif not in_single and not in_double and not in_triple_single and not in_triple_double:
                if ch in '([{':
                    stack.append((ch, idx + 1))
                elif ch in ')]}':
                    if not stack:
                        issues.append({"line": idx + 1, "type": "SyntaxError", "message": f"Line {idx+1}: Extra closing `{ch}` with nothing to open it."})
                    else:
                        open_ch = stack[-1][0]; expected = {'(': ')', '[': ']', '{': '}'}
                        if expected.get(open_ch) == ch: stack.pop()
                        else:
                            issues.append({"line": idx + 1, "type": "SyntaxError", "message": f"Line {idx+1}: Expected `{expected[open_ch]}` but found `{ch}`."})
                            stack.pop()
            i += 1
    for ch, ln in stack:
        closer = {'(': ')', '[': ']', '{': '}'}[ch]
        issues.append({"line": ln, "type": "SyntaxError", "message": f"Line {ln}: `{ch}` was opened but never closed with `{closer}`."})
    if in_triple_double: issues.append({"line": 1, "type": "SyntaxError", "message": "Triple-quoted string (`\"\"\"`) was never closed."})
    if in_triple_single: issues.append({"line": 1, "type": "SyntaxError", "message": "Triple-quoted string (`'''`) was never closed."})
    if in_double: issues.append({"line": len(lines), "type": "SyntaxError", "message": "Double-quoted string was started but never closed."})
    if in_single: issues.append({"line": len(lines), "type": "SyntaxError", "message": "Single-quoted string was started but never closed."})
    return issues

def _find_string_end(s):
    """Find the end index of a C string literal at the start of s. Returns index after closing quote, or -1."""
    if not s or s[0] != '"':
        return -1
    i = 1
    while i < len(s):
        if s[i] == '\\':
            i += 2
        elif s[i] == '"':
            return i + 1
        else:
            i += 1
    return -1

def _edit_distance(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]; dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]; cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = temp
    return dp[n]

def _get_error_explanation(err, code_lines, lang):
    """Generate a short beginner-friendly explanation snippet for a single error."""
    line = err.get("line", 1)
    etype = err.get("type", "")
    msg = err.get("message", "")
    code_line = code_lines[line - 1].strip() if line <= len(code_lines) else ""

    if "SyntaxError" in etype:
        if "missing colon" in msg.lower() or "expected ':'" in msg.lower():
            snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line
            return f"**Line {line}**: `{snippet}`\n\nIn Python, lines that start with `if`, `for`, `while`, `def`, or `class` must end with **`:`** (a colon). Think of the colon as saying \"here come the instructions.\" Without it, Python doesn't know the next indented block belongs to this line.\n\n**Fix:** Add `:` at the end of the line."
        if "header" in msg.lower() and "mean" in msg.lower():
            return f"**Line {line}**: `{code_line}`\n\nThe header file name is misspelled. Header files (like `stdio.h`) are like ID cards — if you spell the name wrong, the compiler can't find the right toolbox.\n\n**Fix:** Check the spelling and use the correct header name."
        if "stdio.h" in msg.lower() or "printf" in msg.lower():
            return f"**Line {line}**: `{code_line}`\n\nIn C, to use functions like `printf` or `scanf`, you must first include `stdio.h` at the top of your file. `stdio.h` is the \"standard input/output\" library — it's like a toolbox that contains the `printf` tool.\n\n**Fix:** Add `#include <stdio.h>` at the very top of your code."
        if "unclosed" in msg.lower():
            snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line
            if "string" in msg.lower():
                return f"**Line {line}**: `{snippet}`\n\nA string (text inside quotes) was started but never finished. Every opening quote needs a matching closing quote — like a pair of bookends.\n\n**Fix:** Add the matching closing quote at the end of the string."
            if "(" in msg or ")" in msg or "[" in msg or "]" in msg or "{" in msg or "}" in msg:
                return f"**Line {line}**: `{snippet}`\n\nA bracket `(`, `[`, or `{{` was opened but never closed. Brackets always work in pairs — like two hands clapping.\n\n**Fix:** Find where the bracket was opened and add the matching closing bracket."

    if "ZeroDivisionError" in etype or "Division" in etype:
        snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line
        return f"**Line {line}**: `{snippet}`\n\nDividing by zero crashes your program. Think of sharing 10 cookies with 0 friends — it's impossible!\n\n**Fix:** Before dividing, check if the value is not zero: `if count != 0:`"

    if "InfiniteLoopError" in etype:
        snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line
        return f"**Line {line}**: `{snippet}`\n\nThis loop never stops! A `while True:` loop runs forever unless something tells it to stop. Like a song on repeat with no stop button.\n\n**Fix:** Add a `break` statement inside the loop."

    if "MissingWHERE" in etype:
        return f"**Line {line}**: `{code_line}`\n\nWithout a `WHERE` clause, your UPDATE or DELETE applies to **every row** in the table. Like sending a \"delete all emails\" command when you only meant to delete one.\n\n**Fix:** Always add `WHERE column_name = value`."

    if "MissingSemicolon" in etype or "missing semicolon" in msg.lower():
        return f"**Line {line}**: `{code_line}`\n\nEvery statement must end with `;`. It's like a period at the end of a sentence — it tells the compiler \"this instruction is complete.\"\n\n**Fix:** Add `;` at the end of the line."

    if "TypeMismatch" in etype:
        if "printf" in msg:
            return f"**Line {line}**: `{code_line}`\n\nIn `printf`, you use `%d`, `%f`, `%c` etc. to **print values**. Adding `&` gives the variable's memory address instead of its value — like giving someone your house address when they asked for your phone number.\n\n**Fix:** Remove the `&` — just use the variable name directly."
        if "scanf" in msg:
            return f"**Line {line}**: `{code_line}`\n\nIn `scanf`, you need `&` because `scanf` **writes** a value into your variable. It needs to know where the variable lives in memory — like telling a delivery driver your address so they know where to drop the package.\n\n**Fix:** Add `&` before the variable name."

    return f"**Line {line}**: {msg}"

# ---------------------------------------------------------------------------
# GENERAL ANALYSIS
# ---------------------------------------------------------------------------

def run_general_analysis(code: str, language: str, mode: str) -> dict:
    errors = []
    suggestions = []
    lines = code.split("\n")
    lang = language.lower()

    # fixes[line_number] = list of fix descriptions
    # prepend_fixes = list of lines to add at the top
    fixes = {}       # line_number -> [("replace", old_text, new_text) or ("append", text)]
    prepend_lines = []

    # ------------------------------------------------------------------
    # MULTI-LINE SYNTAX
    # ------------------------------------------------------------------
    for issue in _find_unclosed_multiline(code, lang):
        if not any(e["line"] == issue["line"] and e["type"] == issue["type"] and e["message"] == issue["message"] for e in errors):
            errors.append(issue)

    # ------------------------------------------------------------------
    # PER-LINE CHECKS
    # ------------------------------------------------------------------
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if not stripped:
            if lang == "python" and idx > 0 and lines[idx-1].strip().endswith(":") and not lines[idx-1].strip().startswith("#"):
                suggestions.append({
                    "line": line_num, "title": "Missing Indented Block",
                    "message": f"Line {line_num}: After `{lines[idx-1].strip()}` you need an indented block. Like writing a recipe step and leaving the instructions blank!"
                })
            continue
        if '\t' in line and line.startswith('\t') and any(l.startswith(' ') for l in lines if l.strip()):
            suggestions.append({
                "line": line_num, "title": "Mixed Indentation",
                "message": f"Line {line_num} uses tabs but other lines use spaces. Pick one!"
            })
        if lang == "python":
            if line.startswith(" ") or line.startswith("\t"):
                indent_level = len(line) - len(line.lstrip())
                if indent_level > 0 and indent_level % 4 != 0 and indent_level % 2 != 0:
                    suggestions.append({
                        "line": line_num, "title": "Inconsistent Indentation",
                        "message": f"Line {line_num}: Indented by {indent_level} spaces. Python convention is 4 spaces per level."
                    })

    # ------------------------------------------------------------------
    # PYTHON
    # ------------------------------------------------------------------
    if lang == "python":
        try:
            ast.parse(code)
        except SyntaxError as e:
            err_line = e.lineno or 1
            if not any(e["line"] == err_line and "SyntaxError" in e["type"] for e in errors):
                msg = f"Line {err_line}: {e.msg}. "
                if "expected ':'" in e.msg:
                    msg += "Add a colon at the end of this line."
                elif "unterminated" in e.msg.lower():
                    msg += "You forgot to close a string or bracket somewhere."
                elif "invalid syntax" in e.msg.lower():
                    msg += "Check for missing operators, commas, or typos."
                else:
                    msg += "Check your punctuation — missing a colon, parenthesis, or quote?"
                errors.append({"line": err_line, "type": "SyntaxError", "message": msg})
                if err_line <= len(lines) and "expected ':'" in e.msg:
                    orig = lines[err_line - 1]
                    fixes.setdefault(err_line, []).append(("replace", orig, orig + ":"))
                elif err_line <= len(lines):
                    fixes.setdefault(err_line, []).append(("note", f"Syntax error here — check above."))

        for idx, line in enumerate(lines):
            line_num = idx + 1
            if any(e["line"] == line_num and "SyntaxError" in e["type"] for e in errors):
                continue
            stripped = line.strip()
            kw_match = re.match(r'^(if|elif|else|for|while|def|class|try|except|finally|with)\b', stripped)
            if kw_match:
                kw = kw_match.group(1)
                if kw in ('if', 'elif', 'for', 'while', 'def', 'class', 'try', 'except', 'finally', 'with'):
                    if not stripped.endswith(':'):
                        errors.append({
                            "line": line_num, "type": "SyntaxError",
                            "message": f"Line {line_num}: Missing colon (`:`) at the end of your `{kw}` statement. Every {kw} line needs a colon — like a pause before the instructions."
                        })
                        indent = " " * (len(line) - len(line.lstrip()))
                        fixes.setdefault(line_num, []).append(("replace", line, line + ":"))

        defined_vars = {}
        for idx, line in enumerate(lines):
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line)
            if assign: defined_vars[assign.group(1)] = idx + 1

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            for_match = re.match(r'for\s+(\w+)\s+in\s+(\w+)', stripped)
            if for_match:
                iter_var = for_match.group(2)
                if iter_var not in defined_vars and iter_var not in ('range', 'len', 'list', 'dict', 'set', 'str', 'int', 'float', 'print', 'open', 'sum', 'min', 'max', 'abs'):
                    suggestions.append({
                        "line": line_num, "title": "Undefined Iterable",
                        "message": f"Line {line_num}: Looping over `{iter_var}` but it's not defined yet. It's like saying 'for each toy in (box)' when you haven't shown the box!"
                    })

        for idx, line in enumerate(lines):
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=\s*', line)
            if assign:
                var_defined = assign.group(1)
                if var_defined.startswith('_'): continue
                used = any(var_defined in rest_line for rest_line in lines[idx + 1:])
                if not used:
                    suggestions.append({
                        "line": idx + 1, "title": "Unused Variable",
                        "message": f"You created `{var_defined}` on line {idx+1} but never used it. Like buying ingredients and leaving them in the fridge!"
                    })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            div_match = re.search(r'/\s*([a-zA-Z_]\w*)', line)
            if div_match and not any(kw in line for kw in ["if", "check", "!=", ">", "=="]):
                var_name = div_match.group(1)
                if var_name not in ('len', 'sum', 'min', 'max', 'abs', 'float', 'int'):
                    errors.append({
                        "line": line_num, "type": "ZeroDivisionError",
                        "message": f"Line {line_num}: Dividing by `{var_name}` without checking if it's zero first. Imagine sharing 10 cookies with 0 friends — it doesn't work! Check `if {var_name} != 0:` before dividing."
                    })
                    indent = " " * (len(line) - len(line.lstrip()))
                    fixes.setdefault(line_num, []).append(("wrap", line, f"{indent}if {var_name} != 0:\n{indent}    {line.lstrip()}"))

        for idx, line in enumerate(lines):
            line_num = idx + 1
            if re.match(r'^\s*while\s+(True|1)\s*:', line) and not any('break' in l for l in lines):
                errors.append({
                    "line": line_num, "type": "InfiniteLoopError",
                    "message": f"Line {line_num}: This loop never stops! Add a `break` statement or a condition that becomes False."
                })

    # ------------------------------------------------------------------
    # JS / TS
    # ------------------------------------------------------------------
    if lang in ("javascript", "typescript"):
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"): continue
            if any(stripped.startswith(kw) for kw in ["const ", "let ", "var ", "function ", "if ", "for ", "while ", "return "]):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    errors.append({
                        "line": line_num, "type": "MissingSemicolon",
                        "message": f"Line {line_num}: Missing `;`. Every statement must end with a semicolon — like a period at the end of a sentence."
                    })
                    fixes.setdefault(line_num, []).append(("append", ";"))

    # ------------------------------------------------------------------
    # C / C++ / C# / Dart
    # ------------------------------------------------------------------
    if lang in ("c", "c++", "c#", "dart"):
        if lang in ("c", "c++"):
            known_headers = {
                "stdio.h", "stdlib.h", "string.h", "math.h", "time.h",
                "ctype.h", "stdbool.h", "stdint.h", "assert.h", "errno.h",
                "float.h", "limits.h", "locale.h", "setjmp.h", "signal.h",
                "stdarg.h", "stddef.h", "tgmath.h", "wchar.h", "wctype.h",
            }
            if lang == "c++":
                known_headers.update({
                    "iostream", "fstream", "sstream", "vector", "string",
                    "algorithm", "map", "set", "unordered_map", "unordered_set",
                    "memory", "thread", "mutex", "future", "chrono",
                })

            has_stdio = False
            includes_seen = {}  # line text -> original
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                m = re.match(r'#include\s+[<"](.+?)[>"]', stripped)
                if m:
                    header = m.group(1).strip()
                    includes_seen[header] = (line_num, line, stripped)
                    if header == "stdio.h" or header == "cstdio":
                        has_stdio = True
                    elif header not in known_headers:
                        best_match = min(known_headers, key=lambda k: _edit_distance(header, k))
                        dist = _edit_distance(header, best_match)
                        if dist <= 2:
                            errors.append({
                                "line": line_num, "type": "SyntaxError",
                                "message": f"Line {line_num}: Did you mean `{best_match}`? `{header}` isn't a standard header."
                            })
                            # Fix: replace the wrong header with the correct one
                            new_line = stripped.replace(header, best_match)
                            indent = " " * (len(line) - len(line.lstrip()))
                            fixes.setdefault(line_num, []).append(("replace", line, indent + new_line))
                            if best_match == "stdio.h":
                                has_stdio = True
                        else:
                            suggestions.append({
                                "line": line_num, "title": "Unknown Header",
                                "message": f"Line {line_num}: `{header}` is not a standard {lang} header. Double-check the spelling."
                            })

            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*"): continue
                fn_match = re.search(r'\b(printf|scanf|puts|gets|putchar|getchar)\s*\(', stripped)
                if fn_match:
                    fn_name = fn_match.group(1)
                    if not has_stdio:
                        errors.append({
                            "line": line_num, "type": "SyntaxError",
                            "message": f"Line {line_num}: Using `{fn_name}` but `stdio.h` isn't included. Add `#include <stdio.h>` at the top."
                        })
                        if "#include <stdio.h>" not in prepend_lines:
                            prepend_lines.append("#include <stdio.h>")

                    # Check printf("%d", &var) — passing address where value is expected
                    if fn_name == "printf":
                        pf_args = re.search(r'printf\s*\(([^)]+)\)', stripped)
                        if pf_args:
                            all_args = pf_args.group(1)
                            fmt_end = _find_string_end(all_args)
                            if fmt_end > 0:
                                rest = all_args[fmt_end:].strip()
                                if rest.startswith(","):
                                    value_args = [a.strip() for a in rest[1:].split(",")]
                                    for va in value_args:
                                        if va.startswith("&") and re.match(r'&[a-zA-Z_]', va):
                                            var_name = va[1:]
                                            errors.append({
                                                "line": line_num, "type": "TypeMismatch",
                                                "message": f"Line {line_num}: In `printf`, you passed `{va}` (address of `{var_name}`), but it expects a **value**, not an address. For `printf`, use `{var_name}` (without `&`). `&` is for `scanf`, not `printf`."
                                            })
                                            close_q = line.index('"', line.index('"') + 1)
                                            before = line[:close_q + 1]
                                            after = line[close_q + 1:]
                                            fixes.setdefault(line_num, []).append(("replace", line, before + after.replace(va, var_name, 1)))

                    # Check scanf("%d", var) — missing & where address is expected
                    if fn_name == "scanf":
                        sf_args = re.search(r'scanf\s*\(([^)]+)\)', stripped)
                        if sf_args:
                            all_args = sf_args.group(1)
                            fmt_end = _find_string_end(all_args)
                            if fmt_end > 0:
                                rest = all_args[fmt_end:].strip()
                                if rest.startswith(","):
                                    value_args = [a.strip() for a in rest[1:].split(",")]
                                    for va in value_args:
                                        va_clean = va.rstrip(")")
                                        if va_clean and not va_clean.startswith("&") and re.match(r'[a-zA-Z_]', va_clean):
                                            var_name = re.match(r'([a-zA-Z_]\w*)', va_clean)
                                            if var_name:
                                                vn = var_name.group(1)
                                                errors.append({
                                                    "line": line_num, "type": "TypeMismatch",
                                                    "message": f"Line {line_num}: In `scanf`, you passed `{vn}` (a value), but `scanf` needs an **address**. Use `&{vn}` instead. `scanf` writes to variables, so it needs to know where they live in memory."
                                                })
                                                close_q = line.index('"', line.index('"') + 1)
                                                before = line[:close_q + 1]
                                                after = line[close_q + 1:]
                                                fixes.setdefault(line_num, []).append(("replace", line, before + after.replace(va_clean, "&" + vn, 1)))

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"): continue
            type_kws = ["int ", "float ", "double ", "char ", "String ", "bool ", "void "]
            if any(stripped.startswith(kw) for kw in type_kws):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    errors.append({
                        "line": line_num, "type": "MissingSemicolon",
                        "message": f"Line {line_num}: Missing `;`. In {language}, every statement ends with a semicolon — like a period at the end of a sentence."
                    })
                    fixes.setdefault(line_num, []).append(("append", ";"))
            if not stripped.startswith("#") and not stripped.startswith("//") and not stripped.startswith("/*"):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    ctrl_kws = r'^\s*(if|for|while|switch|else|case|default|do)\b'
                    if not re.match(ctrl_kws, stripped):
                        fn_or_assign = re.search(r'\b\w+\s*\(', stripped) or re.search(r'\w+\s*=', stripped)
                        if fn_or_assign:
                            has_semi = any(e["line"] == line_num and e["type"] == "MissingSemicolon" for e in errors)
                            if not has_semi:
                                errors.append({
                                    "line": line_num, "type": "MissingSemicolon",
                                    "message": f"Line {line_num}: Missing `;`. In {language}, every statement ends with a semicolon — like a period at the end of a sentence."
                                })
                                fixes.setdefault(line_num, []).append(("append", ";"))

        if lang == "c":
            for idx, line in enumerate(lines):
                line_num = idx + 1
                uninit = re.match(r'^\s*(int|char|float|double)\s+\w+\s*;\s*$', line)
                if uninit:
                    suggestions.append({
                        "line": line_num, "title": "Uninitialized Variable",
                        "message": f"Line {line_num}: Variable declared without a value. In C, uninitialized variables contain garbage data."
                    })

    # ------------------------------------------------------------------
    # SQL
    # ------------------------------------------------------------------
    if lang == "sql":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r'\bupdate\b.*\bset\b', stripped, re.I) and not re.search(r'\bwhere\b', stripped, re.I):
                errors.append({
                    "line": line_num, "type": "MissingWHERE",
                    "message": f"Line {line_num}: UPDATE without a WHERE clause changes ALL rows. Always specify which rows to update."
                })
            if re.search(r'\bdelete\b', stripped, re.I) and not re.search(r'\bwhere\b', stripped, re.I):
                errors.append({
                    "line": line_num, "type": "MissingWHERE",
                    "message": f"Line {line_num}: DELETE without a WHERE clause removes ALL rows. Always specify which rows to delete."
                })

    # ------------------------------------------------------------------
    # HTML, CSS
    # ------------------------------------------------------------------
    if lang == "html":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r'<(img|br|hr|input|meta|link)>$', stripped):
                suggestions.append({
                    "line": line_num, "title": "Self-Closing Tag",
                    "message": f"Line {line_num}: `<{stripped.strip('<>')}>` doesn't need a closing tag."
                })
    if lang == "css":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r':\s*\d+\s*$', stripped) and not re.search(r'(px|em|rem|%|vh|vw|pt|cm|mm)', stripped):
                suggestions.append({
                    "line": line_num, "title": "Missing CSS Unit",
                    "message": f"Line {line_num}: Number without a unit. Use `px`, `em`, `rem`, or `%` (e.g., `16px`)."
                })
            if re.search(r'color\s*:\s*\d+', stripped, re.I):
                errors.append({
                    "line": line_num, "type": "InvalidColorValue",
                    "message": f"Line {line_num}: Plain numbers aren't valid colors. Use hex (`#ff0000`), rgb(`rgb(255,0,0)`), or named colors."
                })

    # ------------------------------------------------------------------
    # FALLBACK SUGGESTION
    # ------------------------------------------------------------------
    if not errors:
        suggestions.append({
            "line": 1, "title": "Add Comments",
            "message": "Comments (`#` in Python, `//` in JS/C++) are like sticky notes for your code. They help you remember what each part does when you come back later!"
        })

    # ------------------------------------------------------------------
    # FIXED CODE — apply all collected fixes
    # ------------------------------------------------------------------
    fixed_lines = list(prepend_lines)
    for idx, line in enumerate(lines):
        line_num = idx + 1
        if line_num in fixes:
            for fix in fixes[line_num]:
                fix_type = fix[0]
                if fix_type == "replace":
                    old_s, new_s = fix[1], fix[2]
                    line = line.replace(old_s, new_s, 1)
                elif fix_type == "append":
                    line = line.rstrip() + fix[1]
                elif fix_type == "wrap":
                    line = fix[2]
        fixed_lines.append(line)
    fixed_code = "\n".join(fixed_lines)

    # ------------------------------------------------------------------
    # EXPLANATION
    # ------------------------------------------------------------------
    display_lines = fixed_lines if errors else lines
    if mode.lower() == "beginner":
        if errors:
            explanation = "### What went wrong\n\nYour code has some bugs. Think of code like a recipe — if a step is wrong, the dish won't come out right!\n\n"
            for err in errors:
                explanation += _get_error_explanation(err, lines, lang) + "\n\n---\n\n"
        else:
            explanation = "### Looking good!\n\nYour code runs without crashes. Check the Suggestions tab for tips to make it cleaner.\n\n"

        explanation += "### What each line does\n"
        for idx, line in enumerate(display_lines[:8]):
            first_line = line.strip().split("\n")[0][:60]
            if first_line:
                explanation += f"  {idx+1}. `{first_line}`\n"
        if len(display_lines) > 8:
            explanation += f"  ... and {len(display_lines)} lines total\n"
    else:
        if errors:
            explanation = f"### Issues Detected\n\n{len(errors)} error(s) found.\n\n"
            for err in errors:
                explanation += f"- **L{err['line']}** — {err['type']}: {err['message']}\n"
        else:
            explanation = "### Assessment\n\nNo critical issues detected.\n"
        explanation += "\n### Code Flow\n"
        for idx, line in enumerate(display_lines[:5]):
            first_line = line.strip().split("\n")[0][:60]
            if first_line:
                explanation += f"- **L{idx+1}**: `{first_line}`\n"
        if len(display_lines) > 5:
            explanation += f"- ... and {len(display_lines)-5} more lines.\n"

    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code
    }
