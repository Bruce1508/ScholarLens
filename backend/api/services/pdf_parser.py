"""
PDF Parser Service
Extracts text from PDF files using pdfplumber
"""
import pdfplumber
from typing import Optional, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class PDFParser:
    """Service for extracting text and data from PDF files"""

    def extract_text(self, pdf_path: str) -> str:
        """
        Extract plain text from PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as string
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # Clean up text
            text = self._clean_text(text)
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text

        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            return ""

    def extract_structured_data(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract structured data from PDF (attempt to identify sections)

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with identified sections
        """
        try:
            sections = {
                "full_text": "",
                "contact": "",
                "education": "",
                "experience": "",
                "skills": "",
                "achievements": "",
                "summary": ""
            }

            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"

                sections["full_text"] = full_text

                # Try to identify sections using common headers
                sections["contact"] = self._extract_section(full_text,
                    ["contact", "email", "phone", "address"])
                sections["education"] = self._extract_section(full_text,
                    ["education", "academic", "university", "college", "degree"])
                sections["experience"] = self._extract_section(full_text,
                    ["experience", "work", "employment", "professional"])
                sections["skills"] = self._extract_section(full_text,
                    ["skills", "technical", "competencies", "technologies"])
                sections["achievements"] = self._extract_section(full_text,
                    ["achievements", "awards", "honors", "accomplishments"])
                sections["summary"] = self._extract_section(full_text,
                    ["summary", "objective", "profile", "about"])

            return sections

        except Exception as e:
            logger.error(f"Failed to extract structured data: {e}")
            return {"full_text": "", "error": str(e)}

    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text

        Args:
            text: Raw text from PDF

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that might break parsing
        text = text.replace('\x00', '')

        # Fix common OCR issues
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬂ', 'fl')

        # Trim
        text = text.strip()

        return text

    def _extract_section(self, text: str, keywords: list) -> str:
        """
        Try to extract a specific section from the text

        Args:
            text: Full text
            keywords: Keywords that might indicate the section

        Returns:
            Extracted section text
        """
        text_lower = text.lower()

        # Find the earliest keyword match
        start_pos = -1
        for keyword in keywords:
            pos = text_lower.find(keyword.lower())
            if pos != -1 and (start_pos == -1 or pos < start_pos):
                start_pos = pos

        if start_pos == -1:
            return ""

        # Extract text from that position
        # Try to find the next section header or take next 500 chars
        section_text = text[start_pos:start_pos + 500]

        # Try to find natural break points
        next_sections = ["education", "experience", "skills", "achievements",
                        "references", "contact", "summary", "objective"]

        for next_section in next_sections:
            if next_section not in keywords:
                next_pos = text_lower.find(next_section, start_pos + len(keywords[0]))
                if next_pos != -1:
                    section_text = text[start_pos:next_pos]
                    break

        return section_text.strip()

    def extract_email(self, text: str) -> Optional[str]:
        """
        Extract email from text

        Args:
            text: Text to search

        Returns:
            Email if found, None otherwise
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        """
        Extract phone number from text

        Args:
            text: Text to search

        Returns:
            Phone number if found, None otherwise
        """
        # US phone number patterns
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}'
        ]

        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        return None

    def extract_gpa(self, text: str) -> Optional[float]:
        """
        Extract GPA from text

        Args:
            text: Text to search

        Returns:
            GPA if found, None otherwise
        """
        # Look for GPA patterns like "GPA: 3.85" or "3.85/4.0"
        gpa_patterns = [
            r'GPA[:\s]+([0-4]\.[0-9]{1,2})',
            r'([0-4]\.[0-9]{1,2})[/\s]+4\.0',
            r'Grade Point Average[:\s]+([0-4]\.[0-9]{1,2})'
        ]

        for pattern in gpa_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    gpa = float(match.group(1))
                    if 0 <= gpa <= 4.0:
                        return gpa
                except:
                    continue

        return None

# Singleton instance
pdf_parser = PDFParser()