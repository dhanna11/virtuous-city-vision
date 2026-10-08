#!/usr/bin/env python3
"""Identity mock-ups for the Virtuous City Vision: three light directions x (cover, architecture, timeline)."""
import math
from pathlib import Path

OUT = Path(__file__).with_name("identity-mockups.html")

AR_TITLE = "إنهاء حرب غزة يجب أن يعيد إلينا إنسانيتنا"
HE_TITLE = "סיום המלחמה בעזה חייב להשיב לנו את אנושיותנו"
AR_CITY, HE_CITY = "المدينة الفاضلة", "העיר המעולה"
AR_SAADA, HE_SAADA = "السعادة", "האושר"
AR_WISDOM, HE_WISDOM = "بيت الحكمة", "בית החכמה"

BLOCKS = [  # (name, short)
    ("Coalition core", "The Board of Peace incubates the Coalition for Canaan · the Virtuous City Convention · three sets of guarantees"),
    ("Coalition continuity", "0–2 years incubation · 0–10 coalition of the willing · 10–20 alliance model · 20–30 voluntary confederation"),
    ("Security & stabilization", "Demilitarization and DDR · the ISF · West Bank joint patrols"),
    ("Arab partners & trust funds", "Egypt as security anchor · a Reconstruction Custodian · the Virtuous City Trust Fund"),
    ("Governance & economy", "The Virtuous City Council · the Economic Plan · the Palestinian Labor Movement"),
    ("Education & reconciliation", "The House of Wisdom and Peace · the Multiple Truths framework"),
]
PHASES = [  # (start, end, name, sub, milestones)
    (0, 2, "Board of Peace incubation", "", ["Conclude the war via the Virtuous City Convention", "Deploy the ISF", "Activate NCAG governance", "Formalize the Coalition for Canaan"]),
    (0, 10, "Coalition of the willing", "stabilization", ["Full-scale demilitarization and rebuild", "PA reforms toward statehood", "Complete IDF disengagement from Gaza"]),
    (10, 20, "Alliance model", "integration", ["Support for state recognition", "Abraham Accords expansion", "Initial West Bank disengagement"]),
    (20, 30, "Voluntary confederation", "full maturity", ["Full mutual recognition", "Full freedom of movement", "Final borders and withdrawal"]),
]

def wedge(cx, cy, r0, r1, a0, a1):
    p = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    x0, y0 = p(r1, a0); x1, y1 = p(r1, a1); x2, y2 = p(r0, a1); x3, y3 = p(r0, a0)
    return f"M{x0:.1f},{y0:.1f} A{r1},{r1} 0 0 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 0 0 {x3:.1f},{y3:.1f} Z"

def star8(cx, cy, r, ri):
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5 - 90); rr = r if i % 2 == 0 else ri
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return " ".join(pts)

def girih_band(w, y, h, color, fill="none"):
    """a band of eight-pointed stars and the crosses between them"""
    n = int(w // h); s = w / n; out = []
    for i in range(n):
        cx = s * i + s / 2
        out.append(f'<polygon points="{star8(cx, y + h / 2, h * .46, h * .3)}" fill="{fill}" stroke="{color}" stroke-width="2"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{y + h / 2:.1f}" r="{h * .1:.1f}" fill="{color}"/>')
        if i: out.append(f'<path d="M{s * i:.1f},{y + h * .2:.1f} L{s * i:.1f},{y + h * .8:.1f}" stroke="{color}" stroke-width="1.5"/>')
    return "".join(out)

def slide(inner, bg, extra_style=""):
    return f'<section class="s" style="background:{bg};{extra_style}">{inner}</section>'

# ================================================================ A · Manuscript of the House of Wisdom
A = dict(paper="#f3ead6", ink="#2a2118", lapis="#1f3d73", terra="#a3442a", gold="#a8823a", rule="#c9b48a",
         serif="'EB Garamond', Georgia, serif", ar="'Amiri', serif", he="'Frank Ruhl Libre', serif", label="'EB Garamond', Georgia, serif")

def a_frame(inner, folio):
    c = A
    band = f'<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px" aria-hidden="true">' \
           f'<rect x="56" y="48" width="1808" height="984" fill="none" stroke="{c["gold"]}" stroke-width="3"/>' \
           f'<rect x="68" y="60" width="1784" height="960" fill="none" stroke="{c["rule"]}" stroke-width="1.5"/>' \
           f'<g transform="translate(68 0)">{girih_band(1784, 60, 34, c["gold"])}</g></svg>'
    foot = (f'<p style="position:absolute;left:128px;bottom:76px;font:600 22px/1 {c["label"]};letter-spacing:4px;color:{c["terra"]};text-transform:uppercase">{folio}</p>'
            f'<p style="position:absolute;right:128px;bottom:76px;font:600 22px/1 {c["label"]};letter-spacing:4px;color:{c["gold"]}">X.COM/THEKINGDAVIDJR</p>')
    return slide(band + inner + foot, c["paper"])

def a_cover():
    c = A
    return a_frame(f'''
<div style="position:absolute;left:0;right:0;top:150px;text-align:center">
  <p style="font:400 64px/1.3 {c['ar']};color:{c['lapis']}" dir="rtl" lang="ar">{AR_CITY}</p>
  <p style="font:500 26px/1 {c['label']};letter-spacing:10px;color:{c['terra']};margin-top:6px">THE VIRTUOUS CITY VISION</p>
  <p style="font:400 54px/1.3 {c['he']};color:{c['lapis']};margin-top:10px" dir="rtl" lang="he">{HE_CITY}</p>
  <svg viewBox="0 0 400 40" style="width:400px;height:40px;margin:24px auto 8px;display:block"><line x1="0" y1="20" x2="170" y2="20" stroke="{c['gold']}" stroke-width="2"/><polygon points="{star8(200, 20, 16, 9)}" fill="{c['terra']}"/><line x1="230" y1="20" x2="400" y2="20" stroke="{c['gold']}" stroke-width="2"/></svg>
  <h1 style="font:500 108px/1.04 {c['serif']};color:{c['ink']};max-width:1500px;margin:0 auto">Ending the Gaza War Must Restore Our Humanity</h1>
  <p style="font:400 36px/1.4 {c['ar']};color:{c['ink']};opacity:.75;margin-top:26px" dir="rtl" lang="ar">{AR_TITLE}</p>
  <p style="font:400 32px/1.4 {c['he']};color:{c['ink']};opacity:.75" dir="rtl" lang="he">{HE_TITLE}</p>
  <p style="font:italic 400 34px/1 {c['serif']};color:{c['terra']};margin-top:34px">David Hanna Jr. · a private author’s proposal · October 2026</p>
</div>''', "Cover")

def a_arch():
    c = A; cx, cy = 520, 560; out = []
    cols = [c["lapis"], c["terra"], c["gold"], c["lapis"], c["terra"], c["gold"]]
    for i, (name, _) in enumerate(BLOCKS):
        a0, a1 = -90 + i * 60 + 2, -90 + (i + 1) * 60 - 2
        out.append(f'<path d="{wedge(cx, cy, 170, 390, a0, a1)}" fill="{cols[i]}" fill-opacity=".12" stroke="{cols[i]}" stroke-width="2.5"/>')
        am = math.radians((a0 + a1) / 2); tx, ty = cx + 280 * math.cos(am), cy + 280 * math.sin(am)
        words = name.split(" "); half = (len(words) + 1) // 2
        lines = [" ".join(words[:half]), " ".join(words[half:])] if len(words) > 1 else [name]
        out.append(f'<text x="{tx:.0f}" y="{ty - (len(lines) - 1) * 17:.0f}" text-anchor="middle" font-family="EB Garamond" font-size="30" font-weight="600" fill="{c["ink"]}">' +
                   "".join(f'<tspan x="{tx:.0f}" dy="{0 if k == 0 else 34}">{l}</tspan>' for k, l in enumerate(lines)) + '</text>')
        nx, ny = cx + 420 * math.cos(am), cy + 420 * math.sin(am)
        out.append(f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="20" fill="{c["paper"]}" stroke="{cols[i]}" stroke-width="2"/><text x="{nx:.0f}" y="{ny + 8:.0f}" text-anchor="middle" font-family="EB Garamond" font-size="24" font-weight="700" fill="{cols[i]}">{i + 1}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="{c["paper"]}" stroke="{c["gold"]}" stroke-width="3"/>')
    out.append(f'<polygon points="{star8(cx, cy, 140, 104)}" fill="none" stroke="{c["gold"]}" stroke-width="1.5"/>')
    out.append(f'<text x="{cx}" y="{cy - 34}" text-anchor="middle" font-family="Amiri" font-size="48" fill="{c["lapis"]}">{AR_SAADA}</text>')
    out.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-family="EB Garamond" font-size="34" font-weight="600" fill="{c["ink"]}">The telos</text>')
    out.append(f'<text x="{cx}" y="{cy + 58}" text-anchor="middle" font-family="Frank Ruhl Libre" font-size="36" fill="{c["lapis"]}">{HE_SAADA}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="440" fill="none" stroke="{c["rule"]}" stroke-width="1.5" stroke-dasharray="4 8"/>')
    legend = "".join(f'<div style="display:flex;gap:18px;align-items:baseline;border-top:1px solid {c["rule"]};padding:12px 0">'
                     f'<span style="font:700 28px/1 {c["serif"]};color:{cols[i]};width:30px">{i + 1}</span><div><p style="font:600 30px/1.1 {c["serif"]};color:{c["ink"]}">{n}</p>'
                     f'<p style="font:400 23px/1.3 {c["serif"]};color:{c["ink"]};opacity:.78;margin-top:4px">{s}</p></div></div>' for i, (n, s) in enumerate(BLOCKS))
    return a_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{"".join(out)}</svg>
<div style="position:absolute;left:1010px;top:130px;width:790px">
  <p style="font:600 24px/1 {c['label']};letter-spacing:6px;color:{c['terra']}">THE ARCHITECTURE</p>
  <h2 style="font:500 60px/1.05 {c['serif']};color:{c['ink']};margin:12px 0 10px">Six organs of one healthy body</h2>
  <p style="font:italic 400 26px/1.3 {c['serif']};color:{c['lapis']};margin-bottom:14px">“each part of society functioning harmoniously, like organs in a healthy body”: Al-Farabi</p>
  {legend}
</div>''', "The core thesis")

def gantt(c, x0, y0, w, rowh, font, labfont, colors, bar_style="rect", grid=True, numfont=None):
    """years 0..30 across w; one row per phase"""
    numfont = numfont or labfont; k = w / 30; out = []
    for yr in range(0, 31, 5):
        x = x0 + yr * k
        if grid: out.append(f'<line x1="{x:.0f}" y1="{y0 - 20}" x2="{x:.0f}" y2="{y0 + rowh * 4}" stroke="{c["rule"]}" stroke-width="1" stroke-dasharray="{"" if yr % 10 == 0 else "3 6"}"/>')
        out.append(f'<text x="{x:.0f}" y="{y0 - 34}" text-anchor="middle" font-family="{numfont}" font-size="24" fill="{c["ink"]}" opacity=".7">{"year " if yr == 0 else ""}{yr}</text>')
    for i, (s, e, name, sub, ms) in enumerate(PHASES):
        y = y0 + i * rowh + 10; x = x0 + s * k; bw = (e - s) * k; col = colors[i]; bh = 46
        if bar_style == "stone":
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="{bh}" rx="3" fill="{col}" fill-opacity=".9"/>')
            for j in range(1, int(bw // 120) + 1):
                out.append(f'<line x1="{x + j * 120:.0f}" y1="{y}" x2="{x + j * 120:.0f}" y2="{y + bh}" stroke="{c["paper"]}" stroke-opacity=".5" stroke-width="2"/>')
        elif bar_style == "line":
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="{bh}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2.5"/>')
            out.append(f'<polygon points="{x + bw:.0f},{y - 8} {x + bw + 10:.0f},{y + bh / 2:.0f} {x + bw:.0f},{y + bh + 8}" fill="{col}"/>')
        else:
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="{bh}" rx="23" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="2.5"/>')
        label = name + (f" · {sub}" if sub else "")
        right = s >= 15
        tx, anchor = (x + bw - 18, "end") if right else ((x + 18, "start") if bw > 400 else (x + bw + 22, "start"))
        out.append(f'<text x="{tx:.0f}" y="{y + 32}" text-anchor="{anchor}" font-family="{labfont}" font-size="27" font-weight="600" fill="{c["paper"] if bar_style == "stone" and bw > 400 else c["ink"]}">{label}</text>')
        mx = x + bw if right else (x + 18 if bw > 400 else x + bw + 22)
        out.append(f'<text x="{mx:.0f}" y="{y + bh + 34}" text-anchor="{anchor}" font-family="{font}" font-size="23" fill="{c["ink"]}" opacity=".8">{" · ".join(ms)}</text>')
    # the incubation sits inside the first decade: a bracket says so
    return "".join(out)

def a_time():
    c = A
    g = gantt(c, 150, 380, 1620, 140, "EB Garamond", "EB Garamond", [c["terra"], c["lapis"], c["gold"], c["lapis"]])
    return a_frame(f'''
<div style="position:absolute;left:128px;top:130px;width:1660px">
  <p style="font:600 24px/1 {c['label']};letter-spacing:6px;color:{c['terra']}">3 · COALITION CONTINUITY</p>
  <h2 style="font:500 66px/1.05 {c['serif']};color:{c['ink']};margin-top:12px">Roughly 30 years: an incubation and three phases</h2>
  <p style="font:italic 400 28px/1.3 {c['serif']};color:{c['lapis']};margin-top:10px">Nobody disarms without a future. Each phase after the incubation is an optional expanded mandate.</p>
</div>
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{g}</svg>''', "Coalition continuity")

# ================================================================ B · Jerusalem stone and olive
B = dict(paper="#ebe3d3", stone="#ded3bd", ink="#2b2a24", olive="#5d6b2e", sea="#22677f", red="#8c2f2a", rule="#c8bba0",
         serif="'Lora', Georgia, serif", head="'Marcellus', Georgia, serif", ar="'Reem Kufi', sans-serif", he="'David Libre', serif")

def arch_path(x, y, w, h):
    r = w / 2
    return f"M{x},{y + h} L{x},{y + r} A{r},{r} 0 0 1 {x + w},{y + r} L{x + w},{y + h} Z"

def b_frame(inner, foot):
    c = B
    tex = (f'background:{c["paper"]};background-image:'
           f'linear-gradient(0deg, rgba(0,0,0,.035) 1px, transparent 1px),linear-gradient(90deg, rgba(0,0,0,.025) 1px, transparent 1px);'
           f'background-size:240px 80px, 480px 80px')
    f = (f'<p style="position:absolute;left:128px;bottom:64px;font:400 22px/1 {c["head"]};letter-spacing:4px;color:{c["olive"]};text-transform:uppercase">{foot}</p>'
         f'<p style="position:absolute;right:128px;bottom:64px;font:400 22px/1 {c["head"]};letter-spacing:4px;color:{c["sea"]}">X.COM/THEKINGDAVIDJR</p>')
    return slide(inner + f, c["paper"], tex)

def olive_sprig(x, y, s, col):
    leaves = "".join(f'<ellipse cx="{x + i * 26 * s:.0f}" cy="{y + (-14 if i % 2 else 14) * s:.0f}" rx="{20 * s:.0f}" ry="{7 * s:.0f}" transform="rotate({-30 if i % 2 else 30} {x + i * 26 * s:.0f} {y + (-14 if i % 2 else 14) * s:.0f})" fill="{col}"/>' for i in range(1, 8))
    return f'<path d="M{x},{y} L{x + 210 * s:.0f},{y}" stroke="{col}" stroke-width="{3 * s:.1f}"/>{leaves}'

def b_cover():
    c = B
    return b_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px" aria-hidden="true">
  <path d="{arch_path(360, 90, 1200, 900)}" fill="{c['stone']}" stroke="{c['olive']}" stroke-width="4"/>
  <path d="{arch_path(384, 114, 1152, 876)}" fill="none" stroke="{c['rule']}" stroke-width="2"/>
  <g transform="translate(-20 0)">{olive_sprig(745, 955, 1, c['olive'])}</g><g transform="translate(1945 0) scale(-1 1)">{olive_sprig(745, 955, 1, c['olive'])}</g>
</svg>
<div style="position:absolute;left:460px;width:1000px;top:250px;text-align:center">
  <p style="font:400 54px/1.2 {c['ar']};color:{c['sea']}" dir="rtl" lang="ar">{AR_CITY}</p>
  <p style="font:400 26px/1 {c['head']};letter-spacing:12px;color:{c['red']};margin:16px 0">THE VIRTUOUS CITY VISION</p>
  <p style="font:700 46px/1.2 {c['he']};color:{c['sea']}" dir="rtl" lang="he">{HE_CITY}</p>
  <h1 style="font:400 84px/1.08 {c['head']};color:{c['ink']};margin-top:34px">Ending the Gaza War Must Restore Our Humanity</h1>
  <p style="font:400 30px/1.5 'Noto Naskh Arabic', serif;color:{c['ink']};opacity:.75;margin-top:24px" dir="rtl" lang="ar">{AR_TITLE}</p>
  <p style="font:400 30px/1.3 {c['he']};color:{c['ink']};opacity:.7" dir="rtl" lang="he">{HE_TITLE}</p>
  <p style="font:italic 400 30px/1 {c['serif']};color:{c['olive']};margin-top:30px">David Hanna Jr. · October 2026</p>
</div>''', "")

def b_arch():
    c = B; out = []; w, h, gap, x0, y0 = 250, 440, 22, 128, 380
    cols = [c["olive"], c["sea"], c["red"], c["olive"], c["sea"], c["red"]]
    for i, (name, short) in enumerate(BLOCKS):
        x = x0 + i * (w + gap)
        out.append(f'<path d="{arch_path(x, y0, w, h)}" fill="{c["stone"]}" stroke="{cols[i]}" stroke-width="3"/>')
        out.append(f'<text x="{x + w / 2}" y="{y0 + 92}" text-anchor="middle" font-family="Marcellus" font-size="44" fill="{cols[i]}">{i + 1}</text>')
    lintel = f'<rect x="{x0 - 10}" y="{y0 + h}" width="{6 * w + 5 * gap + 20}" height="26" fill="{c["olive"]}"/>'
    keystone = f'<rect x="{x0 - 10}" y="{y0 - 120}" width="{6 * w + 5 * gap + 20}" height="70" fill="{c["sea"]}" fill-opacity=".1" stroke="{c["sea"]}" stroke-width="2"/>'
    texts = "".join(f'<div style="position:absolute;left:{x0 + i * (w + gap) + 18}px;top:{y0 + 130}px;width:{w - 36}px;text-align:center">'
                    f'<p style="font:400 27px/1.15 {c["head"]};color:{c["ink"]}">{n}</p><p style="font:400 20px/1.3 {c["serif"]};color:{c["ink"]};opacity:.8;margin-top:12px">{s}</p></div>'
                    for i, (n, s) in enumerate(BLOCKS))
    return b_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{keystone}{"".join(out)}{lintel}</svg>
<div style="position:absolute;left:128px;top:96px;width:1660px">
  <p style="font:400 24px/1 {c['head']};letter-spacing:6px;color:{c['red']}">THE ARCHITECTURE</p>
  <h2 style="font:400 60px/1.1 {c['head']};color:{c['ink']};margin-top:10px">Six arches, one structure</h2>
</div>
<p style="position:absolute;left:128px;width:1664px;top:{y0 - 104}px;text-align:center;font:400 28px/1.3 {c['serif']};color:{c['sea']}">The Board of Peace incubates the Coalition for Canaan: the keystone that holds the arcade</p>
{texts}''', "The core thesis")

def b_time():
    c = B; out = []; x0, w = 560, 1230; k = w / 30
    for i, (s_, e, name, sub, ms) in enumerate(PHASES):
        y = 800 - i * 138; col = [c["red"], c["olive"], c["sea"], c["olive"]][i]
        x = x0 + s_ * k; bw = (e - s_) * k
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="104" fill="{col}" fill-opacity=".88"/>')
        for j in range(1, int(bw // 120) + 1):
            jx = x + j * 120 - (60 if i % 2 else 0)
            if jx < x + bw - 10: out.append(f'<line x1="{jx:.0f}" y1="{y}" x2="{jx:.0f}" y2="{y + 104}" stroke="{c["paper"]}" stroke-opacity=".4" stroke-width="3"/>')
        out.append(f'<text x="{x0 - 30}" y="{y + 44}" text-anchor="end" font-family="Marcellus" font-size="30" fill="{col}">{name}</text>')
        out.append(f'<text x="{x0 - 30}" y="{y + 80}" text-anchor="end" font-family="Lora" font-size="22" fill="{c["ink"]}" fill-opacity=".8">{s_}–{e} years{" · " + sub if sub else ""}</text>')
        if bw > 300:
            out.append(f'<text x="{x + 18:.0f}" y="{y + 44}" font-family="Lora" font-size="21" fill="{c["paper"]}">{ms[0]}</text>')
            out.append(f'<text x="{x + 18:.0f}" y="{y + 78}" font-family="Lora" font-size="21" fill="{c["paper"]}">{ms[1]}</text>')
        else:
            out.append(f'<text x="{x + bw + 18:.0f}" y="{y + 44}" font-family="Lora" font-size="21" fill="{c["ink"]}">{" · ".join(ms[:2])}</text>')
            out.append(f'<text x="{x + bw + 18:.0f}" y="{y + 78}" font-family="Lora" font-size="21" fill="{c["ink"]}">{" · ".join(ms[2:4])}</text>')
    out.append(f'<rect x="{x0 - 10}" y="904" width="{w + 20}" height="14" fill="{c["ink"]}" fill-opacity=".7"/>')
    for yr in range(0, 31, 10):
        out.append(f'<text x="{x0 + yr * k:.0f}" y="950" text-anchor="middle" font-family="Marcellus" font-size="24" fill="{c["ink"]}">{"year " if yr == 0 else ""}{yr}</text>')
    return b_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{"".join(out)}</svg>
<div style="position:absolute;left:128px;top:96px;width:1660px">
  <p style="font:400 24px/1 {c['head']};letter-spacing:6px;color:{c['red']}">3 · COALITION CONTINUITY</p>
  <h2 style="font:400 60px/1.1 {c['head']};color:{c['ink']};margin-top:14px">Built course by course over roughly 30 years</h2>
  <p style="font:italic 400 28px/1.35 {c['serif']};color:{c['olive']};margin-top:12px">The incubation is the foundation. Each course above it is an optional expanded mandate.</p>
</div>''', "Coalition continuity")

# ================================================================ C · Round City plan
C = dict(paper="#f7f6f1", ink="#1c2a42", teal="#0f6e6a", red="#b8452a", rule="#cfd5dd",
         sans="'IBM Plex Sans', Arial, sans-serif", mono="'IBM Plex Mono', monospace", ar="'IBM Plex Sans Arabic', sans-serif", he="'IBM Plex Sans Hebrew', sans-serif")

def c_frame(inner, foot):
    c = C
    grid = (f'background-color:{c["paper"]};background-image:linear-gradient({c["rule"]} 1px, transparent 1px),linear-gradient(90deg, {c["rule"]} 1px, transparent 1px);'
            f'background-size:48px 48px;background-position:-1px -1px')
    f = (f'<p style="position:absolute;left:128px;bottom:56px;font:500 20px/1 {c["mono"]};letter-spacing:3px;color:{c["teal"]};text-transform:uppercase;background:{c["paper"]};padding:6px 10px">{foot or "Sheet 01"}</p>'
         f'<p style="position:absolute;right:128px;bottom:56px;font:500 20px/1 {c["mono"]};letter-spacing:3px;color:{c["ink"]};background:{c["paper"]};padding:6px 10px">X.COM/THEKINGDAVIDJR</p>')
    return slide(inner + f, c["paper"], grid)

def round_city(cx, cy, r, c, labels=False):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["paper"]}" stroke="{c["ink"]}" stroke-width="4"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r - 24}" fill="none" stroke="{c["ink"]}" stroke-width="1.5"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r * .42:.0f}" fill="none" stroke="{c["ink"]}" stroke-width="2"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r * .25:.0f}" fill="{c["paper"]}" stroke="{c["teal"]}" stroke-width="3"/>']
    for i in range(6):
        a = math.radians(-90 + i * 60 + 30)
        out.append(f'<line x1="{cx + r * .25 * math.cos(a):.0f}" y1="{cy + r * .25 * math.sin(a):.0f}" x2="{cx + r * math.cos(a):.0f}" y2="{cy + r * math.sin(a):.0f}" stroke="{c["ink"]}" stroke-width="2"/>')
    for i in range(36):  # street grid in the ring
        a = math.radians(i * 10)
        out.append(f'<line x1="{cx + r * .44 * math.cos(a):.0f}" y1="{cy + r * .44 * math.sin(a):.0f}" x2="{cx + (r - 26) * math.cos(a):.0f}" y2="{cy + (r - 26) * math.sin(a):.0f}" stroke="{c["rule"]}" stroke-width="1"/>')
    return "".join(out)

def c_cover():
    c = C
    return c_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px" aria-hidden="true">{round_city(1450, 540, 380, c)}
  <text x="1450" y="552" text-anchor="middle" font-family="IBM Plex Sans Arabic" font-size="34" font-weight="500" fill="{c['teal']}">{AR_WISDOM}</text>
  <text x="1450" y="966" text-anchor="middle" font-family="IBM Plex Mono" font-size="20" fill="{c['teal']}">BAYT AL-HIKMAH · THE HOUSE OF WISDOM · BAGHDAD</text>
  <line x1="1450" y1="160" x2="1450" y2="100" stroke="{c['red']}" stroke-width="2"/><text x="1450" y="88" text-anchor="middle" font-family="IBM Plex Mono" font-size="20" fill="{c['red']}">N · THE ROUND CITY PLAN, 762</text>
</svg>
<div style="position:absolute;left:128px;top:160px;width:900px">
  <p style="font:500 24px/1 {c['mono']};letter-spacing:4px;color:{c['teal']};background:{c['paper']};display:inline-block;padding:4px 8px">THE VIRTUOUS CITY VISION · DRAFT PLAN</p>
  <h1 style="font:600 92px/1.02 {c['sans']};color:{c['ink']};margin-top:28px;background:{c['paper']}">Ending the Gaza War Must Restore Our Humanity</h1>
  <div style="display:flex;gap:40px;margin-top:34px;background:{c['paper']};padding:6px 0">
    <p style="font:500 44px/1.2 {c['ar']};color:{c['teal']}" dir="rtl" lang="ar">{AR_CITY}</p>
    <p style="font:500 40px/1.3 {c['he']};color:{c['teal']}" dir="rtl" lang="he">{HE_CITY}</p>
  </div>
  <p style="font:400 26px/1.45 {c['ar']};color:{c['ink']};opacity:.75;margin-top:18px;background:{c['paper']}" dir="rtl" lang="ar">{AR_TITLE}</p>
  <p style="font:400 26px/1.45 {c['he']};color:{c['ink']};opacity:.75;background:{c['paper']}" dir="rtl" lang="he">{HE_TITLE}</p>
  <p style="font:400 26px/1 {c['mono']};color:{c['ink']};margin-top:36px;background:{c['paper']};display:inline-block;padding:4px 0">David Hanna Jr. · October 2026</p>
</div>''', "Sheet 00 · cover")

def c_arch():
    c = C; cx, cy, r = 560, 560, 380; out = [round_city(cx, cy, r, c)]
    for i, (name, _) in enumerate(BLOCKS):
        a = math.radians(-90 + i * 60); mx, my = cx + r * .7 * math.cos(a), cy + r * .7 * math.sin(a)
        out.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="30" fill="{c["red"] if i == 0 else c["ink"]}"/><text x="{mx:.0f}" y="{my + 9:.0f}" text-anchor="middle" font-family="IBM Plex Mono" font-size="26" font-weight="600" fill="{c["paper"]}">{i + 1:02d}</text>')
    out.append(f'<text x="{cx}" y="{cy - 22}" text-anchor="middle" font-family="IBM Plex Sans Arabic" font-size="30" fill="{c["teal"]}">{AR_SAADA}</text>')
    out.append(f'<text x="{cx}" y="{cy + 12}" text-anchor="middle" font-family="IBM Plex Sans" font-weight="600" font-size="24" fill="{c["ink"]}">THE TELOS</text>')
    out.append(f'<text x="{cx}" y="{cy + 48}" text-anchor="middle" font-family="IBM Plex Sans Hebrew" font-size="28" fill="{c["teal"]}">{HE_SAADA}</text>')
    legend = "".join(f'<div style="display:flex;gap:20px;padding:13px 16px;border-bottom:1px solid {c["rule"]};background:{c["paper"]}">'
                     f'<span style="font:600 24px/1.3 {c["mono"]};color:{c["red"] if i == 0 else c["ink"]}">{i + 1:02d}</span><div><p style="font:600 28px/1.2 {c["sans"]};color:{c["ink"]}">{n}</p>'
                     f'<p style="font:400 21px/1.35 {c["sans"]};color:{c["ink"]};opacity:.78;margin-top:4px">{s}</p></div></div>' for i, (n, s) in enumerate(BLOCKS))
    return c_frame(f'''
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{"".join(out)}</svg>
<div style="position:absolute;left:1030px;top:110px;width:760px">
  <p style="font:500 22px/1 {c['mono']};letter-spacing:4px;color:{c['teal']};background:{c['paper']};display:inline-block;padding:4px 8px">SHEET 01 · THE ARCHITECTURE</p>
  <h2 style="font:600 54px/1.08 {c['sans']};color:{c['ink']};margin:14px 0 18px;background:{c['paper']}">Six districts around one telos</h2>
  <div style="border:2px solid {c['ink']}">{legend}</div>
</div>''', "Sheet 01 · the core thesis")

def c_time():
    c = C
    g = gantt(c, 150, 400, 1620, 135, "IBM Plex Sans", "IBM Plex Sans", [c["red"], c["teal"], c["ink"], c["teal"]], bar_style="line", numfont="IBM Plex Mono")
    return c_frame(f'''
<div style="position:absolute;left:128px;top:110px;width:1660px">
  <p style="font:500 22px/1 {c['mono']};letter-spacing:4px;color:{c['teal']};background:{c['paper']};display:inline-block;padding:4px 8px">SHEET 03 · COALITION CONTINUITY</p>
  <h2 style="font:600 60px/1.08 {c['sans']};color:{c['ink']};margin-top:14px;background:{c['paper']};display:inline-block">Roughly 30 years: an incubation and three phases</h2>
  <p style="font:400 26px/1.3 {c['sans']};color:{c['ink']};opacity:.8;margin-top:10px;background:{c['paper']};display:inline-block">Each phase after the incubation is an optional expanded mandate.</p>
</div>
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px">{g}</svg>''', "Sheet 03 · coalition continuity")

DIRS = [("A · Manuscript of the House of Wisdom", "Parchment, ink, lapis and terracotta · EB Garamond with Amiri (Arabic) and Frank Ruhl Libre (Hebrew) · girih star borders · the architecture as a rota around Farabi’s happiness", [a_cover(), a_arch(), a_time()]),
        ("B · Jerusalem stone and olive", "Limestone, olive, sea blue and deep red · Marcellus and Lora with Reem Kufi (Arabic) and David Libre (Hebrew) · arches and stone courses · the timeline built from the foundation up", [b_cover(), b_arch(), b_time()]),
        ("C · The Round City plan", "Drafting paper and linework · IBM Plex Sans in Latin, Arabic and Hebrew (one family for all three) · Baghdad’s Round City, home of the House of Wisdom, as the master map", [c_cover(), c_arch(), c_time()])]

FONTS = ("https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Amiri&family=Frank+Ruhl+Libre:wght@400;500;700"
         "&family=Marcellus&family=Lora:ital,wght@0,400;1,400&family=Reem+Kufi&family=Noto+Naskh+Arabic&family=David+Libre:wght@400;700"
         "&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500&family=IBM+Plex+Sans+Hebrew:wght@400;500&display=swap")

body = "".join(f'<h2 class="dir">{t}</h2><p class="desc">{d}</p>' + "".join(f'<div class="frame"><div class="fit">{s}</div></div>' for s in slides) for t, d, slides in DIRS)
OUT.write_text(f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Identity mock-ups</title>
<link rel="stylesheet" href="{FONTS}">
<style>
  :root {{ color-scheme: light; }}
  body {{ margin:0; background:#d9d6cf; font-family:'IBM Plex Sans', Arial, sans-serif; color:#222; padding:24px 16px 64px; }}
  .wrap {{ max-width:1200px; margin:0 auto; }}
  h1.top {{ font-size:26px; margin:0 0 6px; }} p.lead {{ margin:0 0 24px; color:#555; }}
  h2.dir {{ font-size:22px; margin:40px 0 4px; }} p.desc {{ margin:0 0 14px; color:#555; font-size:15px; }}
  .frame {{ position:relative; width:100%; aspect-ratio:16/9; overflow:hidden; margin:0 0 18px; box-shadow:0 8px 30px rgba(0,0,0,.18); }}
  .fit {{ position:absolute; left:0; top:0; width:1920px; height:1080px; transform-origin:0 0; }}
  .s {{ position:relative; width:1920px; height:1080px; overflow:hidden; box-sizing:border-box; }}
  .s * {{ box-sizing:border-box; }} .s h1, .s h2, .s p {{ margin:0; }}
</style>
<div class="wrap">
<h1 class="top">The Virtuous City Vision · three light identities</h1>
<p class="lead">Cover, architecture and timeline in each direction. The Arabic and Hebrew are working translations, to be checked by native speakers.</p>
{body}
</div>
<script>
  const fit = () => document.querySelectorAll('.frame').forEach(f => f.firstElementChild.style.transform = `scale(${{f.clientWidth / 1920}})`);
  addEventListener('resize', fit); fit();
</script>
''')
print("wrote", OUT, OUT.stat().st_size // 1024, "KB")
