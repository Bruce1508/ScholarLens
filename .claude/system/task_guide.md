# system/task_guide.md

## 1. Purpose of This File
This document defines how **Claude Code** should interpret, load, and execute prompt files in the `.claude/prompts/` directory.  
It explains the **task mapping**, **data flow**, and **execution chain** that connect backend logic with LLM prompt agents.  
Claude Code must treat this file as the authoritative guide for handling prompt-based tasks across the system.

---

## 2. General Execution Model
The system uses a **modular agent chain** architecture.  
Each task is handled by one self-contained prompt file, following a standardized input–output protocol (always JSON).

### Core Principles:
1. Each prompt has a **single purpose** (Persona Builder, Essay Generator, etc.).  
2. All LLM outputs must be **strict JSON**, validated against schemas in `.claude/utils/schema_examples.md`.  
3. Claude Code must use **chain-of-tasks execution**, never merging multiple prompt logics into one.  
4. The backend invokes each prompt using API-specific logic in `/backend/api/services/claude_service.py`.  
5. Claude Code must automatically recognize which prompt to use based on request type or API endpoint name.

---

## 3. Task → Prompt Mapping

| Task Name | Description | Prompt File | Consumed By |
|-----------|-------------|-------------|-------------|
| **Cluster Labeling** | Label and describe winner essay clusters using style patterns | `cluster_labeler.md` | Backend (Offline / Initialization) |
| **Persona Builder** | Extract persona weights, tone, and values from scholarship description | `persona_builder.md` | `/api/v1/persona/analyze` |
| **Essay Generator** | Generate tailored essay paragraphs based on persona and student profile | `essay_generator.md` | `/api/v1/essay/generate` |
| **Evaluation Agent** | Compare generic vs adaptive drafts and produce alignment metrics | `evaluation_agent.md` | `/api/v1/essay/evaluate` |
| **Mirror Test** | Evaluate an existing essay vs scholarship persona and suggest improvements | `mirror_test.md` | `/api/v1/essay/mirror-test` |

---

## 4. Standard Input/Output Schemas

### A. Input Schema (Generic)
Every LLM prompt receives a structured JSON input:

```json
{
  "task": "persona_builder",
  "inputs": {
    "description": "Scholarship description text here...",
    "student_profile": {
      "name": "Alice",
      "GPA": 3.8,
      "activities": ["volunteering", "robotics"],
      "goals": "Improve STEM education access."
    },
    "context": "optional — previous task outputs if chained"
  }
}
```

### B. Output Schema (Generic)
All LLM responses must follow strict JSON format:

```json
{
  "success": true,
  "data": {
    "persona_name": "Community Builder",
    "tone": "Empathetic and purposeful",
    "weights": {
      "Leadership": 0.4,
      "Community": 0.35,
      "Academics": 0.25
    },
    "rationale": "Scholarship emphasizes social leadership and service."
  }
}
```

Each prompt file defines its own schema variant (see `.claude/utils/schema_examples.md`).

---

## 5. Task Chain (Execution Order)
Claude Code must follow this strict sequence when executing combined analysis:

**Cluster Labeler → Persona Builder → Essay Generator → Evaluation Agent → Mirror Test**

### Step Breakdown

#### Cluster Labeler
- Runs offline or periodically.
- Input: winner essay corpus.
- Output: cluster labels (`clusters.json`).

#### Persona Builder
- Input: scholarship description text.
- Output: persona JSON (`persona_name`, `weights`, `tone`, `rationale`).

#### Essay Generator
- Input: persona JSON + student profile.
- Output: essay JSON array of paragraphs with `focus`, `reason`, `alignment_score`.

#### Evaluation Agent
- Input: adaptive essay + generic essay.
- Output: comparative metrics (`alignment_gain`, `tone_consistency`, score delta).

#### Mirror Test (optional)
- Input: existing essay + persona JSON.
- Output: per-paragraph feedback and improvement suggestions.

---

## 6. Prompt Invocation Guidelines
Claude Code must adhere to these operational principles:

### 6.1 File Selection
The backend determines which `.md` prompt file to load based on task parameter.

Example mapping in pseudocode:
```python
PROMPT_MAP = {
    "persona_builder": ".claude/prompts/persona_builder.md",
    "essay_generator": ".claude/prompts/essay_generator.md",
    "mirror_test": ".claude/prompts/mirror_test.md",
    "cluster_labeler": ".claude/prompts/cluster_labeler.md",
    "evaluation_agent": ".claude/prompts/evaluation_agent.md",
}
```

### 6.2 Execution Context
- Each prompt runs independently — never rely on previous LLM memory.
- If chaining is required, explicitly pass prior output as context.
- Claude Code must not modify prompt text dynamically, only feed parameters through code.

### 6.3 Expected Response Handling
- Always parse JSON safely (try/except).
- Validate output keys against schema (strict match).
- If Claude's output contains non-JSON text, fallback to regex cleanup (`{...}` extraction only).

### 6.4 Retry Logic
- If API returns non-JSON or truncated output, retry up to 2 times with the same payload.
- Claude Code should not generate retry logic differently per prompt — use shared function `safe_claude_call()` in backend services.

---

## 7. Claude Code Behavior Guidelines

### 7.1 When Claude Writes Code
When generating or modifying backend or frontend code, Claude Code must:
- Use this document to identify which prompt corresponds to which endpoint.
- Never mix logic between unrelated prompts.
- Ensure prompt_name and API endpoint naming remain consistent (e.g., `/api/v1/essay/generate` → `essay_generator.md`).

### 7.2 When Claude Updates Prompts
When editing `.claude/prompts/.md`:
- Keep instructions concise and structured (no more than 50 lines).
- Always include explicit JSON output schema.
- End every prompt with:
  - Return valid JSON only. Do not include commentary or markdown.

### 7.3 When Claude Evaluates Changes
Before approving generated changes:
- Check if correct prompt file was invoked.
- Confirm output schema matches expected structure.
- Validate that code references correct backend service.
- Confirm naming matches conventions from `coding_rules.md`.

---

## 8. Example Task Flow (Full Chain)

### Input
- Student: GPA 3.8, volunteering, robotics
- Scholarship Description: "We support leaders who improve their communities through STEM innovation."

### Step-by-Step

#### Persona Builder →
Output:
```json
{
  "persona_name": "Innovative Leader",
  "weights": {"Leadership":0.45,"Innovation":0.35,"Community":0.20},
  "tone": "Ambitious and visionary"
}
```

#### Essay Generator →
Output: 3 paragraphs with tags [Leadership], [Innovation], [Community].

#### Evaluation Agent →
Output:
```json
{"alignment_gain": 0.27, "message": "Adaptive essay better matches scholarship priorities."}
```

#### Mirror Test (optional) →
Suggests specific rewrite points.

---

## 9. Task Ownership

| Task | Primary Developer | File | LLM Role |
|------|-------------------|------|----------|
| Persona Builder | Backend AI Engineer | `persona_builder.md` | Extract values & weights |
| Essay Generator | Full Stack Engineer | `essay_generator.md` | Generate draft + rationale |
| Evaluation Agent | Backend Engineer | `evaluation_agent.md` | Compare and score essays |
| Mirror Test | AI Researcher | `mirror_test.md` | Feedback on essay alignment |
| Cluster Labeler | Data Scientist | `cluster_labeler.md` | Archetype identification |

Claude Code should automatically associate edits with these logical owners when creating commits or PRs.

---

## 10. Testing and Validation
After editing or executing a prompt, Claude Code should:
- Run validation script `/backend/tests/test_prompts.py` (if available).
- Confirm JSON keys are consistent with `schema_examples.md`.
- Log prompt name and task ID for reproducibility.
- Store successful outputs in `/data/test_outputs/`.

---

## 11. Debugging Instructions
If Claude encounters:
- **Invalid JSON:** clean output and retry.
- **Missing keys:** default to "N/A" for optional fields.
- **Low coherence essay output:** re-run generation with `temperature=0.7`.
- **Token overflow:** request shorter output (limit paragraphs = 3).

Claude Code should never silently skip a failing task — always log errors in `backend/api/services/claude_service.py`.

---

## 12. Summary
- Each task = one `.md` prompt file.
- Input/Output strictly JSON.
- Chain order: `cluster_labeler` → `persona_builder` → `essay_generator` → `evaluation_agent` → `mirror_test`.
- Use `task_guide.md` as the single source of truth for how Claude interacts with each prompt.

Claude Code must always refer here before generating or executing LLM-driven logic.
