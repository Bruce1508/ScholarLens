"""
Claude API Service - Simplified for Hackathon
Core functions only, no complex validation
"""
import os
import json
from typing import Dict, List, Any
from anthropic import Anthropic
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        """Initialize Claude client with API key from environment"""
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            logger.warning("CLAUDE_API_KEY not found in environment. Service will fail on API calls.")
            # Still initialize to allow code to run without API key for testing structure

        self.client = Anthropic(api_key=api_key) if api_key else None
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
        self.temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "2048"))

        # Load prompts directly (simplified - no file loading)
        self.prompts = self._load_inline_prompts()

    def _load_inline_prompts(self) -> Dict[str, str]:
        """Inline prompts for speed - no file loading needed"""
        return {
            "persona_builder": """You are analyzing a scholarship description to extract its personality genome.
                Output JSON ONLY with this exact structure:
                {
                    "persona_name": "string (e.g., 'The Innovation Leader')",
                    "tone": "string (e.g., 'Ambitious and Visionary')",
                    "weights": {
                        "Academics": float 0-1,
                        "Leadership": float 0-1,
                        "Community": float 0-1,
                        "Innovation": float 0-1,
                        "FinancialNeed": float 0-1,
                        "Research": float 0-1
                    },
                    "rationale": "string (1-2 sentences)"
                }

                Rules:
                - Weights must sum to 1.0 (±0.01)
                - Identify what the scholarship values most
                - No markdown, only JSON

                Scholarship Description:
                """,

            "essay_generator": """Generate a 3-paragraph scholarship essay that aligns with the given persona.
                Output JSON ONLY with this structure:
                {
                    "persona_name": "string",
                    "tone_used": "string",
                    "essay": [
                        {
                            "paragraph": "string (paragraph text)",
                            "focus": "string (Academics/Leadership/Community/Innovation/FinancialNeed/Research)",
                            "reason": "string (why this focus)",
                            "alignment_score": float 0-1
                        }
                    ],
                    "overall_alignment": float 0-1,
                    "summary": "string"
                }

                Write naturally, personally, and match the scholarship's tone.
                Each paragraph should be 80-100 words.

                Input:
                """,

            "evaluation_agent": """Compare two essays against a scholarship persona.
                Output JSON ONLY with this structure:
                {
                    "persona_name": "string",
                    "trait_alignment": {
                        "Academics": float 0-1,
                        "Leadership": float 0-1,
                        "Community": float 0-1,
                        "Innovation": float 0-1,
                        "FinancialNeed": float 0-1,
                        "Research": float 0-1
                    },
                    "baseline_alignment": {
                        "Academics": float 0-1,
                        "Leadership": float 0-1,
                        "Community": float 0-1,
                        "Innovation": float 0-1,
                        "FinancialNeed": float 0-1,
                        "Research": float 0-1
                    },
                    "alignment_gain": float,
                    "tone_consistency_score": float 0-1,
                    "summary": "string (why adaptive is better)",
                    "recommendation": "string (start with action verb)"
                }

                Input:
                """
        }

    def analyze_persona(self, scholarship_description: str) -> Dict[str, Any]:
        """
        Analyze scholarship and extract personality genome
        """
        if not self.client:
            # Return mock data if no API key
            return self._mock_persona_response()

        try:
            prompt = self.prompts["persona_builder"] + scholarship_description

            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Clean response - remove any markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())

            # Log success
            logger.info(f"Successfully analyzed persona: {result.get('persona_name', 'Unknown')}")

            return result

        except Exception as e:
            logger.error(f"Error in analyze_persona: {str(e)}")
            # Return mock data on error
            return self._mock_persona_response()

    def generate_essay(self, persona: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate adaptive essay based on persona and student profile
        """
        if not self.client:
            return self._mock_essay_response(persona)

        try:
            # Prepare input data
            input_data = {
                "persona": persona,
                "student_profile": student_profile
            }

            prompt = self.prompts["essay_generator"] + json.dumps(input_data, indent=2)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Clean response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())

            logger.info("Successfully generated adaptive essay")

            return result

        except Exception as e:
            logger.error(f"Error in generate_essay: {str(e)}")
            return self._mock_essay_response(persona)

    def compare_essays(self, persona: Dict[str, Any], adaptive_essay: List[str], baseline_essay: List[str]) -> Dict[str, Any]:
        """
        Compare adaptive vs baseline essays
        """
        if not self.client:
            return self._mock_evaluation_response(persona)

        try:
            # Prepare input data
            input_data = {
                "persona": persona,
                "adaptive_essay": adaptive_essay,
                "baseline_essay": baseline_essay
            }

            prompt = self.prompts["evaluation_agent"] + json.dumps(input_data, indent=2)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.3,  # Lower temperature for evaluation
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Clean response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text.strip())

            logger.info(f"Evaluation complete. Alignment gain: {result.get('alignment_gain', 0)}")

            return result

        except Exception as e:
            logger.error(f"Error in compare_essays: {str(e)}")
            return self._mock_evaluation_response(persona)

    # Mock responses for testing without API key
    def _mock_persona_response(self) -> Dict[str, Any]:
        """Mock persona response for testing"""
        return {
            "persona_name": "The Innovation Leader",
            "tone": "Ambitious and Forward-Thinking",
            "weights": {
                "Academics": 0.20,
                "Leadership": 0.35,
                "Community": 0.15,
                "Innovation": 0.30,
                "FinancialNeed": 0.00,
                "Research": 0.00
            },
            "rationale": "This scholarship emphasizes leadership and innovation in STEM fields."
        }

    def _mock_essay_response(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Mock essay response for testing"""
        return {
            "persona_name": persona.get("persona_name", "The Leader"),
            "tone_used": persona.get("tone", "Professional"),
            "essay": [
                {
                    "paragraph": "Leading my school's robotics team taught me that innovation isn't just about building machines—it's about building futures. When we faced budget constraints, I organized coding workshops for younger students, turning our challenge into an opportunity to inspire the next generation of STEM leaders.",
                    "focus": "Leadership",
                    "reason": "Emphasizing leadership aligns with the scholarship's primary focus",
                    "alignment_score": 0.85
                },
                {
                    "paragraph": "My proudest innovation was developing an AI-powered tutoring app that helped struggling students improve their math scores by 30%. This project combined my technical skills with my passion for educational equity, demonstrating how technology can bridge academic gaps.",
                    "focus": "Innovation",
                    "reason": "Showcasing innovation in education technology",
                    "alignment_score": 0.80
                },
                {
                    "paragraph": "These experiences have shaped my vision to pursue computer science with a focus on educational technology. I aim to develop accessible learning platforms that adapt to individual needs, ensuring every student has the tools to reach their potential.",
                    "focus": "Academics",
                    "reason": "Connecting achievements to academic goals",
                    "alignment_score": 0.75
                }
            ],
            "overall_alignment": 0.80,
            "summary": "Essay successfully emphasizes leadership and innovation while maintaining authentic voice."
        }

    def _mock_evaluation_response(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """Mock evaluation response for testing"""
        return {
            "persona_name": persona.get("persona_name", "The Leader"),
            "trait_alignment": {
                "Academics": 0.70,
                "Leadership": 0.85,
                "Community": 0.60,
                "Innovation": 0.80,
                "FinancialNeed": 0.00,
                "Research": 0.20
            },
            "baseline_alignment": {
                "Academics": 0.75,
                "Leadership": 0.50,
                "Community": 0.40,
                "Innovation": 0.45,
                "FinancialNeed": 0.00,
                "Research": 0.15
            },
            "alignment_gain": 0.25,
            "tone_consistency_score": 0.88,
            "summary": "The adaptive essay shows 25% better alignment with scholarship values, particularly in leadership and innovation aspects.",
            "recommendation": "Use the adaptive essay - it clearly demonstrates stronger alignment with the scholarship's focus on innovation and leadership."
        }

# Singleton instance
claude_service = ClaudeService()