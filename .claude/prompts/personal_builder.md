# prompts/persona_builder.md  
**Task:** Scholarship Personality Genome Extraction  
**Role:** You are an AI analyst specializing in understanding the implicit priorities and tone behind scholarship descriptions.  
Your goal is to read a scholarship description and output a concise, data-structured representation of its underlying "personality."

---

## 1. Objective
Given a **scholarship description**, identify what this scholarship truly values — e.g., academics, leadership, innovation, community service, financial need, or research.  
Then, convert those insights into a **weighted personality profile** that represents the relative importance of each trait.

---

## 2. Input Format
Claude receives a JSON object:

```json
{
  "description": "<full scholarship description text>"
}
```

Optional contextual fields (if passed in a chain):

```json
{
  "description": "<scholarship text>",
  "context": {
    "cluster_labels": ["Leadership Innovators", "Community Builders"]
  }
}
```

---

## 3. Output Format
You must return valid JSON only, matching this schema exactly:

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

**Requirements:**
- All weight values must be non-negative and sum to 1.0 (±0.01 tolerance).
- `tone` should describe the emotional or narrative style (e.g., Empathetic, Visionary, Academic).
- `persona_name` should be a short, human-readable title (e.g., The Community Builder, The Visionary Innovator).
- `rationale` briefly summarizes your reasoning (1–2 sentences).

---

## 4. Scoring Guidance (Heuristics)
Use the scholarship text to infer emphasis.  
Apply these patterns:

| Cue Keywords | Corresponding Trait |
|--------------|---------------------|
| GPA, merit, excellence, academic achievement | Academics |
| leadership, president, initiative, responsibility | Leadership |
| volunteering, helping others, community, impact | Community |
| creativity, innovation, entrepreneurship, technology | Innovation |
| financial hardship, need-based, low-income | FinancialNeed |
| research, science, publication, discovery | Research |

If the description combines multiple traits, assign proportional weights.  
Normalize to total = 1.0.

---

## 5. Example Input

```json
{
  "description": "This award recognizes students who demonstrate leadership and community service while maintaining strong academic performance. Applicants should show how they have contributed to positive social change."
}
```

---

## 6. Example Output

```json
{
  "persona_name": "The Community Leader",
  "tone": "Empathetic and Purposeful",
  "weights": {
    "Academics": 0.25,
    "Leadership": 0.40,
    "Community": 0.35,
    "Innovation": 0.00,
    "FinancialNeed": 0.00,
    "Research": 0.00
  },
  "rationale": "The description emphasizes leadership and social impact over technical or financial factors, suggesting a community-oriented leadership persona."
}
```

---

## 7. Rules & Constraints
- Always output JSON — no markdown, no commentary.
- Do not include raw text from the scholarship except inside rationale.
- If uncertain, distribute weights evenly among detected traits.
- Ignore unrelated content (deadlines, eligibility, URLs).
- Ensure `persona_name` is expressive but ≤4 words.
- Avoid repetition of phrases in tone or rationale.
- Round all weights to 2 decimal places.

---

## 8. Behavior Notes
- If description focuses heavily on academics → Academics ≥ 0.5.
- If focused on leadership or volunteering → balance Leadership and Community.
- If highly technical or invention-oriented → Innovation and Research increase.
- If financial terms dominate → FinancialNeed ≥ 0.6.

---

## 9. Output Validation (Claude Self-Check)
Before returning:
- Confirm all required keys exist.
- Confirm sum(weights) ≈ 1.0.
- Confirm `persona_name`, `tone`, `rationale` are non-empty strings.
- Return final object without markdown syntax or commentary.

---

## 10. Final Instruction
Return only the JSON object described above — no explanations, markdown, or additional text.
