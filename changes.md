# CodeSage Change Documentation (`changes.md`)

This file logs all architectural, backend, and frontend modifications implemented to construct the **CodeSage** AI debugging and tutoring platform.

---

## 1. Project Directory Structure
Scaffolded a full-stack monorepo layout containing isolated client and server spaces:
- **`frontend/`**: Vite + React single-page application.
- **`backend/`**: Native Python HTTP server microservice.

---

## 2. Backend Implementation (Python)

### Created: `backend/app/main.py`
- Implemented a **zero-dependency native HTTP server** based on Python's built-in `http.server` library to solve package compilation bottlenecks (such as `pydantic-core` wheels lacking compiled binaries on Python 3.14.2).
- Designed custom REST router pathways supporting:
  - `POST /api/analyze`: Parses submitted code snippets and caches them.
  - `GET /api/dashboard`: Aggregates dynamic statistics, historical upload logs, and trend data.
  - `GET /api/submission/{id}`: Resolves step-by-step reports for matching logs.
- Configured a **CORS Responder** responding to standard and pre-flight OPTIONS headers.
- Maintained an active in-memory cache to sync frontend submission logs in real-time.

### Created: `backend/app/analyzer.py`
- Coded a heuristic analysis engine diagnosing programming errors:
  - Python `ZeroDivisionError` (e.g. dividing values by un-validated variables or list counts).
  - Python `TypeError` (e.g. computing index variables directly or combining strings/integers).
  - Python `SyntaxError` via `ast.parse` for real syntax error detection.
  - Missing colons after Python keywords (`if`, `for`, `while`, `def`, `class`, etc.).
  - Unclosed string quotes and mismatched brackets (all languages).
  - Undefined variables/iterables in Python for-loops.
  - Tab vs space mixed indentation detection.
  - JavaScript / TypeScript syntax omissions (e.g. missing semicolons in variable definitions).
  - C/C++/C#/Dart uninitialized variables and missing semicolons.
  - SQL `UPDATE`/`DELETE` without `WHERE` clause detection.
  - HTML self-closing void element consistency.
  - CSS missing units and invalid color values.
  - Infinite Loops (`while True` or `while(true)` blocks devoid of break keywords).
- Multi-line bracket/quote tracking via `_find_unclosed_multiline()` — detects unmatched `(`, `[`, `{` and unclosed string literals across the entire code, not just per-line.
- Demo snippet matching changed from normalized structural comparison to **exact string match** — only the exact default demo text matches, preventing user code from hijacking demo results.
- Removed frontend `runLocalAnalysis` fake predefined matchers (was matching any code containing `"calculate_average"` or `"prices"`) — replaced with proper error state when backend is unreachable.
- Removed frontend hardcoded initial analysis state — analysis starts empty until user clicks Analyze.
- C/C++ include-file validation: detects misspelled standard headers (e.g. `stdo.h` → `stdio.h`) using Levenshtein distance, and `printf`/`scanf` used without `#include <stdio.h>`.
- Duplicate error suppression — missing colon regex check skips if AST already reported a SyntaxError on that line.
- Beginner-friendly explanations with plain English and everyday analogies (cookies, recipes, sticky notes).
- Fixed code generation with zero-division guards.

### Created: `backend/app/gemini_service.py`
- Integrated Google Gemini 2.5 Flash API for AI-powered code analysis.
- Two prompt modes: beginner (plain English, analogies, line-by-line) and intermediate (technical).
- Fallback to local analyzer when Gemini is unavailable or returns errors.
- Added 2-second hard timeout via daemon thread — prevents blocking the server when Gemini is slow or rate-limited.

### Updated: `backend/app/main.py`
- Added Gemini API integration with fallback to local heuristic analyzer.
- Environment variable support via `load_dotenv()`.
- CORS configured with `FRONTEND_URL` from environment.
- Added `_safe_write()` to catch `ConnectionAbortedError`/`BrokenPipeError` when clients disconnect — prevents server crash loops.
- All `self.wfile.write()` calls replaced with `self._safe_write()` for graceful disconnect handling.

### Created: `backend/requirements.txt`
- Configured standard backend packages (`fastapi`, `uvicorn`, `pydantic`) as fallback documentation indicators.

---

## 3. Frontend Implementation (React)

### Configured: `frontend/package.json`
- Installed **`lucide-react`** to render premium UI iconography (Award medals, fire flames, bugs, rockets, play symbols, and check marks).

### Replaced: `frontend/src/index.css`
- Wrote a unified global **Design System & Aesthetics Theme** utilizing Outfit and JetBrains Mono fonts.
- Tailored harmonious color variables via modern **HSL values**:
  - Primary Purple: HSL `(242, 60%, 59%)`
  - Error Indicators: HSL `(348, 77%, 57%)`
- Created styles for custom scrollbars, badges, glowing borders, card transitions, and active line-height wrappers.

### Created: `frontend/src/components/Header.jsx`
- Formed a navigation header containing active route tracking tabs, SVGs representing the hexagonal bracket icon, and active profile displays.

### Created: `frontend/src/components/Footer.jsx`
- Built a site footer detailing site maps, copyrights, and terms of service policies.

### Created: `frontend/src/constants/languages.js`
- Centralized language definitions for 17 languages: Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, Dart, Ruby, PHP, Swift, Kotlin, C#, SQL, HTML, CSS.
- `extToLanguage()` maps file extensions to language keys.
- `acceptExtensions()` generates HTML `accept` attribute for file uploads.
- Used across Home, Analyze, and Dashboard pages.

### Created: `frontend/src/pages/Home.jsx`
- Built the Landing page incorporating the hero block, how-it-works grids, and standard pricing blocks.
- Embedded an **interactive weakness code editor preview** illustrating Python loop errors with a custom active insights popover.
- Hero section language badges limited to first 7 languages + "+ MORE" link.
- Pricing buttons redirect to login page if user is not authenticated.

### Created: `frontend/src/pages/Login.jsx`
- Login form with email/password fields and password visibility toggle.
- Google social authentication button.
- Sets `isLoggedIn` state on successful login and redirects to dashboard.

### Created: `frontend/src/pages/Signup.jsx`
- Signup form with name, email, and password fields.
- Google social authentication button.
- Redirects through onboarding flow (onboarding-learning → onboarding-level → dashboard) after signup.

### Created: `frontend/src/pages/Payment.jsx`
- Checkout page with plan summary (Pro/Classroom), card details form, and success state.
- Auth-gated: redirects to login if user is not signed in.

### Created: `frontend/src/pages/Analyze.jsx`
- Constructed the main workspace featuring:
  - Custom monospace text area with active line numbers.
  - Language selection lists and local file upload systems.
  - Toggle switches evaluating explanations as *Beginner* or *Intermediate*.
  - A tabbed reporting pane detailing Errors, Suggestions, Explanations, and Fixed Code.
  - An inline red/green line-by-line **code diff comparison renderer**.
  - Direct connection to port 8000 alongside an **instant local analysis fallback** if the Python server is offline.

### Created: `frontend/src/pages/Learn.jsx`
- Designed the tutoring page incorporating recursion consoles, mastery maps, and quotes.

### Created: `frontend/src/pages/Dashboard.jsx`
- Built an analytics dashboard displaying total counts, filters for languages, and lockable badge matrices.
- Designed a **fully custom, responsive SVG Line Chart** representing error histories, utilizing curved vector paths and gradient fills under the data lines.

### Updated: `frontend/src/App.jsx`
- Added auth route gating: `/analyze`, `/dashboard`, `/learn`, `/payment` are protected behind `isLoggedIn` state.
- Passing `isLoggedIn`, `setIsLoggedIn`, and `currentPlan` to child components.
- Login and Signup pages handled separately (no auth gate).

### Updated: `frontend/src/components/Header.jsx`
- Navigation items include pricing (with scroll-to logic), login/signup when logged out.
- Shows user profile and dashboard link when logged in.
- Fixed Dashboard navbar disappearing bug by removing redundant login redirect.

### Updated: `frontend/src/pages/Analyze.jsx`
- Language selector now imports from `constants/languages.js` for consistent 17-language list.
- `DEFAULT_SNIPPETS` and `DEFAULT_FILENAMES` maps provide language-specific starter code.
- File upload accept attribute generated from `acceptExtensions()`.
- API fetch URL uses `import.meta.env.VITE_API_URL` environment variable.

### Updated: `frontend/src/pages/Dashboard.jsx`
- Language filter dropdown uses centralized `languages.js` constants.
- API fetch URL uses `import.meta.env.VITE_API_URL` environment variable.

### Created: `frontend/.env`
- Contains `VITE_API_URL=http://localhost:8000` for backend API.

### Created: `backend/.env`
- Contains `GEMINI_API_KEY`, `BACKEND_PORT=8000`, `ENVIRONMENT=development`, `FRONTEND_URL=http://localhost:5173`.

---

## 4. Housekeeping & Cleanups
- **[DELETE] `backend/app/router.py`**: Removed redundant FastAPI router file to ensure a perfectly clean, consolidated, single-file server deployment.

---

## 5. Learning Path Intelligence (USP #1 — README)

Updated `README.md` to explain how CodeSage tracks mistakes over time:
- Instead of just flagging one-off errors, CodeSage spots what each student struggles with again and again (like "loop logic" or "variable scoping").
- It builds a personal weakness report: *"You struggle with loop logic and variable scoping. Here are 3 exercises."*
- No other tool tracks a student's growth across sessions like this. It turns CodeSage from a one-shot debugger into a learning companion.

---

## 6. Explain Like I'm a Student (USP #2 — README)

Updated `README.md` to highlight CodeSage's beginner-friendly explanations:
- Most AI tools explain errors in developer jargon. CodeSage explains at the student's own level (Beginner or Intermediate).
- Beginner mode uses everyday analogies, not technical words. For example: *"Your loop never stops because there's no exit condition — think of it like a song on repeat with no stop button."*
- Replit and Copilot don't offer level-aware explanations like this.

---

## 7. Diverse Error Detection Test Suite

### Initial round (30 tests)
Ran 30 comprehensive tests covering all supported languages with three error types (syntax, logical, runtime):

| Language | Tests | What was tested |
|---|---|---|
| Python | 11 | Missing colon on `if`/`for`/`def`, unclosed parens/brackets, `=` vs `==` in conditions, infinite `while True`, division guard, bare `except:`, name typos (Levenshtein), mutable default args, mixed indentation |
| JavaScript | 5 | Missing semicolons on `const`/`let`/`var`/`return`, loose `==` vs `===`, `parseInt` without radix, `var` → `let`/`const` suggestion |
| C | 7 | Missing semicolons on declarations, header typo auto-fix (`stdi.h` → `stdio.h`), `=` in `if` conditions, `void main` → `int main`, `printf(&x)` mismatch, `scanf(no &)` mismatch, missing `#include <stdio.h>` |
| SQL | 3 | `UPDATE`/`DELETE` without `WHERE`, `= NULL` → `IS NULL` |
| HTML | 1 | Missing `<!DOCTYPE html>` |
| CSS | 1 | Unclosed `{` brace |
| Demos | 2 | Exact-match hardcoded demos (calculate_average, loop_price) |

**Result: 30/30 tests passed.**

### Expanded round (52 tests) — added edge cases, negative tests, fix verification
Added coverage for:
- **Python edge cases**: `elif`/`while`/`class`/`try`/`with` missing colons, `=` in `elif`/`while`, name typo with multiple defined vars, division WITH guard (surrounding `if` check now works), builtins not flagged
- **JS edge cases**: valid code silence, multiple `==` per line, `===` not flagged, `parseInt` with radix not flagged, `var` + semicolon combo
- **C/C++ edge cases**: `while` with `=`, unknown headers (>2 Levenshtein distance) show suggestion not error, C++ `iostream` isolated from C mode, multi-`&` removal in one printf, multi-error per line (semicolon + `&`)
- **SQL edge cases**: `UPDATE`/`DELETE` with `WHERE` not flagged, `IS NULL` not flagged
- **HTML/CSS edge cases**: doctype not flagged, closed brace not flagged, proper units not flagged
- **Negative tests**: all 7 languages tested with valid code → zero false positives
- **Explanation verification**: beginner analogies confirmed present for `=`, `printf(&x)`, `void main`
- **Intermediate mode**: all detections work in both beginner and intermediate modes

**Result: 52/52 tests passed.**

---

## 8. Bugs Fixed During Testing

### 8.1 `printf("%d %d", &a, &b)` — second `&` not removed
**File**: `backend/app/analyzer.py` (printf fix section)
**Issue**: Each `&` arg generated a separate `("replace", original_line, new_line)` fix. After the first fix replaced the line, the second fix couldn't find `original_line` anymore — silently did nothing. Only the first `&a` was removed; `&b` stayed.
**Fix**: Accumulate all arg replacements into a single `fixed_after` variable, then create ONE fix per printf/scanf line.

### 8.2 Division guard flagged even when `if count != 0:` guard existed above
**File**: `backend/app/analyzer.py` (division check)
**Issue**: Guard check only looked at the CURRENT line for "if", "!=" keywords. `result = x / count` on its own line didn't contain these words, so it was flagged even though `if count != 0:` guarded it on the previous line.
**Fix**: Scan up to 3 lines above the division for `if <var>` or `<var> !=` patterns before flagging.

### 8.3 `=` vs `==` in conditions produced duplicate errors
**File**: `backend/app/analyzer.py` (Python + C `=` checks)
**Issue**: Both `ast.parse` (Python's built-in parser) AND the heuristic regex caught `x=5` in an `if`. Two `AssignmentInCondition` errors on the same line.
**Fix**: Added dedup check before appending — only fire if no existing `AssignmentInCondition` on that line.

### 8.4 Missing CSS unit regex didn't match numbers before `}`
**File**: `backend/app/analyzer.py` (CSS section)
**Issue**: Regex `:\s*\d+\s*$` required the number to be at end of line. `font-size: 16 }` (with trailing `}`) didn't match.
**Fix**: Updated to `:\s*\d+\s*[;}\s]*$` to allow `;` / `}` after the number.

---

## 9. `=` vs `==` Detection — Inline Conditions

### Problem
The original C `=` check only looked at lines STARTING with `if`/`while`/`switch`. Code like `int x; if(x=5){}` (multiple statements on one line) was missed.

### Fix (`backend/app/analyzer.py:610-628`)
Changed from `re.match(ctrl_keywords, stripped)` (line must start with `if`) to `re.search(r'\b(if|while|switch)\s*\(', stripped)` (keyword can appear anywhere in line). Extracts text inside the parentheses and checks for `=` inside them only.

Same change applied to the Python `=` check (`analyzer.py:408-417`) — switched from `re.match(r'^\s*(if|elif|while)\b', stripped)` to `re.search(r'\b(if|elif|while)\b', stripped)` so inline `elif` on the same line as preceding code is caught.

---

## 10. Frontend Cleanup

### Removed `import React` from Header.jsx
React 17+ JSX transform doesn't require `import React` at the top of component files. ESLint flagged it as unused. Removed to pass lint check. Build verified clean with `npx vite build`.

---

## 11. Missing `#` on Preprocessor Directives — Plain Text Bug

### Problem
Lines like `include <stdio.h>` (without `#`) were silently ignored. The `#include` regex required `#` at the start, so these lines matched nothing and the analyzer reported "no critical issues found." Same for `define`, `ifdef`, `ifndef`, `endif`, `pragma`, `undef`, `error`, `warning` without `#`.

### Fix (`backend/app/analyzer.py`)
Added three new detection passes after the `#include` loop:

1. **`include <header>` / `include "header"` without `#`** — regex `include\s+[<"](.+?)[>"]`. Flags as `SyntaxError` with message explaining preprocessor directives need `#`. Auto-fix: prepends `#` to the line. Also sets `has_stdio = True` if the header is `stdio.h` or `cstdio`, preventing duplicate `#include <stdio.h>` insertion from the `printf`/`scanf` check.

2. **`include header` (no angle brackets, no `#`)** — regex `include\s+(\S+)`. Flags as `SyntaxError` with message about missing both `#` and `<>`. Auto-fix: rewrites to `#include <header>`.

3. **Other preprocessor directives without `#`** — checks for `define`, `ifdef`, `ifndef`, `endif`, `pragma`, `undef`, `error`, `warning`, `line` at line start (without `#`). Each triggers a `SyntaxError` with `preprocessor directive` explanation. Auto-fix: prepends `#`.

### Explanation added (`_get_error_explanation`)
- `"preprocessor directive"` in message → explains `#include`/`#define` are special instructions for before compilation, needs `#` to work
- `"include"` + `"angle"` in message → explains `#include <filename.h>` is the correct form, missing `#` and `<>` makes the compiler confused

### Tests
- `include <stdio.h>` without `#` → error detected, `#` prepended, no duplicate `#include` insertion
- `include stdio.h` (no `<>`, no `#`) → error detected, rewritten to `#include <stdio.h>`
- `define MAX 100` without `#` → error detected, `#` prepended
- `ifdef`/`endif` without `#` → both detected
- Proper `#include <stdio.h>` → zero false positives (no regression)
- All 30 existing regression tests pass
