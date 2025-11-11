# CLAUDE.md  
**Project:** Adaptive Scholarship Matching + AI Drafting  
**Purpose:** Central configuration for Claude Code — defines architecture, conventions, commands, and LLM workflow.  

---

## 🧰 1. Bash Commands
- `npm run dev` — Start development server (FastAPI backend + React frontend)  
- `npm run build` — Build project for production (frontend + backend)  
- `npm run start` — Run production build  
- `npm run lint` — Lint and format all code  
- `npm run lint:fix` — Auto-fix lint issues  
- `npm run typecheck` — Run TypeScript type checking  
- `npm run test` — Run all Jest test suites  
- `npm run test:single [path]` — Run a specific test file  
- `npm run analyze` — Analyze frontend bundle size  
- `npm run seed` — Seed local database with sample data  

---

## 💻 2. Code Style & Conventions
- Use **ES Modules** (`import/export`) — not CommonJS (`require`)  
- All new files must use **TypeScript** (`.ts`, `.tsx`)  
- Prefer **async/await** over raw Promises  
- Always wrap async operations in `try/catch` blocks  
- Destructure imports when possible:  

```ts
import { analyzeScholarship, generateEssay } from '@/api/controllers';
```

- Add JSDoc comments for public functions and complex logic
- Each function performs one responsibility
- Avoid procedural nesting — use helper functions

---

## 🏗️ 3. Architecture & Key Files

### Frontend (/frontend)
- `/src/components` — React UI components (Heatmap, EssayView)
- `/src/hooks` — Custom reusable hooks
- `/src/stores` — Zustand stores for global state
- `/src/utils` — Utility functions (alignment, color mapping)
- `/src/constants` — Shared constants (traits, colors, weights)

### Backend (/backend)
- `/api/routes` — FastAPI route definitions
- `/api/controllers` — Business logic (persona builder, generator)
- `/api/middleware` — Logging, error handling
- `/api/services` — Claude API integration and clustering logic

### Data (/data)
- `scholarships.json` — Scholarship descriptions
- `/winner_essays/` — Corpus of winner essays
- `clusters.json` — Winner essay cluster metadata

### Claude Prompts (/.claude/prompts)
- `persona_builder.md` — Extracts scholarship personality genome
- `essay_generator.md` — Generates essay + tagging JSON
- `mirror_test.md` — Analyzes user essays against persona
- `cluster_labeler.md` — Describes cluster archetypes
- `evaluation_agent.md` — Compares adaptive vs generic outputs

---

## 🧠 4. State Management (Zustand)
- Each store handles a single domain (`useEssayStore`, `useScholarshipStore`)
- Use Immer middleware for nested updates
- Keep selectors minimal and memoized
- Always clear stores on logout or session reset

---

## 🎨 5. Frontend (React)
- Every component requires a test in `__tests__/`
- Props must be strongly typed with TypeScript interfaces
- Use custom hooks for stateful logic
- Avoid prop drilling (prefer store or context)
- Max file length = 300 lines
- Large components → split into smaller files
- Use `React.memo()` for expensive re-renders
- Use React Testing Library for UI tests

---

## 🧪 6. Testing Requirements
- All new logic must include tests
- Test folder mirrors component structure
- ≥ 80% coverage for backend & critical paths

**Frameworks:**
- Jest → Unit & integration tests
- React Testing Library → Frontend
- Use single test runs during iteration (`npm run test:single`)
- Full suite before merge

---

## 🌿 7. Git Workflow

### Branch naming convention:
- `feature/<short-name>` (e.g. `feature/persona-engine`)
- `bugfix/<short-name>`
- `docs/<short-name>`

### Commit message format:
- `feat(persona): add scholarship genome parser`
- `fix(heatmap): resolve color mismatch`

### Workflow:
- Rebase before pushing (`git pull --rebase`)
- No merge commits to main
- Use PR review → squash merge after approval

---

## 🧩 8. Database & Migrations
- **Database:** PostgreSQL 14+
- Run all migrations before dev startup
- **Naming:** `001_create_personas_table.sql`
- Include rollback scripts for every migration
- Document schema changes in CLAUDE.md → Changelog section
- Test with `npm run seed` after migration

---

## ⚙️ 9. Environment Setup

### Requirements
- **Node.js:** v18.x (`nvm use 18`)
- **Python:** 3.11+
- **PostgreSQL:** 14+

### Setup Steps
1. Install dependencies:
   ```bash
   npm ci
   ```

2. Copy environment file:
   ```bash
   cp .env.example .env.local
   ```

3. Required variables:
   ```
   DATABASE_URL=postgresql://...
   CLAUDE_API_KEY=...
   FRONTEND_URL=http://localhost:5173
   ```

4. Start development:
   ```bash
   npm run dev
   ```

---

## 🌐 10. API Endpoints Pattern

### RESTful routes
- Pattern: `/api/v1/resource`

### HTTP Methods
- `GET` → Retrieve
- `POST` → Create
- `PUT` → Update
- `DELETE` → Remove

### JSON response format
```json
{
  "success": true,
  "data": {},
  "error": null
}
```

### Common status codes
- `200` → OK
- `400` → Bad Request
- `401` → Unauthorized
- `500` → Server Error

**Important:** Validate all inputs on backend — never trust frontend data

---

## ⚡ 11. Performance & Optimization
- Code-split React components (lazy loading)
- Memoize heavy computations with `useMemo` / `useCallback`
- Optimize assets & use lazy loading
- Gzip/Brotli compression in production
- Log API latency via FastAPI middleware
- Use selectors to prevent unnecessary re-renders

---

## ✅ 12. Pre-Commit Checklist
- `npm run typecheck` — No TS errors
- `npm run lint:fix` — No lint issues
- All tests passed
- CLAUDE.md updated if new patterns added
- Commit message follows convention
- PR created and linked

---

## ⚠️ 13. Common Gotchas
- **Zustand state leak** → Reset on logout
- **Async race conditions** → Use `AbortController`
- **Image imports** → Static imports only
- **Circular dependencies** → Check before commit
- **Stale closures** → Track hook dependencies carefully

---

## 🔍 14. Code Review Checklist
- Code style compliance
- TypeScript types verified
- All errors handled
- Tests cover new logic
- No redundant complexity
- Docs/comments updated
- No performance regressions

---

## 🤖 15. Claude Code Integration

### Prompt Chain Execution Order:
1. `cluster_labeler.md` — Build cluster archetypes from winner essays
2. `persona_builder.md` — Extract persona weights & tone from scholarship
3. `essay_generator.md` — Generate tailored essay + paragraph tags
4. `evaluation_agent.md` — Compare adaptive vs generic draft
5. `mirror_test.md` (Optional) — Analyze existing user essay

### Rules:
- Each sub-prompt must output strict JSON only
- All prompt schemas defined in `.claude/utils/schema_examples.md`
- When adding new tasks → update mapping here

---

## 🗂️ 16. Folder Tree Overview

```text
/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── services/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── stores/
│   │   └── utils/
├── data/
│   ├── scholarships.json
│   ├── winner_essays/
│   └── clusters.json
└── .claude/
    ├── CLAUDE.md
    ├── prompts/
    ├── system/
    └── utils/
```

---
