-- ======================================================
-- Database Indexes for ScholarLens
-- Run this after initial migration
-- ======================================================

-- Speed up joins
CREATE INDEX IF NOT EXISTS idx_persona_scholarship
ON personas(scholarship_id);

CREATE INDEX IF NOT EXISTS idx_essay_student
ON essays(student_profile_id);

CREATE INDEX IF NOT EXISTS idx_essay_persona
ON essays(persona_id);

CREATE INDEX IF NOT EXISTS idx_evaluation_persona
ON evaluations(persona_id);

CREATE INDEX IF NOT EXISTS idx_evaluation_adaptive_essay
ON evaluations(adaptive_essay_id);

CREATE INDEX IF NOT EXISTS idx_evaluation_baseline_essay
ON evaluations(baseline_essay_id);

-- JSONB indexing for fast queries on JSON fields
CREATE INDEX IF NOT EXISTS idx_persona_weights
ON personas USING GIN(weights);

CREATE INDEX IF NOT EXISTS idx_essay_paragraphs
ON essays USING GIN(paragraphs);

CREATE INDEX IF NOT EXISTS idx_scholarship_metadata
ON scholarships USING GIN(metadata);

CREATE INDEX IF NOT EXISTS idx_cluster_weights
ON winner_essay_clusters USING GIN(weights);

CREATE INDEX IF NOT EXISTS idx_cluster_keywords
ON winner_essay_clusters USING GIN(keywords);

-- Full-text search on scholarship descriptions
CREATE INDEX IF NOT EXISTS idx_scholarship_description_fts
ON scholarships USING GIN(to_tsvector('english', description));

CREATE INDEX IF NOT EXISTS idx_scholarship_criteria_fts
ON scholarships USING GIN(to_tsvector('english', criteria));

-- Time-based queries
CREATE INDEX IF NOT EXISTS idx_scholarship_deadline
ON scholarships(deadline);

CREATE INDEX IF NOT EXISTS idx_scholarship_created
ON scholarships(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_essay_created
ON essays(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_api_log_created
ON api_logs(created_at DESC);

-- API logs filtering
CREATE INDEX IF NOT EXISTS idx_api_log_prompt_type
ON api_logs(prompt_type);

CREATE INDEX IF NOT EXISTS idx_api_log_status
ON api_logs(status);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_essay_type_alignment
ON essays(essay_type, overall_alignment DESC);

CREATE INDEX IF NOT EXISTS idx_api_log_type_status
ON api_logs(prompt_type, status);
