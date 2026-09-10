from pathlib import Path
from html import escape

assets = Path('assets')
BG, PANEL, CYAN, YELLOW, RED, WHITE, MUTED = '#0B0D0D', '#121616', '#5DD6C7', '#F4CF55', '#FF3B30', '#F4F4F2', '#A3AAA7'

def text(x, y, value, size=18, color=WHITE, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'

def svg(name, height, title, description, content):
    body = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" fill="none" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<rect x=".5" y=".5" width="999" height="{height-1}" rx="16" fill="{BG}" stroke="#293130"/>
<g font-family="Arial, Helvetica, sans-serif">{content}</g>
</svg>
'''
    (assets / name).write_text(body, encoding='utf-8')

svg('header.svg', 350, 'Aadit Hire — AI/ML engineer and Formula 1 fan',
    'AI/ML Engineer · Agentic Systems · Motorsport Analytics. Mumbai, India. Python, ML and LLM systems. F1 and Financial ML. Cheering for George Russell. Original circuit artwork.',
    f'''<defs><clipPath id="edge"><rect width="1000" height="350" rx="16"/></clipPath></defs>
<g clip-path="url(#edge)">
<path d="M700 0H1000V350H585Z" fill="{PANEL}"/>
<path d="M930 -20L785 370M958 -20L813 370" stroke="{CYAN}" stroke-opacity=".12" stroke-width="12"/>
<path d="M0 0H1000" stroke="{CYAN}" stroke-width="7"/>
{text(36, 44, 'ENGINEERING / OFF THE GRID', 14, CYAN, 700, 'letter-spacing="2"')}
{text(34, 126, 'AADIT HIRE', 73, WHITE, 800, 'letter-spacing="-3"')}
{text(36, 164, 'AI/ML Engineer · Agentic Systems · Motorsport Analytics', 20, WHITE)}
<rect x="36" y="194" width="149" height="33" rx="16" fill="{CYAN}"/>
{text(110, 216, 'Mumbai, India', 16, BG, 700, 'text-anchor="middle"')}
{text(36, 264, 'Python / ML / LLM Systems', 20, MUTED)}
{text(36, 294, 'F1 + Financial ML', 20, WHITE, 700)}
<path d="M716 238L749 213Q758 206 774 206H884Q924 206 913 231L893 277Q885 295 861 284L820 263H762Q733 263 716 238Z" stroke="#344542" stroke-width="18"/>
<path d="M716 238L749 213Q758 206 774 206H884Q924 206 913 231L893 277Q885 295 861 284L820 263H762Q733 263 716 238Z" stroke="{CYAN}" stroke-width="2"/>
<circle cx="885" cy="206" r="7" fill="{YELLOW}"/>
<path d="M707 231L699 237M712 239L704 245" stroke="{RED}" stroke-width="3"/>
{text(816, 321, 'SUNDAYS: GEORGE RUSSELL', 13, YELLOW, 700, 'text-anchor="middle" letter-spacing="1"')}
</g>''')

svg('project-pitwall.svg', 252, 'F1 Virtual Pitwall V2 — 5.207s MAE',
    'Held-out 5-lap PIT transition MAE 5.207 seconds, down from 6.789 seconds. Validated with 97 offline and 21 live tests. Python, FastAPI, FastF1, Pydantic.',
    f'''<path d="M16 1H984" stroke="{CYAN}" stroke-width="3"/>
{text(32, 35, '01 / RACE STRATEGY', 14, CYAN, 700, 'letter-spacing="1.5"')}
{text(32, 91, 'F1 VIRTUAL', 40, WHITE, 800)}
{text(32, 137, 'PITWALL V2', 40, WHITE, 800)}
{text(32, 174, '97 offline + 21 live tests', 17, MUTED)}
<rect x="611" y="22" width="365" height="168" rx="12" fill="{PANEL}"/>
{text(635, 54, 'HELD-OUT 5-LAP PIT TRANSITION', 13, MUTED, 700)}
{text(635, 116, '5.207s', 59, YELLOW, 800)}
{text(850, 116, 'MAE', 23, YELLOW, 700)}
{text(635, 154, '↓ from 6.789s', 21, WHITE)}
<path d="M32 204H968" stroke="#293130"/>
{text(32, 233, 'Python · FastAPI · FastF1 · Pydantic', 18, CYAN)}''')

svg('project-finpulse.svg', 164, 'FinPulse — financial research',
    'Financial research terminal. Next.js, Python, Supabase, pgvector, MCP.',
    f'''<path d="M1 20V144" stroke="{CYAN}" stroke-width="3"/>
{text(32, 34, '02 / FINANCIAL RESEARCH', 14, CYAN, 700, 'letter-spacing="1.5"')}
{text(32, 89, 'FinPulse', 44, WHITE, 800)}
<rect x="683" y="40" width="285" height="42" rx="21" fill="{PANEL}" stroke="#293130"/>
{text(825, 67, 'EQUITIES + CRYPTO', 17, YELLOW, 700, 'text-anchor="middle"')}
<path d="M32 116H968" stroke="#293130"/>
{text(32, 145, 'Next.js · Python · Supabase · pgvector · MCP', 18, CYAN)}''')

svg('project-goco.svg', 140, 'GOCO AI — programming education',
    'Co-Founder and AI/ML Developer. FastAPI, JavaCC, SQLite, Ollama, Qwen.',
    f'''<path d="M1 20V120" stroke="{YELLOW}" stroke-width="3"/>
{text(32, 31, '03 / PROGRAMMING EDUCATION', 13, YELLOW, 700, 'letter-spacing="1.5"')}
{text(32, 78, 'GOCO AI', 37, WHITE, 800)}
{text(968, 68, 'Co-Founder & AI/ML Developer', 18, MUTED, 400, 'text-anchor="end"')}
<path d="M32 97H968" stroke="#293130"/>
{text(32, 124, 'FastAPI · JavaCC · SQLite · Ollama · Qwen', 18, CYAN)}''')

# Text badges stay local and readable without third-party icon requests.
groups = [
    ('AI / ML', ['Python', 'PyTorch', 'Scikit-learn', 'Hugging Face'], CYAN),
    ('AI Systems', ['RAG', 'MCP', 'Agents', 'Ollama', 'pgvector'], YELLOW),
    ('Backend / Data', ['FastAPI', 'PostgreSQL', 'Supabase', 'Docker'], CYAN),
    ('Web', ['Next.js', 'React', 'Node.js'], YELLOW),
]
content = ''
for i, (label, items, color) in enumerate(groups):
    x, y = 24 + (i % 2) * 484, 24 + (i // 2) * 126
    content += f'<rect x="{x}" y="{y}" width="468" height="112" rx="10" fill="{PANEL}"/>'
    content += text(x+18, y+30, label, 21, color, 700)
    left = x+18
    for item in items:
        width = len(item)*8.2+20
        content += f'<rect x="{left}" y="{y+51}" width="{width}" height="34" rx="7" fill="#202827" stroke="#34413E"/>'
        content += text(left+width/2, y+73, item, 15, WHITE, 400, 'text-anchor="middle"')
        left += width+7
svg('stack.svg', 286, 'Tech I work with', 'AI/ML: Python, PyTorch, Scikit-learn, Hugging Face. AI Systems: RAG, MCP, Agents, Ollama, pgvector. Backend/Data: FastAPI, PostgreSQL, Supabase, Docker. Web: Next.js, React, Node.js.', content)

Path('README.md').write_text('''<!-- HERO -->
<img src="assets/header.svg" width="100%" alt="Aadit Hire — AI/ML Engineer · Agentic Systems · Motorsport Analytics. Mumbai, India. Python, ML and LLM systems. F1 + Financial ML. George Russell fan." />

<!-- ABOUT -->
I'm Aadit, an AI/ML engineer from Mumbai. I like building models that help make useful decisions. Right now, that means race strategy, financial research, and agentic AI. On race weekends, I'm cheering for George Russell.

<!-- PROJECTS -->
## What I'm building

<a href="https://github.com/AaditHire/f1-virtual-pitwall-V2">
  <img src="assets/project-pitwall.svg" width="100%" alt="F1 Virtual Pitwall V2. Held-out 5-lap PIT transition MAE: 5.207s, down from 6.789s. 97 offline + 21 live tests. Python · FastAPI · FastF1 · Pydantic." />
</a>

Replays historical races without leaking future information, then models pit, tyre, and traffic decisions.

[View Pitwall →](https://github.com/AaditHire/f1-virtual-pitwall-V2)

<a href="https://github.com/AaditHire/FinPulse">
  <img src="assets/project-finpulse.svg" width="100%" alt="FinPulse — financial research for equities and crypto. Next.js · Python · Supabase · pgvector · MCP." />
</a>

A financial research terminal bringing portfolio analytics, SEC/news retrieval, RAG, specialist agents, and MCP tools together.

[View FinPulse →](https://github.com/AaditHire/FinPulse)

<img src="assets/project-goco.svg" width="100%" alt="GOCO AI — Co-Founder and AI/ML Developer. FastAPI · JavaCC · SQLite · Ollama · Qwen." />

AI infrastructure for competitive programming and learning, with learner modelling, coding workflows, and contest-safe assistance.

<!-- GOCO_PUBLIC_URL: add a verified public URL when available. -->

<!-- STACK -->
## Tech I work with

<img src="assets/stack.svg" width="100%" alt="AI/ML: Python, PyTorch, Scikit-learn, Hugging Face. AI Systems: RAG, MCP, Agents, Ollama, pgvector. Backend/Data: FastAPI, PostgreSQL, Supabase, Docker. Web: Next.js, React, Node.js." />

<!-- TELEMETRY: Stage 2 replaces these working links with verified GitHub visuals. -->
## On GitHub

[Repositories](https://github.com/AaditHire?tab=repositories) · [Contributions](https://github.com/AaditHire?tab=overview) · [Pitwall commits](https://github.com/AaditHire/f1-virtual-pitwall-V2/commits/main) · [FinPulse commits](https://github.com/AaditHire/FinPulse/commits/main) · [FinPulse workflows](https://github.com/AaditHire/FinPulse/actions)

<!-- DEVELOPMENT LAP: Stage 2 adds the real contribution grid and race-car renderer. -->

<!-- RESEARCH -->
## Currently exploring

Local LLMs, agent evaluation, race-strategy simulation, financial ML, and reinforcement learning.

<!-- CONTACT -->
---

Have something interesting in mind? [Let's talk.](mailto:hire.aadit@gmail.com)

[GitHub](https://github.com/AaditHire) · [LinkedIn](https://linkedin.com/in/aadit-hire) · [Email](mailto:hire.aadit@gmail.com)
''', encoding='utf-8')
