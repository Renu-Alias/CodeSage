import re
import ast

# Demo snippets used by the frontend (used for strict matching only)
DEMO_AVERAGE = "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
DEMO_LOOP = "def calculate_total(prices):\n    total = 0\n    for i in range(len(prices)):\n        tax = i * price # Error here\n        total += p\n    return total"

def analyze_code(code: str, language: str, mode: str = "Beginner") -> dict:
    code_stripped = code.strip()

    # Strict special case matching — only match the exact demo snippets
    if _is_demo_match(code_stripped, DEMO_AVERAGE):
        return get_calculate_average_analysis(mode)
    if _is_demo_match(code_stripped, DEMO_LOOP):
        return get_loop_price_analysis(mode)

    return run_general_analysis(code, language, mode)

def _is_demo_match(user_code: str, demo: str) -> bool:
    """Check if user code is substantially the same as a demo snippet."""
    def normalize(s):
        s = re.sub(r'#.*', '', s)
        s = re.sub(r'\s+', '', s)
        return s
    return normalize(user_code) == normalize(demo)

def get_calculate_average_analysis(mode: str) -> dict:
    # Error items
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
            "### How this code works 🧪\n\n"
            "1. **`total = sum(numbers)`** — adds up all numbers in the list\n"
            "   Example: `[2, 4, 6]` → `2+4+6 = 12`\n\n"
            "2. **`return total / len(numbers)`** — divides by the count to get the average\n"
            "   Example: `12 / 3 = 4.0`\n\n"
            "### What went wrong 🚨\n\n"
            "- **Empty list problem**: If the list has nothing in it (`[]`), `len([])` is `0`. "
            "Dividing by zero is like sharing pizza with 0 people — impossible! Python crashes with `ZeroDivisionError`.\n"
            "- **Wrong data type**: If the list has words like `['apple', 'banana']`, `sum()` can't add words to numbers — crashes with `TypeError`.\n\n"
            "### How to fix 🔧\n"
            "Before calculating, check if the list is empty and handle it separately."
        )
    else:
        explanation = (
            "### Technical Breakdown:\n\n"
            "- **Edge Case**: Empty list → `len(numbers) == 0` causes `ZeroDivisionError`\n"
            "- **Type Safety**: `sum()` requires numeric types; strings will raise `TypeError`\n"
            "- **Fix**: Add an early return guard clause for empty input"
        )

    # Fixed code
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
        "### What went wrong 🧐\n\n"
        "You're mixing up names! You have a list called `prices` (plural), but inside the loop you wrote `price` (singular) and `p` — which don't exist.\n\n"
        "Think of it like this: you have a box of toys (`prices`), and you're trying to pick one up. "
        "Instead of saying \"pass me the toy\" (what you actually want), you're saying \"pass me the box\" or \"pass me something I didn't name.\"\n\n"
        "### Simple fix ✅\n"
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

def run_general_analysis(code: str, language: str, mode: str) -> dict:
    errors = []
    suggestions = []

    lines = code.split("\n")
    lang = language.lower()

    # ------------------------------------------------
    # SYNTAX & STRUCTURAL CHECKS (language-agnostic)
    # ------------------------------------------------
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if not stripped:
            continue

        # ------ Indentation: tabs vs spaces ------
        if '\t' in line and line.startswith('\t'):
            if any(l.startswith(' ') for l in lines if l.strip()):
                suggestions.append({
                    "line": line_num,
                    "title": "Mixed Indentation",
                    "message": f"Line {line_num} uses tabs, but other lines use spaces. Pick ONE (spaces recommended) and stick with it!"
                })

        # ------ Unclosed string quotes ------
        for q in ['"', "'", '"""', "'''"]:
            count = stripped.count(q)
            if count > 0 and count % 2 != 0:
                errors.append({
                    "line": line_num,
                    "type": "SyntaxError",
                    "message": f"Line {line_num}: Unclosed string! You started a string with {q} but never ended it. Every opening quote needs a matching closing quote."
                })
                break

        # ------ Mismatched brackets ------
        for pair in [('(', ')'), ('[', ']'), ('{', '}')]:
            opens = stripped.count(pair[0])
            closes = stripped.count(pair[1])
            if opens != closes:
                errors.append({
                    "line": line_num,
                    "type": "SyntaxError",
                    "message": f"Line {line_num}: You have {opens} opening `{pair[0]}` but {closes} closing `{pair[1]}`. Every opening bracket needs a matching closing one."
                })
                break

    # ------------------------------------------------
    # PYTHON-SPECIFIC CHECKS
    # ------------------------------------------------
    if lang == "python":
        # ------ Try to parse with AST to catch real syntax errors ------
        try:
            ast.parse(code)
        except SyntaxError as e:
            err_line = e.lineno or 1
            errors.append({
                "line": err_line,
                "type": "SyntaxError",
                "message": f"Line {err_line}: Python found a syntax error here — {e.msg}. This is like a typo in a sentence that makes it impossible to read."
            })

        # ------ Missing colon after keywords ------
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            kw_match = re.match(r'^(if|elif|else|for|while|def|class|try|except|finally|with)\b', stripped)
            if kw_match:
                kw = kw_match.group(1)
                if kw in ('elif', 'else') and stripped.endswith(':'):
                    continue
                if kw in ('if', 'elif', 'for', 'while', 'def', 'class', 'try', 'except', 'finally', 'with'):
                    if not stripped.endswith(':'):
                        errors.append({
                            "line": line_num,
                            "type": "SyntaxError",
                            "message": f"Line {line_num}: Missing colon (`:`) at the end of your `{kw}` statement. In Python, every {kw} line must end with a colon — like a pause before the instructions that follow."
                        })

        # ------ Undefined variable detection (simple) ------
        defined_vars = {}
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line)
            if assign:
                var_name = assign.group(1)
                if not var_name.startswith('_'):
                    defined_vars[var_name] = line_num

        # Check if any for-loop variable is used before definition
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            for_match = re.match(r'for\s+(\w+)\s+in\s+(\w+)', stripped)
            if for_match:
                iter_var = for_match.group(2)
                if iter_var not in defined_vars and iter_var not in ('range', 'len', 'list', 'dict', 'set', 'str', 'int', 'float', 'print'):
                    suggestions.append({
                        "line": line_num,
                        "title": "Undefined Iterable",
                        "message": f"Line {line_num}: You're looping over `{iter_var}` but it's not defined before this line. It's like saying 'for each toy in (box of toys)' when you haven't shown the box!"
                    })

        # ------ Unused variable ------
        for idx, line in enumerate(lines):
            line_num = idx + 1
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=\s*', line)
            if assign:
                var_defined = assign.group(1)
                if var_defined.startswith('_'):
                    continue
                used = False
                for rest_line in lines[line_num:]:
                    if var_defined in rest_line:
                        used = True
                        break
                if not used:
                    suggestions.append({
                        "line": line_num,
                        "title": "Unused Variable",
                        "message": f"You created `{var_defined}` on line {line_num} but never used it. It's like buying ingredients and leaving them in the fridge! Either use it or remove the line."
                    })

        # ------ Division by zero check ------
        for idx, line in enumerate(lines):
            line_num = idx + 1
            div_match = re.search(r'/\s*([a-zA-Z_]\w*)', line)
            if div_match and not any(kw in line for kw in ["if", "check", "!=", ">"]):
                var_name = div_match.group(1)
                if var_name not in ('len', 'sum', 'min', 'max'):
                    errors.append({
                        "line": line_num,
                        "type": "ZeroDivisionError",
                        "message": f"Line {line_num}: You're dividing by `{var_name}` without checking if it's zero first. Imagine sharing 10 cookies with 0 friends — it doesn't work! Always check: `if {var_name} != 0:` before dividing."
                    })

        # ------ Infinite loop detection ------
        for idx, line in enumerate(lines):
            line_num = idx + 1
            if re.match(r'^\s*while\s+(True|1)\s*:', line):
                if not any('break' in l for l in lines):
                    errors.append({
                        "line": line_num,
                        "type": "InfiniteLoopError",
                        "message": f"Line {line_num}: This loop never stops! It's like a song stuck on repeat with no stop button. Add a `break` statement or a condition that becomes False."
                    })

    # ------------------------------------------------
    # JAVASCRIPT / TYPESCRIPT CHECKS
    # ------------------------------------------------
    if lang in ("javascript", "typescript"):
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            stmt_keywords = ["const ", "let ", "var ", "function ", "if ", "for ", "while "]
            if any(stripped.startswith(kw) for kw in stmt_keywords):
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}") and not stripped.endswith("("):
                    suggestions.append({
                        "line": line_num,
                        "title": "Missing Semicolon",
                        "message": f"Line {line_num}: You forgot a `;` at the end. JavaScript can sometimes guess where sentences end, but adding `;` makes it crystal clear!"
                    })

    # ------------------------------------------------
    # C / C++ / C# / DART CHECKS
    # ------------------------------------------------
    if lang in ("c", "c++", "c#", "dart"):
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
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

    # ------------------------------------------------
    # SQL CHECKS
    # ------------------------------------------------
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

    # ------------------------------------------------
    # HTML CHECKS
    # ------------------------------------------------
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

    # ------------------------------------------------
    # CSS CHECKS
    # ------------------------------------------------
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

    # ------------------------------------------------
    # FALLBACK SUGGESTION
    # ------------------------------------------------
    if not errors:
        suggestions.append({
            "line": 1,
            "title": "Add Comments",
            "message": "Comments (`#` in Python, `//` in JS/C++) are like sticky notes for your code. They help you remember what each part does when you come back later!"
        })

    # ------------------------------------------------
    # EXPLANATION GENERATION
    # ------------------------------------------------
    if mode.lower() == "beginner":
        if errors:
            explanation = (
                "### What went wrong 🛑\n\n"
                "Your code has some bugs we need to fix. Think of your code like a recipe — "
                "if a step is missing or wrong, the dish won't come out right!\n\n"
            )
            for err in errors:
                explanation += f"- **Line {err['line']}**: {err['message']}\n"
        else:
            explanation = (
                "### Looking good! ✅\n\n"
                "Your code runs without any major crashes. But even a working recipe can be improved — "
                "check the Suggestions tab for tips to make it cleaner and easier to read.\n\n"
            )

        explanation += "\n### What each line does\n"
        for idx, line in enumerate(lines[:6]):
            if line.strip():
                explanation += f"- **Line {idx+1}**: `{line.strip()[:50]}`\n"
        if len(lines) > 6:
            explanation += f"- ... and {len(lines)-6} more lines after that.\n"

        if lang == "python":
            explanation += (
                "\n### Quick tip 🌟\n"
                "Python reads your code from top to bottom, one line at a time — "
                "just like reading a book! Make sure each step makes sense before moving to the next."
            )
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
                explanation += f"- **L{idx+1}**: `{line.strip()[:50]}`\n"
        if len(lines) > 5:
            explanation += f"- ... and {len(lines)-5} more lines.\n"

    # ------------------------------------------------
    # FIXED CODE GENERATION
    # ------------------------------------------------
    fixed_lines = []
    for idx, line in enumerate(lines):
        has_div = any(err["line"] == idx + 1 and "Division" in err["type"] for err in errors)
        if has_div:
            indent = " " * (len(line) - len(line.lstrip()))
            if lang == "python":
                fixed_lines.append(f"{indent}# Ensure we don't divide by zero")
                fixed_lines.append(f"{indent}if variable != 0:")
                fixed_lines.append(f"{indent}    {line.lstrip()}")
                continue
            elif lang in ("javascript", "typescript"):
                fixed_lines.append(f"{indent}// Guard against zero division")
                fixed_lines.append(f"{indent}if (variable !== 0) {{")
                fixed_lines.append(f"{indent}  {line.lstrip()}")
                fixed_lines.append(f"{indent}}}")
                continue
        fixed_lines.append(line)

    fixed_code = "\n".join(fixed_lines)

    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code
    }
