# utils/testcases.md  
**Purpose:**  
Provide standardized example inputs and outputs for validating each `.claude/prompts/` file.  
These serve as reference data for integration tests, schema verification, and Claude Code dry runs.  
All testcases below follow minimal yet representative examples covering key logical patterns.

---

## 🧩 1. persona_builder.md

### Test Input
```json
{
  "description": "This scholarship honors students who combine strong academics with leadership in community outreach programs that improve social wellbeing."
}
```

### Expected Output
```json
{
  "persona_name": "The Academic Leader",
  "tone": "Purposeful and Reflective",
  "weights": {
    "Academics": 0.35,
    "Leadership": 0.40,
    "Community": 0.25,
    "Innovation": 0.00,
    "FinancialNeed": 0.00,
    "Research": 0.00
  },
  "rationale": "The description blends academic excellence with leadership in community engagement, suggesting an academically strong and socially active persona."
}
```

### Validation Focus
- Ensure all weights sum to ~1.0
- Verify persona naming follows pattern The [Adjective] [Trait]
- Confirm tone descriptive and rationale under 2 sentences

---

## 🧠 2. essay_generator.md

### Test Input
```json
{
  "persona": {
    "persona_name": "The Community Builder",
    "tone": "Empathetic and Uplifting",
    "weights": {
      "Academics": 0.20,
      "Leadership": 0.30,
      "Community": 0.40,
      "Innovation": 0.10,
      "FinancialNeed": 0.00,
      "Research": 0.00
    }
  },
  "student_profile": {
    "name": "Maria",
    "GPA": 3.7,
    "activities": ["volunteer mentor", "local coding workshops"],
    "achievements": ["organized STEM tutoring sessions for kids"],
    "goals": "to make technology education accessible to everyone"
  }
}
```

### Expected Output
```json
{
  "persona_name": "The Community Builder",
  "tone_used": "Empathetic and Uplifting",
  "essay": [
    {
      "paragraph": "As a volunteer mentor, I have seen firsthand how sharing knowledge builds stronger, more connected communities.",
      "focus": "Community",
      "reason": "Highlights empathy and collaboration central to community service.",
      "alignment_score": 0.42
    },
    {
      "paragraph": "Leading local coding workshops taught me how teamwork and patience can transform potential into real change.",
      "focus": "Leadership",
      "reason": "Demonstrates leadership through service and education.",
      "alignment_score": 0.32
    },
    {
      "paragraph": "I hope to continue developing tools that expand access to STEM learning for underrepresented groups.",
      "focus": "Innovation",
      "reason": "Connects innovation with inclusivity, aligning with community vision.",
      "alignment_score": 0.26
    }
  ],
  "overall_alignment": 0.33,
  "summary": "Essay maintains a caring tone and reflects the scholarship's emphasis on leadership through service and innovation in education."
}
```

### Validation Focus
- Exactly 3 paragraphs
- Focus tags valid and non-repeated
- Alignment scores normalized (~persona weights)

---

## 🔎 3. cluster_labeler.md

### Test Input
```json
{
  "cluster_id": 7,
  "samples": [
    "Designing low-cost prosthetic hands taught me to apply creativity for human-centered solutions.",
    "Through invention, I learned empathy and purpose in engineering for accessibility.",
    "Innovation to me means improving lives through practical science."
  ]
}
```

### Expected Output
```json
{
  "cluster_id": 7,
  "archetype_name": "The Humanitarian Innovator",
  "style_summary": "Optimistic, invention-driven essays connecting creativity with social good.",
  "dominant_tone": "Inspirational and Compassionate",
  "weights": {
    "Academics": 0.15,
    "Leadership": 0.10,
    "Community": 0.25,
    "Innovation": 0.45,
    "FinancialNeed": 0.00,
    "Research": 0.05
  },
  "keywords": ["innovation", "accessibility", "engineering", "purpose", "creativity"]
}
```

### Validation Focus
- Check archetype name 2–4 words
- Style summary under 25 words
- Weights normalized to 1.0

---

## ⚖️ 4. evaluation_agent.md

### Test Input
```json
{
  "persona": {
    "persona_name": "The Visionary Innovator",
    "tone": "Ambitious and Forward-Thinking",
    "weights": {
      "Academics": 0.20,
      "Leadership": 0.25,
      "Community": 0.15,
      "Innovation": 0.40,
      "FinancialNeed": 0.00,
      "Research": 0.00
    }
  },
  "adaptive_essay": [
    "As robotics captain, I led my team to build assistive devices improving accessibility.",
    "Innovation excites me because it bridges creativity and empathy to solve real challenges.",
    "My dream is to make engineering a tool for inclusion, not privilege."
  ],
  "baseline_essay": [
    "I am passionate about science and technology.",
    "I enjoy participating in school projects and learning from my peers.",
    "I want to pursue a degree in engineering."
  ]
}
```

### Expected Output
```json
{
  "persona_name": "The Visionary Innovator",
  "trait_alignment": {
    "Academics": 0.70,
    "Leadership": 0.75,
    "Community": 0.60,
    "Innovation": 0.90,
    "FinancialNeed": 0.00,
    "Research": 0.00
  },
  "baseline_alignment": {
    "Academics": 0.65,
    "Leadership": 0.45,
    "Community": 0.35,
    "Innovation": 0.40,
    "FinancialNeed": 0.00,
    "Research": 0.00
  },
  "alignment_gain": 0.27,
  "tone_consistency_score": 0.92,
  "summary": "Adaptive essay integrates innovation and empathy effectively, improving tone and alignment across all weighted traits.",
  "recommendation": "Use the adaptive essay. It reflects the persona's creative and community-driven focus."
}
```

### Validation Focus
- Numeric fields in [0,1]
- Gain positive (>0.1)
- Recommendation starts with verb ("Use", "Revise", etc.)

---

## 🪞 5. mirror_test.md (Future Integration)

### Test Input
```json
{
  "persona": {
    "persona_name": "The Community Leader",
    "tone": "Empathetic and Purposeful",
    "weights": {
      "Academics": 0.25,
      "Leadership": 0.40,
      "Community": 0.35,
      "Innovation": 0.00,
      "FinancialNeed": 0.00,
      "Research": 0.00
    }
  },
  "essay": [
    "My volunteering experience at a local youth center taught me patience and collaboration.",
    "Balancing academics with service helped me learn leadership rooted in empathy.",
    "I hope to continue creating spaces where everyone feels valued."
  ]
}
```

### Expected Output
```json
{
  "persona_name": "The Community Leader",
  "feedback": [
    {
      "paragraph_index": 1,
      "focus_detected": "Community",
      "alignment_score": 0.85,
      "suggestion": "Expand on measurable community outcomes for stronger impact."
    },
    {
      "paragraph_index": 2,
      "focus_detected": "Leadership",
      "alignment_score": 0.78,
      "suggestion": "Emphasize empathy-driven leadership more clearly."
    },
    {
      "paragraph_index": 3,
      "focus_detected": "Community",
      "alignment_score": 0.82,
      "suggestion": "Conclude with a sentence reinforcing purpose and future goals."
    }
  ],
  "overall_alignment": 0.82,
  "improvement_summary": "Essay aligns well but could highlight leadership intent more explicitly in the second paragraph."
}
```

### Validation Focus
- One feedback per paragraph
- Alignment values within 0–1
- Suggestions actionable and concise

---

## ✅ 6. Testing Procedure
- Store this file under `.claude/utils/testcases.md`.
- Each testcase can be loaded by backend validator for dry-run simulation.

For automated checks:
- Validate JSON schema conformity using `schema_examples.md`.
- Verify numeric normalization and string field presence.

Testing entrypoints (recommended):
- `test_persona_builder()`
- `test_essay_generator()`
- `test_cluster_labeler()`
- `test_evaluation_agent()`
- `test_mirror_test()` (when implemented)

---

## 🧾 7. Notes
- All examples are intentionally concise to keep LLM cost low during prompt testing.
- When running regression tests, each expected output can be used as gold data for comparison.
- Any schema deviation should raise a validation warning before merge or release.

---

## Final Instruction:
This file should be read-only for runtime agents.  
Only update when schema or prompt structure changes.
