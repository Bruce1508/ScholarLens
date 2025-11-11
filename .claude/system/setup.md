# system/setup.md

## 1. Purpose of This File

This document describes the **architecture**, **environment**, and **repository layout** of the project so that:

- Human developers understand the structure quickly.
- Claude Code has enough context to:
  - Locate relevant files.
  - Propose correct changes.
  - Respect existing patterns and boundaries.

Claude Code should treat this file as **read-only reference**, not something to modify unless explicitly instructed.

---

## 2. Project Overview

**Project Name:** Adaptive Scholarship Matching + AI Drafting  
**Goal:**  
Build a system that:

1. Analyzes scholarship descriptions to infer their underlying **values and personality**.  
2. Learns patterns from **winner essays** (clustering/style archetypes).  
3. Generates **scholarship-specific application drafts** for a given student profile.  
4. Provides **explainable output**:
   - Paragraph-level tagging (which value each paragraph targets).
   - Visual heatmap and radar charts of alignment.  
5. Compares **generic vs adaptive** drafts to demonstrate improvement.

---

## 3. Tech Stack

### Backend

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Responsibilities:**
  - Expose REST API endpoints (`/api/v1/...`).
  - Call Anthropic/Claude APIs using defined prompts.
  - Run clustering logic over winner essays.
  - Compute alignment scores and derived metrics.

### Frontend

- **Language:** TypeScript
- **Framework:** React (SPA or Next.js-style structure)
- **State:** Zustand for global state management
- **Responsibilities:**
  - Collect scholarship description or select existing.
  - Collect student profile data.
  - Call backend endpoints to:
    - Analyze scholarship persona.
    - Generate tailored essay.
    - Run mirror test and comparative evaluation.
  - Render:
    - Essay with paragraph-level highlights.
    - Alignment radar chart.
    - Explanations per paragraph.

### Data / Storage

- **Database:** PostgreSQL 14+ for persistent entities:
  - Scholarships, personas (optional, depending on final design).
  - Cached analysis results.
- **Flat Files:** JSON and text under `/data`:
  - Source descriptions.
  - Winner essays.
  - Clustering metadata.

### Claude / LLM

- **Provider:** Anthropic Claude (via API)  
- **Usage:**
  - Persona extraction (Scholarship Personality Genome).
  - Essay generation + tagging.
  - Cluster labeling.
  - Mirror test + evaluation.

---

## 4. Repository Layout (High-Level)

Expected structure (may be refined; Claude Code should respect this intent):

```text
/
├── backend/
│   ├── api/
│   │   ├── routes/         # FastAPI route definitions
│   │   ├── controllers/    # Business logic: persona, generator, mirror test
│   │   └── services/       # Claude/LLM, clustering, scoring helpers
│   ├── db/
│   │   ├── migrations/     # SQL migration scripts
│   │   └── models/         # ORM or plain SQL helpers
│   └── core/               # Config, dependency injection, startup
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components (Heatmap, RadarChart, Forms)
│   │   ├── hooks/          # Custom hooks
│   │   ├── stores/         # Zustand stores
│   │   ├── utils/          # General-purpose helpers
│   │   ├── constants/      # Trait names, colors, etc.
│   │   └── pages/ or app/  # Entry points (depending on CRA vs Next)
│   └── public/             # Static assets
│
├── data/
│   ├── scholarships.json   # Collected scholarship descriptions
│   ├── winner_essays/      # Corpus of past winning essays (raw text/JSON)
│   └── clusters.json       # Derived cluster metadata (ids, labels, centroids)
│
├── .claude/
│   ├── CLAUDE.md           # Global project configuration (root file)
│   ├── system/
│   │   ├── setup.md        # This file
│   │   ├── coding_rules.md # Style, lint, naming conventions
│   │   └── task_guide.md   # How tasks map to prompts
│   ├── prompts/
│   │   ├── persona_builder.md
│   │   ├── essay_generator.md
│   │   ├── mirror_test.md
│   │   ├── cluster_labeler.md
│   │   └── evaluation_agent.md
│   └── utils/
│       ├── schema_examples.md
│       └── testcases.md
│
├── package.json
├── tsconfig.json
├── pyproject.toml / requirements.txt
└── README.md
```

Claude Code should use this tree to locate relevant files when planning or editing.

---

## 5. Logical Architecture & Data Flow

High-level request flow (for core use case "generate tailored essay with explainability"):

### Frontend
- User selects/inputs a scholarship description.
- User fills in a student profile (GPA, activities, projects, goals).

### Backend – Analysis
- Frontend sends description to `/api/v1/persona/analyze`.
- Backend calls Claude using `persona_builder.md` → returns:
  - `persona_name`
  - `tone`
  - `weights` (Academics, Leadership, Community, Innovation, etc.)
  - `rationale`
- Backend may persist persona (optional) or return directly.

### Backend – Essay Generation
- Frontend sends persona + student profile to `/api/v1/essay/generate`.
- Backend calls Claude with `essay_generator.md` → returns:
  - Array of paragraphs, each with:
    - paragraph text
    - focus tag
    - reason
    - alignment_score (or raw features)
- Backend post-processes scores, computes aggregated alignment metrics.

### Frontend – Visualization
- Render essay paragraphs with highlight by focus.
- Render radar chart comparing:
  - Scholarship persona weights.
  - Effective emphasis found in essay.

### Mirroring and Evaluation (Optional)
- Existing essay → `/api/v1/essay/mirror-test` (Claude uses `mirror_test.md`).
- Comparative evaluation generic vs adaptive → `evaluation_agent.md`.

### Winner Clustering (Supporting Analysis)
Winner clustering is a supporting analysis that runs offline or as a separate step:
- Embedding + clustering code in backend services.
- Claude's `cluster_labeler.md` used to label each cluster (archetype description).
- Persona extraction may reference these archetypes, but critical path does not require real-time clustering.

---

## 6. Environment & Dependencies

### Node / Frontend
- **Node.js:** v18.x
- **Package manager:** npm (use `npm ci` for installs)
- **Core libs** (indicative, not exhaustive):
  - React
  - Zustand
  - React Testing Library
  - Charting library (e.g., Recharts / Chart.js)
  - TypeScript

### Python / Backend
- **Python:** 3.11+
- FastAPI
- Uvicorn / Gunicorn for serving
- HTTP client for Claude API (e.g., httpx)
- **Optional:**
  - SentenceTransformers / similar for embeddings
  - Scikit-learn (for clustering)
  - SQLAlchemy or similar ORM (if not raw SQL)

### Database
- **PostgreSQL** 14+
- Docker compose may be used for local dev (if defined; Claude should respect existing config).

### LLM / Claude
- Environment variable: `CLAUDE_API_KEY`
- All LLM calls must follow the schemas in `.claude/utils/schema_examples.md`.
- Claude Code must not alter API keys or secrets.

---

## 7. Instructions for Claude Code

### When operating in this repository, Claude Code should:

#### Read before editing
- Use `CLAUDE.md` (root) as the main project guide.
- Use `system/setup.md` (this file) to understand architecture.
- Use `system/coding_rules.md` for naming, lint, and style.
- Use `system/task_guide.md` to understand prompt/task mapping.

#### Respect structure
- Place new backend API endpoints under `backend/api/routes/`.
- Place business logic under `backend/api/controllers/` or `backend/api/services/`.
- Place new React components under `frontend/src/components/` with tests in corresponding `__tests__/` directory.
- Do not create new top-level directories without strong reason.

#### Preserve JSON schemas
- For personas, essays, and evaluations, use the schemas defined in `.claude/utils/schema_examples.md`.
- Do not change JSON shapes without explicit instruction and accompanying migration in code.

#### Prefer incremental changes
- Modify existing files where logical, instead of duplicating functionality.
- When refactoring, keep behavior stable and ensure tests (where they exist) remain valid.

#### Keep tasks scoped
- If a requested change spans backend and frontend:
  - Update backend endpoints first (controllers/services).
  - Then adjust frontend calls and UI.
- For LLM behavior changes:
  - Prefer editing prompt files under `.claude/prompts/`.
  - Avoid mixing prompt logic into application code.

#### Generate testable changes
- For new modules/functions, also generate tests following the testing rules defined elsewhere (`coding_rules.md`).
- Keep tests close to the code they validate.

---

## 8. Non-Goals / Out-of-Scope for Claude

Claude Code should generally avoid:
- Redesigning core architecture (e.g., changing FastAPI to another framework) unless explicitly requested.
- Introducing new external services or paid dependencies without clear reason.
- Modifying `.env` files or secret management.
- Large, multi-file refactors that are not tightly connected to the requested change.

---

## 9. Summary for Planning

- **Backend** → FastAPI, persona + essay APIs, clustering, scoring.
- **Frontend** → React + Zustand, displays essay + heatmap + radar charts.
- **Data** → Scholarships + winner essays + cluster metadata.
- **Claude** → Structured prompts in `.claude/prompts/`, orchestrated via logic described in `task_guide.md`.

Claude Code should use this file as the primary mental model of the project when planning and executing code modifications.
