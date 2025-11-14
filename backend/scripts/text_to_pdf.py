"""
Convert text resume to PDF
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
import sys
from pathlib import Path

def text_to_pdf(text_file, pdf_file):
    """
    Convert text file to PDF
    """
    # Read text file
    with open(text_file, 'r') as f:
        lines = f.readlines()

    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2c3e50')
    )

    # Process lines
    for i, line in enumerate(lines):
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 6))
            continue

        # First line is the name (header)
        if i == 0:
            p = Paragraph(line, header_style)
        # Lines in all caps are section headers
        elif line.isupper() and len(line) < 50:
            elements.append(Spacer(1, 12))
            p = Paragraph(line, section_style)
        # Bullet points
        elif line.startswith('•'):
            p = Paragraph(line, normal_style)
        # Regular text
        else:
            p = Paragraph(line, normal_style)

        elements.append(p)

    # Build PDF
    doc.build(elements)
    print(f"✅ PDF created: {pdf_file}")

if __name__ == "__main__":
    # Convert sample resume
    text_file = Path(__file__).parent.parent / "test_data" / "sample_resume.txt"
    pdf_file = Path(__file__).parent.parent / "test_data" / "sample_resume.pdf"

    text_to_pdf(str(text_file), str(pdf_file))