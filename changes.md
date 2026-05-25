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
  - JavaScript / TypeScript syntax omissions (e.g. missing semicolons in variable definitions).
  - Infinite Loops (`while True` or `while(true)` blocks devoid of break keywords).
- Built detailed, explainable response blocks tailored to mock code structures.

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

### Created: `frontend/src/pages/Home.jsx`
- Built the Landing page incorporating the hero block, how-it-works grids, and standard pricing blocks.
- Embedded an **interactive weakness code editor preview** illustrating Python loop errors with a custom active insights popover.

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

### Replaced: `frontend/src/App.jsx` & `frontend/src/App.css`
- Wired the primary page navigation engine, shared sample code states, header/footer shells, and dynamic grid layouts.

---

## 4. Housekeeping & Cleanups
- **[DELETE] `backend/app/router.py`**: Removed redundant FastAPI router file to ensure a perfectly clean, consolidated, single-file server deployment.
