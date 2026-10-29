
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
)


NAVY = colors.HexColor("#183153")
BLUE = colors.HexColor("#315D91")
DARK = colors.HexColor("#263445")
MUTED = colors.HexColor("#637083")
LINE = colors.HexColor("#D8E0EA")


def safe_text(text):
    """Escape user text before adding it to ReportLab paragraphs."""
    return escape(str(text))


def split_lines(text):
    """Return non-empty lines from a resume section."""
    return [
        line.strip().lstrip("•●▪- ").strip()
        for line in str(text).splitlines()
        if line.strip()
    ]


def footer(canvas, doc):
    """Add a subtle footer and page number."""
    canvas.saveState()

    width, _ = A4

    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(
        18 * mm,
        14 * mm,
        width - 18 * mm,
        14 * mm,
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        18 * mm, 9 * mm, "PROFESSIONAL RESUME"
    )
    canvas.drawRightString(
        width - 18 * mm,
        9 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def generate_resume_pdf(
    name,
    email,
    phone,
    summary,
    skills,
    experience,
    education,
    projects,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=19 * mm,
        rightMargin=19 * mm,
        topMargin=17 * mm,
        bottomMargin=21 * mm,
        title=f"{name} - Professional Resume",
        author=name,
    )

    base = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        alignment=TA_LEFT,
        textColor=NAVY,
        spaceAfter=5,
    )

    contact_style = ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=MUTED,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=BLUE,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13.5,
        textColor=DARK,
        alignment=TA_LEFT,
        spaceAfter=5,
        splitLongWords=True,
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-9,
        bulletIndent=0,
        spaceAfter=4,
    )

    story = []

    # Name and contact details
    story.append(Paragraph(safe_text(name.strip()), name_style))

    contact_parts = [
        value.strip()
        for value in (email, phone)
        if value and value.strip()
    ]

    if contact_parts:
        story.append(
            Paragraph(
                "  |  ".join(map(safe_text, contact_parts)),
                contact_style,
            )
        )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=NAVY,
            spaceAfter=5,
        )
    )

    # Professional summary
    if summary.strip():
        story.append(
            Paragraph("PROFESSIONAL SUMMARY", heading_style)
        )

        story.append(
            Paragraph(
                safe_text(summary.strip()),
                body_style,
            )
        )

    # Skills
    if skills.strip():
        story.append(
            Paragraph("KEY SKILLS", heading_style)
        )

        for line in split_lines(skills):
            story.append(
                Paragraph(
                    "• " + safe_text(line),
                    bullet_style,
                )
            )

    # Experience
    if experience.strip():
        story.append(
            Paragraph("EXPERIENCE", heading_style)
        )

        for line in split_lines(experience):
            story.append(
                Paragraph(
                    "• " + safe_text(line),
                    bullet_style,
                )
            )

    # Education
    if education.strip():
        story.append(
            Paragraph("EDUCATION", heading_style)
        )

        for line in split_lines(education):
            story.append(
                Paragraph(
                    "• " + safe_text(line),
                    bullet_style,
                )
            )

    # Projects
    if projects.strip():
        story.append(
            Paragraph("PROJECTS", heading_style)
        )

        for line in split_lines(projects):
            story.append(
                Paragraph(
                    "• " + safe_text(line),
                    bullet_style,
                )
            )

    doc.build(
        story,
        onFirstPage=footer,
        onLaterPages=footer,
    )

    buffer.seek(0)
    return buffer.getvalue()
