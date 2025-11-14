"""
AI Extractor Service
Uses Claude API to extract structured profile data from resume text
"""
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from api.services.claude_service import claude_service

logger = logging.getLogger(__name__)

class AIExtractor:
    """Service for AI-powered data extraction from resumes"""

    def __init__(self):
        self.claude = claude_service

    def extract_profile_from_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured profile data from resume text using Claude

        Args:
            resume_text: Plain text from resume

        Returns:
            Dictionary with extracted profile data
        """
        if not resume_text:
            return self._empty_profile()

        prompt = f"""You are analyzing a resume to extract structured information.
Extract all relevant information and return JSON ONLY with this exact structure:
{{
    "name": "string",
    "email": "string or null",
    "phone": "string or null",
    "gpa": float or null,
    "activities": ["activity1", "activity2"],
    "achievements": ["achievement1", "achievement2"],
    "goals": "string describing career goals or objectives",
    "skills": ["skill1", "skill2", "skill3"],
    "education": [
        {{
            "school": "string",
            "degree": "string",
            "field": "string",
            "graduation_year": "string or null",
            "gpa": float or null
        }}
    ],
    "work_experience": [
        {{
            "company": "string",
            "role": "string",
            "duration": "string",
            "description": "string",
            "key_achievements": ["achievement1", "achievement2"]
        }}
    ],
    "certifications": ["cert1", "cert2"],
    "languages": ["English (Native)", "Spanish (Fluent)"],
    "awards": ["award1", "award2"],
    "extraction_confidence": float between 0.0 and 1.0
}}

Important extraction rules:
- Extract actual data from the resume, don't make up information
- If a field is not found, use null or empty array
- For GPA, extract only if explicitly mentioned (0.0-4.0 scale)
- For activities, include clubs, organizations, volunteer work
- For achievements, include quantifiable accomplishments
- For skills, include both technical and soft skills
- Calculate extraction_confidence based on how much data was found (0.0=no data, 1.0=all fields filled)
- Goals can be extracted from objective, summary, or career goals sections

Resume Text:
{resume_text}

Return ONLY valid JSON, no markdown or commentary."""

        try:
            # Call Claude API
            if not self.claude.client:
                logger.warning("Claude API not available, using mock extraction")
                return self._mock_extraction(resume_text)

            message = self.claude.client.messages.create(
                model=self.claude.model,
                max_tokens=2048,
                temperature=0.3,  # Lower temperature for more consistent extraction
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

            # Parse JSON
            result = json.loads(response_text.strip())

            # Validate and clean result
            result = self._validate_extracted_data(result)

            logger.info(f"Successfully extracted profile with confidence: {result.get('extraction_confidence', 0)}")
            return result

        except Exception as e:
            logger.error(f"Error in AI extraction: {str(e)}")
            return self._fallback_extraction(resume_text)

    def _validate_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean extracted data

        Args:
            data: Raw extracted data

        Returns:
            Cleaned and validated data
        """
        # Ensure all required fields exist
        validated = {
            "name": data.get("name", ""),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "gpa": data.get("gpa"),
            "activities": data.get("activities", []),
            "achievements": data.get("achievements", []),
            "goals": data.get("goals", ""),
            "skills": data.get("skills", []),
            "education": data.get("education", []),
            "work_experience": data.get("work_experience", []),
            "certifications": data.get("certifications", []),
            "languages": data.get("languages", []),
            "awards": data.get("awards", []),
            "extraction_confidence": data.get("extraction_confidence", 0.5)
        }

        # Validate GPA
        if validated["gpa"] is not None:
            try:
                gpa = float(validated["gpa"])
                if gpa < 0 or gpa > 4.0:
                    validated["gpa"] = None
                else:
                    validated["gpa"] = round(gpa, 2)
            except:
                validated["gpa"] = None

        # Ensure arrays are actually arrays
        array_fields = ["activities", "achievements", "skills", "education",
                       "work_experience", "certifications", "languages", "awards"]
        for field in array_fields:
            if not isinstance(validated[field], list):
                validated[field] = []

        # Clean strings in arrays
        for field in ["activities", "achievements", "skills", "certifications", "languages", "awards"]:
            validated[field] = [str(item).strip() for item in validated[field] if item]

        # Validate confidence score
        try:
            conf = float(validated["extraction_confidence"])
            validated["extraction_confidence"] = max(0.0, min(1.0, conf))
        except:
            validated["extraction_confidence"] = 0.5

        return validated

    def _fallback_extraction(self, resume_text: str) -> Dict[str, Any]:
        """
        Fallback extraction using regex patterns when AI fails

        Args:
            resume_text: Resume text

        Returns:
            Basic extracted data
        """
        from api.services.pdf_parser import pdf_parser

        result = self._empty_profile()

        # Try to extract basic information
        email = pdf_parser.extract_email(resume_text)
        if email:
            result["email"] = email

        phone = pdf_parser.extract_phone(resume_text)
        if phone:
            result["phone"] = phone

        gpa = pdf_parser.extract_gpa(resume_text)
        if gpa:
            result["gpa"] = gpa

        # Extract name (usually at the beginning)
        lines = resume_text.split('\n')
        if lines:
            # First non-empty line is often the name
            for line in lines[:5]:
                line = line.strip()
                if line and len(line) < 50 and not any(char in line for char in ['@', '|', '•']):
                    result["name"] = line
                    break

        # Look for skills section
        skills_keywords = ["Python", "Java", "JavaScript", "React", "SQL", "Machine Learning",
                          "Leadership", "Communication", "Problem Solving", "Teamwork"]
        found_skills = []
        text_lower = resume_text.lower()
        for skill in skills_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        result["skills"] = found_skills[:10]  # Limit to 10 skills

        result["extraction_confidence"] = 0.3  # Low confidence for fallback

        return result

    def _mock_extraction(self, resume_text: str) -> Dict[str, Any]:
        """
        Mock extraction for testing without API

        Args:
            resume_text: Resume text

        Returns:
            Mock extracted data
        """
        # Use fallback extraction as mock
        result = self._fallback_extraction(resume_text)
        result["extraction_confidence"] = 0.7  # Moderate confidence for mock
        return result

    def _empty_profile(self) -> Dict[str, Any]:
        """
        Return empty profile structure

        Returns:
            Empty profile dictionary
        """
        return {
            "name": "",
            "email": None,
            "phone": None,
            "gpa": None,
            "activities": [],
            "achievements": [],
            "goals": "",
            "skills": [],
            "education": [],
            "work_experience": [],
            "certifications": [],
            "languages": [],
            "awards": [],
            "extraction_confidence": 0.0
        }

    def calculate_confidence(self, extracted_data: Dict[str, Any]) -> float:
        """
        Calculate extraction confidence based on filled fields

        Args:
            extracted_data: Extracted profile data

        Returns:
            Confidence score between 0.0 and 1.0
        """
        important_fields = ["name", "email", "education", "skills", "work_experience"]
        optional_fields = ["gpa", "phone", "activities", "achievements", "goals",
                          "certifications", "languages", "awards"]

        score = 0.0
        max_score = 0.0

        # Important fields worth more
        for field in important_fields:
            max_score += 2.0
            value = extracted_data.get(field)
            if value:
                if isinstance(value, list) and len(value) > 0:
                    score += 2.0
                elif isinstance(value, str) and value.strip():
                    score += 2.0
                elif value is not None:
                    score += 2.0

        # Optional fields worth less
        for field in optional_fields:
            max_score += 1.0
            value = extracted_data.get(field)
            if value:
                if isinstance(value, list) and len(value) > 0:
                    score += 1.0
                elif isinstance(value, str) and value.strip():
                    score += 1.0
                elif value is not None:
                    score += 1.0

        confidence = score / max_score if max_score > 0 else 0.0
        return round(confidence, 2)

# Singleton instance
ai_extractor = AIExtractor()