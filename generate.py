import re
from config import *
from xml.sax.saxutils import escape as _xe, quoteattr as _qa

# Markdown 风格链接：[显示文字](https://完整链接)，可出现在 HANDLE / BIO / ABOUT 等字段
_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

def svg_text_md(x, y, s, attrs, link_fill="#7040a8"):
    """将含 [label](url) 的字符串渲染为 SVG <text>，链接可点击并在新标签页打开。"""
    if s is None or not _MD_LINK.search(s):
        return f'<text x="{x}" y="{y}" {attrs}>{_xe(s or "")}</text>'
    parts = []
    pos = 0
    for m in _MD_LINK.finditer(s):
        if m.start() > pos:
            parts.append(f"<tspan>{_xe(s[pos:m.start()])}</tspan>")
        href = _qa(m.group(2).strip())
        parts.append(
            f"<a href={href} target=\"_blank\" rel=\"noopener noreferrer\">"
            f'<tspan fill="{link_fill}" text-decoration="underline">{_xe(m.group(1))}</tspan></a>'
        )
        pos = m.end()
    if pos < len(s):
        parts.append(f"<tspan>{_xe(s[pos:])}</tspan>")
    return f'<text x="{x}" y="{y}" {attrs}>{"".join(parts)}</text>'

# ── tag theme lookup ──────────────────────────────────────────
THEMES = {
    "purple": {"bg":"#f0e8ff","stroke":"#d4b8f8","text":"#7040b8"},
    "pink":   {"bg":"#fff0f6","stroke":"#f5c0d8","text":"#c04888"},
    "blue":   {"bg":"#eef4ff","stroke":"#b8d0f8","text":"#3060b8"},
    "teal":   {"bg":"#e8faf5","stroke":"#a8e0d0","text":"#207860"},
    "green":  {"bg":"#eef8e8","stroke":"#b0d898","text":"#387020"},
}

# ── pixel shiba rects ─────────────────────────────────────────
def build_shiba_rects():
    gx,gy,ps = 49,38,7
    CR="#F5C87A"; TN="#D8952A"; IE="#D87060"
    WH="#FFF4E8"; EY="#2A1808"; NS="#3A1005"; TG="#D85060"
    rects=[]
    def add(c,r,col):
        rects.append(f'<rect x="{gx+c*ps}" y="{gy+r*ps}" width="{ps}" height="{ps}" fill="{col}"/>')
    for c in [2,3,12,13]: add(c,0,CR)
    for row in [1,2]:
        for c in [1,2,4,11,13,14]: add(c,row,CR)
        add(3,row,IE); add(12,row,IE)
    for c in range(2,14): add(c,3,CR)
    for row in [4,5]:
        for c in range(1,15): add(c,row,CR)
    for row in [6,7]:
        for c in [1,2,5,6,7,8,9,10,13,14]: add(c,row,CR)
        for c in [3,4,11,12]: add(c,row,EY)
    for c in range(1,15): add(c,8,CR)
    for c in [1,2,13,14]: add(c,9,CR)
    for c in range(3,13): add(c,9,WH)
    for c in [1,2,13,14]: add(c,10,CR)
    for c in [3,4,11,12]: add(c,10,WH)
    for c in range(5,11): add(c,10,NS)
    for c in [1,2,13,14]: add(c,11,CR)
    for c in [3,4,5,10,11,12]: add(c,11,WH)
    for c in range(6,10): add(c,11,TG)
    for c in range(2,14): add(c,12,CR)
    for c in range(1,15): add(c,13,CR)
    for row in [14,15]:
        for c in [1,2,13,14]: add(c,row,CR)
        for c in range(3,13): add(c,row,WH)
    for c in [1,2,13,14]: add(c,16,TN)
    for c in [3,4,11,12]: add(c,16,CR)
    for c in [1,2,13,14]: add(c,17,TN)
    return '\n'.join(rects)

# ── tag pills ─────────────────────────────────────────────────
def build_tags():
    out = []
    x = 200
    for tag in TAGS:
        th = THEMES.get(tag["theme"], THEMES["purple"])
        txt = tag["text"]
        w = max(70, len(txt)*8 + 24)
        cx = x + w//2
        out.append(f'<rect x="{x}" y="155" width="{w}" height="24" rx="12" fill="{th["bg"]}" stroke="{th["stroke"]}" stroke-width="1"/>')
        out.append(f'<text x="{cx}" y="171" font-family="sans-serif" font-size="12" font-weight="600" fill="{th["text"]}" text-anchor="middle">{txt}</text>')
        x += w + 10
    return '\n'.join(out)

# ── about me grid ─────────────────────────────────────────────
def build_about():
    out = []
    positions = [(46,252,60,251,268),(422,252,436,251,268),
                 (46,300,60,299,316),(422,300,436,299,316)]
    for i,(item) in enumerate(ABOUT[:4]):
        cx,cy,tx,ty1,ty2 = positions[i]
        dot = item["dot"]
        out.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{dot}"/>')
        out.append(svg_text_md(tx, ty1, item["title"], 'font-family="sans-serif" font-size="14" font-weight="600" fill="#3a2460"', link_fill="#5040a0"))
        out.append(svg_text_md(tx, ty2, item["sub"], 'font-family="sans-serif" font-size="12" fill="#a888cc"', link_fill="#8060c0"))
    return '\n'.join(out)

# ── bio lines ─────────────────────────────────────────────────
def build_bio():
    out = []
    base_y = 390
    for i, line in enumerate(BIO[:3]):
        out.append(
            svg_text_md(
                36,
                base_y + i * 22,
                line,
                'font-family="sans-serif" font-size="13" fill="#5a4070"',
                link_fill="#5040a0",
            )
        )
    return "\n".join(out)

# ── phrase animations ─────────────────────────────────────────
def build_phrases():
    out = []
    for i,ph in enumerate(PHRASES[:5]):
        out.append(f'<text x="200" y="143" class="p{i}">{ph}</text>')
    return '\n'.join(out)

# ── assemble SVG ──────────────────────────────────────────────
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
<defs>
  <linearGradient id="dg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"   stop-color="#e8d4f8" stop-opacity="0"/>
    <stop offset="0.3" stop-color="#e8d4f8"/>
    <stop offset="0.7" stop-color="#e8d4f8"/>
    <stop offset="1"   stop-color="#e8d4f8" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
.eo{{animation:eblink 5s 2s ease-in-out infinite}}
.ec{{opacity:0;animation:eblink-c 5s 2s ease-in-out infinite}}
@keyframes eblink{{0%,85%,100%{{opacity:1}}90%,95%{{opacity:0}}}}
@keyframes eblink-c{{0%,85%,100%{{opacity:0}}90%,95%{{opacity:1}}}}
.tl{{transform-origin:156px 95px;animation:wag 1.3s ease-in-out infinite}}
@keyframes wag{{0%,100%{{transform:rotate(-8deg)}}50%{{transform:rotate(16deg)}}}}
.p0,.p1,.p2,.p3,.p4{{opacity:0}}
.p0{{animation:sp 20s 0s infinite}}
.p1{{animation:sp 20s 4s infinite}}
.p2{{animation:sp 20s 8s infinite}}
.p3{{animation:sp 20s 12s infinite}}
.p4{{animation:sp 20s 16s infinite}}
@keyframes sp{{0%,2%{{opacity:0}}7%{{opacity:1}}17%{{opacity:1}}22%,100%{{opacity:0}}}}
.cur{{animation:cur 0.8s step-end infinite}}
@keyframes cur{{0%,100%{{opacity:1}}50%{{opacity:0}}}}
.sdot{{animation:sd 2.2s ease-in-out infinite}}
@keyframes sd{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
.st1{{animation:tw 2.5s 0s ease-in-out infinite}}
.st2{{animation:tw 2.5s 0.8s ease-in-out infinite}}
.st3{{animation:tw 2.5s 1.6s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:0.25}}50%{{opacity:1}}}}
.sk1{{animation:sk 7s 0s linear infinite}}
.sk2{{animation:sk 8s 2.5s linear infinite}}
.sk3{{animation:sk 6s 4.5s linear infinite}}
.sk4{{animation:sk 9s 1s linear infinite}}
@keyframes sk{{0%{{transform:translate(0,0) rotate(0deg);opacity:0}}8%{{opacity:0.65}}92%{{opacity:0.3}}100%{{transform:translate(-28px,510px) rotate(540deg);opacity:0}}}}
</style>
<rect width="800" height="500" rx="20" fill="#fffaff"/>
<rect width="800" height="500" rx="20" fill="none" stroke="#ead8f5" stroke-width="1.5"/>
<circle cx="762" cy="30" r="3" fill="#e8d0f5"/>
<circle cx="750" cy="42" r="2" fill="#f5c8e0"/>
<circle cx="38"  cy="472" r="2.5" fill="#dcc8f5"/>
<circle cx="52"  cy="484" r="2" fill="#f0d0e8"/>
<ellipse cx="660" cy="-8" rx="7" ry="5" fill="#f8c8d8" class="sk1"/>
<ellipse cx="715" cy="-5" rx="5" ry="7" fill="#f5c0d4" class="sk2"/>
<circle  cx="752" cy="-9" r="5"          fill="#fdd0e4" class="sk3"/>
<ellipse cx="688" cy="-6" rx="6" ry="4" fill="#f8c8d8" class="sk4"/>
<rect x="28" y="28" width="150" height="150" rx="18" fill="#f7effe" stroke="#dfc8f5" stroke-width="1.5"/>
{build_shiba_rects()}
<rect x="83" y="59" width="42" height="9" rx="4" fill="#FFF4E8" opacity="0.45"/>
<g class="eo">
  <rect x="70" y="80" width="14" height="14" rx="2" fill="#2A1808"/>
  <rect x="126" y="80" width="14" height="14" rx="2" fill="#2A1808"/>
  <rect x="72" y="81" width="4" height="4" rx="1" fill="#ffffff" opacity="0.5"/>
  <rect x="128" y="81" width="4" height="4" rx="1" fill="#ffffff" opacity="0.5"/>
</g>
<g class="ec">
  <rect x="70" y="86" width="14" height="5" rx="2" fill="#2A1808"/>
  <rect x="126" y="86" width="14" height="5" rx="2" fill="#2A1808"/>
</g>
<ellipse cx="59"  cy="106" rx="9" ry="6" fill="#F4A0B0" opacity="0.6"/>
<ellipse cx="137" cy="106" rx="9" ry="6" fill="#F4A0B0" opacity="0.6"/>
<g class="tl">
  <circle cx="156" cy="92" r="8" fill="#F5C87A"/>
  <circle cx="160" cy="82" r="7" fill="#F5C87A"/>
  <circle cx="161" cy="73" r="6" fill="#D8952A"/>
</g>
<text x="200" y="58" font-family="sans-serif" font-size="11" fill="#c0a0d8" letter-spacing="4">{SUBTITLE}</text>
<text x="200" y="95" font-family="sans-serif" font-size="30" font-weight="700" fill="#3a2460">{NAME}</text>
{svg_text_md(200, 117, HANDLE, 'font-family="monospace" font-size="12" fill="#9878b8"', link_fill="#7040a8")}
<g font-family="sans-serif" font-size="14" fill="#7040a8">
{build_phrases()}
  <text x="200" y="143" class="cur" fill="#b070e0">|</text>
</g>
{build_tags()}
<line x1="28" y1="200" x2="772" y2="200" stroke="url(#dg)" stroke-width="1"/>
<text x="36" y="224" font-family="sans-serif" font-size="10" fill="#c0a0d8" letter-spacing="3">A B O U T   M E</text>
{build_about()}
<line x1="28" y1="345" x2="772" y2="345" stroke="url(#dg)" stroke-width="1"/>
<text x="36" y="368" font-family="sans-serif" font-size="10" fill="#c0a0d8" letter-spacing="3">I N T R O</text>
{build_bio()}
<line x1="28" y1="455" x2="772" y2="455" stroke="url(#dg)" stroke-width="1"/>
<circle cx="46" cy="477" r="5" fill="#6db85a" class="sdot"/>
<text x="58" y="481" font-family="sans-serif" font-size="11" font-weight="600" fill="#5aa84a">{STATUS_TEXT}</text>
<text x="690" y="483" font-family="sans-serif" font-size="16" fill="#c8b0e8" class="st1">&#x2666;</text>
<text x="712" y="483" font-family="sans-serif" font-size="16" fill="#c8b0e8" class="st2">&#x2666;</text>
<text x="734" y="483" font-family="sans-serif" font-size="16" fill="#c8b0e8" class="st3">&#x2666;</text>
</svg>'''

import xml.etree.ElementTree as ET
try:
    ET.fromstring(svg)
    with open('profile-card.svg','w') as f:
        f.write(svg)
    print("profile-card.svg generated successfully!")
except ET.ParseError as e:
    print(f"XML error: {e}")
