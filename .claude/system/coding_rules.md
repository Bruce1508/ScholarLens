# system/coding_rules.md

## 1. Purpose of This File
This document defines all **coding conventions**, **linting standards**, **naming schemes**, and **file structure rules** for the project.  
Claude Code must strictly follow these conventions when writing, modifying, or refactoring code.  
The objective is to keep the codebase consistent, maintainable, and easy to navigate across backend, frontend, and Claude prompt layers.

---

## 2. Language & Framework Standards

### Backend (Python)
- **Language:** Python 3.11+  
- **Framework:** FastAPI  
- **Formatter:** `black` (line length = 88)  
- **Linter:** `flake8`, `isort`  
- **Typing:** full type annotations required for public functions  
- **Docstrings:** use Google-style docstrings for all functions  

```python
def generate_persona(description: str) -> dict:
    """
    Analyze scholarship description and return personality weights.

    Args:
        description (str): Scholarship description text.

    Returns:
        dict: JSON-compatible object with weights and persona_name.
    """
```

- **Async I/O:** always prefer `async def` for I/O operations.
- **Error Handling:** wrap external calls (LLM, DB, HTTP) with try/except; log meaningful context.

### Frontend (TypeScript / React)
- **Language:** TypeScript (.ts, .tsx)
- **Formatter:** prettier + ESLint (Airbnb or Next.js base config)
- **Naming Convention:** PascalCase for components, camelCase for variables, CONSTANT_CASE for constants.

**React Hooks:**
- All custom hooks start with `use` (e.g., `useEssayStore`, `usePersonaAnalysis`).
- Avoid side effects inside render paths.

**Imports:**
```ts
import { EssayHeatmap, RadarChart } from '@/components';
```
- No relative paths that traverse more than two levels (`../../` discouraged).

- **Type Annotations:** all props, hooks, and functions must specify interfaces or types.
- **Comments:** use `//` for inline, `/** ... */` for function documentation.
- **Asynchronous Logic:** use async/await; never chain `.then()` unnecessarily.

---

## 3. Naming Rules

### General Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `alignmentScore`, `personaWeights` |
| Functions | camelCase | `fetchScholarships`, `generateEssay` |
| Classes | PascalCase | `EssayController`, `HeatmapRenderer` |
| Components | PascalCase | `EssayCard`, `PersonaView` |
| Files (React) | PascalCase.tsx | `EssayHeatmap.tsx` |
| Files (utils/hooks) | camelCase.ts | `calculateAlignment.ts`, `useEssayStore.ts` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TRAITS`, `API_BASE_URL` |
| Enums | PascalCase + singular | `FocusType.Leadership` |

### Folder & File Placement
- **React Components:** `/frontend/src/components/`
- **Custom Hooks:** `/frontend/src/hooks/`
- **Zustand Stores:** `/frontend/src/stores/`
- **Utilities & Constants:** `/frontend/src/utils/`, `/frontend/src/constants/`
- **API Controllers:** `/backend/api/controllers/`
- **Claude Prompts:** `/.claude/prompts/` (one prompt per agent)

---

## 4. File Header & Documentation Rules
Each non-trivial source file must start with a brief docstring or header comment explaining its purpose.

**Example (backend):**
```python
"""
controllers/persona_controller.py
Handles scholarship persona extraction using the Claude API.
"""
```

**Example (frontend):**
```ts
/**
 * EssayHeatmap.tsx
 * Displays generated essay paragraphs with color-coded highlights
 * based on persona focus and alignment score.
 */
```

---

## 5. Function Design Rules
- Each function should perform a single logical operation.
- Maximum function length: ~40 lines (prefer smaller, modular helpers).
- Avoid deeply nested if/else — prefer early returns.
- Always type input parameters and return values.

For asynchronous backend functions:
```python
async def fetch_persona(scholarship_id: str) -> Persona:
    try:
        response = await client.get(...)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch persona: {e}")
        raise HTTPException(status_code=500, detail="Persona fetch failed.")
```

- Avoid hard-coded strings → move to constants file.
- Prefer pure functions where side effects aren't required.

---

## 6. Testing Standards

### Frontend
- Use React Testing Library for rendering components.
- Each component → one test file under `__tests__/`.
- Minimal snapshot + functional behavior test.
- Avoid testing implementation details; focus on visible behavior.

### Backend
- Use pytest for unit/integration tests.
- Tests under `backend/tests/` mirror controller structure.
- Mock Claude API responses in tests (no live API calls).
- Each new API endpoint → at least one happy-path + one failure test.

### Coverage
- Aim for ≥80% coverage in business logic and key components.
- Run `npm run test:single` for specific modules while developing.
- Full `npm run test` before committing or PR submission.

---

## 7. Logging, Errors, and Exceptions

### Backend
- Logs must include: timestamp, module, severity, and short message.
- Use Python logging library (no print statements).

### Frontend
- Errors should:
  - Be caught in a boundary (ErrorBoundary component).
  - Log via a central logger (`utils/logger.ts`).
  - No silent failures — always handle rejections.

**Error example (frontend):**
```ts
try {
  const response = await generateEssay(profile);
  setEssay(response.data);
} catch (error) {
  console.error("Essay generation failed:", error);
  showToast("Essay generation failed");
}
```

---

## 8. Lint & Format Rules

### ESLint / Prettier
- Enforce semicolons, single quotes, 2-space indent.
- Max line length: 100.
- No unused imports or variables.
- `no-console` in production code (allowed in development).
- Sort imports automatically via ESLint rule.

### Black / Flake8 (Python)
- Line length: 88.
- Import sorting via `isort`.
- No wildcard imports (`from module import *` forbidden).
- Docstring required for all public functions.

---

## 9. Commit & Pull Request Rules

### Commit Messages
Follow the conventional commits standard:
- `<type>(scope): short description`
- Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `style`

**Examples:**
- `feat(persona): implement adaptive weighting algorithm`
- `fix(essay): prevent null alignment scores in response`

### Pull Requests
Each PR must include:
- Description of changes.
- Screenshots (if UI change).
- Checklist:
  - Tests added or updated.
  - No lint/type errors.
  - Follows file structure and naming conventions.

---

## 10. Claude Code-Specific Instructions
Claude Code must:
- Use these naming and linting rules when auto-generating code.
- Always infer which layer to modify:
  - If prompt-related → edit `.claude/prompts/`
  - If logic-related → edit backend controllers or services.
  - If UI-related → edit React components or hooks.
- Always maintain correct import paths and consistent naming.
- Never output code violating Prettier or Black style rules.
- Use examples from this file to infer proper formatting.

---

## 11. Code Review Criteria (Human + Claude)
During PR review or Claude Code validation, ensure:
- Code adheres to conventions here.
- Naming reflects intent clearly.
- Function and file length remain within limits.
- Logging and error handling follow guidelines.
- All new logic includes test coverage.
- Comments are meaningful and up-to-date.
- No unused or dead code.
- No circular imports or redundant files.

---

## 12. Quick Reference Table

| Category | Tool / Convention | Key Command |
|----------|-------------------|-------------|
| Formatter | Prettier / Black | `npm run lint:fix` / `black .` |
| Type Checking | TypeScript / mypy | `npm run typecheck` |
| Linter | ESLint / flake8 | `npm run lint` / `flake8` |
| Tests | Jest / pytest | `npm run test` |
| Naming | camelCase / PascalCase | Consistent across layers |
| Commits | Conventional Commits | `feat(scope): message` |

Claude Code must use this document as the source of truth for all naming, style, and structure-related decisions in this repository.
