from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def build_analysis_report_pdf(analysis_id, state):
    buffer = BytesIO()

    def clean_text(value):
        text = str(value or "")
        text = (
            text.replace("\u25a0", "-")
            .replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u00a0", " ")
        )
        return " ".join(text.split())

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=colors.HexColor("#111827"),
        spaceAfter=10,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        spaceAfter=10,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.HexColor("#1d4ed8"),
        spaceBefore=10,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.HexColor("#111827"),
        spaceBefore=6,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#111827"),
        spaceAfter=6,
    )
    muted = ParagraphStyle("Muted", parent=body, textColor=colors.HexColor("#6b7280"))

    def p(text, style=body):
        return Paragraph(clean_text(text), style)

    def bullets(items):
        if not isinstance(items, list) or not items:
            return ListFlowable([ListItem(p("No data available.", muted))], bulletType="bullet")
        lis = []
        for item in items[:40]:
            lis.append(ListItem(p(item, body)))
        return ListFlowable(lis, bulletType="bullet", leftIndent=14)

    def kv_dict(d):
        if not isinstance(d, dict) or not d:
            return [p("Not available.", muted)]
        out = []
        for key, val in d.items():
            out.append(p("<b>%s:</b> %s" % (clean_text(key), clean_text(val)), body))
        return out

    results = (state or {}).get("results") or {}
    ats = results.get("ats") or {}
    improvements = results.get("improvements") or {}
    skill_gap = results.get("skill_gap") or {}
    career = results.get("career_paths") or {}
    roadmap = results.get("roadmap") or {}

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
        title="CareerPath ATS Studio Report",
        author="CareerPath ATS Studio",
    )

    story = []
    story.append(p("CareerPath ATS Studio Report", title_style))
    story.append(p("Analysis ID: %s" % analysis_id, meta_style))
    story.append(p("Generated: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"), meta_style))
    story.append(Spacer(1, 8))

    story.append(p("Executive Summary", h1))
    story.append(p("<b>ATS Score:</b> %s/100" % clean_text(ats.get("ats_score", "N/A")), body))
    if ats.get("final_summary"):
        story.append(p(ats.get("final_summary"), body))
    if skill_gap.get("recommendation_level"):
        story.append(p("<b>Readiness:</b> %s" % skill_gap.get("recommendation_level"), body))
    if career.get("final_recommendation"):
        story.append(p("<b>Career Recommendation:</b> %s" % career.get("final_recommendation"), body))
    story.append(Spacer(1, 6))

    story.append(p("ATS Breakdown", h1))
    story.extend(kv_dict(ats.get("breakdown") or {}))
    story.append(Spacer(1, 6))

    story.append(p("Strengths", h1))
    story.append(bullets(ats.get("strengths") or []))
    story.append(Spacer(1, 6))

    story.append(p("Weaknesses", h1))
    story.append(bullets(ats.get("weaknesses") or []))
    story.append(PageBreak())

    story.append(p("Improvements Plan", h1))
    story.append(p("Headline Improvements", h2))
    story.append(bullets(improvements.get("headline_improvements") or []))
    story.append(p("Formatting Improvements", h2))
    story.append(bullets(improvements.get("formatting_improvements") or []))
    story.append(p("Content Improvements", h2))
    story.append(bullets(improvements.get("content_improvements") or []))
    story.append(p("Keyword Optimization", h2))
    story.append(bullets(improvements.get("keyword_optimization") or []))
    story.append(p("Bullet Point Improvements", h2))
    story.append(bullets(improvements.get("bullet_point_improvements") or []))
    story.append(p("Priority Actions", h2))
    story.append(bullets(improvements.get("priority_actions") or []))
    story.append(PageBreak())

    story.append(p("Skill Gap Analysis", h1))
    story.append(p("Missing Skills", h2))
    story.append(bullets(skill_gap.get("missing_skills") or []))
    story.append(p("Critical Gaps", h2))
    story.append(bullets(skill_gap.get("critical_gaps") or []))
    story.append(p("Priority Skills To Learn", h2))
    story.append(bullets(skill_gap.get("priority_skills_to_learn") or []))
    if skill_gap.get("market_alignment"):
        story.append(p("Market Alignment", h2))
        story.append(p(skill_gap.get("market_alignment"), body))
    story.append(PageBreak())

    if isinstance(career, dict) and career.get("top_paths"):
        story.append(p("Career Path Recommendations", h1))
        top_paths = career.get("top_paths") or []
        if isinstance(top_paths, list):
            for idx, path in enumerate(top_paths[:3], start=1):
                if not isinstance(path, dict):
                    continue
                story.append(p("%s. %s" % (idx, path.get("path", "Career Path")), h2))
                story.append(p("Why this fits", body))
                story.append(bullets(path.get("why_fit") or []))
                story.append(p("Missing skills", body))
                story.append(bullets(path.get("missing_skills") or []))
                story.append(p("Projects to build", body))
                story.append(bullets(path.get("projects_to_build") or []))
                story.append(p("Next 4 weeks plan", body))
                story.append(bullets(path.get("next_4_weeks_plan") or []))
        story.append(PageBreak())

    story.append(p("Learning Roadmap", h1))

    def phase_block(title, data):
        story.append(p(title, h2))
        if not isinstance(data, dict) or not data:
            story.append(p("Not available.", muted))
            return
        if data.get("duration"):
            story.append(p("<b>Duration:</b> %s" % data.get("duration"), body))
        if data.get("skills"):
            story.append(p("Skills", body))
            story.append(bullets(data.get("skills")))
        if data.get("tools"):
            story.append(p("Tools", body))
            story.append(bullets(data.get("tools")))
        if data.get("mini_projects"):
            story.append(p("Mini Projects", body))
            story.append(bullets(data.get("mini_projects")))
        if data.get("projects"):
            projects = data.get("projects")
            story.append(p("Projects", body))
            story.append(bullets(projects))
        if data.get("interview_prep_topics"):
            story.append(p("Interview Prep Topics", body))
            story.append(bullets(data.get("interview_prep_topics")))

    phase_block("Phase 1: Fundamentals", roadmap.get("phase_1_fundamentals") or {})
    phase_block("Phase 2: Core Projects", roadmap.get("phase_2_core_projects") or {})
    phase_block("Phase 3: Advanced Internship Prep", roadmap.get("phase_3_advanced_internship_prep") or {})

    if roadmap.get("final_outcome"):
        story.append(p("Final Outcome", h2))
        story.append(p(roadmap.get("final_outcome"), body))
    if roadmap.get("career_readiness_level"):
        story.append(p("Career Readiness Level", h2))
        story.append(p(roadmap.get("career_readiness_level"), body))

    doc.build(story)
    buffer.seek(0)
    return buffer

