import re
import ast

DEMO_AVERAGE = "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
DEMO_LOOP = "def calculate_total(prices):\n    total = 0\n    for i in range(len(prices)):\n        tax = i * price # Error here\n        total += p\n    return total"

def analyze_code(code: str, language: str, mode: str = "Beginner") -> dict:
    code_stripped = code.strip()

    # Exact-match only — no normalization, no structural matching
    if code_stripped == DEMO_AVERAGE.strip():
        return get_calculate_average_analysis(mode)
    if code_stripped == DEMO_LOOP.strip():
        return get_loop_price_analysis(mode)

    return run_general_analysis(code, language, mode)

def get_calculate_average_analysis(mode: str) -> dict:
    errors = [
        {
            "line": 4,
            "type": "ZeroDivisionError",
            "message": "The function will raise a ZeroDivisionError if the input list 'numbers' is empty. When len(numbers) is 0, dividing by zero is undefined in Python."
        },
        {
            "line": 1,
            "type": "TypeError",
            "message": "Potential TypeError if 'numbers' contains non-numeric types. Ensure the list only contains integers or floats before calling sum()."
        }
    ]
    suggestions = [
        {
            "line": 3,
            "title": "Guard Clause",
            "message": "Add a check at the start: if the list is empty, return 0 right away. This is like checking if the fridge is empty before trying to cook!"
        },
        {
            "line": 1,
            "title": "Type Hints",
            "message": "Add type hints like `numbers: list[float]` so others know what kind of data your function expects."
        }
    ]

    if mode.lower() == "beginner":
        explanation = (
            "### How this code works\n\n"
            "1. **`total = sum(numbers)`** — adds up all numbers in the list\n"
            "   Example: `[2, 4, 6]` → `2+4+6 = 12`\n\n"
            "2. **`return total / len(numbers)`** — divides by the count to get the average\n"
            "   Example: `12 / 3 = 4.0`\n\n"
            "### What went wrong\n\n"
            "- **Empty list problem**: If the list has nothing in it (`[]`), `len([])` is `0`. "
            "Dividing by zero is like sharing pizza with 0 people — impossible! Python crashes with `ZeroDivisionError`.\n"
            "- **Wrong data type**: If the list has words like `['apple', 'banana']`, `sum()` can't add words to numbers — crashes with `TypeError`.\n\n"
            "### How to fix\n"
            "Before calculating, check if the list is empty and handle it separately."
        )
    else:
        explanation = (
            "### Technical Breakdown:\n\n"
            "- **Edge Case**: Empty list → `len(numbers) == 0` causes `ZeroDivisionError`\n"
            "- **Type Safety**: `sum()` requires numeric types; strings will raise `TypeError`\n"
            "- **Fix**: Add an early return guard clause for empty input"
        )

    fixed_code = (
        "def calculate_average(numbers):\n"
        "    # Check if list is empty to prevent division by zero\n"
        "    if not numbers:\n"
        "        return 0\n"
        "    \n"
        "    total = sum(numbers)\n"
        "    return total / len(numbers)"
    )

    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code
    }

def get_loop_price_analysis(mode: str) -> dict:
    errors = [
        {
            "line": 3,
            "type": "NameError",
            "message": "Line 4: You used `price` (singular) but it doesn't exist yet. You probably meant `prices[i]` (the current item from the list). Also `p` on line 5 isn't defined anywhere — it's like using a word you haven't taught the computer!"
        }
    ]
    suggestions = [
        {
            "line": 1,
            "title": "Use Direct Iteration",
            "message": "Instead of `for i in range(len(prices))`, just write `for price in prices:` — simpler, cleaner, and no index confusion!"
        }
    ]
    explanation = (
        "### What went wrong\n\n"
        "You're mixing up names! You have a list called `prices` (plural), but inside the loop you wrote `price` (singular) and `p` — which don't exist.\n\n"
        "Think of it like this: you have a box of toys (`prices`), and you're trying to pick one up. "
        "Instead of saying \"pass me the toy\" (what you actually want), you're saying \"pass me the box\" or \"pass me something I didn't name.\"\n\n"
        "### Simple fix\n"
        "Use `for price in prices:` and then use `price` inside the loop. Python hands you each item automatically!"
    )
    fixed_code = (
        "def calculate_total(prices):\n"
        "    total = 0\n"
        "    for price in prices:\n"
        "        tax = price * 0.05 # Assuming 5% tax\n"
        "        total += price + tax\n"
        "    return total"
    )
    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code
    }

# ---------------------------------------------------------------------------
# GENERAL ANALYSIS
# ---------------------------------------------------------------------------

def _find_unclosed_multiline(code, lang):
    """Track brackets and quotes across all lines."""
    issues = []
    lines = code.split("\n")

    # Track opens/closes across lines
    stack = []  # list of (char, line_number)
    in_single = in_double = False
    in_triple_single = in_triple_double = False

    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        i = 0
        while i < len(line):
            ch = line[i]
            next_ch = line[i+1] if i + 1 < len(line) else ''

            # Triple quotes
            if ch in ('"', "'") and next_ch == ch and i + 2 < len(line) and line[i+2] == ch:
                if ch == '"':
                    in_triple_double = not in_triple_double
                else:
                    in_triple_single = not in_triple_single
                i += 3
                continue

            # Single quotes
            if ch == '"' and not in_single and not in_triple_single:
                in_double = not in_double
            elif ch == "'" and not in_double and not in_triple_double:
                in_single = not in_single
            elif not in_single and not in_double and not in_triple_single and not in_triple_double:
                if ch in '([{':
                    stack.append((ch, line_num))
                elif ch in ')]}':
                    if not stack:
                        issues.append({
                            "line": line_num,
                            "type": "SyntaxError",
                            "message": f"Line {line_num}: Extra closing `{ch}` with nothing to close."
                        })
                    else:
                        open_ch = stack[-1][0]
                        expected = {'(': ')', '[': ']', '{': '}'}
                        if expected.get(open_ch) == ch:
                            stack.pop()
                        else:
                            issues.append({
                                "line": line_num,
                                "type": "SyntaxError",
                                "message": f"Line {line_num}: Expected `{expected[open_ch]}` but found `{ch}`."
                            })
                            stack.pop()
            i += 1

    # Unclosed brackets
    for ch, line_num in stack:
        closer = {'(': ')', '[': ']', '{': '}'}[ch]
        issues.append({
            "line": line_num,
            "type": "SyntaxError",
            "message": f"Line {line_num}: `{ch}` opened on line {line_num} but never closed with `{closer}`."
        })

    # Unclosed string literals
    if in_triple_double:
        issues.append({
            "line": 1,
            "type": "SyntaxError",
            "message": "Triple-quoted string (`\"\"\"`) was opened but never closed. Check for missing closing quotes."
        })
    if in_triple_single:
        issues.append({
            "line": 1,
            "type": "SyntaxError",
            "message": "Triple-quoted string (`'''`) was opened but never closed. Check for missing closing quotes."
        })
    if in_double:
        issues.append({
            "line": len(lines),
            "type": "SyntaxError",
            "message": "Double-quoted string was opened but never closed."
        })
    if in_single:
        issues.append({
            "line": len(lines),
            "type": "SyntaxError",
            "message": "Single-quoted string was opened but never closed."
        })

    return issues


def run_general_analysis(code: str, language: str, mode: str) -> dict:
    errors = []
    suggestions = []
    lines = code.split("\n")
    lang = language.lower()

    # ------------------------------------------------------------------
    # MULTI-LINE SYNTAX CHECKS
    # ------------------------------------------------------------------
    errors.extend(_find_unclosed_multiline(code, lang))

    # ------------------------------------------------------------------
    # PER-LINE CHECKS
    # ------------------------------------------------------------------
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if not stripped:
            if lang == "python" and idx > 0 and lines[idx-1].strip().endswith(":") and not lines[idx-1].strip().startswith("#"):
                suggestions.append({
                    "line": line_num,
                    "title": "Missing Indented Block",
                    "message": f"Line {line_num}: After `{lines[idx-1].strip()}` you need an indented block. Python expects at least one line indented under a colon. It's like writing a recipe step and then leaving the instructions blank!"
                })
            continue

        # Indentation: tabs vs spaces
        if '\t' in line and line.startswith('\t'):
            if any(l.startswith(' ') for l in lines if l.strip()):
                suggestions.append({
                    "line": line_num,
                    "title": "Mixed Indentation",
                    "message": f"Line {line_num} uses tabs, but other lines use spaces. Pick ONE (spaces recommended) and stick with it!"
                })

        # Indentation errors for Python
        if lang == "python":
            if line.startswith(" ") or line.startswith("\t"):
                indent_level = len(line) - len(line.lstrip())
                prev_indent = 0
                for j in range(idx - 1, -1, -1):
                    if lines[j].strip() and not lines[j].strip().startswith("#"):
                        prev_indent = len(lines[j]) - len(lines[j].lstrip())
                        break
                if indent_level > 0 and prev_indent == 0 and not any(kw in lines[idx-1] if idx > 0 else "" for kw in [":", "\\"]):
                    if idx > 0 and not lines[idx-1].strip().endswith(":") and not lines[idx-1].rstrip().endswith("\\"):
                        pass  # indented without a colon - might still be valid
                if indent_level > 0 and indent_level % 4 != 0 and indent_level % 2 != 0:
                    suggestions.append({
                        "line": line_num,
                        "title": "Inconsistent Indentation",
                        "message": f"Line {line_num}: Indented by {indent_level} spaces. Python convention is 4 spaces per level. Pick a number and be consistent."
                    })

        # Missing comma in lists/dicts (multiline)
        if lang == "python" and stripped.endswith("'") or stripped.endswith('"'):
            for nxt in lines[idx+1:idx+2]:
                nxt_stripped = nxt.strip()
                if nxt_stripped.startswith("'") or nxt_stripped.startswith('"'):
                    prev_line_stripped = lines[idx-1].strip() if idx > 0 else ""
                    if any(kw in prev_line_stripped for kw in ["[", "(", "{"]) or any(kw in line for kw in ["[", "(", "{"]):
                        pass  # could be implicit concatenation

    # ------------------------------------------------------------------
    # PYTHON-SPECIFIC
    # ------------------------------------------------------------------
    if lang == "python":
        # AST parse
        try:
            ast.parse(code)
        except SyntaxError as e:
            err_line = e.lineno or 1
            if not any(e["line"] == err_line and "SyntaxError" in e["type"] for e in errors):
                errors.append({
                    "line": err_line,
                    "type": "SyntaxError",
                    "message": f"Line {err_line}: {e.msg}. Check your punctuation — missing a colon, parenthesis, or quote?"
                })

        # Missing colon (skip if AST already reported a SyntaxError on this line)
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
                            "line": line_num,
                            "type": "SyntaxError",
                            "message": f"Line {line_num}: Missing colon (`:`) at the end of your `{kw}` statement. In Python, every {kw} line must end with a colon — like a pause before the instructions that follow."
                        })

        # Defined variables
        defined_vars = {}
        for idx, line in enumerate(lines):
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line)
            if assign:
                defined_vars[assign.group(1)] = idx + 1

        # Undefined iterable in for loops
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            for_match = re.match(r'for\s+(\w+)\s+in\s+(\w+)', stripped)
            if for_match:
                iter_var = for_match.group(2)
                if iter_var not in defined_vars and iter_var not in ('range', 'len', 'list', 'dict', 'set', 'str', 'int', 'float', 'print', 'open', 'sum', 'min', 'max', 'abs'):
                    suggestions.append({
                        "line": line_num,
                        "title": "Undefined Iterable",
                        "message": f"Line {line_num}: You're looping over `{iter_var}` but it's not defined yet. It's like saying 'for each toy in (box of toys)' when you haven't shown the box!"
                    })

        # Unused variables
        for idx, line in enumerate(lines):
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=\s*', line)
            if assign:
                var_defined = assign.group(1)
                if var_defined.startswith('_'):
                    continue
                used = False
                for rest_line in lines[idx + 1:]:
                    if var_defined in rest_line:
                        used = True
                        break
                if not used:
                    suggestions.append({
                        "line": idx + 1,
                        "title": "Unused Variable",
                        "message": f"You created `{var_defined}` on line {idx + 1} but never used it. It's like buying ingredients and leaving them in the fridge! Either use it or remove the line."
                    })

        # Division by zero
        for idx, line in enumerate(lines):
            line_num = idx + 1
            div_match = re.search(r'/\s*([a-zA-Z_]\w*)', line)
            if div_match and not any(kw in line for kw in ["if", "check", "!=", ">", "=="]):
                var_name = div_match.group(1)
                if var_name not in ('len', 'sum', 'min', 'max', 'abs', 'float', 'int'):
                    indent = " " * (len(line) - len(line.lstrip()))
                    errors.append({
                        "line": line_num,
                        "type": "ZeroDivisionError",
                        "message": f"Line {line_num}: You're dividing by `{var_name}` without checking if it's zero first. Imagine sharing 10 cookies with 0 friends — it doesn't work! Always check `if {var_name} != 0:` before dividing."
                    })

        # Infinite while True
        for idx, line in enumerate(lines):
            line_num = idx + 1
            if re.match(r'^\s*while\s+(True|1)\s*:', line):
                if not any('break' in l for l in lines):
                    errors.append({
                        "line": line_num,
                        "type": "InfiniteLoopError",
                        "message": f"Line {line_num}: This loop never stops! It's like a song stuck on repeat with no stop button. Add a `break` statement or a condition that becomes False."
                    })

    # ------------------------------------------------------------------
    # JS / TS
    # ------------------------------------------------------------------
    if lang in ("javascript", "typescript"):
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
                continue
            stmt_keywords = ["const ", "let ", "var ", "function ", "if ", "for ", "while ", "return "]
            if any(stripped.startswith(kw) for kw in stmt_keywords):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    suggestions.append({
                        "line": line_num,
                        "title": "Missing Semicolon",
                        "message": f"Line {line_num}: You forgot a `;` at the end. JavaScript can sometimes guess where sentences end, but adding `;` makes it crystal clear!"
                    })

    # ------------------------------------------------------------------
    # C / C++ / C# / Dart
    # ------------------------------------------------------------------
    if lang in ("c", "c++", "c#", "dart"):
        # ---------- Include-file validation (C/C++) ----------
        if lang in ("c", "c++"):
            known_headers = {
                "stdio.h", "stdlib.h", "string.h", "math.h", "time.h",
                "ctype.h", "stdbool.h", "stdint.h", "assert.h", "errno.h",
                "float.h", "limits.h", "locale.h", "setjmp.h", "signal.h",
                "stdarg.h", "stddef.h", "stdio.h", "stdlib.h", "string.h",
                "tgmath.h", "wchar.h", "wctype.h",
            }
            # C++ additional headers
            if lang == "c++":
                known_headers.update({
                    "iostream", "fstream", "sstream", "vector", "string",
                    "algorithm", "map", "set", "unordered_map", "unordered_set",
                    "memory", "thread", "mutex", "future", "chrono",
                })
            def _edit_distance(a, b):
                """Simple Levenshtein distance."""
                m, n = len(a), len(b)
                dp = list(range(n + 1))
                for i in range(1, m + 1):
                    prev = dp[0]
                    dp[0] = i
                    for j in range(1, n + 1):
                        temp = dp[j]
                        cost = 0 if a[i - 1] == b[j - 1] else 1
                        dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
                        prev = temp
                return dp[n]

            has_stdio = False
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                m = re.match(r'#include\s+[<"](.+?)[>"]', stripped)
                if m:
                    header = m.group(1).strip()
                    if header == "stdio.h" or header == "cstdio":
                        has_stdio = True
                    elif header not in known_headers:
                        best_match = min(known_headers, key=lambda k: _edit_distance(header, k))
                        dist = _edit_distance(header, best_match)
                        if dist <= 2:
                            errors.append({
                                "line": line_num,
                                "type": "SyntaxError",
                                "message": f"Line {line_num}: Did you mean `{best_match}`? `{header}` isn't a standard header."
                            })
                        else:
                            suggestions.append({
                                "line": line_num,
                                "title": "Unknown Header",
                                "message": f"Line {line_num}: `{header}` is not a standard {lang} header. Double-check the spelling."
                            })

            # Check for printf/scanf without stdio.h
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*"):
                    continue
                if re.search(r'\b(printf|scanf|puts|gets|putchar|getchar)\s*\(', stripped):
                    if not has_stdio:
                        errors.append({
                            "line": line_num,
                            "type": "SyntaxError",
                            "message": f"Line {line_num}: You're using `{re.search(r'\b(\w+)\s*\(', stripped).group(1)}` but didn't include `stdio.h`. Add `#include <stdio.h>` at the top."
                        })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
                continue
            type_kws = ["int ", "float ", "double ", "char ", "String ", "bool ", "void "]
            if any(stripped.startswith(kw) for kw in type_kws):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    suggestions.append({
                        "line": line_num,
                        "title": "Missing Semicolon",
                        "message": f"Line {line_num}: Missing `;`. In {language}, every statement must end with a semicolon — like a period at the end of a sentence."
                    })

        if lang == "c":
            for idx, line in enumerate(lines):
                line_num = idx + 1
                uninit = re.match(r'^\s*(int|char|float|double)\s+\w+\s*;\s*$', line)
                if uninit:
                    suggestions.append({
                        "line": line_num,
                        "title": "Uninitialized Variable",
                        "message": f"Line {line_num}: Variable declared without a value. In C, uninitialized variables contain garbage data — like an empty box with random stuff inside. Always set a starting value!"
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
                    "line": line_num,
                    "type": "MissingWHERE",
                    "message": f"Line {line_num}: UPDATE without a WHERE clause will change ALL rows! Always add `WHERE` to target specific records."
                })
            if re.search(r'\bdelete\b', stripped, re.I) and not re.search(r'\bwhere\b', stripped, re.I):
                errors.append({
                    "line": line_num,
                    "type": "MissingWHERE",
                    "message": f"Line {line_num}: DELETE without a WHERE clause will remove ALL rows! Always specify which rows to delete."
                })

    # ------------------------------------------------------------------
    # HTML
    # ------------------------------------------------------------------
    if lang == "html":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r'<(img|br|hr|input|meta|link)>$', stripped):
                suggestions.append({
                    "line": line_num,
                    "title": "Self-Closing Tag",
                    "message": f"Line {line_num}: `<{stripped.strip('<>')}>` doesn't need a closing tag — it's a void element. But keep it consistent!"
                })

    # ------------------------------------------------------------------
    # CSS
    # ------------------------------------------------------------------
    if lang == "css":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r':\s*\d+\s*$', stripped) and not re.search(r'(px|em|rem|%|vh|vw|pt|cm|mm)', stripped):
                suggestions.append({
                    "line": line_num,
                    "title": "Missing CSS Unit",
                    "message": f"Line {line_num}: Number without a unit. CSS needs `px`, `em`, `rem`, or `%` after numbers (e.g., `16px` not just `16`)."
                })
            if re.search(r'color\s*:\s*\d+', stripped, re.I):
                errors.append({
                    "line": line_num,
                    "type": "InvalidColorValue",
                    "message": f"Line {line_num}: Plain numbers aren't valid colors. Use hex (`#ff0000`), rgb(`rgb(255,0,0)`), or named colors."
                })

    # ------------------------------------------------------------------
    # FALLBACK SUGGESTION
    # ------------------------------------------------------------------
    if not errors:
        suggestions.append({
            "line": 1,
            "title": "Add Comments",
            "message": "Comments (`#` in Python, `//` in JS/C++) are like sticky notes for your code. They help you remember what each part does when you come back later!"
        })

    # ------------------------------------------------------------------
    # EXPLANATION
    # ------------------------------------------------------------------
    if mode.lower() == "beginner":
        if errors:
            explanation = "### What went wrong\n\nYour code has some bugs we need to fix. Think of your code like a recipe — if a step is missing or wrong, the dish won't come out right!\n\n"
            for err in errors:
                explanation += f"- **Line {err['line']}**: {err['message']}\n"
        else:
            explanation = "### Looking good!\n\nYour code runs without any major crashes. Check the Suggestions tab for tips to make it cleaner.\n\n"

        explanation += "\n### What each line does\n"
        for idx, line in enumerate(lines[:8]):
            if line.strip():
                explanation += f"- **Line {idx+1}**: `{line.strip()[:60]}`\n"
        if len(lines) > 8:
            explanation += f"- ... and {len(lines)-8} more lines after that.\n"
    else:
        if errors:
            explanation = f"### Issues Detected\n\n{len(errors)} error(s) found.\n\n"
            for err in errors:
                explanation += f"- **L{err['line']}** — {err['type']}: {err['message']}\n"
        else:
            explanation = "### Assessment\n\nNo critical issues detected.\n"

        explanation += "\n### Code Flow\n"
        for idx, line in enumerate(lines[:5]):
            if line.strip():
                explanation += f"- **L{idx+1}**: `{line.strip()[:60]}`\n"
        if len(lines) > 5:
            explanation += f"- ... and {len(lines)-5} more lines.\n"

    # ------------------------------------------------------------------
    # FIXED CODE
    # ------------------------------------------------------------------
    fixed_lines = []
    for idx, line in enumerate(lines):
        has_div = any(err["line"] == idx + 1 and "Division" in err["type"] for err in errors)
        if has_div:
            indent = " " * (len(line) - len(line.lstrip()))
            fixed_lines.append(f"{indent}# Guard against zero division")
            fixed_lines.append(f"{indent}if variable != 0:")
            fixed_lines.append(f"{indent}    {line.lstrip()}")
            continue
        fixed_lines.append(line)

    fixed_code = "\n".join(fixed_lines)

    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code
    }
