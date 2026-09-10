from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "Aadit_Hire_Resume.pdf"


def register_fonts() -> dict[str, str]:
    font_dir = Path(r"C:\Windows\Fonts")
    candidates = {
        "serif": font_dir / "cambria.ttc",
        "serif_bold": font_dir / "cambriab.ttf",
        "serif_italic": font_dir / "cambriai.ttf",
        "serif_bold_italic": font_dir / "cambriaz.ttf",
    }
    names = {
        "serif": "ResumeCambria",
        "serif_bold": "ResumeCambria-Bold",
        "serif_italic": "ResumeCambria-Italic",
        "serif_bold_italic": "ResumeCambria-BoldItalic",
    }
    if all(path.exists() for path in candidates.values()):
        for key, path in candidates.items():
            pdfmetrics.registerFont(TTFont(names[key], str(path)))
        pdfmetrics.registerFontFamily(
            "ResumeCambria",
            normal=names["serif"],
            bold=names["serif_bold"],
            italic=names["serif_italic"],
            boldItalic=names["serif_bold_italic"],
        )
        return names
    return {
        "serif": "Times-Roman",
        "serif_bold": "Times-Bold",
        "serif_italic": "Times-Italic",
        "serif_bold_italic": "Times-BoldItalic",
    }


FONTS = register_fonts()
styles = getSampleStyleSheet()

name_style = ParagraphStyle(
    "Name",
    parent=styles["Normal"],
    fontName=FONTS["serif_bold"],
    fontSize=20.6,
    leading=21.8,
    alignment=TA_CENTER,
    spaceAfter=2,
    textColor=colors.black,
)
contact_style = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName=FONTS["serif"],
    fontSize=9.3,
    leading=11.6,
    alignment=TA_CENTER,
    textColor=colors.black,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName=FONTS["serif_bold"],
    fontSize=10.1,
    leading=11.6,
    spaceBefore=9.5,
    spaceAfter=0,
    textColor=colors.black,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName=FONTS["serif"],
    fontSize=9.3,
    leading=12.2,
    alignment=TA_LEFT,
    textColor=colors.black,
)
body_italic = ParagraphStyle(
    "BodyItalic",
    parent=body_style,
    fontName=FONTS["serif_italic"],
)
right_italic = ParagraphStyle(
    "RightItalic",
    parent=body_style,
    fontName=FONTS["serif_italic"],
    alignment=TA_RIGHT,
)
entry_style = ParagraphStyle(
    "Entry",
    parent=body_style,
    fontName=FONTS["serif_bold"],
    fontSize=10.1,
    leading=12.2,
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=17,
    firstLineIndent=-8,
    rightIndent=1,
    bulletIndent=4,
    spaceBefore=0,
    spaceAfter=3.0,
)
project_bullet_style = ParagraphStyle(
    "ProjectBullet",
    parent=bullet_style,
    fontSize=9.25,
    leading=11.8,
    spaceAfter=1.5,
)


def section(title: str) -> Table:
    table = Table([[Paragraph(title, section_style)]], colWidths=[7.31 * inch])
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5.2),
                ("LINEBELOW", (0, 0), (-1, -1), 0.7, colors.black),
            ]
        )
    )
    table.spaceAfter = 3.6
    return table


def two_col(left: str, right: str, left_style=entry_style, right_style=right_italic) -> Table:
    table = Table(
        [[Paragraph(left, left_style), Paragraph(right, right_style)]],
        colWidths=[5.78 * inch, 1.53 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def project_header(
    title: str,
    tech: str,
    url: str,
    date: str,
    live_url: str | None = None,
) -> Table:
    links = []
    if live_url:
        links.append(f'<link href="{live_url}" color="black"><u>[live]</u></link>')
    links.append(f'<link href="{url}" color="black"><u>[code]</u></link>')
    link = " ".join(links)
    left = Paragraph(f"<b>{title}</b> | {tech}", entry_style)
    middle = Paragraph(link, ParagraphStyle("CodeLink", parent=body_style, alignment=TA_CENTER))
    right = Paragraph(date, right_italic)
    table = Table([[left, middle, right]], colWidths=[5.00 * inch, 0.91 * inch, 1.40 * inch])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def bullets(items: list[str], style=bullet_style) -> list[Paragraph]:
    return [Paragraph(f"• {item}", style) for item in items]


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Aadit Hire Resume")
    canvas.setAuthor("Aadit Hire")
    canvas.setSubject("Resume of Aadit Hire")
    canvas.restoreState()


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=0.50 * inch,
        rightMargin=0.46 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.30 * inch,
        title="Aadit Hire Resume",
        author="Aadit Hire",
        subject="Resume of Aadit Hire",
    )

    story = [
        Paragraph("Aadit Hire", name_style),
        Paragraph(
            '+91 9820097187&nbsp;&nbsp;|&nbsp;&nbsp;hire.aadit@gmail.com&nbsp;&nbsp;|&nbsp;&nbsp;'
            '<link href="https://www.linkedin.com/in/aadit-hire-24a343320/" color="black"><u>linkedin/aadit-hire</u></link>'
            '&nbsp;&nbsp;|&nbsp;&nbsp;'
            '<link href="https://github.com/AaditHire" color="black"><u>github/AaditHire</u></link>'
            '&nbsp;&nbsp;|&nbsp;&nbsp;Mumbai, India',
            contact_style,
        ),
        Spacer(1, 2),
        section("EDUCATION"),
        two_col(
            "SVKM's Dwarkadas J. Sanghvi College of Engineering - CGPA: 7.10",
            "2022 - 2026",
        ),
        two_col(
            "Bachelor of Technology (B. Tech) in Computer Engineering",
            "Mumbai, India",
            body_style,
            right_italic,
        ),
        Paragraph(
            "<i>Relevant Coursework:</i> Artificial Intelligence, Machine Learning, Deep Learning",
            body_style,
        ),
        section("TECHNICAL SKILLS"),
        Paragraph("<b>Languages:</b> Python, SQL", body_style),
        Paragraph(
            "<b>AI and ML:</b> Scikit-learn, PyTorch, TensorFlow, Hugging Face, LLMs, RAG, Reinforcement Learning, Feature Engineering",
            body_style,
        ),
        Paragraph(
            "<b>Frameworks and Libraries:</b> FastAPI, Next.js, React.js, Node.js, Express.js, Pandas, NumPy, Pydantic",
            body_style,
        ),
        Paragraph(
            "<b>Data and Tools:</b> PostgreSQL, Supabase, pgvector, SQLite, Snowflake, Git/GitHub, Docker, GitHub Actions, MCP",
            body_style,
        ),
        section("EXPERIENCE"),
        KeepTogether(
            [
                two_col("GOCO - Co-Founder and AI/ML Developer", "Aug 2025 - Present"),
                *bullets(
                    [
                        "<b>Led a cross-functional team of five interns</b>, including three software engineering interns, through a <b>three-month product expansion cycle</b>; reviewed architectures and validated GitHub pull requests.",
                        "Architected a <b>hierarchical 1-vs-1 matchmaking backend</b> with Node.js, Sequelize, and PostgreSQL on Supabase, expanding city to region to global over approximately 90 seconds before bot fallback.",
                        "Validated matchmaking with <b>approximately 30 concurrent students without failures</b>; guided a competitive-programming interface with JSON test-case validation.",
                        "Built <b>GOCO AI from scratch</b> as a provider-independent FastAPI platform with JavaCC compiler integration, SQLite learner evidence, mastery tracking, and deterministic recommendations.",
                        "Engineered <b>contest-safe mode routing and durable battleground snapshots</b> with idempotent event handling, bounded timelines, and grounded post-match response guardrails.",
                        "Developed <b>Ollama/Qwen interview workflows</b> with microphone capture; directed three-tier course access with question-level locking and optimized website SEO.",
                    ]
                ),
            ]
        ),
        Spacer(1, 6.0),
        KeepTogether(
            [
                two_col("Rogue Code - Web Developer Intern", "Jun 2024 - Aug 2024"),
                *bullets(
                    [
                        "Implemented <b>website SEO improvements</b> to strengthen crawlability, indexing, and page discoverability.",
                        "Integrated web pages with a <b>Supabase database</b> for structured application data storage and retrieval.",
                        "Built and tested <b>database-backed CRUD workflows</b> for reliable record retrieval and updates.",
                        "Implemented an <b>Excel data export</b> feature through the xlsx library, <b>reducing manual reporting by 80%</b>.",
                    ]
                ),
            ]
        ),
        section("PROJECTS"),
        KeepTogether(
            [
                project_header(
                    "FinPulse",
                    "Next.js, Python, Supabase, Groq, MCP",
                    "https://github.com/AaditHire/FinPulse",
                    "Jan 2026 - Present",
                    "https://web-sand-pi-45.vercel.app/",
                ),
                *bullets(
                    [
                        "Built an <b>owner-only financial research terminal</b> for live portfolio monitoring across equities and crypto;<br/>integrated macro data, SEC filings, financial news, and authenticated workspaces in one Next.js interface.",
                        "Created live valuations, selectable <b>30-day asset charts</b>, alerts, data-health reporting, and authenticated owner access.",
                        "Implemented <b>hybrid full-text and pgvector RAG</b> for SEC filings and owner-uploaded research documents;<br/>orchestrated specialist agents with cited Groq synthesis, quota controls, and evidence-only fallbacks.",
                        "Built a scoped <b>Streamable HTTP MCP endpoint</b> with hashed tokens for market, research, and portfolio tools;<br/>kept approval-gated alerts separate from read-only operations and excluded brokerage actions.",
                        "Automated portfolio-aware news ranking, semantic deduplication, and scheduled delivery through <b>GitHub Actions</b>;<br/>sent responsive Gmail digests with configurable timing and retry-safe delivery history.",
                    ],
                    project_bullet_style,
                ),
            ]
        ),
        Spacer(1, 6.0),
        KeepTogether(
            [
                project_header(
                    "F1 Virtual Pitwall V2",
                    "Python, FastAPI, FastF1, Pydantic",
                    "https://github.com/AaditHire/f1-virtual-pitwall-V2",
                    "Jul 2026 - Present",
                ),
                *bullets(
                    [
                        "Built a <b>FastAPI F1 data hub</b> with normalized Jolpica, OpenF1, FastF1, and RSS provider adapters;<br/>served seasons, sessions, grids, results, standings, news, and timezone-aware APIs from one backend.",
                        "Created <b>timestamped full-grid historical replay</b> using only facts available at each leader-lap cutoff;<br/>preserved temporal integrity through cached race archives, normalized identities, and explicit timing gaps.",
                        "Developed <b>leakage-controlled tyre, pit-loss, traffic, undercut, and overcut analysis</b> with explicit uncertainty.",
                        "Engineered <b>short-horizon pit strategy and pit-cycle models</b> using chronological priors and causal features;<br/>modeled traffic, tyre state, pit obligations, and conservative uncertainty before surfacing decisions.",
                        "Reduced held-out five-lap PIT transition MAE from <b>6.789s to 5.207s</b>; verified with <b>97 offline and 21 live tests</b>.",
                    ],
                    project_bullet_style,
                ),
            ]
        ),
        section("CERTIFICATIONS AND ACHIEVEMENTS"),
        Paragraph(
            "• Professional Certification in <b>Applied Data Science, Artificial Intelligence, Deep Learning and Generative AI</b>",
            bullet_style,
        ),
        Paragraph(
            "• <b>Copyright Holder</b> of GOCO Programming Language and IDE - GOCO APP - 2025",
            bullet_style,
        ),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(OUTPUT)


if __name__ == "__main__":
    build()
