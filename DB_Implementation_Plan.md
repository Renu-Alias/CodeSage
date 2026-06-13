# CodeSage — Supabase Database Implementation Plan

This document outlines how to enable persistent database storage for the entire CodeSage project using Supabase. It is tailored to the current stack: React + Vite frontend, Python stdlib API backend, in-memory `SUBMISSION_HISTORY`, and mock client-side auth.

---

## Best Database Choice: PostgreSQL (SQL)

Supabase is built on **PostgreSQL**. You do not pick MongoDB, MySQL, etc. — Postgres is included and is the right fit for CodeSage.

### Why SQL / Postgres Fits This Project

| Need | Why Postgres Works |
|------|-------------------|
| Users, submissions, classrooms, subscriptions | Clear relationships (`user → submissions → analysis`) |
| Dashboard metrics, weakness reports, streaks | Aggregations (`COUNT`, `GROUP BY`, time-series) are natural in SQL |
| Per-user data isolation | Row Level Security (RLS) ties rows to `auth.users` |
| Roadmap (v2 badges, v3 classrooms) | Relational model scales without reshaping the schema |

### What “Database Language” Means in Practice

1. **Schema & migrations → SQL**  
   Define tables, indexes, RLS policies, and triggers in `.sql` files via the [Supabase CLI](https://supabase.com/docs/guides/cli).

2. **App access layer → JavaScript + Python**  
   - **Frontend:** `@supabase/supabase-js` for auth, session, and some reads/writes  
   - **Backend:** `supabase` (Python) or `psycopg2` / SQLAlchemy for server-side writes after Gemini analysis  

You write **SQL for structure** and use **SDKs for runtime queries** — not a separate “database language” choice.

---

## Recommended Architecture for CodeSage

```mermaid
flowchart LR
    subgraph frontend [React Frontend]
        Auth[Supabase Auth]
        UI[Pages: Dashboard, Analyze, etc.]
    end

    subgraph supabase [Supabase]
        PG[(PostgreSQL)]
        RLS[Row Level Security]
    end

    subgraph backend [Python API]
        Analyze["/api/analyze + Gemini"]
    end

    UI --> Auth
    Auth --> PG
    UI -->|"JWT + code"| Analyze
    Analyze -->|"save submission + analysis"| PG
    UI -->|"reads with RLS"| PG
```

### Suggested Split

- **Supabase Auth** on the frontend (replaces `isLoggedIn` in `App.jsx`)
- **Python backend** keeps Gemini analysis; after analysis, it persists to Postgres using the user’s JWT or a service role
- **Frontend** reads dashboard/history directly from Supabase (with RLS), or via your Python API if you prefer a single API surface

---

## Step-by-Step: Enable Database for the Whole Project

### Phase 1 — Supabase Project & Schema

1. **Create a Supabase project** at [supabase.com](https://supabase.com).
2. **Install Supabase CLI** and link the project:
   ```bash
   npm install -g supabase
   supabase login
   supabase init
   supabase link --project-ref <your-project-ref>
   ```
3. **Design core tables** (SQL migrations in `supabase/migrations/`):

   | Table | Purpose |
   |-------|---------|
   | `profiles` | Extends `auth.users` (display name, plan, settings) |
   | `submissions` | Replaces `SUBMISSION_HISTORY` in `main.py` |
   | `analyses` | Full Gemini/local analysis JSON per submission |
   | `weakness_topics` | Aggregated mistake categories (v2) |
   | `badges` / `user_badges` | Gamification (v2) |
   | `classrooms` / `classroom_members` | Teacher/student (v3) |
   | `subscriptions` | Plan tier, limits (Free/Pro/Classroom) |

4. **Enable RLS on every user-owned table** and add policies like:
   - Users can only `SELECT`/`INSERT` their own `submissions`
   - Teachers can `SELECT` submissions for students in their classroom

5. **Run migrations:**
   ```bash
   supabase db push
   ```

### Phase 2 — Auth (Required, Not Optional)

The project roadmap already lists: *“User auth via Supabase”*.

1. Enable **Email** (and optionally **Google OAuth**) in Supabase Dashboard → Authentication.
2. Install frontend client:
   ```bash
   cd frontend && npm install @supabase/supabase-js
   ```
3. Add env vars:
   ```env
   # frontend/.env
   VITE_SUPABASE_URL=https://xxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJ...

   # backend/.env
   SUPABASE_URL=https://xxxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJ...   # server only, never in frontend
   ```
4. Replace mock login in `Login.jsx` / `SignUp.jsx` with `supabase.auth.signInWithPassword()` / `signUp()`.
5. Gate protected routes in `App.jsx` on `supabase.auth.getSession()` instead of `isLoggedIn`.

### Phase 3 — Wire Persistence

1. **Replace in-memory storage** in `backend/app/main.py`:
   - On `POST /api/analyze`: verify `Authorization: Bearer <jwt>`, run analysis, `INSERT` into `submissions` + `analyses`.
   - On `GET /api/dashboard`: query by `user_id` instead of global `SUBMISSION_HISTORY`.
2. **Scope all data by `user_id`** — today submissions are global and shared across everyone.
3. **Update `Dashboard.jsx` and `Analyze.jsx`** to send the Supabase session token to the Python API.
4. **Move classroom state** from React-only (`Classroom.jsx`) into `classrooms` tables when you reach v3.

### Phase 4 — Production Hardening

1. Tighten CORS in `main.py` from `*` to `FRONTEND_URL`.
2. Add indexes on `submissions(user_id, created_at)`.
3. Use **Supabase local dev** (`supabase start`) for offline work.
4. Store secrets only in `.env` (already gitignored).

---

## Which Other Supabase Services Do You Need?

| Service | Need It? | Why for CodeSage |
|---------|----------|------------------|
| **Database (Postgres)** | **Yes — core** | All persistent data |
| **Auth** | **Yes — core** | Real users; RLS depends on `auth.uid()` |
| **Row Level Security** | **Yes — core** | Multi-tenant safety (students only see their data) |
| **Storage** | Optional later | If you add file uploads instead of paste-only code |
| **Edge Functions** | Optional | Could proxy Gemini, but you already have a Python backend |
| **Realtime** | Optional (v3) | Live classroom dashboards |
| **Vector / pgvector** | Optional (future) | Semantic search over past submissions |
| **Supabase Studio** | Included | SQL editor, table browser, auth users |

### Not from Supabase

- **Payments** — `Payment.jsx` is simulated today. Use **Stripe** (or similar); store subscription status in Postgres.
- **Gemini** — stays in your Python backend with `GEMINI_API_KEY`.

---

## Minimal Schema Example (Starting Point)

```sql
-- profiles (1:1 with auth.users)
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  plan text default 'free' check (plan in ('free', 'pro', 'classroom')),
  created_at timestamptz default now()
);

-- submissions (replaces SUBMISSION_HISTORY)
create table public.submissions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  filename text not null,
  language text not null,
  code text not null,
  errors_count int default 0,
  suggestions_count int default 0,
  created_at timestamptz default now()
);

alter table public.submissions enable row level security;

create policy "Users read own submissions"
  on public.submissions for select
  using (auth.uid() = user_id);

create policy "Users insert own submissions"
  on public.submissions for insert
  with check (auth.uid() = user_id);
```

---

## Practical Recommendation

**Start with three Supabase products only:** Postgres + Auth + RLS.

That covers MVP persistence (upload history, per-user dashboard) and matches the project roadmap. Add Storage, Realtime, or Edge Functions when a concrete feature needs them — not upfront.

### Order of Work

1. Supabase project + SQL schema  
2. Auth on the frontend  
3. Persist submissions from `/api/analyze`  
4. Dashboard reads from the database  
5. Subscriptions (Stripe + `profiles.plan`)  
6. Classrooms (v3)

---

## Current State (Baseline)

Before implementation, the project has:

- **No database, ORM, or migrations** — all persistence is in-memory or mocked
- **`SUBMISSION_HISTORY`** in `backend/app/main.py` — global, not user-scoped
- **Mock auth** — `isLoggedIn` boolean in `frontend/src/App.jsx`; no API or credential checks
- **Supabase** — mentioned only on the roadmap in `README.md`; no code or schema in the repo

---

*CodeSage — Debug smarter. Learn faster. Code better.*
