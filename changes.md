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
