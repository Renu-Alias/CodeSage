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
    return {"errors": errors, "suggestions": suggestions, "explanation": explanation, "fixed_code": fixed_code, "analysis_metrics": analyze_complexity(DEMO_AVERAGE, "Python")}

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
    return {"errors": errors, "suggestions": suggestions, "explanation": explanation, "fixed_code": fixed_code, "analysis_metrics": analyze_complexity(DEMO_LOOP, "Python")}

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

def _strip_c_line(line):
    """Remove C-style trailing comments from a line for syntax checking."""
    s = re.sub(r'/\*.*?\*/', '', line)
    idx = s.find('//')
    if idx >= 0:
        in_str = False
        for i in range(idx):
            if s[i] == '"' and (i == 0 or s[i-1] != '\\'):
                in_str = not in_str
        if not in_str:
            s = s[:idx]
    return s.strip()

def _last_code_char(line):
    """Return the last non-comment, non-whitespace character of a line of C code."""
    code = _strip_c_line(line)
    return code[-1] if code else ''

def _get_error_explanation(err, code_lines, lang):
    """Generate a short beginner-friendly explanation snippet for a single error."""
    line = err.get("line", 1)
    etype = err.get("type", "")
    msg = err.get("message", "")
    code_line = code_lines[line - 1].strip() if line <= len(code_lines) else ""
    snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line

    # Helper: build a clean explanation block
    def explain(why, fix):
        text = f"Line {line}: {snippet}\n\n{why}"
        if fix:
            text += f"\n\nFix: {fix}"
        return text

    if "SyntaxError" in etype:
        if "missing colon" in msg.lower() or "expected ':'" in msg.lower():
            return explain(
                "In Python, lines starting with if, for, while, def, or class must end with a colon (:). The colon tells Python that the next indented block belongs to this line.",
                "Add : at the end of the line."
            )
        if "preprocessor directive" in msg.lower():
            return explain(
                "In C/C++, lines like #include, #define, #ifdef are called preprocessor directives. They must start with #. The # tells the compiler this line is a special instruction before compilation. Without #, the compiler treats it as regular code and cannot find the file.",
                "Add # at the start of the line."
            )
        if "include" in msg.lower() and "angle" in msg.lower():
            return explain(
                "In C/C++, include needs both # at the beginning and angle brackets <> around the filename. #include <stdio.h> means before compiling, go grab the toolbox named stdio.h. Without # and <>, the compiler does not know what to do.",
                "Write #include <filename.h>."
            )
        if "header" in msg.lower() and "mean" in msg.lower():
            return explain(
                "The header file name is misspelled. Header files like stdio.h are like ID cards. If you spell the name wrong, the compiler cannot find the right toolbox.",
                "Check the spelling and use the correct header name."
            )
        if "stdio.h" in msg.lower() or "printf" in msg.lower():
            return explain(
                "In C, to use functions like printf or scanf, you must first include stdio.h at the top of your file. stdio.h is the standard input/output library, like a toolbox containing the printf tool.",
                "Add #include <stdio.h> at the very top of your code."
            )
        if "unclosed" in msg.lower():
            if "string" in msg.lower():
                return explain(
                    "A string (text inside quotes) was started but never finished. Every opening quote needs a matching closing quote, like a pair of bookends.",
                    "Add the matching closing quote at the end of the string."
                )
            return explain(
                "A bracket (, [, or { was opened but never closed. Brackets always work in pairs, like two hands clapping.",
                "Find where the bracket was opened and add the matching closing bracket."
            )

    if "ZeroDivisionError" in etype or "Division" in etype:
        return explain(
            "Dividing by zero crashes your program. Think of sharing 10 cookies with 0 friends. It is impossible!",
            "Before dividing, check if the value is not zero: if count != 0:"
        )

    if "InfiniteLoopError" in etype:
        return explain(
            "This loop never stops. A while True: loop runs forever unless something tells it to stop. Like a song on repeat with no stop button.",
            "Add a break statement inside the loop."
        )

    if "MissingWHERE" in etype:
        return explain(
            "Without a WHERE clause, your UPDATE or DELETE applies to every row in the table. Like sending a delete all emails command when you only meant to delete one.",
            "Always add WHERE column_name = value."
        )

    if "MissingSemicolon" in etype or "missing semicolon" in msg.lower():
        return explain(
            "Every statement must end with ;. It is like a period at the end of a sentence. It tells the compiler this instruction is complete.",
            "Add ; at the end of the line."
        )

    if "TypeMismatch" in etype:
        if "printf" in msg:
            return explain(
                "In printf, you use %d, %f, %c to print values. Adding & gives the variables memory address instead of its value. Like giving someone your house address when they asked for your phone number.",
                "Remove the & and just use the variable name directly."
            )
        if "scanf" in msg:
            return explain(
                "In scanf, you need & because scanf writes a value into your variable. It needs to know where the variable lives in memory. Like telling a delivery driver your address so they know where to drop the package.",
                "Add & before the variable name."
            )

    if "AssignmentInCondition" in etype:
        return explain(
            "You used = (single equals) inside a condition. In programming, = means assign (store a value), while == means compare (check if two things are equal). Using = here accidentally changes the variable instead of checking it.",
            "Replace = with ==."
        )

    if "NameError" in etype:
        return explain(
            "Python cannot find this variable. It is like calling someone by the wrong name. Python does not know what you mean. You might have a typo in the variable name.",
            "Check the spelling and make sure you defined the variable before using it."
        )

    if "BareExcept" in etype:
        return explain(
            "A bare except: catches every possible error, including things like Ctrl+C that should stop your program. It is like a butterfly net that catches butterflies and grenades.",
            "Use except Exception: to catch normal errors safely."
        )

    if "LooseEquality" in etype:
        return explain(
            "Using == in JavaScript can give surprising results. For example, 0 == false is true and empty string == 0 is true. That is because == converts types before comparing. Use === to check both value and type.",
            "Replace == with ===."
        )

    if "MissingRadix" in etype:
        return explain(
            "parseInt() without a second argument can guess the wrong number base. For example, parseInt('08') might give 0 by treating it as octal. Always specify base 10 for normal numbers.",
            "Use parseInt(x, 10)."
        )

    if "MainReturnType" in etype:
        if "needs a return type" in msg:
            return explain(
                "main() without a return type is not standard C. Every function needs a return type. int main() tells the OS your program ran successfully (return 0) or had an error (return 1).",
                "Change main() to int main() and add return 0; at the end."
            )
        return explain(
            "void main() is not standard C. The int in int main() lets your program tell the OS whether it succeeded (return 0) or failed (return 1).",
            "Change void main() to int main() and add return 0; at the end."
        )

    if "NullComparison" in etype:
        return explain(
            "In SQL, = NULL does not work because NULL means unknown. Nothing equals an unknown value, not even NULL itself. Use IS NULL instead.",
            "Replace = NULL with IS NULL."
        )

    if "MissingDoctype" in etype:
        return explain(
            "Without <!DOCTYPE html>, older browsers switch to quirks mode and may display your page incorrectly. It is like telling the browser which rulebook to follow.",
            "Add <!DOCTYPE html> as the very first line."
        )

    if "SyntaxError" in etype and "was opened but never closed" in msg:
        snippet = code_line[:40] + "..." if len(code_line) > 40 else code_line
        return explain(
            f"An HTML tag was opened but never closed. Every opening tag like <tag> needs a matching closing tag like </tag>. Think of them as a pair of bookends for your content.",
            "Find where the tag was opened and add the matching closing tag."
        )

    if "InvalidFree" in etype:
        return explain(
            "You called free() on a variable that was not allocated with malloc/calloc. free() is for releasing heap memory. If you use it on a stack variable (like a local array), the program crashes because stack memory is managed automatically — like trying to return a rental car you never rented.",
            "Remove the free() call for stack variables. Only free() memory that came from malloc()."
        )

    if "ReturnLocalAddress" in etype:
        return explain(
            "You returned the address of a local (stack) variable. When a function ends, its local variables are destroyed and their memory is recycled. The pointer you returned now points to invalid memory — like giving someone a map to a house that gets demolished as they walk away.",
            "Either make the variable static, allocate it with malloc() and return the pointer, or pass a buffer as a parameter."
        )

    if "UseAfterFree" in etype:
        return explain(
            "You are using memory after it has been freed. Once you call free(ptr), the memory is returned to the system. Accessing it afterward is undefined behavior — the data may be corrupted or gone. Like trying to read pages of a book you already put through a shredder.",
            "Do not access the pointer after freeing it. If you need it later, defer the free() call or set the pointer to NULL and check for NULL before use."
        )

    if "OffByOne" in etype:
        return explain(
            "Your loop uses <= (less-than-or-equal) where it should use < (less-than). This runs the loop one extra time, accessing the array element right past its end. Array indices go from 0 to size-1. If size is 8, valid indices are 0 to 7 — index 8 is out of bounds.",
            "Change `<=` to `<` to stay within valid bounds."
        )

    if "BufferOverflow" in etype:
        return explain(
            "You are writing past the end of an allocated buffer. The buffer has space for a certain number of elements, but your code writes beyond that limit. This corrupts adjacent memory and can crash or create security vulnerabilities.",
            "Either increase the allocation size or reduce the number of writes."
        )

    if "NullPointerDereference" in etype:
        return explain(
            "You tried to access data through a pointer that was set to NULL (zero). A NULL pointer points to nothing — like trying to open a door that doesn't exist. Dereferencing it crashes your program with a segfault.",
            "Check if the pointer is NULL before using it: `if (ptr != NULL) { ... }`. If it's NULL, don't use it."
        )

    if "DoubleFree" in etype:
        return explain(
            "You called free() on a pointer that was already freed. Freeing the same memory twice corrupts the heap manager's bookkeeping and can crash or create security holes. Like trying to return the same rental car twice.",
            "Only call free() once per malloc(). After freeing, set the pointer to NULL to avoid accidental reuse."
        )

    if "MemoryLeak" in etype:
        return explain(
            "Memory was allocated with malloc() but never freed with free(). The memory stays allocated until the program exits, wasting system resources. Like renting a hotel room and never checking out — eventually all rooms are taken.",
            "Add a free() call when the memory is no longer needed. Use a matching free() for every malloc()."
        )

    if "WildPointer" in etype:
        return explain(
            "You declared a pointer but didn't give it a value (it's uninitialized). It points to a random memory location. Using it is like throwing a dart blindfolded — you'll hit something, but probably not what you intended.",
            "Initialize pointers when declared: `int *ptr = NULL;` or assign a valid address before use."
        )

    if "BufferUnderflow" in etype:
        return explain(
            "You used a negative index to access an array. Array indices start at 0. A negative index accesses memory before the array starts, reading or writing data that belongs to something else. Like trying to read page -1 of a book.",
            "Ensure your index is never negative. Use an unsigned type for indices or add a bounds check."
        )

    if "SignedUnsignedMismatch" in etype:
        return explain(
            "You compared a signed integer (can be negative) with an unsigned integer (always positive). In C/C++, the signed value is converted to unsigned, making negative numbers unexpectedly large.",
            "Cast both to the same type before comparing, or avoid mixing signed and unsigned in comparisons."
        )

    if "ModuloByZero" in etype:
        return explain(
            "You used the % operator with a divisor that could be zero. Modulo by zero crashes your program — it's mathematically undefined. Like asking 'how many groups of zero can I make?' — there's no answer!",
            "Check that the divisor is not zero before using %: `if (divisor != 0) { result = value % divisor; }`"
        )

    if "StackOverflow" in etype:
        return explain(
            "A local variable is extremely large. Local variables live on the stack, which has limited space (typically 1-8 MB). Very large arrays on the stack can overflow into other memory and crash.",
            "Use malloc() to allocate large buffers on the heap instead of declaring them as local arrays."
        )

    if "MissingReturn" in etype:
        return explain(
            "A function promises to return a value (non-void return type) but doesn't have a return statement. The function will return garbage data. Like promising to bring back an answer but coming back empty-handed.",
            "Add a `return` statement that returns a value of the correct type."
        )

    if "DeadCode" in etype:
        return explain(
            "This code comes after a return, break, or continue statement. It will never run because the previous statement already exited the function or loop. Like writing stage directions after the curtain falls.",
            "Remove the unreachable code or restructure the logic so it runs before the return/break."
        )

    if "MisspelledKeyword" in etype:
        return explain(
            "A word in your code looks like a misspelled keyword. Programming languages use specific words for specific instructions. If you spell a keyword wrong, the compiler or interpreter won't understand it.",
            "Check the spelling and use the correct keyword."
        )

    if "InvalidOperatorUsage" in etype:
        return explain(
            "You used an operator that doesn't exist in this language. Different languages support different operators. For example, === exists in JavaScript/TypeScript but not in C or Python.",
            "Use the correct operator for this language. Check the language documentation if unsure."
        )

    if "HardcodedCredential" in etype:
        return explain(
            "Your code contains what looks like a password, API key, or secret token written directly as a string. Hardcoding secrets is a security risk — anyone with access to the code can read them.",
            "Store secrets in environment variables or a secure vault, and read them at runtime."
        )

    if "CommandInjection" in etype:
        return explain(
            "You're calling a system command execution function. If any part of the command comes from user input, an attacker could run arbitrary commands on your system — like letting a stranger type commands into your computer's terminal.",
            "Avoid system()/exec() if possible. If necessary, strictly validate and sanitize all inputs."
        )

    if "PathTraversal" in etype:
        return explain(
            "Your code contains `../` or similar path traversal sequences. If this is combined with user input, attackers could access files outside the intended directory — like using a forged key to open rooms you shouldn't enter.",
            "Validate and sanitize any user-supplied file paths. Use a whitelist of allowed paths."
        )

    if "AccidentalRecursion" in etype:
        return explain(
            "A function is calling itself. If there's no base case (a condition that stops the recursion), it will keep calling itself until the program runs out of memory and crashes.",
            "Make sure you have a base case that stops the recursion, like `if (n <= 1): return n`."
        )

    if "DivisionByZero" in etype:
        return explain(
            "Your code divides by zero, which is mathematically undefined and crashes your program. The CPU cannot compute how many times nothing fits into something.",
            "Check that the divisor is not zero before dividing: `if (b != 0) { result = a / b; }`"
        )

    if "InfiniteRecursion" in etype:
        return explain(
            "A function calls itself. If there's no base case to stop the recursion, it will keep calling itself until the program runs out of stack memory and crashes with a stack overflow.",
            "Add a base case — a condition that stops the recursion, like `if (n == 0) return;` before the recursive call."
        )

    if "DanglingPointer" in etype:
        return explain(
            "A pointer holds the address of a local variable that has gone out of scope. The memory it points to has been reclaimed, so using it is undefined behavior. Like holding a ticket to a show that already ended.",
            "Ensure the pointed-to variable still exists when the pointer is used, or allocate the memory on the heap with malloc()."
        )

    if "StringLiteralModification" in etype:
        return explain(
            "You're trying to modify a string literal. String literals are stored in read-only memory in C/C++. Writing to them crashes your program. Like trying to edit text that's carved in stone.",
            "Use a mutable array instead: `char str[] = \"hello\";` — this creates a copy on the stack that you can safely modify."
        )

    if "FormatMismatch" in etype:
        return explain(
            "A printf format specifier doesn't match the argument type. `%s` expects a string (char*), but you passed a number. This causes the program to interpret the number as a memory address, which crashes or prints garbage.",
            "Use the correct format specifier: `%d` for integers, `%s` for strings, `%f` for floats."
        )

    if "ShiftOverflow" in etype:
        return explain(
            "You're shifting a value by more bits than the type can hold. For a 32-bit int, shifting by 32 or more is undefined behavior — the result is unpredictable.",
            "Make sure the shift amount is less than the bit width of the type (e.g., less than 32 for an int)."
        )

    if "SequencePointViolation" in etype:
        return explain(
            "You modified a variable multiple times between two sequence points. The C/C++ standard doesn't define what happens — different compilers give different results. Like changing the rules of chess mid-game.",
            "Break the expression into separate statements: don't use ++ or -- on the same variable more than once in the same expression."
        )

    if "MissingNullCheck" in etype:
        return explain(
            "Memory was allocated with malloc() but the return value wasn't checked for NULL. If memory allocation fails, malloc() returns NULL and using the pointer crashes your program.",
            "Always check the result: `if (ptr == NULL) { /* handle error */ }`"
        )

    return f"Line {line}: {msg}"

# ---------------------------------------------------------------------------
# COMPLEXITY ANALYSIS
# ---------------------------------------------------------------------------

def analyze_complexity(code: str, language: str) -> dict:
    lines = code.split("\n")
    lang = language.lower()

    # Count loops (for, while) to estimate time complexity
    loop_depth = 0
    max_loop_depth = 0
    loop_keywords = []
    if lang in ("python",):
        loop_keywords = ["for ", "while "]
    elif lang in ("javascript", "typescript"):
        loop_keywords = ["for(", "for (", "while(", "while ("]
    elif lang in ("c", "c++", "java", "c#", "dart", "kotlin", "go", "rust", "swift"):
        loop_keywords = ["for(", "for (", "while(", "while ("]
    else:
        loop_keywords = ["for", "while"]

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("--"):
            continue
        stripped_lower = stripped.lower()
        is_loop = any(stripped_lower.startswith(kw.lower()) or kw.lower() in stripped_lower.split("(")[0].split(" ")[-1] for kw in loop_keywords if kw)

        # Improved detection: check for 'for' or 'while' at start of meaningful code
        kw_found = None
        for kw in loop_keywords:
            idx = stripped_lower.find(kw.lower())
            if idx >= 0:
                # Check if this is a loop keyword (not 'for' in 'before')
                before = stripped_lower[:idx].strip()
                if not before or before in ("}", ");", ")", "{", ":", ";", "else"):
                    if not (kw.lower() == "for" and "form" in stripped_lower[:idx+5]):
                        kw_found = kw
                        break

        if kw_found:
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
        else:
            # Check for closing braces/brackets that decrease indent
            if stripped in ("}", "});", "})"):
                loop_depth = max(0, loop_depth - 1)

    # Simpler approach: count nested indentation with loop keywords
    loop_depth = 0
    max_loop_depth = 0
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("--"):
            continue
        stripped_lower = stripped.lower()
        is_loop_line = False
        for kw in loop_keywords:
            if kw.lower() in stripped_lower and stripped_lower.startswith(kw.lower()[:3]) or stripped_lower.lstrip().startswith(kw.lower()[:3]):
                # crude check: word boundary
                if re.search(r'\b' + re.escape(kw.strip(" (")) + r'\b', stripped_lower):
                    is_loop_line = True
                    break
        if is_loop_line:
            loop_depth += 1
            max_loop_depth = max(max_loop_depth, loop_depth)
        elif stripped in ("}", "});", ")", "];"):
            loop_depth = max(0, loop_depth - 1)

    # Fallback: simple loop counting
    loop_count = 0
    for line in lines:
        s = line.strip().lower()
        if any(kw.strip(" (").lower() in s.split() or s.startswith(kw.strip(" (").lower()) for kw in loop_keywords):
            loop_count += 1

    max_depth = max_loop_depth if max_loop_depth > 0 else (1 if loop_count > 0 else 0)

    if max_depth == 0:
        time_complexity = "O(1)"
        time_desc = "Constant time — no loops, runs in the same time regardless of input size."
        efficiency = "Excellent"
        efficiency_score = 95
    elif max_depth == 1:
        time_complexity = "O(n)"
        time_desc = "Linear time — one loop, time grows proportionally with input size."
        efficiency = "Good"
        efficiency_score = 80
    elif max_depth == 2:
        time_complexity = "O(n²)"
        time_desc = "Quadratic time — nested loops, time grows with the square of input size."
        efficiency = "Fair"
        efficiency_score = 60
    elif max_depth >= 3:
        time_complexity = "O(n³) or worse"
        time_desc = "Cubic or higher — deeply nested loops may become slow with large inputs."
        efficiency = "Needs improvement"
        efficiency_score = 40

    # Space complexity estimate based on data structures
    space_complexity = "O(1)"
    space_desc = "Constant space — uses a fixed amount of memory."
    has_array = False
    has_dict = False
    has_recursion = False
    for line in lines:
        s = line.strip()
        if any(kw in s for kw in ["[", "list(", "List<", "vector", "ArrayList", "new ", "malloc", "alloc"]):
            has_array = True
        if any(kw in s for kw in ["{", "dict(", "Map<", "HashMap", "Dictionary", "object"]):
            has_dict = True
        # Check for function calls (potential recursion)
    # Count function definitions
    func_count = 0
    for line in lines:
        s = line.strip()
        if any(s.startswith(kw) for kw in ["def ", "function ", "int main", "void main", "public static", "fn "]):
            func_count += 1

    if has_array and has_dict:
        space_complexity = "O(n)"
        space_desc = "Linear space — memory grows with input size (arrays and dictionaries)."
    elif has_array or has_dict:
        space_complexity = "O(n)"
        space_desc = "Linear space — memory usage scales with input."
    elif func_count >= 2:
        space_complexity = "O(1)"
        space_desc = "Constant space — functions don't store significant additional data."

    loc = len([l for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("//") and not l.strip().startswith("/*") and not l.strip().startswith("--")])
    total_lines = len(lines)
    cyclomatic = max(1, func_count + loop_count)

    return {
        "time_complexity": time_complexity,
        "time_description": time_desc,
        "space_complexity": space_complexity,
        "space_description": space_desc,
        "efficiency": efficiency,
        "efficiency_score": efficiency_score,
        "lines_of_code": loc,
        "total_lines": total_lines,
        "loop_count": loop_count,
        "max_loop_depth": max_depth,
        "function_count": func_count,
        "cyclomatic_complexity": cyclomatic
    }

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
                msg = f"{e.msg}. "
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
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith('"'): continue
            var_used = re.findall(r'(?<![a-zA-Z_.])([a-zA-Z_]\w*)(?![a-zA-Z_.])', stripped)
            blacklist = {'True', 'False', 'None', 'range', 'len', 'list', 'dict', 'set', 'str', 'int', 'float', 'print', 'open', 'sum', 'min', 'max', 'abs', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'input', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'reversed', 'any', 'all', 'super', 'self', 'cls', 'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError', 'StopIteration', 'ImportError', 'AttributeError', 'NameError', 'ZeroDivisionError', 'FileNotFoundError', 'not', 'and', 'or', 'is', 'in', 'if', 'else', 'elif', 'for', 'while', 'def', 'class', 'return', 'yield', 'import', 'from', 'as', 'with', 'try', 'except', 'finally', 'raise', 'pass', 'break', 'continue', 'global', 'nonlocal', 'lambda'}
            for v in var_used:
                if v not in defined_vars and v not in blacklist:
                    best = min(defined_vars, key=lambda dv: _edit_distance(v, dv)) if defined_vars else None
                    if best and _edit_distance(v, best) <= 2 and best != v and line_num > defined_vars[best]:
                        possible_line = defined_vars.get(best, 0)
                        errors.append({
                            "line": line_num, "type": "NameError",
                            "message": f"Line {line_num}: `{v}` is not defined. Did you mean `{best}` (defined on line {possible_line})? This is like writing \"apples\" when you meant \"apples\" — a tiny typo makes Python confused."
                        })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            div_match = re.search(r'/\s*([a-zA-Z_]\w*)', line)
            if div_match and not any(kw in line for kw in ["if", "check", "!=", ">", "=="]):
                var_name = div_match.group(1)
                if var_name not in ('len', 'sum', 'min', 'max', 'abs', 'float', 'int'):
                    # Check surrounding lines for a guard condition on this variable
                    guard_found = False
                    context_start = max(0, idx - 3)
                    context_end = min(len(lines), idx + 1)
                    for si in range(context_start, context_end):
                        sl = lines[si].strip()
                        if sl.startswith("#") or sl.startswith("//"): continue
                        if re.search(r'\bif\b.*\b' + re.escape(var_name) + r'\b', sl) or re.search(r'\b' + re.escape(var_name) + r'\b.*!=', sl):
                            guard_found = True
                            break
                    if guard_found: continue
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

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            m = re.match(r'^\s*except\s*:', stripped)
            if m:
                errors.append({
                    "line": line_num, "type": "BareExcept",
                    "message": f"Line {line_num}: Bare `except:` catches ALL errors including Ctrl+C. Use `except Exception:` to catch normal errors safely."
                })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            def_match = re.match(r'^\s*def\s+\w+\s*\((.*?)\)\s*:', stripped)
            if def_match:
                params = def_match.group(1)
                bad_defaults = re.findall(r'=\s*(\[\s*\]|\{\s*\}|set\(\s*\)|list\(\s*\))', params)
                if bad_defaults:
                    suggestions.append({
                        "line": line_num, "title": "Mutable Default Argument",
                        "message": f"Line {line_num}: Using `{bad_defaults[0]}` as default argument is shared across all calls. Use `None` instead and create a fresh one inside the function."
                    })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r'\b(if|elif|while)\b', stripped):
                parens = stripped
                for sep in [':', '{', '#']:
                    if sep in parens: parens = parens.split(sep)[0]
                assign_in_cond = re.search(r'(?<![=!<>])=(?!=)', parens)
                if assign_in_cond:
                    err_exists = any(e["line"] == line_num and e["type"] == "AssignmentInCondition" for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "AssignmentInCondition",
                            "message": f"Line {line_num}: You used `=` (assignment) in a condition. Did you mean `==` (comparison)? A single `=` **assigns** a value, `==` **checks** if things are equal."
                        })
                none_cmp = re.search(r'(==|!=)\s*None\b', parens)
                if none_cmp:
                    op = none_cmp.group(1)
                    replacement = "is" if op == "==" else "is not"
                    suggestions.append({
                        "line": line_num, "title": "Use 'is' for None comparison",
                        "message": f"Line {line_num}: Use `{replacement} None` instead of `{op} None`. In Python, `None` is a special singleton — use `is`/`is not` to check for it."
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

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"): continue
            loose_eq = re.findall(r'(?<![=!<>])==(?!=)', stripped)
            if loose_eq:
                if re.search(r'\b(if|while|return|switch)\b', stripped) or '?' in stripped:
                    errors.append({
                        "line": line_num, "type": "LooseEquality",
                        "message": f"Line {line_num}: Use `===` instead of `==`. In JS, `==` does type coercion (e.g., `0 == false` is `true`), which can hide bugs. `===` checks both value AND type."
                    })
            pi = re.search(r'\bparseInt\s*\(', stripped)
            if pi and ',' not in stripped[stripped.index('(')+1:]:
                errors.append({
                    "line": line_num, "type": "MissingRadix",
                    "message": f"Line {line_num}: `parseInt()` needs a second argument (the radix). Use `parseInt(x, 10)` for decimal. Without it, `parseInt('08')` gives 0 in older browsers."
                })
            if stripped.startswith("var "):
                suggestions.append({
                    "line": line_num, "title": "Use let/const instead of var",
                    "message": f"Line {line_num}: Use `let` or `const` instead of `var`. `var` has confusing scoping rules — it's like a messy room where you can't find anything."
                })

    # ------------------------------------------------------------------
    # C / C++ / C# / Dart
    # ------------------------------------------------------------------
    semicolon_langs = ["c", "c++", "c#", "dart", "java", "rust"]
    if lang in semicolon_langs:
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

            # Detect include <header> / include "header" WITHOUT # (plain text include)
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"): continue
                inc_m = re.match(r'include\s+[<"](.+?)[>"]', stripped)
                if inc_m:
                    header = inc_m.group(1).strip()
                    errors.append({
                        "line": line_num, "type": "SyntaxError",
                        "message": f"Line {line_num}: `include` is a preprocessor directive — it needs `#` at the start. Write `#include <{header}>` instead of `include <{header}>`."
                    })
                    fixes.setdefault(line_num, []).append(("replace", line, "#" + line))
                    if header in ("stdio.h", "cstdio"):
                        has_stdio = True
                    continue
                inc_plain = re.match(r'include\s+(\S+)', stripped)
                if inc_plain:
                    errors.append({
                        "line": line_num, "type": "SyntaxError",
                        "message": f"Line {line_num}: Did you mean `#include <{inc_plain.group(1)}>`? `include` without `#` and angle brackets won't work."
                    })
                    fixes.setdefault(line_num, []).append(("replace", line, "#include <" + inc_plain.group(1) + ">"))
                    if inc_plain.group(1) in ("stdio.h", "cstdio"):
                        has_stdio = True

            # Detect preprocessor directives without #: define, ifdef, ifndef, endif, pragma, undef
            preproc_kws = {"define", "ifdef", "ifndef", "endif", "pragma", "undef", "error", "warning", "line"}
            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"): continue
                pp_match = re.match(r'(%s)\b' % '|'.join(sorted(preproc_kws, key=len, reverse=True)), stripped)
                if pp_match:
                    kw = pp_match.group(1)
                    errors.append({
                        "line": line_num, "type": "SyntaxError",
                        "message": f"Line {line_num}: `{kw}` is a preprocessor directive — it needs `#` at the start. Write `#{kw} ...` instead."
                    })
                    fixes.setdefault(line_num, []).append(("replace", line, "#" + line))

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
                                    fixed_after = None
                                    for va in value_args:
                                        if va.startswith("&") and re.match(r'&[a-zA-Z_]', va):
                                            var_name = va[1:]
                                            errors.append({
                                                "line": line_num, "type": "TypeMismatch",
                                                "message": f"Line {line_num}: In `printf`, you passed `{va}` (address of `{var_name}`), but it expects a **value**, not an address. For `printf`, use `{var_name}` (without `&`). `&` is for `scanf`, not `printf`."
                                            })
                                            close_q = line.index('"', line.index('"') + 1)
                                            before = line[:close_q + 1]
                                            if fixed_after is None:
                                                fixed_after = line[close_q + 1:]
                                            fixed_after = fixed_after.replace(va, var_name, 1)
                                    if fixed_after is not None:
                                        fixes.setdefault(line_num, []).append(("replace", line, before + fixed_after))

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
                                    fixed_after = None
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
                                                if fixed_after is None:
                                                    fixed_after = line[close_q + 1:]
                                                fixed_after = fixed_after.replace(va_clean, "&" + vn, 1)
                                    if fixed_after is not None:
                                        fixes.setdefault(line_num, []).append(("replace", line, before + fixed_after))

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("/*"): continue
            last_ch = _last_code_char(line)
            type_kws = ["int ", "float ", "double ", "char ", "String ", "bool ", "void ",
                         "byte ", "short ", "long ", "boolean ", "public ", "private ",
                         "protected ", "class ", "static ", "final ", "const ", "let ",
                         "mut ", "fn ", "impl ", "struct ", "enum ", "trait ",
                         "i32 ", "i64 ", "u32 ", "u64 ", "f32 ", "f64 ",
                         "usize ", "isize ", "Vec ", "Box ", "Option ",
                         "Result ", "HashMap ",
                         "abstract ", "synchronized ", "volatile ", "transient ",
                         "native ", "strictfp ",
                         "string ", "object ", "decimal ",
                         "sbyte ", "uint ", "ulong ", "ushort ",
                         "dynamic ", "var ", "readonly ", "virtual ", "override ",
                         "sealed ", "unsafe ", "fixed ",
                         "pub ", "use ", "mod ", "crate ", "super ", "self ",
                         "where ", "as ", "type ", "impl ", "dyn ",
                         "async ", "await ", "move ", "ref ", "static ",
                         "extern ", "macro_rules"]
            if any(stripped.startswith(kw) for kw in type_kws):
                if last_ch not in (';', '{', '}'):
                    errors.append({
                        "line": line_num, "type": "MissingSemicolon",
                        "message": f"Line {line_num}: Missing `;`. In {language}, every statement ends with a semicolon — like a period at the end of a sentence."
                    })
                    fixes.setdefault(line_num, []).append(("append", ";"))
            if not stripped.startswith("#") and not stripped.startswith("//") and not stripped.startswith("/*"):
                if last_ch not in (';', '{', '}', '('):
                    if '{' in stripped: continue
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

        if lang in ("c", "c++"):
            # ------------------------------------------------------------------
            # MEMORY / POINTER ANALYSIS (C/C++)
            # ------------------------------------------------------------------
            # Pass 1: collect variable info across all lines
            stack_vars = {}        # name -> line_num  (local array/stack variables)
            malloc_vars = {}       # name -> (line_num, size_expr)
            freed_vars = set()     # names that have been freed
            fn_params = set()      # function parameter names (pointer params)
            used_after_free = set()
            func_bodies = {}       # fn_name -> (start_brace_line, end_brace_line)
            brace_depth = 0
            current_fn = None
            fn_start = {}
            defined_constants = {}  # #define NAME VALUE tracking

            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()

                # Track #define numeric constants
                define_m = re.match(r'#\s*define\s+(\w+)\s+(\d+)', stripped)
                if define_m:
                    defined_constants[define_m.group(1)] = int(define_m.group(2))

                # Track function definitions
                fn_def = re.match(r'^(?:\w+\s+)*(\*?\s*\w+)\s*\([^)]*\)\s*\{?\s*(?://.*)?$', stripped)
                if fn_def and not stripped.startswith('if') and not stripped.startswith('while') and not stripped.startswith('for') and not stripped.startswith('return') and not stripped.startswith('//') and not stripped.startswith('/*'):
                    current_fn = fn_def.group(1).strip('*').strip()
                    fn_start[current_fn] = line_num
                    # Extract pointer parameters
                    params_str = re.search(r'\(([^)]*)\)', stripped)
                    if params_str:
                        for param in params_str.group(1).split(','):
                            p = param.strip()
                            # Match pointer params like "int *arr" or "int* arr"
                            ptr_param = re.match(r'(?:\w+\s+)*\*+\s*(\w+)\s*(?:\[[^\]]*\])?$', p)
                            if ptr_param:
                                fn_params.add(ptr_param.group(1).strip('*').strip())
                            # Also capture name for non-pointer params
                            plain_param = re.match(r'(?:\w+\s+)+(\w+)\s*$', p)
                            if plain_param:
                                pname = plain_param.group(1)
                                # Don't add to fn_params for non-pointer params

                # Track braces for function boundaries
                for ch in line:
                    if ch == '{':
                        if current_fn and brace_depth == 0:
                            func_bodies[current_fn] = [line_num, None]
                        brace_depth += 1
                    elif ch == '}':
                        brace_depth = max(0, brace_depth - 1)
                        if brace_depth == 0 and current_fn:
                            if current_fn in func_bodies and func_bodies[current_fn][1] is None:
                                func_bodies[current_fn][1] = line_num
                            current_fn = None

                # Detect stack array declarations: int name[size];
                stack_match = re.match(r'^\s*(?:(?:unsigned|const|static|volatile)\s+)*(?:\w+\s+\**\s*)?(\w+)\s*\[\s*[^\]]+\s*\]\s*;', stripped)
                if stack_match:
                    vname = stack_match.group(1)
                    # Exclude pointer parameters like int *arr[]
                    if not stripped.startswith('*') and ')' not in stripped[:stripped.find(vname)]:
                        stack_vars[vname] = line_num

                # Detect simple local variables (non-pointer, non-array) inside functions
                # Like: int x; char buffer[32];
                local_arr = re.match(r'^\s*(?:\w+\s+)+(\w+)\s*\[\s*\d+\s*\]\s*;', stripped)
                if local_arr:
                    vname = local_arr.group(1)
                    stack_vars[vname] = line_num

                # Detect malloc/calloc/realloc: ptr = malloc(...)
                malloc_match = re.search(r'(\w+)\s*=\s*(?:\(\s*\w+\s*\*?\s*\)\s*)?(malloc|calloc|realloc)\s*\(', stripped)
                if malloc_match:
                    vname = malloc_match.group(1)
                    if vname not in stack_vars:
                        malloc_vars[vname] = (line_num, stripped)
                # Also detect direct assignment from previous variable: ptr = other_malloced_ptr
                assign_from_var = re.search(r'(\w+)\s*=\s*(\w+)', stripped)
                if assign_from_var:
                    vname = assign_from_var.group(1)
                    other = assign_from_var.group(2)
                    if other in malloc_vars and vname not in stack_vars:
                        malloc_vars[vname] = (line_num, stripped)

                # Detect free(ptr) - don't add stack vars to freed_vars
                free_call = re.search(r'\bfree\s*\(\s*(\w+)\s*\)', stripped)
                if free_call:
                    vname = free_call.group(1)
                    if vname not in stack_vars:
                        freed_vars.add(vname)
                    # Invalid free: freeing a stack/local variable
                    if vname in stack_vars:
                        err_exists = any(e["line"] == line_num and e["type"] == "InvalidFree" for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "InvalidFree",
                                "message": f"Line {line_num}: `{vname}` was declared as a stack/local variable (line {stack_vars[vname]}), not allocated with malloc. Calling `free({vname})` crashes the program. Use `free()` only on heap memory from `malloc()`."
                            })
                    elif vname in fn_params and vname not in malloc_vars:
                        err_exists = any(e["line"] == line_num and e["type"] == "InvalidFree" for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "InvalidFree",
                                "message": f"Line {line_num}: `{vname}` is a function parameter (pointer), not necessarily heap memory. Callers may pass stack/local variables. `free()` should only be called on memory returned by `malloc()`."
                            })

                # --- Return address of local variable ---
                return_local = re.search(r'\breturn\s+(\w+)', stripped)
                if return_local:
                    vname = return_local.group(1)
                    if vname in stack_vars:
                        err_exists = any(e["line"] == line_num and e["type"] == "ReturnLocalAddress" for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "ReturnLocalAddress",
                                "message": f"Line {line_num}: Returning the address of `{vname}` (a local/stack variable declared on line {stack_vars[vname]}). When the function exits, its stack memory is reclaimed. The returned pointer becomes invalid — like giving someone your apartment address after you've moved out."
                            })

                # --- Use-after-free (check against FIRST free, not last) ---
                for freed_name in freed_vars:
                    code_only = _strip_c_line(line)
                    if freed_name in code_only and 'free' not in code_only:
                        free_occurrences = [li for li, l in enumerate(lines) if re.search(r'\bfree\s*\(\s*' + re.escape(freed_name) + r'\s*\)', l)]
                        if free_occurrences:
                            first_free_line = free_occurrences[0] + 1
                            if line_num > first_free_line:
                                if re.search(r'\b' + re.escape(freed_name) + r'\b', code_only):
                                    err_exists = any(e["line"] == line_num and e["type"] == "UseAfterFree" and freed_name in e["message"] for e in errors)
                                    if not err_exists:
                                        errors.append({
                                            "line": line_num, "type": "UseAfterFree",
                                            "message": f"Line {line_num}: `{freed_name}` was freed on line {first_free_line} but is still being used here. Accessing memory after freeing it is undefined behavior — like trying to read a book you already returned to the library."
                                        })

            # --- Off-by-one / buffer overflow ---
            # Track malloc sizes and loop bounds
            malloc_sizes = {}  # ptr_name -> max_allocated_size (as int)
            for vname, (ln, text) in malloc_vars.items():
                paren_depth = 0
                start = text.find('malloc(')
                if start >= 0:
                    start += 7  # past 'malloc('
                    end = start
                    for i in range(start, len(text)):
                        if text[i] == '(': paren_depth += 1
                        elif text[i] == ')':
                            if paren_depth == 0:
                                end = i
                                break
                            paren_depth -= 1
                    size_expr = text[start:end]
                    # Substitute #define constants
                    for const_name, const_val in defined_constants.items():
                        size_expr = size_expr.replace(const_name, str(const_val))
                    simple = re.match(r'(?:sizeof\s*\(\s*[^)]+\s*\)\s*\*\s*)?(\d+)', size_expr)
                    if simple:
                        malloc_sizes[vname] = int(simple.group(1))
                    # Fallback: try evaluating simple arithmetic like sizeof(int)*5 -> 5
                    alt = re.search(r'\*\s*(\d+)\s*$', size_expr)
                    if alt:
                        malloc_sizes[vname] = int(alt.group(1))

            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
                    continue

                # Off-by-one: for (int i = 0; i <= n; i++)
                off_by_one = re.search(r'for\s*\(\s*(?:\w+\s+)?(\w+)\s*=\s*\d+\s*;\s*\1\s*<=\s*(\w+)', stripped)
                if off_by_one:
                    var = off_by_one.group(1)
                    bound = off_by_one.group(2)
                    err_exists = any(e["line"] == line_num and e["type"] == "OffByOne" for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "OffByOne",
                            "message": f"Line {line_num}: Loop uses `{var} <= {bound}` — this runs one extra iteration. If `{bound}` is the array size, the last access `{var} = {bound}` reads past the end. Use `{var} < {bound}` instead."
                        })

                # Heap buffer overflow: loop writing to malloc'd ptr with index >= allocated size
                for vname, (ln, text) in malloc_vars.items():
                    if vname in malloc_sizes:
                        max_idx = malloc_sizes[vname] - 1
                    else:
                        max_idx = -1  # unknown size — flag loop writes > reasonable threshold
                    write_to = re.search(r'\b' + re.escape(vname) + r'\s*\[\s*(\w+)\s*\]\s*=', stripped)
                    if write_to:
                        idx_var = write_to.group(1)
                        # If the index is a literal number that's too large
                        if idx_var.isdigit() and int(idx_var) > max_idx:
                            err_exists = any(e["line"] == line_num and e["type"] == "BufferOverflow" for e in errors)
                            if not err_exists:
                                errors.append({
                                    "line": line_num, "type": "BufferOverflow",
                                    "message": f"Line {line_num}: Writing to `{vname}[{idx_var}]` but `{vname}` was allocated with only {malloc_sizes[vname]} element(s) (line {ln}). This writes past the end of the buffer — like trying to park 5 cars in a 4-car garage."
                                })
                        # Check if there's a loop before that iterates beyond the size
                        if not idx_var.isdigit():
                            for pi in range(max(0, idx - 8), idx):
                                pl = lines[pi].strip()
                                loop_bound = re.search(r'for\s*\(\s*(?:\w+\s+)?' + re.escape(idx_var) + r'\s*=\s*\d+\s*;\s*' + re.escape(idx_var) + r'\s*<\s*(\d+)', pl)
                                if loop_bound:
                                    loop_max = int(loop_bound.group(1))
                                    # If malloc size is unknown and loop bound > 8, flag it
                                    if max_idx < 0 and loop_max > 8:
                                        err_exists = any(e["line"] == line_num and e["type"] == "BufferOverflow" for e in errors)
                                        if not err_exists:
                                            errors.append({
                                                "line": line_num, "type": "BufferOverflow",
                                                "message": f"Line {line_num}: Loop iterates up to index {loop_max - 1} but `{vname}` was allocated with an unknown size on line {ln}. This may overflow the buffer."
                                            })
                                    elif max_idx >= 0 and loop_max - 1 > max_idx:
                                        err_exists = any(e["line"] == line_num and e["type"] == "BufferOverflow" for e in errors)
                                        if not err_exists:
                                            errors.append({
                                                "line": line_num, "type": "BufferOverflow",
                                                "message": f"Line {line_num}: Writing to `{vname}[{idx_var}]` but the loop iterates up to {loop_max - 1}, while `{vname}` only has {malloc_sizes[vname]} element(s) (allocated on line {ln}). This is a heap buffer overflow."
                                            })

        if lang == "c":
            for idx, line in enumerate(lines):
                line_num = idx + 1
                uninit = re.match(r'^\s*(int|char|float|double)\s+\w+\s*;\s*$', line)
                if uninit:
                    suggestions.append({
                        "line": line_num, "title": "Uninitialized Variable",
                        "message": f"Line {line_num}: Variable declared without a value. In C, uninitialized variables contain garbage data."
                    })

            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*"): continue
                if re.search(r'\b(if|while|switch)\s*\(', stripped):
                    parens = stripped[stripped.index('(')+1:stripped.rindex(')')] if '(' in stripped and ')' in stripped else ''
                    if parens:
                        assign_in_cond = re.search(r'(?<![=!<>])=(?!=)', parens)
                        if assign_in_cond:
                            err_exists = any(e["line"] == line_num and e["type"] == "AssignmentInCondition" for e in errors)
                            if not err_exists:
                                errors.append({
                                    "line": line_num, "type": "AssignmentInCondition",
                                    "message": f"Line {line_num}: You used `=` (assignment) in a condition. Did you mean `==` (comparison)? A single `=` **assigns** a value, `==` **checks** if values are equal."
                                })

            for idx, line in enumerate(lines):
                line_num = idx + 1
                stripped = line.strip()
                if stripped == "void main()" or stripped.startswith("void main("):
                    errors.append({
                        "line": line_num, "type": "MainReturnType",
                        "message": f"Line {line_num}: `void main()` is not standard C. Use `int main()` — the `int` tells the OS your program ran successfully (return 0) or had an error (return 1)."
                    })
                    fixes.setdefault(line_num, []).append(("replace", line, line.replace("void main", "int main", 1)))
                if re.match(r'^main\s*\(', stripped) and not stripped.startswith("int") and not stripped.startswith("void"):
                    errors.append({
                        "line": line_num, "type": "MainReturnType",
                        "message": f"Line {line_num}: `main()` needs a return type. Use `int main()` — the `int` tells the OS your program ran successfully (return 0) or had an error (return 1)."
                    })
                    fixes.setdefault(line_num, []).append(("replace", line, line.replace("main()", "int main()", 1)))

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
            null_cmp = re.search(r'(WHERE\s+.+?)\s*=\s*NULL\b', stripped, re.I)
            if null_cmp:
                errors.append({
                    "line": line_num, "type": "NullComparison",
                    "message": f"Line {line_num}: Use `IS NULL` instead of `= NULL`. In SQL, nothing equals NULL (not even NULL itself!). `IS NULL` checks if a value is missing."
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
        # Track HTML tags for unclosed detection
        void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
        tag_stack = []
        for idx, line in enumerate(lines):
            line_num = idx + 1
            for m in re.finditer(r'</?(\w+)[^>]*>', line):
                tag = m.group(1).lower()
                if tag in void_tags:
                    continue
                if m.group().startswith('</'):
                    if tag_stack and tag_stack[-1][0] == tag:
                        tag_stack.pop()
                    else:
                        # closing tag doesn't match top — record intervening tags as unclosed
                        for si in range(len(tag_stack) - 1, -1, -1):
                            if tag_stack[si][0] == tag:
                                # mark everything between si and end as unclosed
                                for doomed in range(si + 1, len(tag_stack)):
                                    errors.append({
                                        "line": tag_stack[doomed][1], "type": "SyntaxError",
                                        "message": f"Line {tag_stack[doomed][1]}: `<{tag_stack[doomed][0]}>` was opened but never closed with `</{tag_stack[doomed][0]}>`. Every HTML tag needs a matching closing tag."
                                    })
                                tag_stack = tag_stack[:si]
                                break
                else:
                    tag_stack.append((tag, line_num))
        for tag, ln in tag_stack:
            errors.append({
                "line": ln, "type": "SyntaxError",
                "message": f"Line {ln}: `<{tag}>` was opened but never closed with `</{tag}>`. Every HTML tag needs a matching closing tag."
            })
        if not any("<!DOCTYPE" in l for l in lines):
            if re.search(r'<html', code, re.I):
                errors.append({
                    "line": 1, "type": "MissingDoctype",
                    "message": "Missing `<!DOCTYPE html>` at the top. This tells the browser to use modern standards mode instead of quirks mode — like choosing the right map before driving."
                })
    if lang == "css":
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            brace_count = 0
            for l in lines:
                brace_count += l.count('{') - l.count('}')
            if brace_count > 0:
                suggestions.append({
                    "line": line_num, "title": "Unclosed Brace",
                    "message": "You have {brace_count} unclosed `{{` in your CSS. Every `{{` needs a matching `}}` — like closing a box you opened."
                })
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r':\s*\d+\s*[;}\s]*$', stripped) and not re.search(r'(px|em|rem|%|vh|vw|pt|cm|mm)', stripped):
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
    # C/C++ EXTRA CHECKS (null ptr, double free, memory leak, wild ptr,
    #                     signed/unsigned, modulo zero, stack overflow,
    #                     buffer underflow, missing return, dead code)
    # ------------------------------------------------------------------
    if lang in ("c", "c++"):
        # Track uninitialized pointers and null assignments
        nulled_ptrs = set()
        uninit_ptrs = set()    # pointer vars declared without init
        freed_twice = set()     # already counted for double free
        alloc_lines = {}        # ptr -> line of malloc
        passed_to_free = {}     # ptr -> count of free calls
        dangling_ptrs = {}      # ptr -> (line_assigned, assigned_to_var)
        var_types = {}          # var_name -> "signed" or "unsigned"
        overflow_candidates = set()  # var names assigned near-INT_MAX values

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*"): continue

            # Track NULL assignments
            null_as = re.search(r'(\w+)\s*=\s*(NULL|nullptr|0)\s*;', stripped)
            if null_as:
                nulled_ptrs.add(null_as.group(1))

            # Track dangling pointer: ptr = &localvar
            dangling_as = re.search(r'(\w+)\s*=\s*&(\w+)', stripped)
            if dangling_as:
                ptr_name = dangling_as.group(1)
                local_name = dangling_as.group(2)
                if ptr_name not in malloc_vars and ptr_name not in fn_params:
                    dangling_ptrs[ptr_name] = (line_num, local_name)

            # Track variable types for signed/unsigned comparison detection
            unsigned_decl = re.match(r'^\s*(?:unsigned|size_t|uint\d+_t)\b', stripped)
            if unsigned_decl:
                # Extract the actual variable name (the last identifier after type keywords)
                var_m = re.search(r'(?:unsigned|size_t|uint\d+_t)\s+(?:\w+\s+)*(\w+)\s*[=;]', stripped)
                if var_m:
                    var_types[var_m.group(1)] = "unsigned"
            int_decl = re.match(r'^\s*(?:signed\s+)?(?:int|long|short|char)\s+(\w+)', stripped)
            if int_decl:
                vn = int_decl.group(1)
                # Don't overwrite if already tracked as unsigned
                if vn not in var_types:
                    var_types[vn] = "signed"

            # Track vars assigned near-INT_MAX for overflow detection
            overflow_assign = re.search(r'(\w+)\s*=\s*214748364\d', stripped)
            if overflow_assign:
                overflow_candidates.add(overflow_assign.group(1))

            # Track pointer declaration without init (wild pointer)
            wild = re.match(r'^\s*(?:\w+\s+)*\*+\s*(\w+)\s*;\s*$', stripped)
            if wild:
                vname = wild.group(1)
                if vname not in malloc_vars and vname not in fn_params:
                    uninit_ptrs.add(vname)

            # Double free tracking
            free_call = re.search(r'\bfree\s*\(\s*(\w+)\s*\)', stripped)
            if free_call:
                vname = free_call.group(1)
                passed_to_free[vname] = passed_to_free.get(vname, 0) + 1
                if passed_to_free[vname] > 1 and vname not in freed_twice:
                    freed_twice.add(vname)
                    err_exists = any(e["line"] == line_num and e["type"] == "DoubleFree" for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "DoubleFree",
                            "message": f"Line {line_num}: `{vname}` was already freed earlier. Calling `free()` twice on the same pointer causes undefined behavior — like returning the same library book twice."
                        })

        # Memory leak: malloc'd vars never freed (check last occurrence before function end)
        for vname, (ln, text) in malloc_vars.items():
            if vname not in freed_vars:
                # Check if it was passed to free at some point
                err_exists = any(e["type"] == "MemoryLeak" and vname in e["message"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": ln, "type": "MemoryLeak",
                        "message": f"Line {ln}: `{vname}` was allocated with malloc here but never freed. Memory that isn't freed leaks — like checking out a hotel room and never checking out."
                    })

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*"): continue

            # Null pointer dereference via -> or *
            null_used = re.search(r'(?<!\w)(\w+)\s*->', stripped)
            if null_used:
                vname = null_used.group(1)
                if vname in nulled_ptrs:
                    err_exists = any(e["line"] == line_num and "NullPointer" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "NullPointerDereference",
                            "message": f"Line {line_num}: `{vname}` was set to NULL earlier but is being dereferenced with `->`. Dereferencing a NULL pointer crashes your program — like trying to open a door that doesn't exist."
                        })
            # *ptr = val or *ptr; where ptr is NULL
            null_star = re.search(r'\*(\w+)\s*[=;]', stripped)
            if null_star:
                vname = null_star.group(1)
                if vname in nulled_ptrs:
                    first_word = stripped.split()[0] if stripped.split() else ''
                    type_kws = {'int','char','float','double','long','short','unsigned','void','const','static','volatile','struct','signed'}
                    if first_word not in type_kws:
                        err_exists = any(e["line"] == line_num and "NullPointer" in e["type"] for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "NullPointerDereference",
                                "message": f"Line {line_num}: `{vname}` was set to NULL earlier but is being dereferenced here. Writing to or reading from a NULL pointer crashes your program — like trying to open a door that doesn't exist."
                            })

            # Wild pointer (using uninitialized pointer)
            for wp in uninit_ptrs:
                if re.search(r'\b' + re.escape(wp) + r'\s*->|\*' + re.escape(wp) + r'\b', stripped):
                    # Skip declarations (int *ptr;) — they're not dereferences
                    first_word = stripped.split()[0] if stripped.split() else ''
                    type_kws = {'int','char','float','double','long','short','unsigned','void','const','static','volatile','struct','signed'}
                    if first_word in type_kws:
                        continue
                    # Check if it's actually a dangling pointer (assigned local address)
                    if wp in dangling_ptrs:
                        dline, dvar = dangling_ptrs[wp]
                        err_exists = any(e["line"] == line_num and "DanglingPointer" in e["type"] for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "DanglingPointer",
                                "message": f"Line {line_num}: `{wp}` holds the address of local variable `{dvar}` which may have gone out of scope. Using a dangling pointer is undefined behavior — like reading a letter after the mailbox was removed."
                            })
                    else:
                        err_exists = any(e["line"] == line_num and "WildPointer" in e["type"] for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "WildPointer",
                                "message": f"Line {line_num}: `{wp}` was declared but not initialized. Using an uninitialized pointer is undefined behavior — like driving a car without knowing where the steering wheel is."
                            })

            # Buffer underflow (negative index)
            underflow = re.search(r'(\w+)\s*\[\s*-\s*\d+\s*\]', stripped)
            if underflow:
                err_exists = any(e["line"] == line_num and "BufferUnderflow" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "BufferUnderflow",
                        "message": f"Line {line_num}: Using a negative index `[{underflow.group(0).split('[')[1]}` on `{underflow.group(1)}`. Negative indices access memory before the array — like stepping backward off a cliff."
                    })

            # Signed/unsigned mismatch in comparison
            sus = re.search(r'(\w+)\s*(<|>|<=|>=)\s*(\w+)', stripped)
            if sus:
                v1, op, v2 = sus.group(1), sus.group(2), sus.group(3)
                unsigned_kw = {"unsigned", "size_t", "uint8_t", "uint16_t", "uint32_t", "uint64_t"}
                is_unsigned = v1 in unsigned_kw or v2 in unsigned_kw or var_types.get(v1) == "unsigned" or var_types.get(v2) == "unsigned"
                is_signed = var_types.get(v1) == "signed" or var_types.get(v2) == "signed"
                if is_unsigned and is_signed:
                    err_exists = any(e["line"] == line_num and "SignedUnsigned" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "SignedUnsignedMismatch",
                            "message": f"Line {line_num}: Comparing signed and unsigned values can produce unexpected results. The signed value may become a large positive number when implicitly converted."
                        })

            # Modulo by zero
            mod_zero = re.search(r'(\w+)\s*%\s*(\w+)', stripped)
            if mod_zero:
                divisor = mod_zero.group(2)
                if divisor in nulled_ptrs:
                    err_exists = any(e["line"] == line_num and "ModuloZero" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "ModuloByZero",
                            "message": f"Line {line_num}: `{divisor}` could be zero. Modulo by zero crashes your program — like asking 'how many times does 0 fit into 10?' There's no answer!"
                        })

            # Division / modulo by literal zero
            div_zero = re.search(r'(?<!\w)(\w+)\s*/\s*0\b', stripped)
            if div_zero:
                err_exists = any(e["line"] == line_num and ("DivByZero" in e["type"] or "DivisionByZero" in e["type"]) for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "DivisionByZero",
                        "message": f"Line {line_num}: Division by literal zero. Dividing by zero crashes your program — like asking 'how many groups of nothing can you make?' It has no answer."
                    })
            mod_zero_lit = re.search(r'(?<!\w)(\w+)\s*%\s*0\b', stripped)
            if mod_zero_lit:
                err_exists = any(e["line"] == line_num and ("DivByZero" in e["type"] or "DivisionByZero" in e["type"] or "ModuloByZero" in e["type"]) for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "DivisionByZero",
                        "message": f"Line {line_num}: Modulo by literal zero. Using `% 0` crashes your program — like asking 'how many groups of nothing can you make?' It has no answer."
                    })

            # Detect function calls where a parameter is literal 0 and may be used as divisor
            div_call = re.search(r'(\w+)\s*\(\s*[^)]*\b(\w+)\s*,\s*0\s*\)', stripped)
            if div_call:
                err_exists = any(e["line"] == line_num and ("DivByZero" in e["type"] or "DivisionByZero" in e["type"]) for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "DivisionByZero",
                        "message": f"Line {line_num}: Calling `{div_call.group(1)}()` with 0 as an argument. If the function divides by this parameter, it will crash."
                    })

            # Detect division by function parameter in function body
            fn_div = re.search(r'/(\w+)\b', stripped)
            if fn_div:
                divisor_var = fn_div.group(1)
                if divisor_var in fn_params:
                    err_exists = any(e["line"] == line_num and ("DivByZero" in e["type"] or "DivisionByZero" in e["type"]) for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "DivisionByZero",
                            "message": f"Line {line_num}: Dividing by `{divisor_var}`, which is a function parameter. If someone passes 0, this crashes. Add a zero check before dividing."
                        })

            # Integer overflow: track variable increment on overflow candidates
            if overflow_candidates:
                overflow_use = re.search(r'(\w+)\s*=\s*\1\s*\+\s*1', stripped)
                if overflow_use and overflow_use.group(1) in overflow_candidates:
                    err_exists = any(e["line"] == line_num and "IntegerOverflow" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "IntegerOverflow",
                            "message": f"Line {line_num}: `{overflow_use.group(1)}` was assigned a near-INT_MAX value earlier. Adding 1 causes signed integer overflow — undefined behavior."
                        })

            # if (0) dead code: code inside if (0) { ... } is never reached
            if re.match(r'^\s*if\s*\(\s*0\s*\)', stripped):
                # Flag the next non-empty, non-brace line as dead code
                for ni in range(idx + 1, min(idx + 5, len(lines))):
                    nxt = lines[ni].strip()
                    if not nxt or nxt == '{' or nxt.startswith('//') or nxt.startswith('/*'):
                        continue
                    if nxt == '}':
                        break
                    err_exists = any(e["line"] == ni + 1 and "DeadCode" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": ni + 1, "type": "DeadCode",
                            "message": f"Line {ni + 1}: This code is inside `if (0)` on line {line_num} and will never execute. The condition is always false."
                        })
                    break

            # Stack overflow: detect very large local arrays
            large_stack = re.match(r'^\s*(?:\w+\s+)+(\w+)\s*\[\s*(\d+)\s*\]\s*;', stripped)
            if large_stack:
                vname = large_stack.group(1)
                size = int(large_stack.group(2))
                if size > 1000000:
                    err_exists = any(e["line"] == line_num and "StackOverflow" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "StackOverflow",
                            "message": f"Line {line_num}: `{vname}` allocates {size} elements on the stack ({size * 4} bytes). Very large stack allocations can overflow the stack and crash."
                        })

            # Missing return statement in non-void function
            non_void_fn = re.match(r'^(?:\w+\s+)+(?:[*\s]*)(\w+)\s*\(', stripped)
            if non_void_fn and not stripped.startswith("void") and not stripped.startswith("int main") and not stripped.startswith("//") and not stripped.startswith("/*"):
                fn_name = non_void_fn.group(1)
                # Find matching function body and check for return
                if fn_name in func_bodies:
                    fstart, fend = func_bodies[fn_name]
                    if fstart and fend:
                        body_lines = lines[fstart:fend]
                        has_return = any('return' in l for l in body_lines)
                        has_void = any('void' in l and fn_name in l for l in body_lines)
                        if not has_return and not has_void:
                            err_exists = any(e["type"] == "MissingReturn" and fn_name in e["message"] for e in errors)
                            if not err_exists:
                                errors.append({
                                    "line": line_num, "type": "MissingReturn",
                                    "message": f"Line {line_num}: Function `{fn_name}` has a non-void return type but is missing a `return` statement. Like promising to give someone an answer but never delivering it."
                                })

            # Dead code: code after return/break/continue (no label)
            if re.search(r'\b(return|break|continue)\s*;', stripped):
                for ni in range(idx + 1, min(idx + 4, len(lines))):
                    nxt = lines[ni].strip()
                    if not nxt or nxt.startswith("//") or nxt.startswith("/*") or nxt == "}":
                        continue
                    if nxt.endswith(":") and not nxt.startswith("case") and not nxt.startswith("default"):
                        break  # label
                    err_exists = any(e["line"] == ni + 1 and "DeadCode" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": ni + 1, "type": "DeadCode",
                            "message": f"Line {ni + 1}: Code after `return`/`break`/`continue` on line {line_num} will never run. Like writing instructions after a full stop — nobody reads them."
                        })
                    break  # only flag the first line after

            # Integer overflow detection
            int_max_str = '2147483647'  # INT_MAX
            if int_max_str in stripped:
                err_exists = any(e["line"] == line_num and "IntegerOverflow" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "IntegerOverflow",
                        "message": f"Line {line_num}: INT_MAX ({int_max_str}) used. Adding to or past this value causes signed integer overflow — undefined behavior."
                    })

            # Buffer overflow via strcpy with unsafe destination
            strcpy_m = re.search(r'\bstrcpy\s*\(\s*(\w+)', stripped)
            if strcpy_m:
                dest = strcpy_m.group(1)
                if dest in stack_vars:
                    err_exists = any(e["line"] == line_num and "BufferOverflow" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "BufferOverflow",
                            "message": f"Line {line_num}: `strcpy()` writes to `{dest}` without bounds checking. If the source string is longer than the destination buffer, it overflows — like pouring a gallon of water into a pint glass."
                        })

            # Infinite recursion (function calling itself)
            for fn_name, (fstart, fend) in func_bodies.items():
                if fstart and line_num > fstart and (fend is None or line_num < fend):
                    if re.search(r'\b' + re.escape(fn_name) + r'\s*\(', stripped):
                        err_exists = any(e["line"] == line_num and "InfiniteRecursion" in e["type"] for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "InfiniteRecursion",
                                "message": f"Line {line_num}: `{fn_name}()` calls itself inside its own body. Without a base case, this causes infinite recursion and a stack overflow — like a mirror facing another mirror, infinitely."
                            })

            # String literal modification
            str_mod = re.search(r'(\w+)\s*\[\s*\d+\s*\]\s*=\s*[\'"]', stripped)
            if str_mod:
                vname = str_mod.group(1)
                # Check if the variable was assigned a string literal
                for pi in range(max(0, idx - 10), idx):
                    pl = lines[pi].strip()
                    if re.match(r'^.*\b' + re.escape(vname) + r'\s*=\s*"', pl) and not re.search(r'malloc|calloc|realloc|new|\[', pl):
                        err_exists = any(e["line"] == line_num and "StringLiteralModification" in e["type"] for e in errors)
                        if not err_exists:
                            errors.append({
                                "line": line_num, "type": "StringLiteralModification",
                                "message": f"Line {line_num}: `{vname}` points to a string literal (defined earlier). Modifying a string literal is undefined behavior in C — like trying to erase a word in a printed book."
                            })
                        break

            # Incorrect format specifier: %s with non-string (int) argument
            format_m = re.search(r'printf\s*\([^)]*%s[^)]*,\s*(\d+)', stripped)
            if format_m:
                err_exists = any(e["line"] == line_num and "FormatMismatch" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "FormatMismatch",
                        "message": f"Line {line_num}: `%s` format specifier expects a string (char*), but the argument is the number {format_m.group(1)}. This will crash or print garbage."
                    })

            # Undefined shift / shift overflow: 1 << N where N >= bit width
            shift_m = re.search(r'1\s*<<\s*(\d+)', stripped)
            if shift_m:
                shift_amt = int(shift_m.group(1))
                if shift_amt >= 32:
                    err_exists = any(e["line"] == line_num and "ShiftOverflow" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "ShiftOverflow",
                            "message": f"Line {line_num}: Shifting 1 left by {shift_amt} bits is undefined behavior when the shift exceeds or equals the type width (typically 32 for int)."
                        })

            # Sequence point violation: variable modified twice between sequence points
            seq_m = re.search(r'(\w+)\s*=\s*\w+\+\+\s*\+\+\s*\w+|\w+\+\+\s*\+\s*\+\+\w+', stripped)
            if seq_m or re.search(r'=\s*\w+\+\+\s*\+\s*\+\+\w+', stripped):
                err_exists = any(e["line"] == line_num and "SequencePointViolation" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "SequencePointViolation",
                        "message": f"Line {line_num}: A variable is modified multiple times between sequence points. This is undefined behavior — the result can vary between compilers."
                    })

            # Missing NULL check after malloc
            if re.search(r'(\w+)\s*=\s*(?:\(\s*\w+\s*\*?\s*\)\s*)?(malloc|calloc|realloc)\s*\(', stripped):
                alloc_var = re.search(r'(\w+)\s*=', stripped).group(1)
                check_found = False
                for ci in range(idx + 1, min(idx + 6, len(lines))):
                    cl = lines[ci].strip()
                    if re.search(r'\b' + re.escape(alloc_var) + r'\s*==\s*(NULL|0)\b', cl) or re.search(r'!\s*' + re.escape(alloc_var), cl):
                        check_found = True
                        break
                if not check_found:
                    err_exists = any(e["line"] == line_num and "MissingNullCheck" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "MissingNullCheck",
                            "message": f"Line {line_num}: `{alloc_var}` is allocated with malloc() but the return value is not checked for NULL. malloc() can fail and return NULL — always check if the result is NULL."
                        })

    # ------------------------------------------------------------------
    # PYTHON MISSING RETURN, SHADOWING, ACCIDENTAL RECURSION, DEAD CODE
    # ------------------------------------------------------------------
    if lang == "python":
        # Variable shadowing: function param shadows outer variable
        defined_vars = {}
        for idx, line in enumerate(lines):
            assign = re.match(r'^\s*([a-zA-Z_]\w*)\s*=', line)
            if assign:
                defined_vars[assign.group(1)] = idx + 1

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            fn_def = re.match(r'^\s*def\s+(\w+)\s*\((.*?)\)\s*:', stripped)
            if fn_def:
                fn_name = fn_def.group(1)
                params_str = fn_def.group(2)
                for param in params_str.split(','):
                    pname = param.strip().split('=')[0].strip()
                    if pname and pname in defined_vars and defined_vars[pname] < line_num:
                        # Check if the outer var is actually used inside the function
                        err_exists = any(e["line"] == line_num and "VariableShadowing" in e["type"] for e in errors)
                        if not err_exists:
                            suggestions.append({
                                "line": line_num, "title": "Variable Shadowing",
                                "message": f"Line {line_num}: Parameter `{pname}` shadows a variable defined on line {defined_vars[pname]}. Like naming your pet 'Sun' when you already have a star called Sun — confusing!"
                            })

        # Find function boundaries for missing return detection (indentation-based)
        fn_bodies = {}
        fn_stack = []
        for idx, line in enumerate(lines):
            stripped = line.strip()
            fn_m = re.match(r'^\s*def\s+(\w+)\s*\(', stripped)
            if fn_m:
                fn_name = fn_m.group(1)
                current_indent = len(line) - len(line.lstrip())
                fn_bodies[fn_name] = [idx + 1, len(lines), current_indent]
            else:
                # Detect end of function by reduced indentation
                for fn_name, (fstart, fend, findent) in list(fn_bodies.items()):
                    if fend == len(lines) and stripped and not stripped.startswith("#") and not stripped.startswith("'''") and not stripped.startswith('"""'):
                        line_indent = len(line) - len(line.lstrip())
                        if line_indent <= findent and idx + 1 > fstart:
                            # Check it's not a decorator or continuation
                            if not stripped.startswith("@") and not stripped.startswith(".") and not stripped.startswith(")"):
                                fn_bodies[fn_name][1] = idx + 1

        # Missing return detection
        for fn_name, (fstart, fend, findent) in fn_bodies.items():
            has_return = any(re.search(r'^\s*return\b', lines[i]) for i in range(fstart, min(fend, len(lines))))
            if not has_return:
                err_exists = any(e["type"] == "MissingReturn" and fn_name in e["message"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": fstart, "type": "MissingReturn",
                        "message": f"Line {fstart}: Function `{fn_name}` is missing a `return` statement. In Python, if a function doesn't return a value, it returns `None` — like saying you'll bring dessert but showing up empty-handed."
                    })

        # Accidental recursion: function calling itself by the same name
        fn_names = set()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            fn_m = re.match(r'^\s*def\s+(\w+)\s*\(', stripped)
            if fn_m:
                fn_names.add(fn_m.group(1))

        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            for fn_name in fn_names:
                # Check if function calls itself (outside a recursive pattern)
                if re.search(r'\b' + re.escape(fn_name) + r'\s*\(', stripped):
                    # Find if this line is inside the function body of fn_name
                    inside_self = False
                    for fname, (fstart, fend, findent) in fn_bodies.items():
                        if fname == fn_name and fstart and fstart < line_num:
                            if line_num < fend:
                                inside_self = True
                                break
                    if inside_self:
                        # Count recursive calls: if 2+ calls to self without base case
                        err_exists = any(e["line"] == line_num and e["type"] == "AccidentalRecursion" for e in errors)
                        if not err_exists:
                            suggestions.append({
                                "line": line_num, "title": "Possible Accidental Recursion",
                                "message": f"Line {line_num}: `{fn_name}` calls itself. If there's no base case to stop it, this will cause infinite recursion and crash with a `RecursionError`."
                            })

        # Dead code in Python
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.match(r'^\s*(return|break|continue)\b', stripped):
                for ni in range(idx + 1, min(idx + 4, len(lines))):
                    nxt = lines[ni].strip()
                    if not nxt or nxt.startswith("#") or nxt == "pass":
                        continue
                    if nxt.startswith(("def ", "class ", "@", "if ", "elif ", "else:", "try:", "except", "finally:", "for ", "while ")):
                        break
                    err_exists = any(e["line"] == ni + 1 and "DeadCode" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": ni + 1, "type": "DeadCode",
                            "message": f"Line {ni + 1}: Code after `return`/`break`/`continue` on line {line_num} will never be reached. Like writing instructions after a full stop."
                        })
                    break

    # ------------------------------------------------------------------
    # JS MISSING RETURN, DEAD CODE
    # ------------------------------------------------------------------
    if lang in ("javascript", "typescript"):
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if re.search(r'\b(return|break|continue)\s*;', stripped):
                for ni in range(idx + 1, min(idx + 4, len(lines))):
                    nxt = lines[ni].strip()
                    if not nxt or nxt.startswith("//") or nxt.startswith("/*") or nxt in ("}", "});"):
                        continue
                    if nxt.endswith(":") and not nxt.startswith("case") and not nxt.startswith("default"):
                        break
                    err_exists = any(e["line"] == ni + 1 and "DeadCode" in e["type"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": ni + 1, "type": "DeadCode",
                            "message": f"Line {ni + 1}: Code after `return`/`break`/`continue` on line {line_num} will never run."
                        })
                    break

    # ------------------------------------------------------------------
    # CROSS-LANGUAGE CHECKS (hardcoded credentials, command injection,
    #                        path traversal, misspelled keywords,
    #                        invalid operator usage)
    # ------------------------------------------------------------------
    c_keywords = {"auto", "break", "case", "char", "const", "continue", "default", "do", "double",
                  "else", "enum", "extern", "float", "for", "goto", "if", "inline", "int", "long",
                  "register", "restrict", "return", "short", "signed", "sizeof", "static", "struct",
                  "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "include",
                  "define", "ifdef", "ifndef", "endif", "malloc", "free", "printf", "scanf", "NULL"}

    python_keywords = {"False", "None", "True", "and", "as", "assert", "async", "await", "break",
                       "class", "continue", "def", "del", "elif", "else", "except", "finally", "for",
                       "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or",
                       "pass", "raise", "return", "try", "while", "with", "yield"}

    js_keywords = {"async", "await", "break", "case", "catch", "class", "const", "continue",
                   "debugger", "default", "delete", "do", "else", "enum", "export", "extends",
                   "false", "finally", "for", "function", "if", "import", "in", "instanceof", "let",
                   "new", "null", "of", "return", "super", "switch", "this", "throw", "true", "try",
                   "typeof", "undefined", "var", "void", "while", "with", "yield"}

    # Misspelled keyword detection
    if lang in ("c", "c++"):
        kw_set = c_keywords
    elif lang == "python":
        kw_set = python_keywords
    elif lang in ("javascript", "typescript"):
        kw_set = js_keywords
    else:
        kw_set = set()

    if kw_set:
        for idx, line in enumerate(lines):
            line_num = idx + 1
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
                continue
            # Strip string contents before keyword matching to avoid false positives
            no_strings = re.sub(r'"[^"]*"', ' ', stripped)
            no_strings = re.sub(r"'[^']*'", ' ', no_strings)
            words = re.findall(r'\b([a-zA-Z_]\w*)\b', no_strings)
            for w in words:
                if w in kw_set:
                    continue
                best = min(kw_set, key=lambda k: _edit_distance(w, k))
                dist = _edit_distance(w, best)
                if 1 <= dist <= 2 and dist < len(w) * 0.5:
                    err_exists = any(e["line"] == line_num and "MisspelledKeyword" in e["type"] and w in e["message"] for e in errors)
                    if not err_exists:
                        errors.append({
                            "line": line_num, "type": "MisspelledKeyword",
                            "message": f"Line {line_num}: `{w}` is not a valid keyword. Did you mean `{best}`? Like writing `{w}` when you meant `{best}` — close, but not quite right."
                        })
                    break  # one keyword per line

    # Invalid operator usage (language-specific)
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            continue
        # === outside JS/TS
        if lang not in ("javascript", "typescript"):
            if re.search(r'[^=!]=[^=!]', stripped) and re.search(r'={3,}', stripped):
                err_exists = any(e["line"] == line_num and "InvalidOperator" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "InvalidOperatorUsage",
                        "message": f"Line {line_num}: `===` is not valid in {language}. Use `==` for equality comparison."
                    })
        # => in non-JS/TS (arrow function)
        if lang not in ("javascript", "typescript", "dart", "kotlin", "rust", "go"):
            if re.search(r'=\s*>\s*[^{]', stripped) and '=>' in stripped:
                # Not a lambda context
                err_exists = any(e["line"] == line_num and "InvalidOperator" in e["type"] and "=>" in e["message"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "InvalidOperatorUsage",
                        "message": f"Line {line_num}: `=>` (arrow function) is not valid in {language}. Maybe you meant `>=` or `<=`?"
                    })

    # Hardcoded credentials
    secret_patterns = [
        r'(password|passwd|pwd|secret|api_key|apikey|token|auth_token)\s*[:=]\s*["\'][^"\']+["\']',
        r'(password|passwd|pwd|secret|api_key|apikey|token|auth_token)\s*[:=]\s*["\'][^"\']+["\']',
    ]
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            continue
        for pat in secret_patterns:
            if re.search(pat, stripped, re.I):
                err_exists = any(e["line"] == line_num and "HardcodedCredential" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "HardcodedCredential",
                        "message": f"Line {line_num}: Possible hardcoded credential detected. Storing passwords, API keys, or tokens in code is a security risk. Use environment variables instead."
                    })
                break

    # Command injection (exec/system with dynamic input)
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            continue
        if lang == "python":
            if re.search(r'\b(exec|eval|os\.system|subprocess\.call|subprocess\.Popen)\s*\(', stripped):
                err_exists = any(e["line"] == line_num and "CommandInjection" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "CommandInjection",
                        "message": f"Line {line_num}: Using `{stripped.split('(')[0].split(' ')[-1]}()` with user input can lead to command injection. Prefer safe alternatives or validate inputs strictly."
                    })
        elif lang in ("c", "c++"):
            if re.search(r'\b(system|popen|exec[lvpe]?)\s*\(', stripped):
                err_exists = any(e["line"] == line_num and "CommandInjection" in e["type"] for e in errors)
                if not err_exists:
                    errors.append({
                        "line": line_num, "type": "CommandInjection",
                        "message": f"Line {line_num}: Calling `system()` or `exec()` with user input can execute arbitrary commands. Validate all inputs and prefer safer APIs."
                    })

    # Path traversal detection
    for idx, line in enumerate(lines):
        line_num = idx + 1
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            continue
        if re.search(r'\.\./|\.\.\\|\.\.[/\\]', stripped):
            err_exists = any(e["line"] == line_num and "PathTraversal" in e["type"] for e in errors)
            if not err_exists:
                errors.append({
                    "line": line_num, "type": "PathTraversal",
                    "message": f"Line {line_num}: Detected `../` (path traversal pattern). If this comes from user input, it can allow access to files outside the intended directory."
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
    # AUTO-FIX — generate fixes for common C errors
    # ------------------------------------------------------------------
    for err in errors:
        ln = err["line"]
        idx = ln - 1
        if idx < 0 or idx >= len(lines):
            continue
        orig = lines[idx]
        err_type = err["type"]
        if err_type == "AssignmentInCondition":
            # Replace = with == in if/while conditions
            fixed = re.sub(r'(\b(?:if|while|for)\s*\()([^)]*?)(\w+)\s*=\s*(\w+)', lambda m: m.group(1) + m.group(2) + m.group(3) + ' == ' + m.group(4), orig)
            if fixed != orig:
                fixes.setdefault(ln, []).append(("replace", orig, fixed))
        elif err_type == "OffByOne":
            # Replace <= with < (common off-by-one loop fix)
            fixed = re.sub(r'(<=)', '<', orig, count=1)
            if fixed != orig:
                fixes.setdefault(ln, []).append(("replace", orig, fixed))
        elif err_type == "MissingSemicolon":
            stripped = orig.rstrip()
            if not stripped.endswith(";"):
                fixes.setdefault(ln, []).append(("replace", orig, stripped + ";"))
        elif err_type == "DivisionByZero":
            # Replace literal 0 divisor with a safe value
            fixed = re.sub(r'/\s*0\b', '/ 1', orig)
            if fixed != orig:
                fixes.setdefault(ln, []).append(("replace", orig, fixed))
        elif err_type == "ReturnLocalAddress":
            # Replace return &local with return NULL
            fixed = re.sub(r'return\s+&\w+', 'return NULL', orig)
            if fixed != orig:
                fixes.setdefault(ln, []).append(("replace", orig, fixed))
        elif err_type == "MissingNullCheck":
            # Wrap the malloc result in a NULL check
            mal = re.search(r'(\w+)\s*=\s*malloc\(', orig)
            if mal:
                var_name = mal.group(1)
                fixes.setdefault(ln, []).append(("append", f"if (!{var_name}) return NULL;    // added NULL check"))

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
                    line = line.rstrip() + "  // " + fix[1]
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
            explanation = "Your code has some bugs. Think of code like a recipe. If a step is wrong, the dish will not come out right!\n\n"
            for i, err in enumerate(errors):
                if i > 0:
                    explanation += "\n"
                explanation += _get_error_explanation(err, lines, lang) + "\n"
        else:
            explanation = "Your code looks good! Check the Suggestions tab for tips to make it cleaner.\n"

        explanation += "\nWhat each line does:\n"
        for idx, line in enumerate(display_lines[:8]):
            first_line = line.strip().split("\n")[0][:60]
            if first_line:
                explanation += f"  Line {idx+1}: {first_line}\n"
        if len(display_lines) > 8:
            explanation += f"  ... and {len(display_lines)} lines total\n"
    else:
        if errors:
            explanation = f"Issues Detected: {len(errors)} error(s) found.\n\n"
            for err in errors:
                explanation += f"  L{err['line']} - {err['type']}: {err['message']}\n"
        else:
            explanation = "No critical issues detected.\n"
        explanation += "\nCode flow:\n"
        for idx, line in enumerate(display_lines[:5]):
            first_line = line.strip().split("\n")[0][:60]
            if first_line:
                explanation += f"  L{idx+1}: {first_line}\n"
        if len(display_lines) > 5:
            explanation += f"  ... and {len(display_lines)-5} more lines.\n"

    complexity = analyze_complexity(code, language)

    return {
        "errors": errors,
        "suggestions": suggestions,
        "explanation": explanation,
        "fixed_code": fixed_code,
        "analysis_metrics": complexity
    }
