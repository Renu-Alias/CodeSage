# Changelog

## 2026-06-10 — Classroom Feature & UI Cleanup

### Added
- **Classroom page** (`src/pages/Classroom.jsx`): Full classroom management page with:
  - Create Classroom form (enter name, get 6-character alphanumeric code)
  - Join Classroom form (enter code to join existing class)
  - Persistent classroom cards grid showing all created/joined classrooms
  - Classroom detail view with skeleton loading animation (1.2s simulated delay)
  - Detail view shows three sections: Recent Actions, Tasks Assigned, Upcoming Dues
  - Empty state when no classrooms exist
- **Classroom CSS** (`src/App.css`): Full styling for cards grid, detail panels, action/task/due lists, skeleton shimmer animation, and responsive layout
- **Classroom route** (`src/App.jsx`): Added `'classroom'` to route switch and protected routes list
- **CHANGES.md**: This file

### Changed
- **Header nav** (`src/components/Header.jsx`): "Pricing" nav item replaced with "Classroom" — navigates directly to the Classroom page instead of scrolling to a pricing section
- **Classroom page flow**: Create/Join modals are now inline forms (toggled by buttons) rather than separate success screens — classrooms always visible as cards below the action bar

### Removed
- **Pricing section** from Home page (`src/pages/Home.jsx`): Removed the entire Free/Pro/Classroom pricing tier section (was 85 lines)
- **`selectedPlan` prop**: Removed from `Home.jsx` and `App.jsx` since it was only used by the pricing section
- **Classroom plan** from Payment page (`src/pages/Payment.jsx`): Removed from `PLANS` object — classroom is now a free feature, not a paid tier
- **"Free plan" badge** from Header (`src/components/Header.jsx`): Removed the `<span className="free-plan-badge">Free plan</span>` element from the logged-in header
- **"Get started for free" CTA** from Learn page (`src/pages/Learn.jsx`): Removed the entire CTA banner section at the bottom of the page
- **Obsolete classroom CSS**: Removed old `.classroom-grid`, `.classroom-option*`, `.classroom-success-card`, `.classroom-code-display`, `.classroom-code-text`, `.classroom-code-hint`, `.classroom-success-actions`, `.classroom-list*` styles — replaced with card grid and detail view CSS

### Notes
- Classroom data is currently in-memory only (not persisted to backend) — refreshing the page loses classrooms
- Detail view data is mock/simulated with a 1.2s loading delay to demonstrate skeleton animation
- The Create/Join forms are toggled by buttons in the action bar and collapse when the other button is clicked or when a classroom is created/joined
