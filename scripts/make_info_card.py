#!/usr/bin/env python3
"""
Build a neofetch-style info card SVG to sit to the RIGHT of the ASCII portrait.
The canvas is 840 x 880 to match abhishek-ascii.svg exactly so both terminal
windows align seamlessly side-by-side in the README table.

Static content hand-authored for Abhishek Thakur:
- Work focus, tech stack, contact, and highlights
- Staggered line-by-line terminal reveal animation
- Terminal color palette blocks and prompt with blinking cursor
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 840, 880
PAD = 40
TITLEBAR_H = 36
KEY_X = PAD
VAL_X = PAD + 160
LINE_H = 34

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
KEY = "#ffa657"      # orange keys
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),
    ("kv", "OS", "Linux x86_64"),
    ("kv", "Work", "Limosys · Front-End Developer"),
    ("kv", "Focus", "React · TypeScript · JavaScript"),
    ("kv", "Home", "Thane, India"),
    ("kv", "Now", "Harrison, New Jersey, USA"),
    ("kv", "Email", "abhishekthakur.art@protonmail.com"),
    ("kv", "Portfolio", "iamabhishekt.github.io"),
    ("gap",),
    ("sec", "Tech Stack"),
    ("kv", "Frontend", "React, Next.js, TypeScript, Tailwind CSS, HTML5/CSS3"),
    ("kv", "Backend", "Java, Node.js, Express, Python, REST APIs"),
    ("kv", "DevOps", "Docker, Kubernetes, Linux, Git, CI/CD Pipelines"),
    ("kv", "Learning", "Rust, C, forward-deployed engineering"),
    ("gap",),
    ("sec", "Highlights"),
    ("bul", "Building interfaces in React and TypeScript at Limosys"),
    ("bul", "Rebuilding tools from scratch: a shell in Rust, Redis in C"),
    ("bul", "Learning in public, casual gamer & chess player"),
    ("gap",),
    ("colors",),
]


def esc(s):
    return html.escape(s)


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>',
    '.f { opacity: 0; animation: fadeIn 0.45s cubic-bezier(0.2, 0.8, 0.2, 1) both; }',
    '@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }',
    '@media (prefers-reduced-motion: reduce) { .f { opacity: 1 !important; transform: none !important; animation: none !important; } }',
    '</style>',
    f'<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*20}" cy="{TITLEBAR_H/2}" r="6" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 5}" fill="{MUTED}" font-size="14" '
             f'text-anchor="middle">abhishek@github: ~$ neofetch</text>')

y = TITLEBAR_H + 46
for i, row in enumerate(ROWS):
    kind = row[0]
    delay = 0.15 + i * 0.05
    if kind == "gap":
        y += LINE_H * 0.45
        continue
    if kind == "host":
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" font-size="24" font-weight="700">'
            f'<tspan fill="{GREEN}">abhishek</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{ACCENT}">github</tspan></text>'
            f'<line x1="{KEY_X}" y1="{y+10:.1f}" x2="{W-PAD}" y2="{y+10:.1f}" stroke="{FRAME}" stroke-width="1.5" stroke-opacity="0.8"/>'
        )
        y += 14
    elif kind == "sec":
        title = esc(row[1])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="19" font-weight="700">'
            f'&#8212; {title} &#8212;</text>'
        )
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="18" font-weight="700">{key}</text>'
            f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="18">{val}</text>'
        )
    elif kind == "bul":
        txt = esc(row[1])
        inner = (
            f'<circle cx="{KEY_X+6}" cy="{y-6:.1f}" r="3.5" fill="{GREEN}"/>'
            f'<text x="{KEY_X+22}" y="{y:.1f}" fill="{INK}" font-size="17.5">{txt}</text>'
        )
    elif kind == "colors":
        palette = ["#2e3440", "#bf616a", "#a3be8c", "#ebcb8b", "#81a1c1", "#b48ead", "#88c0d0", "#e5e9f0"]
        bw = 38
        bh = 20
        bx = KEY_X
        rects = []
        for c in palette:
            rects.append(f'<rect x="{bx}" y="{y-12}" width="{bw}" height="{bh}" rx="3" fill="{c}"/>')
            bx += bw + 8
        inner = "".join(rects)
    else:
        continue

    if STATIC:
        parts.append(f"<g>{inner}</g>")
    else:
        parts.append(f'<g class="f" style="animation-delay:{delay:.2f}s">{inner}</g>')
    y += LINE_H

# bottom status bar matching the ascii terminal
status_line_y = H - 42
status_y = status_line_y + 24
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
status_str = "abhishek@github:~$ "
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{MUTED}" font-size="14">{status_str}</text>')
status_offset = PAD + len(status_str) * 14 * 0.6
parts.append(f'<rect x="{status_offset:.1f}" y="{status_y-13:.1f}" width="9" height="16" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H)
