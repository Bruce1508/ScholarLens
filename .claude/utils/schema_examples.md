# utils/schema_examples.md  
**Purpose:**  
Define and document all JSON schemas used across `.claude/prompts/`.  
Claude Code and backend validators must use these patterns to verify prompt outputs before post-processing.  
All fields shown below are **required unless explicitly marked optional**.

---

## 🧩 1. persona_builder.md

### Input Schema
```json
{
  "description": "string",
  "context": {
    "cluster_labels": ["string", "string"]
  }
}
```

### Output Schema
```json
{
  "persona_name": "string",
  "tone": "string",
  "weights": {
    "Academics": "float (0–1)",
    "Leadership": "float (0–1)",
    "Community": "float (0–1)",
    "Innovation": "float (0–1)",
    "FinancialNeed": "float (0–1)",
    "Research": "float (0–1)"
  },
  "rationale": "string"
}
```

### Validation Notes
- All 6 traits must exist in weights.
- Sum(weights) ≈ 1.0 (±0.01).
- All numeric values rounded to 2 decimals.

---

## 🧠 2. essay_generator.md

### Input Schema
```json
{
  "persona": {
    "persona_name": "string",
    "tone": "string",
    "weights": { "string": "float" }
  },
  "student_profile": {
    "name": "string",
    "GPA": "float",
    "activities": ["string"],
    "achievements": ["string"],
    "goals": "string"
  }
}
```

### Output Schema
```json
{
  "persona_name": "string",
  "tone_used": "string",
  "essay": [
    {
      "paragraph": "string",
      "focus": "string (Academics|Leadership|Community|Innovation|FinancialNeed|Research)",
      "reason": "string",
      "alignment_score": "float (0–1)"
    },
    {
      "...": "..."
    }
  ],
  "overall_alignment": "float (0–1)",
  "summary": "string"
}
```

### Validation Notes
- Must contain 3 paragraphs.
- Each object in essay must include all 4 fields.
- `overall_alignment` = mean of alignment scores.
- No text exceeding 120 words per paragraph.

---

## 🔎 3. cluster_labeler.md

### Input Schema
```json
{
  "cluster_id": "integer",
  "samples": ["string", "string", "..."],
  "embedding_summary": {
    "keywords": ["string", "string"]
  }
}
```

### Output Schema
```json
{
  "cluster_id": "integer",
  "archetype_name": "string",
  "style_summary": "string",
  "dominant_tone": "string",
  "weights": {
    "Academics": "float (0–1)",
    "Leadership": "float (0–1)",
    "Community": "float (0–1)",
    "Innovation": "float (0–1)",
    "FinancialNeed": "float (0–1)",
    "Research": "float (0–1)"
  },
  "keywords": ["string", "string", "..."]
}
```

### Validation Notes
- Sum(weights) ≈ 1.0.
- `keywords` must contain ≥3 elements.
- `archetype_name` ≤ 4 words.
- `style_summary` ≤ 25 words.

---

## ⚖️ 4. evaluation_agent.md

### Input Schema
```json
{
  "persona": {
    "persona_name": "string",
    "tone": "string",
    "weights": { "string": "float (0–1)" }
  },
  "adaptive_essay": ["string", "string", "string"],
  "baseline_essay": ["string", "string", "string"]
}
```

### Output Schema
```json
{
  "persona_name": "string",
  "trait_alignment": {
    "Academics": "float (0–1)",
    "Leadership": "float (0–1)",
    "Community": "float (0–1)",
    "Innovation": "float (0–1)",
    "FinancialNeed": "float (0–1)",
    "Research": "float (0–1)"
  },
  "baseline_alignment": {
    "Academics": "float (0–1)",
    "Leadership": "float (0–1)",
    "Community": "float (0–1)",
    "Innovation": "float (0–1)",
    "FinancialNeed": "float (0–1)",
    "Research": "float (0–1)"
  },
  "alignment_gain": "float",
  "tone_consistency_score": "float (0–1)",
  "summary": "string",
  "recommendation": "string"
}
```

### Validation Notes
- All traits must appear in both alignment maps.
- `alignment_gain` = (adaptive_total – baseline_total).
- `summary` ≤ 60 words.
- `recommendation` starts with action verb ("Use", "Revise", "Improve").

---

## 🪞 5. mirror_test.md (for future implementation)

### Input Schema
```json
{
  "persona": {
    "persona_name": "string",
    "tone": "string",
    "weights": { "string": "float" }
  },
  "essay": [
    "string (paragraph 1)",
    "string (paragraph 2)",
    "string (paragraph 3)"
  ]
}
```

### Output Schema
```json
{
  "persona_name": "string",
  "feedback": [
    {
      "paragraph_index": "integer",
      "focus_detected": "string",
      "alignment_score": "float (0–1)",
      "suggestion": "string"
    }
  ],
  "overall_alignment": "float (0–1)",
  "improvement_summary": "string"
}
```

### Validation Notes
- One feedback item per paragraph.
- `suggestion` must be actionable ("Add more community emphasis…", "Tighten academic detail…").
- `overall_alignment` = mean of alignment scores.

---

## 🧾 6. General Validation Rules

| Rule | Enforcement |
|------|-------------|
| JSON only, no markdown | Always |
| All keys must exist | Strict |
| Float range | 0 ≤ value ≤ 1 |
| Sum of weights | ≈ 1.0 |
| String fields | Non-empty |
| Rounding | 2 decimals |
| Output length limits | Enforced by validator in backend |

---

## ✅ 7. Example Schema Reference Map

| Prompt File | Output Root Keys |
|-------------|------------------|
| `persona_builder.md` | `persona_name`, `tone`, `weights`, `rationale` |
| `essay_generator.md` | `essay[]`, `overall_alignment`, `summary` |
| `cluster_labeler.md` | `archetype_name`, `style_summary`, `dominant_tone`, `weights`, `keywords` |
| `evaluation_agent.md` | `trait_alignment`, `baseline_alignment`, `alignment_gain`, `summary`, `recommendation` |
| `mirror_test.md` | `feedback[]`, `overall_alignment`, `improvement_summary` |

---

## Final Note:
All schema definitions in this file serve as reference for validation and testing.  
No model or API call should modify or extend these schemas without explicit documentation updates here.
