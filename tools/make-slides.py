#!/usr/bin/env python3
"""Writes the Virtuous City Vision deck (deck/) and pitch (pitch/) in the Slides export format the
Islamabad Accords repo uses (deck.json + slides/<id>.html). Text is taken from the author's essay; fit.json holds
per-slide type scales found by fit.mjs."""
import json, os, sys, html as H
from pathlib import Path

REPO = Path(os.environ.get("REPO", Path(__file__).resolve().parent.parent))
SITE = "https://dhanna11.github.io/virtuous-city-vision/"
FIT = Path(__file__).with_name("fit.json")
SCALE = json.loads(FIT.read_text()) if FIT.exists() else {}

# Identity A, "Manuscript of the House of Wisdom" (author, 8 Oct 2026; see docs/design/). Light parchment, ink, lapis and
# terracotta, gold for ornament; EB Garamond with Amiri (Arabic) and Frank Ruhl Libre (Hebrew). The old names are kept:
# PAPER is now the text colour (ink) and GOLDL the accent (lapis).
BG, DARK, CARD = "#f3ead6", "#ece0c3", "#faf5e8"
GOLD, GOLDL, GOLDD, PAPER, GREY = "#a8823a", "#1f3d73", "#a8915e", "#2a2118", "#6b5e48"
TERRA, RULE = "#a3442a", "#c9b48a"
SERIF = "'EB Garamond', Georgia, serif"
MONO = SANS = SERIF   # labels are EB Garamond small caps; no sans or mono on the slides
AR, HE = "'Amiri', serif", "'Frank Ruhl Libre', serif"
BORDER, BORDER_S = "rgba(168,130,58,0.35)", "rgba(168,130,58,0.5)"
HANDLE = "X.COM/THEKINGDAVIDJR"
S = 1.0

import math
def px(n): return f"{round(n * S)}px"

def star8(cx, cy, r, ri):
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5 - 90); rr = r if i % 2 == 0 else ri
        pts.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
    return " ".join(pts)

def a(text, href):
    return f'<a href="{href}" target="_blank" rel="noopener" style="color:{GOLDL}; text-underline-offset:4px">{text}</a>'

def emo(e, size=64, color=TERRA):
    """the slide's mark: an eight-pointed girih star (the emoji argument is kept only as a hint of the slide's subject)"""
    r = size / 2
    return (f'<svg aria-hidden="true" viewBox="0 0 {size} {size}" style="width:{px(size)}; height:{px(size)}; flex:none">'
            f'<polygon points="{star8(r, r, r * .96, r * .7)}" fill="none" stroke="{color}" stroke-width="2.5"/>'
            f'<polygon points="{star8(r, r, r * .5, r * .36)}" fill="{color}"/></svg>')

def kick(t, fs=28, color=TERRA, ls=5):
    return (f'<p style="font-family:{SERIF}; font-size:{px(fs)}; font-weight:600; color:{color}; letter-spacing:{ls}px; '
            f'text-transform:uppercase; text-wrap:balance">{t}</p>')

def h2(t, fs=80, color=PAPER):
    return f'<h2 style="font-family:{SERIF}; font-size:{px(fs)}; font-weight:500; color:{color}; line-height:1.08; text-wrap:balance">{t}</h2>'

def head(e, k, t=None, ks=28, ts=80, tc=PAPER):
    inner = kick(k, min(ks, 30)) + (h2(t, ts, tc) if t else "")
    return (f'<div style="display:flex; gap:24px; align-items:center">{emo(e, 56)}'
            f'<div style="flex:1; display:flex; flex-direction:column; gap:14px">{inner}</div></div>')

def p(t, fs=44, font=SERIF, color=PAPER, italic=False, lh=1.3, extra=""):
    it = " font-style:italic;" if italic else ""
    return f'<p style="font-family:{font}; font-size:{px(fs)};{it} color:{color}; line-height:{lh}; text-wrap:pretty{extra}">{t}</p>'

def ul(items, fs=46, color=PAPER, font=SERIF):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'<ul style="text-wrap:pretty; font-family:{font}; font-size:{px(fs)}; color:{color}; line-height:1.32; '
            f'padding:0 0 0 40px; display:flex; flex-direction:column; gap:{px(10)}">{lis}</ul>')

def coda(t, fs=40):
    return (f'<p style="font-family:{SERIF}; font-size:{px(fs)}; font-style:italic; color:{GOLDL}; line-height:1.25; '
            f'text-wrap:pretty; border-top:1px solid {BORDER_S}; padding-top:{px(22)}">{t}</p>')

def card(label, body, e=None, ls=30, bs=36, gold=False, body_font=SERIF, extra=""):
    border = TERRA if gold else BORDER
    lab = (f'<p style="font-family:{SERIF}; font-size:{px(ls)}; font-weight:600; color:{TERRA if gold else GOLDL}; letter-spacing:3px; '
           f'text-transform:uppercase; line-height:1.25">{label}</p>') if label else ""
    b = body if body.startswith("<") else f'<p style="font-family:{body_font}; font-size:{px(bs)}; color:{PAPER}; line-height:1.28; text-wrap:pretty">{body}</p>'
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:{px(12)}; background:{CARD}; border:1px solid {border}; '
            f'border-top:3px solid {TERRA if gold else GOLD}; padding:{px(28)}{extra}">{lab}{b}</div>')

def row(*cards, gap=24):
    return f'<div style="display:flex; gap:{gap}px; align-items:stretch">{"".join(cards)}</div>'

def icon(name, color=GOLDL, size=56):
    return f'<x-icon name="{name}" style="width:{px(size)}; height:{px(size)}; color:{color}"></x-icon>'

def flow(steps):
    """boxes joined by arrows: steps = [(icon, label)]"""
    arrow = f'<x-shape kind="arrow-right" style="width:64px; height:32px; background:{TERRA}; align-self:center"></x-shape>'
    boxes = [(f'<div style="flex:1; display:flex; flex-direction:column; align-items:center; text-align:center; gap:12px; background:{CARD}; '
              f'border:1px solid {BORDER}; border-top:3px solid {GOLD}; padding:{px(24)} 20px">{icon(i)}'
              f'<p style="font-family:{SERIF}; font-size:{px(28)}; font-weight:600; color:{PAPER}; letter-spacing:2px; text-transform:uppercase; line-height:1.25">{t}</p></div>')
             for i, t in steps]
    return f'<div style="display:flex; gap:20px; align-items:stretch">{arrow.join(boxes)}</div>'

def chips(items, fs=32):
    cs = "".join(f'<p style="font-family:{SERIF}; font-size:{px(fs + 2)}; font-weight:500; color:{PAPER}; background:{CARD}; '
                 f'border:1.5px solid {GOLD}; border-radius:40px; padding:{px(10)} {px(28)}; white-space:nowrap">{c}</p>' for c in items)
    return f'<div style="display:flex; flex-wrap:wrap; gap:18px">{cs}</div>'

def timeline(n, hi=None):
    xs = [round(40 + (1584) * (i + .5) / n) for i in range(n)]
    dots = "".join(f'<polygon points="{star8(x, 40, 22 if i == hi else 17, 13 if i == hi else 10)}" fill="{TERRA if i == hi else GOLD}"/>' for i, x in enumerate(xs))
    return (f'<svg aria-label="Timeline with {n} markers" viewBox="0 0 1664 80" style="width:1664px; height:80px; flex:none">'
            f'<line x1="40" y1="40" x2="1624" y2="40" stroke="{GOLD}" stroke-width="2"/>{dots}'
            f'<polygon points="1624,30 1656,40 1624,50" fill="{GOLD}"/></svg>')

def girih_band(w, y, h, color):
    n = int(w // h); st = w / n; out = []
    for i in range(n):
        cx = st * i + st / 2
        out.append(f'<polygon points="{star8(cx, y + h / 2, h * .46, h * .3)}" fill="none" stroke="{color}" stroke-width="1.6"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{y + h / 2:.1f}" r="{h * .09:.1f}" fill="{color}"/>')
    return "".join(out)

# the manuscript page: a double gold frame with a band of girih stars along the top, drawn behind every slide
# (one star, reused 60 times: an SVG <pattern> would print as a bitmap on every PDF page)
_STARS = "".join(f'<use href="#girih" x="{60 + 30 * i}" y="54"/>' for i in range(60))
FRAME = (f'<svg class="xf" aria-hidden="true" viewBox="0 0 1920 1080" style="position:absolute; left:0; top:0; width:1920px; height:1080px; pointer-events:none">'
         f'<defs><g id="girih"><polygon points="{star8(15, 15, 13.8, 9)}" fill="none" stroke="{GOLD}" stroke-width="1.6"/><circle cx="15" cy="15" r="2.7" fill="{GOLD}"/></g></defs>'
         f'<rect x="48" y="40" width="1824" height="1000" fill="none" stroke="{GOLD}" stroke-width="3"/>'
         f'<rect x="60" y="52" width="1800" height="976" fill="none" stroke="{RULE}" stroke-width="1.5"/>{_STARS}</svg>')

def section(sid, inner, foot, bg=BG, gap=32, justify="center"):
    frame = FRAME.replace("girih", "girih-" + sid)
    return (f'<section id="{sid}" data-transition="fade" style="background:{bg}; color:{PAPER}; font-family:{SERIF}; '
            f'padding:128px 128px 160px; display:flex; flex-direction:column; gap:{px(gap)}; justify-content:{justify}">\n{frame}{inner}\n'
            f'<p style="position:absolute; left:128px; bottom:72px; width:800px; font-family:{SERIF}; font-size:22px; font-weight:600; color:{TERRA}; letter-spacing:4px">{foot.upper()}</p>'
            f'<p style="position:absolute; right:128px; bottom:72px; width:800px; text-align:right; font-family:{SERIF}; font-size:22px; font-weight:600; color:{GOLD}; letter-spacing:4px">{HANDLE}</p>\n</section>')

def divider(sid, e, k, t, sub, foot, ar=None, he=None):
    tri = ""
    if ar or he:
        tri = (f'<div style="display:flex; gap:48px; align-items:baseline">'
               + (f'<p dir="rtl" lang="ar" style="font-family:{AR}; font-size:{px(52)}; color:{GOLDL}; line-height:1.3">{ar}</p>' if ar else "")
               + (f'<p dir="rtl" lang="he" style="font-family:{HE}; font-size:{px(46)}; color:{GOLDL}; line-height:1.3">{he}</p>' if he else "") + '</div>')
    inner = (emo(e, 80) + kick(k, 30) + h2(t, 92) + tri + p(sub, 40, italic=True, color=GREY))
    return section(sid, inner, foot, bg=DARK, gap=28)

BRAND = "The Virtuous City Vision"
FARABI = a("Al-Farabi’s", "https://youtube.com/watch?v=uZ30XUDnK-g")
OPINIONS = a("<i>Opinions of the People of the Virtuous City</i>", "https://www.amazon.com/Perfect-State-Abu-Nasr-al-Farabi/dp/1871031761")
SMOTRICH = a("Bezalel Smotrich", "https://hashiloach.org.il/israels-decisive-plan/")
FROMAN = a("Rabbi Menachem Froman", "https://en.wikipedia.org/wiki/Menachem_Froman")
YASSIN = a("Ahmed Yassin", "https://en.wikipedia.org/wiki/Ahmed_Yassin")

# ---------------------------------------------------------------- slides: id -> function returning the section html
SL = {}
def slide(fn):
    SL[fn.__name__.replace("_", "-")] = fn
    return fn

@slide
def cover():
    lines = ["The Telos of the Virtuous City of Gaza", "The Coalition for Canaan", "The House of Wisdom and Peace"]
    ls = "".join(f'<p style="font-family:{SERIF}; font-size:{px(34)}; font-style:italic; color:{GREY}; text-align:right; line-height:50px; height:50px; white-space:nowrap">{l}</p>' for l in lines)
    svg = (f'<svg aria-label="Three parts gathered into one line, ending in peace in the Middle East" viewBox="0 0 300 150" style="width:300px; height:150px">'
           f'<path d="M0,25 C140,25 170,75 240,75" fill="none" stroke="{GOLDD}" stroke-width="3"/><path d="M0,75 C140,75 170,75 240,75" fill="none" stroke="{GOLD}" stroke-width="3"/>'
           f'<path d="M0,125 C140,125 170,75 240,75" fill="none" stroke="{GOLDD}" stroke-width="3"/><path d="M240,75 L292,75" stroke="{GOLDL}" stroke-width="6" stroke-linecap="round"/>'
           f'<circle cx="240" cy="75" r="12" fill="{CARD}" stroke="{GOLDL}" stroke-width="3"/></svg>')
    inner = (f'<div style="flex:1"></div><h1 style="font-family:{SERIF}; font-size:{px(112)}; font-weight:400; color:{GOLD}; line-height:1.05; text-align:center; text-wrap:balance">Ending the Gaza War Must Restore Our Humanity</h1>'
             f'<p style="font-family:{SERIF}; font-size:{px(52)}; font-style:italic; color:{PAPER}; text-align:center">{BRAND}</p>'
             f'<hr style="border-top:1px solid {GOLD}; width:320px; align-self:center">'
             f'<div style="display:flex; align-items:center; justify-content:center; gap:20px"><div style="display:flex; flex-direction:column">{ls}</div>'
             f'<div style="display:flex; align-items:center; gap:16px">{svg}<p style="font-family:{SERIF}; font-size:{px(44)}; color:{GOLDL}; line-height:1.05">Peace in the<br>Middle East</p></div></div>'
             f'<div style="flex:1"></div><p style="font-family:{SERIF}; font-size:32px; color:{PAPER}; text-align:center">David Hanna Jr.</p>'
             f'<p style="font-family:{MONO}; font-size:24px; color:{GOLDD}; letter-spacing:3px; text-align:center">Unofficial · a private author’s proposal · October 2026</p>')
    return section("cover", inner, "", bg=DARK, gap=24, justify="start").replace(
        f'<p style="position:absolute; left:128px; bottom:64px; width:800px; font-family:{MONO}; font-size:24px; color:{GOLDD}; letter-spacing:3px"></p>', "")

@slide
def lead():
    return section("lead", head("🦴", "The core thesis", ks=43) +
        p("The Israeli-Palestinian conflict has long resembled a malformed bone: broken, poorly set, fractured again, and left to limp onward in dysfunction.", 64, lh=1.35) +
        coda("The bone can be reset properly, or harden again into another frozen conflict that guarantees the next war.", 48), "The core thesis", gap=40)

@slide
def moment():
    return section("moment", head("🕰️", "The core thesis · the moment", "The hardened structure has briefly softened") +
        ul(["The Board of Peace is established",
            "Phase Two of Trump’s 20-point plan is underway",
            "Enough pieces of the post-war mosaic are now visible to paint a new architecture for Israel, Palestine, and the wider Middle East"], 52),
        "The core thesis")

@slide
def missing():
    ck = lambda t: card(t, "real, if fledgling, momentum", ls=32, bs=36, body_font=SANS, e="✅")
    return section("missing", head("✨", "The core thesis · what is missing", "The civilizational soul") +
        p("The current trajectory has real, if fledgling, momentum in diplomacy, seed money, and technocratic planning.", 44) +
        row(ck("Diplomacy"), ck("Seed money"), ck("Technocratic planning"),
            card("The civilizational soul", "missing", e="❔", ls=32, bs=36, body_font=SANS, gold=True)) +
        coda("What is missing is the civilizational soul capable of sustaining what the Trump administration is attempting: bringing Peace to the Middle East.", 42),
        "The core thesis")

@slide
def credit():
    return section("credit", head("🏗️", "The core thesis · the scale of the task", "Only a fraction of the money, time, and collective will required", ts=72) +
        ul(["The Trump administration deserves real credit for articulating a multi-billion-dollar economic vision to rebuild and reimagine Gaza as a regional economic hub",
            "This architecture must simultaneously restore Palestinian dignity and prosperity while recovering Israeli existential security",
            "Two nations that prize self-determination above all else",
            "Any architecture will inevitably step on the toes of both peoples · the international community will be asked to shoulder disproportionate responsibility for the consequences"], 42),
        "The core thesis")

@slide
def vision():
    return section("vision", head("🏛️", "The core thesis · the Virtuous City of Gaza", "More than a commercial or tourist center") +
        row(card("A nucleus", "of intellectual, spiritual, and moral renewal", e="🧠", bs=44),
            card("A reconciliation project", "between Western and Islamic civilizations", e="🤝", bs=44),
            card("A covenant", "that the Holy Land must never again become a battlefield for reciprocal genocide", e="📜", bs=44)),
        "The core thesis", gap=44)

@slide
def arc():
    c = lambda t, b, g=False: card(t, b, ls=34, bs=38, body_font=SANS, gold=g)
    return section("arc", head("🧭", "The arc", "A telos, a coalition, and a generation", ks=43, ts=84, tc=PAPER) + timeline(4, 0) +
        row(c("The telos", "the Virtuous City of Gaza", True), c("The coalition", "the Coalition for Canaan, incubated by the Board of Peace"),
            c("The transition", "demilitarization · freedom of movement · reconstruction · the West Bank"),
            c("The frameworks", "five reconciliation frameworks · the House of Wisdom and Peace")),
        "The core thesis", gap=28)

# ---- 1 · the telos
@slide
def sec_telos():
    return divider("sec-telos", "📜", "1 · The telos", "The Telos of the Virtuous City of Gaza",
        f"{FARABI} {OPINIONS} is more than an obscure utopian text preserved under the patronage of a bygone Abbasid Emir · it is the singular spiritual template for Gaza’s rebirth", "The telos")

@slide
def farabi():
    return section("farabi", head("☀️", "The telos · one supreme purpose", "True happiness (sa’ada)") +
        p("To enable every inhabitant to attain true happiness: the full actualization of human potential through intellectual perfection, moral virtue, civic cooperation, and the ultimate union with the divine, culminating in eternal felicity.", 44) +
        ul(["A city is truly virtuous only when its leaders, institutions, education, and shared life mutually support this collective flourishing, in this world and the next",
            "Each part of society functioning harmoniously, like organs in a healthy body"], 38, color=GREY) +
        coda("A nucleus for a new social order and contract among Gaza’s future inhabitants · the political and philosophical north star guiding reconstruction and nation-building after catastrophe", 38),
        "The telos")

@slide
def heritage():
    return section("heritage", head("📖", "The telos · its lineage", "Plato’s Republic, seeded with the soul of Medina") +
        ul(["An Arab-Islamic political and philosophical framework, developed at the height of the Islamic world’s engagement with Greek, Jewish, and Christian thought",
            "Reason, revelation, ethics, and law existed in productive tension rather than outright opposition",
            "That intellectual milieu produced shared advances in philosophy, medicine, mathematics, and jurisprudence",
            "The connection to the divine as the ultimate pathway to happiness"], 46),
        "The telos")

@slide
def education():
    return section("education", head("🎓", "The telos · two peoples", "Education as the foundation of renewal") +
        row(card("For Palestinians", "Education has long functioned as a form of resistance: a way to preserve dignity, identity, and future orientation under occupation, displacement, and hopelessness · Gaza remains among the most educated societies in the Arab world relative to material conditions", bs=36),
            card("With Jewish ethical traditions", "Education, communal responsibility, wise and virtuous rulership, and collective flourishing resonate · a shared moral substrate through which both peoples can recognize legitimate authority, justice, and the raison d’être of their polity", bs=36)) +
        coda("The Virtuous City Vision elevates that instinct into the foundation of Palestinian rebuilding and national renewal.", 40),
        "The telos")

@slide
def positive_telos():
    return section("positive-telos", head("🌱", "The telos · a positive goal", "Something Gaza has never been allowed to have") +
        p("Gaza’s modern political identity has been defined almost entirely by resistance, survival, and siege/occupation. The Virtuous City redefines that horizon toward human flourishing through moral, intellectual, and spiritual development.", 40) +
        row(card("Without a clear telos", "security architectures default to mere conflict management · economic visions risk devolving into a façade of permanent aid dependency", bs=36),
            card("With the Virtuous City as its north star", "Gaza’s reconstruction becomes a civilizational project rather than a humanitarian holding pattern", bs=36, gold=True)) +
        coda("Only once this foundation is established does it make sense to discuss disarmament, reconstruction, and a long-term security architecture.", 38),
        "The telos")

@slide
def scope():
    li = lambda xs: ul(xs, 40)
    return section("scope", head("⚖️", "The telos · its scope", "What the polity is for · not how it is governed") +
        row(card("It does not call for", li(["a philosopher-king", "a clerical guardian", "an elitist Platonic ruling class"])),
            card("The mechanics of modern democracy", li(["constitutional law", "civic accountability", "elected leaders who serve at the public’s pleasure and can be voted out"]), gold=True)) +
        coda("A new telos for Gaza without a supporting architecture is just an aspiration. The current institutional framework, the Board of Peace, isn’t yet able to bear its weight. That can be fixed.", 40),
        "The telos")

# ---- 2 · the Board of Peace and the Coalition for Canaan
@slide
def sec_board():
    return divider("sec-board", "🕊️", "2 · Coalition core", "Three Discordances and a Coalition",
        "President Trump has articulated a broad vision for the Board of Peace as a new international peacemaking body · in its current form, three discordances will harm its ability to end the Israel-Hamas War", "The Board of Peace")

@slide
def discordances():
    c = lambda n, t, b: card(f"{n} · {t}", b, ls=30, bs=33)
    return section("discordances", head("⚠️", "Coalition core · three discordances", "Mandate, coalition, and soul") +
        row(c(1, "Mandate", "A tighter Gaza-first mandate, as initially framed, against the broader peacemaking body with global scope the Charter implies · a concern for many potential member states"),
            c(2, "Composition", "The current composition against the minimum viable coalition · the UK, France, Germany, and the Vatican refuse to join, and only a subset of its Members and Observers are materially significant to the conflict"),
            c(3, "Foundation", "A transactional, administrative, and diplomatic mechanism · without an explicit philosophical and reconciliation substrate, it doesn’t do justice to the human complexity of the conflict")),
        "The Board of Peace", gap=44)

@slide
def incubator():
    return section("incubator", head("🥚", "The Board of Peace · its structural role", "An incubator, not an indefinite administrator") +
        flow([("Globe", "The Board of Peace convenes, authorizes, stabilizes"), ("Users", "A coalition of the willing, tailored to the Gaza conflict"), ("Trust", "An independent guarantor body")]) +
        ul(["The discordances do not require abandoning the Board of Peace · they require clarifying its structural role",
            "It should not administer Gaza indefinitely beyond its authorized two-year mandate",
            "Consistent with Article 3 of the Board of Peace Charter: a subsidiary coalition of the willing, the Coalition for Canaan",
            "A structural pathway for states reluctant to join the Board as currently conceived"], 38),
        "The Board of Peace")

MANDATE = [("⚖️", "Moral", "Break the cycle of genocide"),
           ("🏛️", "Political", "A generational, time-bound pathway to Palestinian self-governance"),
           ("🩺", "Humanitarian", "Stabilize Gaza and address its humanitarian catastrophe"),
           ("🌍", "Civilizational", "Heal the Western–Arab and Islamic divide"),
           ("🕊️", "Spiritual", "Re-covenant the sanctity of peace in the Holy Land")]

@slide
def mandate():
    return section("mandate", head("🖐️", "The Coalition for Canaan", "The Five-Point Mandate", ts=96) +
        row(*[card(f"{i+1} · {t}", b, e=e, ls=26, bs=36) for i, (e, t, b) in enumerate(MANDATE)], gap=18) +
        coda("A focused, semi-independent guarantor bloc, incubated and initially shepherded by the Board, for the broader Israeli–Palestinian conflict", 38),
        "The Coalition for Canaan", gap=40)

def mandate_slide(n, items, fs=48, extra=""):
    e, t, b = MANDATE[n - 1]
    return section(f"mandate-{n}", head(e, f"The Five-Point Mandate · {n} of 5 · {t.lower()}", b, ts=80) + ul(items, fs) + extra, "The Coalition for Canaan")

@slide
def mandate_1(): return mandate_slide(1, ["Israelis widely view the October 7 attack as a genocidal massacre",
    "Palestinians widely view the subsequent Gaza war as genocide",
    "The Coalition commits to formally acknowledging these perceptions and preventing their recurrence"])
@slide
def mandate_2(): return mandate_slide(2, ["Using the Trump Plan to end the Gaza war as a basis · over a 20 to 30-year horizon",
    "The Coalition lays the political, security, and institutional conditions for a Palestinian polity to serve Israel’s long-term security interests",
    "The two-state formula will not be a panacea for the Holy Land · still, a credible exit plan for Palestinian self-governance is necessary for a stable interim regional order",
    "Under the 20-point plan, the PA has a pathway to return to Gaza within this timeframe, so we must plan for success"], 40)
@slide
def mandate_3(): return mandate_slide(3, ["Implement the Trump administration’s 20-point plan",
    "Guarantee Palestinian freedom of movement",
    "Rebuild and protect housing, education, and healthcare infrastructure for those who choose to stay"])
@slide
def mandate_4(): return mandate_slide(4, ["The divide this conflict continues to aggravate",
    "Economic coupling alone cannot resolve it"], 52)
@slide
def mandate_5(): return mandate_slide(5, ["Religious reconciliation frameworks will be developed",
    "Holy sites protected under negotiated covenants grounded in religious legitimacy",
    "Restoring the moral gravity that once restrained mass violence in the Holy Land"])

@slide
def members():
    li = lambda xs: ul(xs, 32, font=SANS)
    return section("members", head("🤝", "The Coalition for Canaan · members", "Who guarantees the architecture") +
        row(card("Initial core members", li(["Israel", "Palestine (PA)", "The core mediator states: the United States, Egypt, Turkey, and Qatar"]), ls=26, gold=True),
            card("Likely additional members", li(["The UAE, Jordan, Saudi Arabia, Norway, the UK", "The Vatican, Germany, France, Italy, and the Netherlands"]), ls=26),
            card("Major ISF contributors, also core", li(["Indonesia", "Morocco", "Kazakhstan", "Kosovo", "Albania"]), ls=26)) +
        coda("They provide the core economic, security, humanitarian, and reconstruction guarantees · Board of Peace members and observers provide ancillary support · roughly one generation: an initial 10-year phase and two optional extensions", 34),
        "The Coalition for Canaan")

@slide
def repeatable():
    return section("repeatable", head("🔁", "The Coalition for Canaan · a repeatable model", "Guarantor coalitions wherever fault lines harden") +
        chips(["Russia–Ukraine", "Armenia–Azerbaijan", "Cambodia–Thailand", "DRC–Rwanda", "India–Pakistan", "future fault-lines not yet erupted"], 34) +
        coda("The strength of the model lies in its ability to stand up conflict-specific architectures, stabilize them, and allow them to mature into durable, self-sustaining frameworks for security.", 42),
        "The Coalition for Canaan", gap=44)

# ---- 3 · the generational timeline
@slide
def timeline_():
    c = lambda t, xs, g=False: card(t, ul(xs, 30, font=SANS), ls=28, gold=g)
    return section("timeline", head("⏳", "3 · Coalition continuity", "Roughly 30 years, in three phases") + timeline(3) +
        row(c("Decade 1 · stabilization", ["Demilitarize Gaza", "Stand up the Coalition of the Willing", "Establish the transitional government", "Begin reconstruction", "Lay the foundations for Palestinian self-governance"]),
            c("Decade 2 · integration", ["Deepen Palestinian self-governance", "Expand economic ties with Israel and the region", "Advance the reconciliation and educational frameworks", "Continue normalization under the Abraham Accords"]),
            c("Decade 3 · full maturity", ["Mutual state recognition", "Voluntary confederation between Israel, Palestine, and the wider Middle East", "Complete Israeli military withdrawal", "Full implementation of the reconciliation frameworks"], True)),
        "The timeline", gap=28)

@slide
def not_utopian():
    return section("not-utopian", head("🌳", "The generational timeline", "Nobody disarms without a future.", ts=96) +
        p("This is by no means a utopian timeline. It represents a generational commitment to doing what no ceasefire, no peace deal, and no economic package has ever attempted: building something durable enough to endure and outlast the next crisis in the Middle East.", 46) +
        coda("With a defined political horizon and substrate, a long-term demilitarization framework for the Strip becomes viable.", 42),
        "The timeline", gap=40)

# ---- 4 · demilitarization
@slide
def sec_demil():
    return divider("sec-demil", "🛡️", "4 · Security & stabilization", "Demilitarization and the Political Transition of Resistance Factions",
        "One Authority, One Law, One Weapon under legitimate Palestinian governance", "Demilitarization")

@slide
def demil():
    return section("demil", head("🤝", "Demilitarization · the principles", "Reciprocal, not unilateral surrender") +
        ul(["Adopts the disarmament, security-transfer, verification, and Israeli-withdrawal arrangements negotiated under the Board of Peace process · no competing framework",
            "Demilitarization must be inseparable from a credible political horizon, conditioned on the agreed withdrawal and political transition",
            "The Palestinian people’s right to self-defense against indefinite occupation is a foundational principle · the settlement is legitimate only insofar as it honors that right through withdrawal and sovereignty"], 40) +
        coda("A demilitarized people under continuing occupation is not at peace but simply defenseless.", 46),
        "Demilitarization")

@slide
def lemkin():
    return section("lemkin", head("📕", "Demilitarization · a matter of principle", "Genocide as a technique of occupation") +
        p("In <i>Axis Rule in Occupied Europe</i>, Raphael Lemkin described a way for an occupying power to secure in peace what it failed to win in war: coordinated political, economic, social, and cultural measures that dismantle the national pattern of the occupied and impose that of the occupier, and not only through mass killing.", 40) +
        p("A framework that disarms Palestinians while leaving permanent external domination in place would reproduce the conditions that sustain resistance and ultimately destabilize the settlement.", 34, color=GREY) +
        coda("Indefinite occupation is no morally neutral substitute for war: it can undo a people without a shot being fired.", 44),
        "Demilitarization")

@slide
def trade():
    return section("trade", head("⚖️", "Demilitarization · the trade", "Factions relinquish coercive power as occupation recedes", ts=72) +
        row(card("Armed factions surrender", "their final coercive lever against occupation · because the alternative has already been tried, at enormous cost, and has not ended the occupation either", bs=38),
            card("The settlement provides", "phased Israeli withdrawal · credible regional and international security guarantees · an enforceable pathway to self-determination and statehood", bs=38, gold=True)) +
        ul(["Responsibility for security passes to legitimate Palestinian institutions under Palestinian authority",
            "Egypt serves as the principal regional security anchor · the Coalition for Canaan sustains the broader framework beyond the Board of Peace process"], 34, color=GREY),
        "Demilitarization")

@slide
def factions():
    return section("factions", head("🗳️", "Demilitarization · the political transition", "Factions survive only by becoming genuinely political", ts=72) +
        ul(["Armed resistance can only be durably displaced by a political system offering legitimate avenues for representation and national self-determination",
            "A pathway into ordinary political life, contingent on verified relinquishment of independent coercive capacity and adherence to the Five-Point Mandate",
            "A common rule of the transitional order, not a bespoke punishment for Hamas",
            "Operating through civilian institutions and accepting pluralist competition · material violations may result in proportionate political restrictions under Palestinian law"], 40),
        "Demilitarization")

@slide
def demob():
    return section("demob", head("🧰", "Demilitarization · into civilian life", "Demobilization without social destruction") +
        chips(["amnesty where appropriate", "employment", "education", "retirement", "social support", "safe relocation", "reconstruction work through the Palestinian Labor Movement"], 32) +
        coda("Ending armed organizations without creating a permanently excluded class of former fighters vulnerable to radicalization, and building an order just and durable enough that renewed militancy no longer seems the only path left.", 42),
        "Demilitarization", gap=44)

# ---- 5 · freedom of movement
@slide
def movement():
    return section("movement", head("🚪", "5 · Palestinian freedom of movement", "A genuine choice for those who wish to leave") +
        p("No people should be forcibly confined to a devastated enclave after mass destruction. Ending cycles of genocidal violence requires not only protection for those who remain, but a genuine choice for those who wish to leave.", 42) +
        ul(["The Coalition will negotiate, coordinate, and ensure pathways for asylum, temporary evacuation, and voluntary relocation during the reconstruction period",
            "Debated transparently and implemented through binding commitments by coalition member states · not left to ad hoc charity or discretionary border policies"], 36, color=GREY),
        "Freedom of movement")

@slide
def evacuation():
    return section("evacuation", head("✈️", "Freedom of movement · two pathways", "Temporary evacuation and asylum") +
        row(card("Temporary evacuation", "Prioritizes civilians unable to safely remain during early reconstruction: the injured, the chronically ill, families with children, those at heightened risk of retaliation or political violence · voluntary, protective, and reversible, with guaranteed best-effort rights of return", bs=33),
            card("Asylum", "Permanent resettlement abroad, with legal resources, employment, education, and family reunification · negotiated with coalition states, monitored by the Board of Peace · case by case, for former faction members who renounced armed violence and face credible threats", bs=33)) +
        coda("Designed to reduce incentives for spoilers, enable demobilization, and prevent cycles of retaliatory violence.", 38),
        "Freedom of movement")

# ---- 6 · the economy
@slide
def labor():
    return section("labor", head("👷", "6 · Reconstruction · Palestinian labor", "Gaza must be rebuilt by Palestinians themselves") +
        ul(["A non-partisan Palestinian Labor Movement, fostered by the Board and Coalition, to absorb, preserve, and redeploy displaced Palestinian human capital",
            "Centering Palestinian labor agency is the clearest check against reconstruction that erodes local ownership and political autonomy",
            "Building on existing Palestinian labor institutions, outside factional politics during the transition",
            "Workers, engineers, teachers, healthcare professionals, civil servants, and demobilized fighters who renounce armed violence · the Palestinian Authority’s reconstruction program as its baseline"], 38),
        "Reconstruction")

@slide
def compact():
    return section("compact", head("📝", "Reconstruction · the United States", "A Compact of Free Association-style agreement", ts=74) +
        ul(["The United States must play a central role in financing and supporting Gaza’s economic revitalization",
            "A proto-compact between the United States and the Palestinian Authority: a legal basis for the American reconstruction vision for Gaza",
            "A pathway to integrate Gaza into global markets while preserving Palestinian agency, dignity, and self-determination",
            "The option to evolve into a full compact upon formal recognition of Palestinian statehood"], 42),
        "Reconstruction")

@slide
def custodian():
    return section("custodian", head("🏦", "Reconstruction · Arab capital", "Without Arab capital, Gaza will not be rebuilt", ts=74) +
        p("At least one Arab state designated as the primary Reconstruction Custodian for the Gaza Strip: partnering with the transitional government to lead fundraising and investment by the Arab and Islamic world, and serving as the Arab world’s point woman for sustaining Gaza’s revival.", 36) +
        row(card("The United Arab Emirates", "currently the most suitable candidate, given its humanitarian contributions to Gaza and its relations with the United States, Egypt, and Israel", bs=34, gold=True),
            card("Saudi Arabia", "could also fill this role, creating a pathway toward normalization tied directly to the broader Israeli-Palestinian process", bs=34)) +
        coda("The choice carries major implications for the future regional order.", 38),
        "Reconstruction")

@slide
def assets():
    return section("assets", head("💰", "Reconstruction · a central financing pillar", "Iranian frozen assets for the Trust Fund") +
        ul(["Redirect a portion of Iranian frozen assets toward the Gaza Reconstruction/Virtuous City Trust Fund, matched by members of the Board of Peace",
            "These assets roughly align in scale with the cost of rebuilding Gaza",
            "One of the few existing capital pools capable of underwriting reconstruction at the necessary scale",
            "It could emerge within a broader diplomatic framework focused on ending the 2026 Iran War"], 44),
        "Reconstruction")

# ---- 7 · the West Bank
@slide
def holy_land_trust():
    return section("holy-land-trust", head("🫒", "7 · The West Bank", "A Holy Land Trust for the occupied West Bank") +
        p("Established by the Board of Peace to preserve a viable pathway toward Palestinian self-governance, uphold the Coalition’s moral and political mandate, and enable deeper normalization with Syria and Lebanon.", 44) +
        coda("Designed from inception as a framework expandable, as conditions permit, to other Israeli-occupied territories within a broader regional settlement framework.", 40),
        "The West Bank", gap=40)

@slide
def ledgers():
    return section("ledgers", head("📒", "The West Bank · two ledgers", "Parallel, without prejudice") +
        row(card("1 · Easements", "internationally funded non-development easements over a defined map of contiguity-critical parcels", bs=38),
            card("2 · Use payments", "from Israel, held in escrow, over the registered footprint of existing settlements and outposts", bs=38)) +
        p("Empty land shall remain empty. Built land shall remain limited to its registered footprint.", 50, color=GOLDL) +
        coda("Neither ledger transfers title, recognizes annexation, or determines final borders · both convert into final-status instruments only upon a negotiated settlement", 36),
        "The West Bank")

@slide
def wb_why():
    return section("wb-why", head("🚨", "The West Bank · why it is critical", "The national pattern of a people") +
        ul([f"Members of the current Israeli governing coalition, like Itamar Ben-Gvir and {SMOTRICH}, have articulated visions of settlement in the Occupied West Bank that result in the national destruction of the Palestinian nation",
            "Lemkin described genocide in two phases: the destruction of the national pattern of the oppressed group, then the imposition of the national pattern of the oppressor",
            "A dynamic that is actively occurring in the West Bank"], 40) +
        coda("The world cannot let this occur, if only to prevent the Jewish soul from being burdened with the crime of genocidal erasure of another people.", 40),
        "The West Bank")

@slide
def wb_both():
    return section("wb-both", head("🔀", "The West Bank · both sides", "Palestinian wisdom, international manpower") +
        row(card("Palestinian leadership", "Palestinian reluctance must not become an obstacle · encouraging settlement in Area C as resistance will find limited success under occupation · any bridging mechanism must not become de facto permanent", bs=33),
            card("The International Stabilization Force", "Explore pilot projects in the West Bank, toward the security architecture of a demilitarized Palestinian state · Israeli manpower constraints · rogue elements within the IDF and settler attacks, long unresolved", bs=33)) +
        coda("The unprecedented international willpower to provide manpower for both Israeli and Palestinian security must not go to waste due to short-term political calculations.", 38),
        "The West Bank")

@slide
def deathbed():
    return section("deathbed", head("🕯️", "The West Bank · a pragmatic compromise", "Keep the two-state horizon on its deathbed", ts=84) +
        p("rather than consigning it to the dustbin of history, preserving territorial compromise as an option for any future political settlement.", 52, italic=True) +
        coda("Because the West Bank remains the linchpin of broader Arab–Israeli normalization, the Board of Peace should pursue these initiatives under the Abraham Accords framework.", 42),
        "The West Bank", gap=40)

# ---- 8 · rehumanization
@slide
def sec_recon():
    return divider("sec-recon", "🤲", "9 · Rehumanization", "Philosophy, Education, and Rehumanization in the Land of Canaan",
        "Security arrangements and economic reconstruction cannot hold if the underlying civilizational logic remains broken", "Rehumanization")

@slide
def recon_why():
    return section("recon-why", head("🧠", "Rehumanization · why", "Narratives that render the Other subhuman") +
        ul(["No postwar framework can succeed without confronting the philosophical and educational drivers that sustain this conflict",
            "Each nation remains trapped in narratives that render the Other as illegitimate, subhuman, or eternal enemy",
            "Point 18 of the 20-point plan must be operationalized and institutionalized into durable curricula, civic programs, and shared reference points",
            "No illusions about hardened attitudes, grief, rage, or the current emotional weather on either side"], 38) +
        coda("The purpose here is definition, not conclusion: to name the missing frameworks so that future generations of leaders can build them into something real.", 38),
        "Rehumanization")

FRAMEWORKS = [("☀️", "The Telos of the Virtuous City of Gaza"), ("🖐️", "The Five-Point Mandate of the Coalition for Canaan"),
              ("🧬", "Shared Canaanite ethnogenesis"), ("📜", "The Judeo-Islamic Tradition"), ("🤝", "The Broader Abrahamic Tradition")]

@slide
def frameworks():
    return section("frameworks", head("🗝️", "Rehumanization · five frameworks", "At the heart of the Virtuous City Vision") +
        row(*[card(str(i + 1), f'<p style="font-family:{SERIF}; font-size:{px(38)}; color:{PAPER}; line-height:1.2">{t}</p>', e=e, ls=30, gold=i < 2) for i, (e, t) in enumerate(FRAMEWORKS)], gap=18) +
        ul(["1–2 · the civilizational and political conditions under which reconstruction and normalization become mutually intelligible",
            "3–5 · educational and rehumanization frameworks, jointly supported by Israel, Palestine, and the Coalition for Canaan"], 34, color=GREY),
        "Rehumanization", gap=40)

@slide
def fw_telos_mandate():
    return section("fw-telos-mandate", head("🧭", "Frameworks · 1 and 2 of 5", "The telos and the mandate") +
        row(card("1 · The telos", "The future Palestinians must be able to operationalize, and Israelis must be able to see · Gaza’s telos cannot merely be the absence of rockets · a Gaza oriented toward education, civic virtue, and human flourishing becomes a security gain rather than a strategic risk", bs=32),
            card("2 · The mandate", "The geopolitical philosophy governing the Architecture: reciprocal obligations, grounded in geopolitical reality · constraints Israel must accept for long-term regional legitimacy, guarantees Palestinians must see · inspired by Ben-Gurion’s early vision of Israel and its sister Arab state in an Arab regional Federation", bs=32)) +
        coda("Together: reconstruction and normalization become mutually intelligible rather than mutually threatening.", 38),
        "Rehumanization")

@slide
def fw_phylogeny():
    return section("fw-phylogeny", head("🧬", "Frameworks · 3 of 5", "Shared Canaanite ethnogenesis") +
        ul(["An anthropological rehumanization framework that acknowledges the shared ethnogenesis of the Israeli and Palestinian nations, rooted in the Land of Canaan",
            "Recognizing divergence, admixture, and other complexities",
            "Without adjudicating modern indigeneity, sovereignty, religion, or national identity",
            "Highly contested in both nations · contention over claims of indigeneity and sovereignty will not be eliminated"], 42),
        "Rehumanization")

@slide
def fw_judeo_islamic():
    return section("fw-judeo-islamic", head("📜", "Frameworks · 4 of 5", "The Formal Establishment of the Judeo-Islamic Tradition", ts=74) +
        ul(["Formalizing the shared philosophical, theological, and intellectual heritage of Jews and Muslims",
            "The very milieu in which the Virtuous City emerged",
            "A buried civilizational overlap that can be taught without forcing theological merger or political surrender"], 48),
        "Rehumanization")

@slide
def fw_abrahamic():
    return section("fw-abrahamic", head("🤝", "Frameworks · 5 of 5", "The Formal Establishment of the Broader Abrahamic Tradition", ts=74) +
        ul(["Consolidating interfaith initiatives into a coherent framework, with shared educational programs",
            "Covenants of coexistence, restraint, and mutual recognition among Jews, Muslims, and Christians",
            "Especially around contested holy sites, where sanctity must once again become covenant"], 42) +
        coda("Both traditions belong within the Abraham Accords: extending normalization beyond diplomatic recognition into structured civilizational, educational, and religious reconciliation architecture.", 36),
        "Rehumanization")

@slide
def precedent():
    return section("precedent", head("🕊️", "Rehumanization · a precedent", "Two very unlikely souls") +
        row(card(FROMAN, "West Bank settler rabbi", bs=36, body_font=SANS), card(YASSIN, "Hamas founder and spiritual leader", bs=36, body_font=SANS)) +
        p("They sought to ground conflict resolution through both Halakha and Sharia. Their effort did not succeed politically, but it perhaps offers the best prototype of the type of formal religious dialogue necessary to bring peace to the Holy Land.", 40) +
        coda("Together, the five frameworks are the moral, educational, and civilizational architecture to move the conflict beyond its zero-sum logic, toward a durable, enforceable peace that operates at the spiritual level.", 34),
        "Rehumanization")

# ---- 9 · the House of Wisdom and Peace
@slide
def house():
    return section("house", head("🏛️", "9 · The House of Wisdom and Peace", "The Board of Peace’s keystone initiative") +
        p("Not a cultural side-project or an NGO vanity mission, but the intellectual anchor of the Virtuous City Vision.", 44, italic=True) +
        ul(["This is where Truth and Reconciliation work must actually live",
            "The originating institution for the educational and interfaith reconciliation frameworks",
            "Where scholars, clerics, educators, and civic leaders formally develop the curricula, covenants, and shared moral language needed to seed peace across generations"], 38) +
        coda("Without an intellectual engine that can produce and legitimize reconciliation frameworks, Israelis and Palestinians will relapse into internecine conflict.", 38),
        "The House of Wisdom")

@slide
def house_history():
    return section("house-history", head("☯️", "The House of Wisdom · its history", "Civilizations can grow through contact") +
        ul(["The original House of Wisdom was a crossroads where the Islamic and Western worlds met through philosophy, science, and medicine",
            "Modern discourse has flattened the relationship between Islam and the West into a clash of civilizations revolving around oil, geopolitics, and resentment",
            "A yin-and-yang character: for every era of conquest and violence, an equal and opposite force of transmission, synthesis, and mutual enrichment"], 42) +
        coda("The House of Wisdom represented the light within that historical collision.", 44),
        "The House of Wisdom")

@slide
def house_wager():
    return section("house-wager", head("🎲", "The House of Wisdom · a wager", "Not an anachronism", ts=96) +
        p("Building a House of Wisdom and Peace in Gaza is a wager that civilizational collision can once again leave a constructive mark upon holy ground long scarred by conflict.", 48) +
        row(card("If it cannot rise from the ashes of Gaza", "the Board of Peace will never be more than a vanity project", bs=40),
            card("If it does", "the Board of Peace would have earned its name and place in the annals of history", bs=40, gold=True)),
        "The House of Wisdom", gap=40)

# ---- the close
@slide
def wtf():
    inner = (f'<div style="flex:1"></div>' + p("Anyone who has lived through these past three years has had to ask themselves one unavoidable question:", 48, color=GREY, italic=True) +
             f'<h2 style="font-family:{SERIF}; font-size:{px(132)}; font-weight:500; color:{TERRA}; line-height:1.05">What the fuck was all this for?</h2><div style="flex:1"></div>')
    return section("wtf", inner, "The close", bg=DARK, gap=40, justify="start")

@slide
def amorphous():
    return section("amorphous", head("⏱️", "The close · an amorphous moment", "The status quo is unacceptable") +
        ul(["We have witnessed the darkest moments in the Israeli–Palestinian conflict by far · the trajectory on both sides resembles nothing less than full national erasure",
            "A rare phase when a conflict that has ossified for generations briefly loses its fixed shape · Israelis and Palestinians alike must seize it",
            "One point of consensus cuts across both nations, regardless of ideology: the status quo is unacceptable",
            "Like it or not, Donald Trump is uniquely positioned: the political legitimacy, institutional leverage, and force of personality to impose a decisive end to the war"], 38),
        "The close")

@slide
def rubble():
    return section("rubble", head("🧱", "The close · Hamas and the Palestinian people", "What’s the worth of ruling over nothing but rubble?", ts=74) +
        ul(["Palestinian steadfastness has always been about remaining on the land under overwhelming pressure",
            "Gaza has been reduced to rubble, and the Palestinian national project remains on its deathbed, despite unprecedented popular support for its liberation movement",
            "The international community will not finance the rebuilding of a territory governed by a people who are structurally committed to another catastrophe",
            "The Virtuous City Vision affirms the Arab-Islamic nature of the Gaza Strip while engaging the West without capitulation or secular erasure"], 36) +
        coda("If Hamas seeks a future beyond governing ruins, endorsing the Virtuous City Vision is the most coherent path available to transform resistance into political survival, dignity, and renewal.", 36),
        "The close")

@slide
def two_state():
    return section("two-state", head("🗺️", "The close · the so-called two-state solution", "No illusions, and no abandonment") +
        row(card("No illusions", "In every version ever proposed, a Palestinian “state” is better understood as an autonomy framework with constrained sovereignty, foreign dependencies, and permanent infringements on security · a century of trauma will not dissolve because borders are redrawn", bs=34),
            card("Abandoning it would be a strategic error", "A credible pathway toward Palestinian self-governance remains the only long-term political horizon capable of anchoring Israel’s regional integration, stabilizing the Holy Land, and reducing the perpetual existential insecurity of Jewish and Palestinian life", bs=34, gold=True)),
        "The close", gap=44)

@slide
def wager_1948():
    return section("wager-1948", head("✡️", "The close · Israel’s founding imagination", "The moral wager of 1948") +
        p("The moral wager was that Israel would become a legitimate state for the safety and security of the Jewish people, and not a messianic engine of hegemony that hardens the region and world against its trajectory.", 46) +
        coda("The Virtuous City Vision, while centered on Gaza, attempts to revive and modernize the alternative trajectory embedded in Israel’s own founding imagination, including Ben-Gurion’s openness to regional federation and binational or confederal horizons with the Arabs.", 38),
        "The close", gap=40)

@slide
def decisive():
    inner = (f'<div style="flex:1"></div>' +
             p("What is proposed here does not ask Israelis or Palestinians to pretend that history can be undone, identities dissolved, or grievances erased.", 50, color=GREY) +
             h2("It asks only that the war end decisively.", 100) +
             p("Periodic wars punctuated by brief ceasefires are morally and strategically unacceptable.", 46, italic=True, color=GOLDL) + f'<div style="flex:1"></div>')
    return section("decisive", inner, "The close", bg=DARK, gap=40, justify="start")

@slide
def close():
    inner = (f'<div style="flex:1"></div>' +
             p("If there is any unifying truth left after these three years of devastation, it is this:", 48, color=GREY, italic=True) +
             h2("the planetary devastation that we have all borne in our nervous systems must never occur again.", 92) + f'<div style="flex:1"></div>')
    return section("close", inner, BRAND, bg=DARK, gap=40, justify="start")

@slide
def p_close():
    inner = (f'<div style="flex:1"></div>' + h2("It asks only that the war end decisively.", 96) +
             p("If there is any unifying truth left after these three years of devastation, it is this: the planetary devastation that we have all borne in our nervous systems must never occur again.", 48) +
             f'<div style="flex:1"></div>' + p(f"Full deck and sources · {a('dhanna11.github.io/virtuous-city-vision/full.html', SITE + 'full.html')}", 28, font=SANS, color=GOLDD))
    return section("p-close", inner, BRAND, bg=DARK, gap=40, justify="start")

@slide
def references():
    src = [(FARABI.replace("’s", "") , "Abu Nasr Muhammad Al-Farabi, a lecture (YouTube)"),
           (OPINIONS, "Al-Farabi, translated as <i>The Perfect State</i>"),
           (a("“Israel’s Decisive Plan”", "https://hashiloach.org.il/israels-decisive-plan/"), "Bezalel Smotrich, <i>HaShiloach</i>"),
           (FROMAN, "Wikipedia"), (YASSIN, "Wikipedia")]
    rows = "".join(f'<li>{t} <span style="color:{GREY}">· {d}</span></li>' for t, d in src)
    named = "Named in the text: Raphael Lemkin, <i>Axis Rule in Occupied Europe</i> · President Trump’s 20-point plan for Gaza (Point 18) · the Board of Peace Charter (Article 3) · the Abraham Accords"
    return section("references", head("📚", "References", "Sources named in the plan", ts=72) +
        f'<ul style="font-family:{SANS}; font-size:{px(34)}; color:{PAPER}; line-height:1.4; padding:0 0 0 40px; display:flex; flex-direction:column; gap:8px">{rows}</ul>' +
        p(named, 30, font=SANS, color=GREY, lh=1.4) +
        p(f"The full text: {a('the plain-text edition', SITE + 'virtuous-city-vision.md')} · © 2026 David Hanna Jr. · text and design licensed CC BY 4.0 · quoted material and sources belong to their authors", 24, font=SANS, color=GOLDD, lh=1.4),
        "References", gap=28, justify="start")

# ---------------------------------------------------------------- pitch-only slides
@slide
def p_telos():
    return section("p-telos", head("📜", "1 · The telos", "The Virtuous City of Gaza") +
        ul([f"{FARABI} {OPINIONS}: the singular spiritual template for Gaza’s rebirth",
            "One supreme purpose: to enable every inhabitant to attain true happiness (sa’ada)",
            "Gaza’s modern political identity has been defined almost entirely by resistance, survival, and siege · the Virtuous City redefines that horizon toward human flourishing",
            "It defines what the polity is for, not how it is governed · the mechanics of governance are those of modern democracy"], 40) +
        coda("Without a clear telos, security architectures default to mere conflict management. With it, Gaza’s reconstruction becomes a civilizational project rather than a humanitarian holding pattern.", 36),
        "The telos")

@slide
def p_board():
    c = lambda n, t, b: card(f"{n} · {t}", b, ls=28, bs=32, body_font=SANS)
    return section("p-board", head("🕊️", "2 · The Board of Peace", "Three discordances and a coalition") +
        row(c(1, "Mandate", "a Gaza-first framing against a Charter with global scope"), c(2, "Composition", "the UK, France, Germany, and the Vatican refuse to join"),
            c(3, "Foundation", "no explicit philosophical and reconciliation substrate")) +
        flow([("Globe", "The Board of Peace incubates"), ("Users", "The Coalition for Canaan"), ("Trust", "An independent guarantor body")]),
        "The Board of Peace", gap=36)

@slide
def p_demil():
    return section("p-demil", head("🛡️", "4 · Demilitarization", "One Authority, One Law, One Weapon") +
        row(card("Armed factions relinquish", "independent coercive power as occupation recedes · a pathway into ordinary political life, and into civilian life for those who demobilize", bs=38),
            card("The settlement provides", "phased Israeli withdrawal · credible regional and international security guarantees · an enforceable pathway to self-determination and statehood", bs=38, gold=True)) +
        p("A demilitarized people under continuing occupation is not at peace but simply defenseless.", 40, italic=True, color=GREY) +
        coda("Nobody disarms without a future.", 56),
        "Demilitarization")

@slide
def p_movement():
    return section("p-movement", head("🚪", "5 · Palestinian freedom of movement", "Protection for those who remain, a choice for those who leave", ts=72) +
        row(card("Temporary evacuation", "for the injured, the chronically ill, families with children, and those at risk · voluntary, protective, and reversible, with best-effort rights of return", bs=36),
            card("Asylum", "permanent resettlement abroad, through binding commitments by coalition member states, monitored by the Board of Peace", bs=36)) +
        coda("No people should be forcibly confined to a devastated enclave after mass destruction.", 42),
        "Freedom of movement")

@slide
def p_economy():
    c = lambda e, t, b, g=False: card(t, b, e=e, ls=26, bs=33, gold=g)
    return section("p-economy", head("🏗️", "6 · Reconstruction", "Gaza must be rebuilt by Palestinians themselves") +
        row(c("👷", "Palestinian Labor Movement", "non-partisan · absorbs, preserves, and redeploys displaced Palestinian human capital", True),
            c("📝", "A US–PA compact", "a Compact of Free Association-style agreement: the legal basis for the American reconstruction vision"),
            c("🏦", "A Reconstruction Custodian", "an Arab state, the UAE or Saudi Arabia, to lead Arab and Islamic investment"),
            c("💰", "A Trust Fund", "a portion of Iranian frozen assets, matched by members of the Board of Peace"), gap=18),
        "Reconstruction", gap=44)

@slide
def p_west_bank():
    return section("p-west-bank", head("🫒", "7 · The West Bank", "A Holy Land Trust") +
        row(card("Easements", "internationally funded, over contiguity-critical parcels", bs=38), card("Use payments", "from Israel, held in escrow, over the registered footprint of settlements", bs=38)) +
        p("Empty land shall remain empty. Built land shall remain limited to its registered footprint.", 48, color=GOLDL) +
        coda("A pragmatic compromise to keep the two-state horizon on its deathbed rather than consigning it to the dustbin of history.", 38),
        "The West Bank")

# ================================================================ v2 (5 Oct 2026): the architecture image
# The author's architecture diagram ("The Virtuous City Vision: A Geopolitical Architecture") regroups the plan into six
# blocks and adds detail. The draft text wins where they conflict; the image's detail is added where it does not.
def ul2(items, fs=28):   # compact list inside a card
    return ul(items, fs, font=SANS)

@slide
def arc():
    c = lambda e, t, b, g=False: card(t, b, e=e, ls=26, bs=27, body_font=SANS, gold=g)
    return section("arc", head("🧭", "The architecture", "The Virtuous City Vision: a geopolitical architecture", ts=74, tc=PAPER) +
        row(c("⏳", "Coalition continuity", "0–2 years Board of Peace incubation · 0–10 coalition of the willing · 10–20 alliance model · 20–30 voluntary confederation"),
            c("🤝", "Coalition core", "the Board of Peace incubates the Coalition for Canaan · a Virtuous City Convention · economic, humanitarian, and peace and security guarantees", True),
            c("📚", "Education & reconciliation", "the House of Wisdom and Peace · the Multiple Truths, Reconciliation and Prosperity Framework"), gap=18) +
        row(c("🛡️", "Security & stabilization", "demilitarization and DDR · the ISF · West Bank joint patrols · support for Israeli disengagement"),
            c("🏦", "Arab partners & trust funds", "Egypt as security anchor · a Reconstruction Custodian · the Virtuous City Trust Fund · the Holy Land Trust"),
            c("🏛️", "Governance & economy", "the telos and a new social contract · the Virtuous City Council · an economic plan · the Palestinian Labor Movement"), gap=18),
        "The core thesis", gap=24)

@slide
def social_contract():
    return section("social-contract", head("🤲", "The telos · a new social contract", "The Virtuous City of Gaza’s telos and new social contract", ts=72) +
        ul(["Inspired by Palestinian education as resistance and al-Farabi’s Virtuous City",
            "Intellectual, moral, and spiritual renewal",
            "Reconstruction of the Palestinian mind, body, and soul"], 48) +
        coda("Transform collective suffering into collective flourishing.", 52),
        "The telos", gap=40)

@slide
def incubator():
    return section("incubator", head("🥚", "Coalition core · the Board of Peace", "An incubator, not an indefinite administrator") +
        flow([("Globe", "The Board of Peace: strategic direction and legitimacy"), ("Users", "A coalition of the willing, tailored to the Gaza conflict"), ("Trust", "An independent guarantor body")]) +
        ul(["The discordances do not require abandoning the Board of Peace · they require clarifying its structural role",
            "It authorizes, creates, and shepherds the Coalition for Canaan, consistent with Article 3 of the Board of Peace Charter",
            "It should not administer Gaza indefinitely beyond its authorized two-year mandate · it spins the coalition off at the end of its UN Security Council mandate",
            "A structural pathway for states reluctant to join the Board as currently conceived"], 36),
        "")

@slide
def convention():
    return section("convention", head("📜", "Coalition core · the Virtuous City Convention", "A founding assembly to conclude the war", ts=78) +
        ul(["The founding assembly where the Virtuous City Vision will be debated, refined, and ratified by all parties",
            "The moral and political terminus of the war",
            "It establishes a new geopolitical order grounded in wisdom, justice, dignity, and the shared pursuit of peace"], 48) +
        coda("The war is concluded through the Convention, in the Board of Peace incubation phase (0–2 years).", 40),
        "", gap=40)

@slide
def mandate():
    return section("mandate", head("🖐️", "The Coalition for Canaan", "The Five-Point Mandate", ts=96) +
        row(*[card(f"{i+1} · {t}", b, e=e, ls=26, bs=36) for i, (e, t, b) in enumerate(MANDATE)], gap=18) +
        coda("A focused, semi-independent guarantor bloc and a 10+ year coalition of the willing, incubated and initially shepherded by the Board, for the broader Israeli–Palestinian conflict", 36),
        "", gap=40)

@slide
def guarantees():
    c = lambda e, t, xs, g=False: card(t, ul2(xs, 28), e=e, ls=26, gold=g)
    return section("guarantees", head("🔐", "The Coalition for Canaan · what it guarantees", "Three sets of guarantees") +
        row(c("🏗️", "Economic & reconstruction", ["A fully funded rebuild of Gaza", "Long-term economic integration of Israel and Palestine into the Middle East and the global economy",
                                                "Favorable trade and investment conditions: a pathway to lasting wisdom, peace, and prosperity"]),
            c("🩺", "Humanitarian", ["Palestinian freedom of movement: the right to stay, leave, resettle, and return", "Guaranteed by the Coalition and binding international law",
                                      "Healthcare infrastructure reconstruction"], True),
            c("🛡️", "Peace & security", ["Assurances for ceasefire adherence", "Mediation, peacekeeping, and coalition deconfliction", "Time-limited universal asylum",
                                          "Protection of humanitarian corridors under international mandate", "Forward progress on the two-state solution"]), gap=18),
        "", gap=36)

@slide
def timeline_():
    c = lambda t, xs, g=False: card(t, ul2(xs, 25), ls=24, gold=g, extra="; gap:10px")
    return section("timeline", head("⏳", "3 · Coalition continuity · the generational timeline", "Roughly 30 years: an incubation and three phases", ts=68) + timeline(4, 0) +
        row(c("0–2 years · Board of Peace incubation", ["Conclude the war via the Virtuous City Convention", "Deploy the ISF security mandate", "Fund and launch Gaza pilots",
                                                         "Activate NCAG governance", "Execute initial DDR and disengagement", "Formalize the Coalition for Canaan"], True),
            c("0–10 years · coalition of the willing · stabilization", ["Full-scale demilitarization and infrastructure rebuild", "Establish the transitional government",
                                                                         "Support PA reforms toward statehood", "Complete IDF disengagement from Gaza"]),
            c("10–20 years · alliance model · integration", ["Deepen Palestinian self-governance", "Support for Palestinian state recognition", "Abraham Accords expansion",
                                                              "Reconciliation and educational frameworks", "Easing of movement restrictions", "Initial Israeli disengagement from the West Bank"]),
            c("20–30 years · voluntary confederation · full maturity", ["Full mutual state recognition", "Full integration of Israel, Palestine, and the wider Middle East",
                                                                         "Full implementation of the reconciliation frameworks", "Full freedom of movement", "Final border demarcation and complete Israeli military withdrawal"]), gap=16) +
        p("Each phase after the incubation is an optional expanded mandate.", 28, font=SANS, color=GREY),
        "", gap=20)

@slide
def ddr():
    return section("ddr", head("🔧", "Security & stabilization · DDR", "Disarmament, demobilization, and reintegration", ts=74) +
        row(card("", ul2(["A hudna recognizing the Palestinian right of self-defense against indefinite occupation",
                          "PLO institutional reform: an adaptation of the “ballot or the bullet” doctrine",
                          "Interim, coalition-verified manpower caps for resistance factions",
                          "Trade guns for the Labor Movement Reconstruction Corps"], 34)),
            card("", ul2(["PA-assisted disarmament",
                          "UXO disposal and offensive weapons prioritization",
                          "Safe passage to coalition states, with security guarantees"], 34))),
        "", gap=40)

@slide
def isf():
    c = lambda e, t, xs, g=False: card(t, ul2(xs, 30), e=e, ls=26, gold=g)
    return section("isf", head("🌐", "Security & stabilization · the International Stabilization Force", "The ISF, in Gaza and the West Bank", ts=76) +
        row(c("🪖", "The ISF", ["A UN and Board of Peace mandate", "American-led, with an Indonesian deputy", "Deploys and supports coalition-trained Palestinian forces in Gaza", "A West Bank pilot"], True),
            c("🤝", "West Bank joint patrols", ["Integrated patrols with the IDF, the ISF, and Palestinian Authority forces"]),
            c("↩️", "Israeli West Bank disengagement", ["Assisting the IDF and the PA during a phased Israeli withdrawal from the West Bank"]), gap=18) +
        p("Each step beyond the ISF is an optional expanded mandate.", 28, font=SANS, color=GREY),
        "", gap=36)

@slide
def movement():
    return section("movement", head("🚪", "5 · Palestinian freedom of movement", "A genuine choice for those who wish to leave") +
        p("No people should be forcibly confined to a devastated enclave after mass destruction. Ending cycles of genocidal violence requires not only protection for those who remain, but a genuine choice for those who wish to leave.", 40) +
        ul(["The right to stay, leave, resettle, and return · guaranteed by the Coalition and binding international law",
            "The Coalition will negotiate, coordinate, and ensure pathways for asylum, temporary evacuation, and voluntary relocation during the reconstruction period",
            "Debated transparently and implemented through binding commitments by coalition member states · not left to ad hoc charity or discretionary border policies"], 34, color=GREY),
        "")

@slide
def egypt():
    return section("egypt", head("🛡️", "6 · Arab partners & trust funds · the security anchor", "Egypt") +
        ul(["Border integrity and security coordination with the ISF",
            "Mediation between Palestinian factions",
            "Primary trainer of the new Gazan police force",
            "Supporting the long-term Gaza demilitarization framework"], 48) +
        coda("Egypt serves as the principal regional security anchor.", 44),
        "", gap=40)

@slide
def custodian():
    return section("custodian", head("🏦", "Arab partners & trust funds · the Reconstruction Custodian", "Without Arab capital, Gaza will not be rebuilt", ts=72) +
        p("At least one Arab state designated as the primary Reconstruction Custodian for the Gaza Strip: partnering with the transitional government to lead fundraising and investment by the Arab and Islamic world, and serving as the Arab world’s point woman for sustaining Gaza’s revival.", 34) +
        row(card("The United Arab Emirates", "currently the most suitable candidate, given its humanitarian contributions to Gaza and its relations with the United States, Egypt, and Israel", bs=31, gold=True),
            card("Saudi Arabia", "could also fill this role, creating a pathway toward normalization tied directly to the broader Israeli-Palestinian process", bs=31)) +
        ul(["Supports the security coordinator · assists the PA with reconstruction fundraising",
            "Modernization and educational revival · Arab accountability to operationalize PA reforms"], 30, color=GREY),
        "", gap=28)

@slide
def assets():
    return section("assets", head("💰", "Arab partners & trust funds · the central financing pillar", "The Virtuous City Trust Fund") +
        ul(["Managed by the Board of Peace (and the Palestinian Authority after reforms) and the World Bank, with assistance from the Reconstruction Custodian",
            "Seed funding from a portion of repurposed Iranian frozen assets, matched by members of the Board of Peace",
            "These assets roughly align in scale with the cost of rebuilding Gaza: one of the few existing capital pools capable of underwriting reconstruction at the necessary scale",
            "Anchors the economic foundation of the Virtuous City Vision · pools donor contributions and drives global fundraising",
            "It could emerge within a broader diplomatic framework focused on ending the 2026 Iran War"], 37),
        "")

@slide
def holy_land_trust():
    return section("holy-land-trust", head("🫒", "7 · The West Bank", "A Holy Land Trust for the occupied West Bank") +
        p("Established by the Board of Peace to preserve a viable pathway toward Palestinian self-governance, uphold the Coalition’s moral and political mandate, and enable deeper normalization with Syria and Lebanon.", 42) +
        ul(["Designed from inception as a framework expandable, as conditions permit, to other Israeli-occupied territories within a broader regional settlement framework",
            "A model expandable to the Golan Heights and Southern Lebanon",
            "It maintains a pathway for Arab–Israeli normalization, guaranteed by the Board of Peace"], 36, color=GREY),
        "", gap=36)

@slide
def council():
    return section("council", head("🏛️", "8 · Governance & economy · the Virtuous City Council", "The Virtuous City Council") +
        p("The rebranded National Committee for the Administration of Gaza (NCAG).", 52) +
        ul(["NCAG governance is activated in the Board of Peace incubation phase",
            "The Palestinian Labor Movement liaises with the NCAG and the Board of Peace"], 42, color=GREY) +
        coda("The telos defines what the polity is for, not how it is governed: the mechanics of governance are those of modern democracy.", 40),
        "", gap=40)

@slide
def econ_plan():
    return section("econ-plan", head("📈", "Governance & economy · the plan", "The Virtuous City Economic Plan") +
        ul(["The Palestinian Authority’s 56 Gaza Recovery and Reconstruction Programs",
            "A Compact of Free Association (COFA) with the United States and the PA for trade, education, and IMEC corridor integration",
            "A humanitarian air and seaport, built from rubble",
            "A Land & Property Preservation and Compensation Unit (the PA Land Registry)",
            "Development of Gaza Marine"], 44),
        "")

@slide
def compact():
    return section("compact", head("📝", "Governance & economy · the United States", "A Compact of Free Association-style agreement", ts=74) +
        ul(["The United States must play a central role in financing and supporting Gaza’s economic revitalization",
            "A proto-compact between the United States and the Palestinian Authority: a legal basis for the American reconstruction vision for Gaza",
            "A pathway to integrate Gaza into global markets while preserving Palestinian agency, dignity, and self-determination",
            "The option to evolve into a full compact upon formal recognition of Palestinian statehood"], 42),
        "")

@slide
def labor():
    return section("labor", head("👷", "Governance & economy · Palestinian labor", "Gaza must be rebuilt by Palestinians themselves") +
        ul(["A non-partisan Palestinian Labor Movement, fostered by the Board and Coalition, to absorb, preserve, and redeploy displaced Palestinian human capital",
            "Centering Palestinian labor agency is the clearest check against reconstruction that erodes local ownership and political autonomy",
            "Building on existing Palestinian labor institutions, outside factional politics during the transition",
            "Workers, engineers, teachers, healthcare professionals, civil servants, and demobilized fighters who renounce armed violence · the Palestinian Authority’s reconstruction program as its baseline"], 38),
        "")

@slide
def labor_transition():
    return section("labor-transition", head("🔨", "Governance & economy · the Palestinian Labor Movement (transitional)", "Rebuilding as resistance", ts=84) +
        row(card("", ul2(["A non-electoral labor and civic institution during the stabilization phase",
                          "Led by civil society: technocrats, educators, and labor leaders",
                          "Recycle Gaza’s human capital without de-Ba’athification",
                          "Integrate the civil service and a civilianized police under oversight"], 32)),
            card("", ul2(["Organize the native Gazan workforce for reconstruction",
                          "Workforce training programs with Board of Peace and coalition contractors",
                          "Anchor Palestinian agency against neocolonial dynamics",
                          "Later evolution into a formal Labor Party once stabilization is achieved"], 32))),
        "", gap=40)

@slide
def fw_phylogeny():
    return section("fw-phylogeny", head("🧬", "Frameworks · 3 of 5", "Shared Canaanite ethnogenesis") +
        ul(["An anthropological rehumanization framework that acknowledges the shared ethnogenesis of the Israeli and Palestinian nations, rooted in the Land of Canaan: a shared Bronze-Age Levantine ethnogenesis",
            "Recognizing divergence, admixture, and other complexities",
            "Without adjudicating modern indigeneity, sovereignty, religion, or national identity",
            "Highly contested in both nations · contention over claims of indigeneity and sovereignty will not be eliminated"], 40),
        "")

@slide
def fw_judeo_islamic():
    return section("fw-judeo-islamic", head("📜", "Frameworks · 4 of 5", "The Formal Establishment of the Judeo-Islamic Tradition", ts=74) +
        ul(["Formalizing the shared philosophical, theological, and intellectual heritage of Jews and Muslims",
            "The very milieu in which the Virtuous City emerged",
            "A Judeo-Islamic core: peace frameworks rooted in shared theology, history, and Sharia and Halakha law, with the Froman–Yassin dialogue as a basis",
            "A buried civilizational overlap that can be taught without forcing theological merger or political surrender"], 42),
        "")

@slide
def fw_abrahamic():
    return section("fw-abrahamic", head("🤝", "Frameworks · 5 of 5", "The Formal Establishment of the Broader Abrahamic Tradition", ts=74) +
        ul(["A universal umbrella for past, current, and future interfaith initiatives and peace covenants, with shared educational programs",
            "Covenants of coexistence, restraint, and mutual recognition among Jews, Muslims, and Christians",
            "Especially around contested holy sites, where sanctity must once again become covenant"], 42) +
        coda("Both traditions belong within the Abraham Accords: extending normalization beyond diplomatic recognition into structured civilizational, educational, and religious reconciliation architecture.", 36),
        "")

@slide
def multiple_truths():
    return section("multiple-truths", head("🕌", "Rehumanization · the framework", "Multiple Truths, Reconciliation and Prosperity", ts=76) +
        ul(["A pan-Arab rebuild of the Bayt al-Hikmah in Gaza: the economic heart of the Virtuous City and the top educational center in the Middle East",
            "Multilateral holy site custodianship, with the relevant Coalition members and religious stakeholders",
            "Acknowledgments for justice: nation-state creation, imperialism, colonialism, genocides, the Nakba",
            "English as the de jure lingua franca"], 42) +
        coda("It grows out of the House of Wisdom and Peace, as an optional expanded mandate.", 38),
        "")

@slide
def house():
    return section("house", head("🏛️", "10 · The House of Wisdom and Peace", "The Board of Peace’s keystone initiative") +
        p("Not a cultural side-project or an NGO vanity mission, but the intellectual anchor of the Virtuous City Vision.", 44, italic=True) +
        ul(["This is where Truth and Reconciliation work must actually live",
            "The originating institution for the educational and interfaith reconciliation frameworks",
            "Where scholars, clerics, educators, and civic leaders formally develop the curricula, covenants, and shared moral language needed to seed peace across generations"], 38) +
        coda("Without an intellectual engine that can produce and legitimize reconciliation frameworks, Israelis and Palestinians will relapse into internecine conflict.", 38),
        "")

@slide
def house_pilots():
    return section("house-pilots", head("🎒", "The House of Wisdom and Peace · the initiative", "Pilots, schools, and a protected public square", ts=76) +
        row(card("Pilot projects", "for the rebuild of educational infrastructure", e="🏫", bs=40),
            card("Every child", "school materials, laptops, and lunch, guaranteed by the Coalition", e="🍎", bs=40, gold=True),
            card("Voices of the Virtuous City", "a protected social media platform to debate the future direction of Gaza", e="📣", bs=40)),
        "", gap=44)

# pitch
@slide
def p_board():
    c = lambda n, t, b: card(f"{n} · {t}", b, ls=28, bs=32, body_font=SANS)
    return section("p-board", head("🕊️", "2 · Coalition core", "Three discordances and a coalition") +
        row(c(1, "Mandate", "a Gaza-first framing against a Charter with global scope"), c(2, "Composition", "the UK, France, Germany, and the Vatican refuse to join"),
            c(3, "Foundation", "no explicit philosophical and reconciliation substrate")) +
        flow([("Globe", "The Board of Peace incubates"), ("Users", "The Coalition for Canaan"), ("Trust", "An independent guarantor body")]) +
        p("A Virtuous City Convention, the founding assembly where the Vision is debated, refined, and ratified by all parties, concludes the war.", 32, font=SANS, color=GREY),
        "", gap=32)

@slide
def p_demil():
    return section("p-demil", head("🛡️", "4 · Security & stabilization", "One Authority, One Law, One Weapon") +
        row(card("Armed factions relinquish", "independent coercive power as occupation recedes · a hudna, PLO reform, and guns traded for the Labor Movement Reconstruction Corps", bs=36),
            card("The settlement provides", "phased Israeli withdrawal · credible regional and international security guarantees · an enforceable pathway to self-determination and statehood", bs=36, gold=True)) +
        p("A demilitarized people under continuing occupation is not at peace but simply defenseless.", 40, italic=True, color=GREY) +
        coda("Nobody disarms without a future.", 56),
        "")

@slide
def p_arab():
    c = lambda e, t, b, g=False: card(t, b, e=e, ls=28, bs=36, gold=g)
    return section("p-arab", head("🏦", "6 · Arab partners & trust funds", "Without Arab capital, Gaza will not be rebuilt") +
        row(c("🛡️", "Egypt · the security anchor", "border integrity, mediation between factions, and the primary trainer of the new Gazan police force"),
            c("🏗️", "A Reconstruction Custodian", "the UAE or Saudi Arabia, leading Arab and Islamic investment and Arab accountability for PA reforms", True),
            c("💰", "The Virtuous City Trust Fund", "the Board of Peace and the World Bank, seeded by repurposed Iranian frozen assets")),
        "", gap=44)

@slide
def p_economy():
    c = lambda e, t, b, g=False: card(t, b, e=e, ls=26, bs=32, gold=g)
    return section("p-economy", head("🏛️", "8 · Governance & economy", "Gaza must be rebuilt by Palestinians themselves") +
        row(c("🏛️", "The Virtuous City Council", "the rebranded National Committee for the Administration of Gaza"),
            c("👷", "Palestinian Labor Movement", "non-partisan · absorbs, preserves, and redeploys displaced Palestinian human capital", True),
            c("📈", "The Economic Plan", "the PA’s 56 programs · a US–PA compact for trade, education, and IMEC · an air and seaport · Gaza Marine"),
            c("🔧", "DDR", "a hudna · interim manpower caps · safe passage · reintegration through the Labor Movement"), gap=18),
        "", gap=44)

# ================================================================ identity A (8 Oct 2026): cover, architecture rota, timeline
# Working translations, to be checked by native speakers (docs/design/README.md).
AR_TITLE = "إنهاء حرب غزة يجب أن يعيد إلينا إنسانيتنا"
HE_TITLE = "סיום המלחמה בעזה חייב להשיב לנו את אנושיותנו"
AR_CITY, HE_CITY = "المدينة الفاضلة", "העיר המעולה"
AR_SAADA, HE_SAADA = "السعادة", "האושר"

def wedge(cx, cy, r0, r1, a0, a1):
    pt = lambda r, ang: (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))
    x0, y0 = pt(r1, a0); x1, y1 = pt(r1, a1); x2, y2 = pt(r0, a1); x3, y3 = pt(r0, a0)
    return f"M{x0:.1f},{y0:.1f} A{r1},{r1} 0 0 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 0 0 {x3:.1f},{y3:.1f} Z"

@slide
def cover():
    divider_svg = (f'<svg aria-hidden="true" viewBox="0 0 400 40" style="width:400px; height:40px; align-self:center; flex:none"><line x1="0" y1="20" x2="170" y2="20" stroke="{GOLD}" stroke-width="2"/>'
                   f'<polygon points="{star8(200, 20, 16, 9)}" fill="{TERRA}"/><line x1="230" y1="20" x2="400" y2="20" stroke="{GOLD}" stroke-width="2"/></svg>')
    inner = (f'<div style="flex:1"></div>'
             f'<p dir="rtl" lang="ar" style="font-family:{AR}; font-size:64px; color:{GOLDL}; line-height:1.25; text-align:center">{AR_CITY}</p>'
             f'<p style="font-family:{SERIF}; font-size:26px; font-weight:500; letter-spacing:10px; color:{TERRA}; text-align:center">THE VIRTUOUS CITY VISION</p>'
             f'<p dir="rtl" lang="he" style="font-family:{HE}; font-size:54px; color:{GOLDL}; line-height:1.25; text-align:center">{HE_CITY}</p>'
             + divider_svg +
             f'<h1 style="font-family:{SERIF}; font-size:108px; font-weight:500; color:{PAPER}; line-height:1.04; text-align:center; text-wrap:balance">Ending the Gaza War Must Restore Our Humanity</h1>'
             f'<p dir="rtl" lang="ar" style="font-family:{AR}; font-size:36px; color:{GREY}; line-height:1.35; text-align:center">{AR_TITLE}</p>'
             f'<p dir="rtl" lang="he" style="font-family:{HE}; font-size:32px; color:{GREY}; line-height:1.3; text-align:center">{HE_TITLE}</p>'
             f'<div style="flex:1"></div>'
             f'<p style="font-family:{SERIF}; font-size:34px; font-style:italic; color:{TERRA}; text-align:center">David Hanna Jr. · Unofficial · a private author’s proposal · October 2026</p>')
    return section("cover", inner, "", gap=14, justify="start")

@slide
def arc():
    cx, cy = 500, 560; out = []
    cols = [GOLDL, TERRA, GOLD, GOLDL, TERRA, GOLD]
    names = [n for n, _ in ARCH]
    for i, name in enumerate(names):
        a0, a1 = -90 + i * 60 + 2, -90 + (i + 1) * 60 - 2
        out.append(f'<path d="{wedge(cx, cy, 165, 380, a0, a1)}" fill="{cols[i]}" fill-opacity=".1" stroke="{cols[i]}" stroke-width="2.5"/>')
        am = math.radians((a0 + a1) / 2); tx, ty = cx + 272 * math.cos(am), cy + 272 * math.sin(am)
        words = name.split(" "); half = (len(words) + 1) // 2
        lines = [" ".join(words[:half]), " ".join(words[half:])] if len(words) > 1 else [name]
        out.append(f'<text x="{tx:.0f}" y="{ty - (len(lines) - 1) * 17 + 8:.0f}" text-anchor="middle" font-family="EB Garamond" font-size="30" font-weight="600" fill="{PAPER}">' +
                   "".join(f'<tspan x="{tx:.0f}" dy="{0 if k == 0 else 34}">{l}</tspan>' for k, l in enumerate(lines)) + '</text>')
        nx, ny = cx + 412 * math.cos(am), cy + 412 * math.sin(am)
        out.append(f'<circle cx="{nx:.0f}" cy="{ny:.0f}" r="21" fill="{BG}" stroke="{cols[i]}" stroke-width="2"/><text x="{nx:.0f}" y="{ny + 8:.0f}" text-anchor="middle" font-family="EB Garamond" font-size="25" font-weight="700" fill="{cols[i]}">{i + 1}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="148" fill="{BG}" stroke="{GOLD}" stroke-width="3"/>')
    out.append(f'<polygon points="{star8(cx, cy, 138, 102)}" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
    out.append(f'<text x="{cx}" y="{cy - 32}" text-anchor="middle" font-family="Amiri" font-size="46" fill="{GOLDL}">{AR_SAADA}</text>')
    out.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-family="EB Garamond" font-size="34" font-weight="600" fill="{PAPER}">The telos</text>')
    out.append(f'<text x="{cx}" y="{cy + 58}" text-anchor="middle" font-family="Frank Ruhl Libre" font-size="36" fill="{GOLDL}">{HE_SAADA}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="436" fill="none" stroke="{RULE}" stroke-width="1.5" stroke-dasharray="4 8"/>')
    legend = "".join(f'<div style="display:flex; gap:18px; align-items:baseline; border-top:1px solid {RULE}; padding:8px 0">'
                     f'<span style="font-family:{SERIF}; font-size:28px; font-weight:700; color:{cols[i]}; width:26px; flex:none">{i + 1}</span><div><p style="font-family:{SERIF}; font-size:30px; font-weight:600; color:{PAPER}; line-height:1.1">{n}</p>'
                     f'<p style="font-family:{SERIF}; font-size:21px; color:{GREY}; line-height:1.25; margin-top:3px">{d}</p></div></div>' for i, (n, d) in enumerate(ARCH))
    inner = (f'<svg class="xf" aria-label="The six blocks of the architecture around the telos" viewBox="0 0 1920 1080" style="position:absolute; left:0; top:0; width:1920px; height:1080px">{"".join(out)}</svg>'
             f'<div style="margin-left:860px; display:flex; flex-direction:column">'
             f'{kick("The architecture", 26)}<h2 style="font-family:{SERIF}; font-size:58px; font-weight:500; color:{PAPER}; line-height:1.05; margin:10px 0 8px">Six organs of one healthy body</h2>'
             f'<p style="font-family:{SERIF}; font-size:25px; font-style:italic; color:{GOLDL}; line-height:1.3; margin-bottom:12px">“each part of society functioning harmoniously, like organs in a healthy body” · Al-Farabi</p>'
             f'{legend}</div>')
    return section("arc", inner, "", gap=0)

ARCH = [("Coalition core", "The Board of Peace incubates the Coalition for Canaan · the Virtuous City Convention · three sets of guarantees"),
        ("Coalition continuity", "0–2 years incubation · 0–10 coalition of the willing · 10–20 alliance model · 20–30 voluntary confederation"),
        ("Security & stabilization", "Demilitarization and DDR · the ISF · West Bank joint patrols · support for Israeli disengagement"),
        ("Arab partners & trust funds", "Egypt as security anchor · a Reconstruction Custodian · the Virtuous City Trust Fund · the Holy Land Trust"),
        ("Governance & economy", "The telos and a new social contract · the Virtuous City Council · the Economic Plan · the Palestinian Labor Movement"),
        ("Education & reconciliation", "The House of Wisdom and Peace · the Multiple Truths, Reconciliation and Prosperity Framework")]

TIMELINE = [  # (start, end, name, sub, milestones)
    (0, 2, "Board of Peace incubation", "", ["Conclude the war via the Virtuous City Convention", "Deploy the ISF security mandate", "Fund and launch Gaza pilots",
                                             "Activate NCAG governance", "Execute initial DDR and disengagement", "Formalize the Coalition for Canaan"]),
    (0, 10, "Coalition of the willing", "stabilization", ["Full-scale demilitarization and infrastructure rebuild", "Establish the transitional government",
                                                          "Support PA reforms toward statehood", "Complete IDF disengagement from Gaza"]),
    (10, 20, "Alliance model", "integration", ["Deepen Palestinian self-governance", "Support for Palestinian state recognition", "Abraham Accords expansion",
                                               "Reconciliation and educational frameworks", "Easing of movement restrictions", "Initial Israeli disengagement from the West Bank"]),
    (20, 30, "Voluntary confederation", "full maturity", ["Full mutual state recognition", "Full integration of Israel, Palestine, and the wider Middle East",
                                                          "Full implementation of the reconciliation frameworks", "Full freedom of movement", "Final border demarcation and complete Israeli military withdrawal"])]

@slide
def timeline_():
    """a Gantt over years 0-30: each phase a bar, its milestones listed beside it in two lines"""
    x0, y0, w, rowh = 150, 362, 1620, 150; k = w / 30; out = []
    cols = [TERRA, GOLDL, GOLD, GOLDL]
    for yr in range(0, 31, 5):
        x = x0 + yr * k
        dash = "none" if yr % 10 == 0 else "3 6"
        out.append(f'<line x1="{x:.0f}" y1="{y0 - 18}" x2="{x:.0f}" y2="{y0 + rowh * 4 - 30}" stroke="{RULE}" stroke-width="1" stroke-dasharray="{dash}"/>')
        out.append(f'<text x="{x:.0f}" y="{y0 - 30}" text-anchor="middle" font-family="EB Garamond" font-size="24" fill="{GREY}">{"year " if yr == 0 else ""}{yr}</text>')
    for i, (s_, e, name, sub, ms) in enumerate(TIMELINE):
        y = y0 + i * rowh; x = x0 + s_ * k; bw = (e - s_) * k; col = cols[i]
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="44" rx="22" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2.5"/>')
        right = s_ >= 15
        lx, anchor = (x + bw - 20, "end") if right else ((x + 20, "start") if bw > 400 else (x + bw + 22, "start"))
        out.append(f'<text x="{lx:.0f}" y="{y + 31}" text-anchor="{anchor}" font-family="EB Garamond" font-size="27" font-weight="600" fill="{PAPER}">{name}</text>')
        mx = x + bw if right else (x + 20 if bw > 400 else x + bw + 22)
        lines = [f"{s_}–{e} years" + (f" · {sub}" if sub else "")] + [" · ".join(ms[j:j + 2]) for j in range(0, len(ms), 2)]
        for j, line in enumerate(lines):
            out.append(f'<text x="{mx:.0f}" y="{y + 70 + j * 25}" text-anchor="{anchor}" font-family="EB Garamond" font-size="{21 if j else 22}" '
                       f'font-weight="{600 if j == 0 else 400}" font-style="{"italic" if j == 0 else "normal"}" fill="{col if j == 0 else GREY}">{line}</text>')
    inner = (f'<svg class="xf" aria-label="Timeline: an incubation and three phases over thirty years" viewBox="0 0 1920 1080" style="position:absolute; left:0; top:0; width:1920px; height:1080px">{"".join(out)}</svg>'
             f'<div style="display:flex; flex-direction:column; gap:10px">{kick("3 · Coalition continuity · the generational timeline", 26)}'
             f'<h2 style="font-family:{SERIF}; font-size:64px; font-weight:500; color:{PAPER}; line-height:1.05">Roughly 30 years: an incubation and three phases</h2>'
             f'<p style="font-family:{SERIF}; font-size:28px; font-style:italic; color:{GOLDL}">Each phase after the incubation is an optional expanded mandate.</p></div>')
    return section("timeline", inner, "", gap=0, justify="start")

@slide
def sec_telos():
    return divider("sec-telos", "📜", "1 · The telos", "The Telos of the Virtuous City of Gaza",
        f"{FARABI} {OPINIONS} is more than an obscure utopian text preserved under the patronage of a bygone Abbasid Emir · it is the singular spiritual template for Gaza’s rebirth", "The telos",
        ar=AR_CITY, he=HE_CITY)

# ================================================================ infographics (8 Oct 2026): flows, a schematic, a ladder, a Venn
# Labels are the slides' own words; nothing here adds numbers or claims.
def wrap(text, n):
    """split text into lines of at most ~n characters"""
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])

def stext(x, y, text, n, size=24, color=None, anchor="start", weight=400, italic=False, lh=1.25, halo=False):
    """multi-line SVG text: wrapped at ~n characters, first baseline at y"""
    color = color or PAPER
    tsp = "".join(f'<tspan x="{x:.0f}" dy="{0 if i == 0 else round(size * lh)}">{l}</tspan>' for i, l in enumerate(wrap(text, n)))
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="EB Garamond" font-size="{size}" font-weight="{weight}" '
            f'{"font-style=" + chr(34) + "italic" + chr(34) + " " if italic else ""}'
            f'{"stroke=" + chr(34) + "#f3ead6" + chr(34) + " stroke-width=" + chr(34) + "6" + chr(34) + " stroke-linejoin=" + chr(34) + "round" + chr(34) + " paint-order=" + chr(34) + "stroke" + chr(34) + " " if halo else ""}'
            f'fill="{color}">{tsp}</text>')

def sbox(x, y, w, h, stroke=None, top=None, fill=None):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or CARD}" stroke="{stroke or BORDER}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="4" fill="{top or GOLD}"/>')

def slabel(x, y, text, color=None, size=22, anchor="start"):
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="EB Garamond" font-size="{size}" font-weight="600" '
            f'letter-spacing="3" fill="{color or GOLDL}">{text.upper()}</text>')

def figure(w, h, body, label):
    return f'<svg role="img" aria-label="{label}" viewBox="0 0 {w} {h}" style="width:{w}px; height:{h}px; flex:none">{body}</svg>'

@slide
def assets():
    out = []
    srcs = [("Seed funding", "A portion of repurposed Iranian frozen assets"),
            ("Matching", "Matched by members of the Board of Peace"),
            ("Donors", "Donor contributions, pooled through global fundraising")]
    for i, (lab, txt) in enumerate(srcs):
        y = 20 + i * 160
        out.append(sbox(0, y, 470, 130, top=TERRA if i == 0 else GOLD))
        out.append(slabel(26, y + 40, lab, TERRA if i == 0 else GOLDL))
        out.append(stext(26, y + 76, txt, 38, 25))
        out.append(f'<path d="M470,{y + 65} C560,{y + 65} 560,{215 + (i - 1) * 50} 650,{215 + (i - 1) * 50}" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="12"/>')
    out.append(sbox(650, 90, 470, 260, stroke=TERRA, top=TERRA))
    out.append(stext(885, 150, "The Virtuous City Trust Fund", 30, 34, TERRA, "middle", 600))
    out.append(stext(885, 205, "Managed by the Board of Peace (and the Palestinian Authority after reforms) and the World Bank, with assistance from the Reconstruction Custodian", 40, 23, GREY, "middle"))
    out.append(f'<path d="M1120,215 L1212,215" stroke="{GOLDL}" stroke-opacity=".55" stroke-width="22"/><polygon points="1210,193 1244,215 1210,237" fill="{GOLDL}" fill-opacity=".8"/>')
    out.append(sbox(1250, 110, 414, 220, top=GOLDL))
    out.append(stext(1457, 170, "Gaza’s reconstruction", 30, 32, PAPER, "middle", 600))
    out.append(stext(1457, 222, "Anchors the economic foundation of the Virtuous City Vision", 32, 24, GREY, "middle"))
    return section("assets", head("💰", "Arab partners & trust funds · the central financing pillar", "The Virtuous City Trust Fund") +
        figure(1664, 500, "".join(out), "Money flows from three sources into the Virtuous City Trust Fund, then to Gaza’s reconstruction") +
        coda("These assets roughly align in scale with the cost of rebuilding Gaza · it could emerge within a broader diplomatic framework focused on ending the 2026 Iran War", 32),
        "", gap=26, justify="start")

def ledger_flow():
    """the Holy Land Trust's two ledgers as rows: the land, who pays, what it pays for, the rule; both end at a settlement"""
    out = []; bw, bh, gap, x0, y0, rowgap = 290, 212, 44, 0, 60, 46
    heads = ["The land", "Who pays", "What it pays for", "The rule"]
    rows = [(GOLDL, ["Empty land", "contiguity-critical parcels, on a defined map"],
                    ["International funds", ""],
                    ["Non-development easements", ""],
                    ["Empty land shall remain empty.", ""]),
            (TERRA, ["Built land", "existing settlements and outposts"],
                    ["Israel", "use payments, held in escrow"],
                    ["Use of the registered footprint", ""],
                    ["Built land shall remain limited to its registered footprint.", ""])]
    for j, h in enumerate(heads):
        out.append(slabel(x0 + j * (bw + gap) + bw / 2, 30, h, GREY, 24, "middle"))
    for i, (col, *cells) in enumerate(rows):
        y = y0 + i * (bh + rowgap)
        for j, (main, sub) in enumerate(cells):
            x = x0 + j * (bw + gap); last = j == 3
            out.append(sbox(x, y, bw, bh, stroke=col if last else None, top=col))
            if sub:
                n = len(wrap(main, 15)); m = len(wrap(sub, 20)); top = y + bh / 2 - (n * 39 + m * 32) / 2 + 30
                out.append(stext(x + bw / 2, top, main, 15, 34, PAPER, "middle", 600, False, 1.15))
                out.append(stext(x + bw / 2, top + n * 39 + 4, sub, 20, 26, GREY, "middle", 400, True, 1.2))
            else:
                n = len(wrap(main, 15))
                out.append(stext(x + bw / 2, y + bh / 2 - (n - 1) * 19 + 11, main, 15, 32, col if last else PAPER, "middle", 600, False, 1.15))
            if j < 3:
                ax = x + bw; ym = y + bh / 2
                out.append(f'<path d="M{ax + 6},{ym} L{ax + gap - 14},{ym}" stroke="{col}" stroke-width="3"/>'
                           f'<polygon points="{ax + gap - 16},{ym - 8} {ax + gap - 4},{ym} {ax + gap - 16},{ym + 8}" fill="{col}"/>')
    fx = x0 + 4 * (bw + gap) + 36; fy = y0; fh = 2 * bh + rowgap; fw = 1664 - fx; mid = fy + fh / 2
    for i in range(2):
        y = y0 + i * (bh + rowgap) + bh / 2; sx_ = x0 + 3 * (bw + gap) + bw
        out.append(f'<path d="M{sx_ + 6},{y} C{sx_ + 40},{y} {fx - 40},{mid} {fx - 12},{mid}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    out.append(f'<polygon points="{fx - 16},{mid - 9} {fx - 2},{mid} {fx - 16},{mid + 9}" fill="{GOLD}"/>')
    out.append(sbox(fx, fy, fw, fh, stroke=GOLD, top=GOLD))
    out.append(f'<polygon points="{star8(fx + fw / 2, fy + 110, 26, 17)}" fill="{GOLD}"/>')
    out.append(stext(fx + fw / 2, fy + 200, "Upon a negotiated settlement", 12, 34, PAPER, "middle", 600, False, 1.15))
    out.append(stext(fx + fw / 2, fy + 330, "both ledgers convert into final-status instruments", 14, 27, GREY, "middle", 400, True, 1.2))
    return figure(1664, y0 + fh + 6, "".join(out), "The Holy Land Trust's two ledgers: international funds buy easements that keep empty land empty; Israel's use payments, held in escrow, cover the registered settlement footprint, which may not grow; at a negotiated settlement both convert into final-status instruments")

@slide
def ledgers():
    return section("ledgers", head("📒", "The West Bank · the Holy Land Trust", "Two parallel, without-prejudice ledgers", ts=66) +
        ledger_flow() +
        coda("Neither ledger transfers title, recognizes annexation, or determines final borders.", 34),
        "", gap=30, justify="start")

@slide
def p_west_bank():
    return section("p-west-bank", head("🫒", "7 · The West Bank", "A Holy Land Trust, with two ledgers", ts=66) +
        ledger_flow() +
        coda("A pragmatic compromise to keep the two-state horizon on its deathbed rather than consigning it to the dustbin of history.", 32),
        "", gap=30, justify="start")

@slide
def trade():
    out = []; lx, rx, top, bot = 700, 964, 70, 500
    out.append(f'<line x1="{lx}" y1="{top}" x2="{lx}" y2="{bot + 20}" stroke="{TERRA}" stroke-width="8" stroke-linecap="round"/>')
    out.append(f'<line x1="{rx}" y1="{top}" x2="{rx}" y2="{bot + 20}" stroke="{GOLDL}" stroke-width="8" stroke-linecap="round"/>')
    rungs = [("Verified relinquishment of independent coercive capacity", "Phased Israeli withdrawal"),
             ("Security passes to legitimate Palestinian institutions under Palestinian authority", "Credible regional and international security guarantees, with Egypt as the regional security anchor"),
             ("A pathway into ordinary political life", "An enforceable pathway to self-determination and statehood")]
    for i, (l, r) in enumerate(rungs):
        y = bot - 40 - i * 150
        out.append(f'<line x1="{lx}" y1="{y}" x2="{rx}" y2="{y}" stroke="{GOLD}" stroke-width="6"/>')
        out.append(f'<circle cx="{(lx + rx) / 2:.0f}" cy="{y}" r="20" fill="{BG}" stroke="{GOLD}" stroke-width="2"/><text x="{(lx + rx) / 2:.0f}" y="{y + 8}" text-anchor="middle" font-family="EB Garamond" font-size="24" font-weight="700" fill="{GOLD}">{i + 1}</text>')
        out.append(stext(lx - 34, y - 10, l, 44, 26, PAPER, "end"))
        out.append(stext(rx + 34, y - 10, r, 44, 26, PAPER, "start"))
    out.append(slabel(lx - 34, 30, "Armed factions relinquish", TERRA, 24, "end"))
    out.append(slabel(rx + 34, 30, "As occupation recedes", GOLDL, 24, "start"))
    out.append(f'<polygon points="{star8((lx + rx) / 2, 40, 30, 20)}" fill="{TERRA}"/>')
    out.append(stext((lx + rx) / 2, bot + 62, "Reciprocal, not unilateral surrender", 60, 26, GREY, "middle", 400, True))
    return section("trade", head("⚖️", "Demilitarization · the trade", "Factions relinquish coercive power as occupation recedes", ts=66) +
        figure(1664, 580, "".join(out), "A ladder: each step by armed factions is paired with a step of the settlement, rising toward statehood") +
        coda("The alternative has already been tried, at enormous cost, and has not ended the occupation either.", 32),
        "", gap=16, justify="start")

@slide
def fw_abrahamic():
    out = []; cx, cy, r = 470, 310, 196
    for name, x, y, col in [("Jews", cx - 120, cy - 70, GOLDL), ("Muslims", cx + 120, cy - 70, TERRA), ("Christians", cx, cy + 135, GOLD)]:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="2.5"/>')
    out.append(slabel(cx - 330, cy - 70, "Jews", GOLDL, 28, "end"))
    out.append(slabel(cx + 330, cy - 70, "Muslims", TERRA, 28, "start"))
    out.append(slabel(cx, cy + 360, "Christians", GOLD, 28, "middle"))
    def badge(x, y, n, col):
        return (f'<circle cx="{x}" cy="{y}" r="17" fill="{BG}" stroke="{col}" stroke-width="2"/>'
                f'<text x="{x}" y="{y + 7}" text-anchor="middle" font-family="EB Garamond" font-size="21" font-weight="700" fill="{col}">{n}</text>')
    out.append(badge(cx, cy - 205, 4, GOLDL))
    out.append(stext(cx, cy - 160, "Judeo-Islamic Tradition", 13, 23, PAPER, "middle", 600, halo=True))
    out.append(f'<polygon points="{star8(cx, cy - 2, 24, 16)}" fill="{TERRA}"/>')
    out.append(badge(cx, cy + 50, 5, TERRA))
    out.append(stext(cx, cy + 96, "Abrahamic Tradition", 11, 23, PAPER, "middle", 600, halo=True))
    fig = figure(960, 690, "".join(out), "Three overlapping circles for Jews, Muslims and Christians: the Judeo-Islamic Tradition where two meet, the Broader Abrahamic Tradition where all three meet")
    right = (f'<div style="flex:1; display:flex; flex-direction:column; gap:{px(22)}">'
             + ul(["A universal umbrella for past, current, and future interfaith initiatives and peace covenants, with shared educational programs",
                   "Covenants of coexistence, restraint, and mutual recognition among Jews, Muslims, and Christians",
                   "Especially around contested holy sites, where sanctity must once again become covenant"], 32)
             + coda("Both traditions belong within the Abraham Accords: extending normalization beyond diplomatic recognition into structured civilizational, educational, and religious reconciliation architecture.", 28)
             + '</div>')
    return section("fw-abrahamic", head("🤝", "Frameworks · 5 of 5", "The Formal Establishment of the Broader Abrahamic Tradition", ts=60) +
        f'<div style="display:flex; gap:40px; align-items:center; margin-top:-24px">{fig}{right}</div>',
        "", gap=0, justify="start")

# ---------------------------------------------------------------- decks
FULL = {"title": BRAND, "order": [
    "cover", "lead", "moment", "missing", "credit", "vision", "arc",
    "sec-telos", "farabi", "heritage", "education", "positive-telos", "social-contract", "scope",
    "sec-board", "discordances", "incubator", "convention", "mandate", "mandate-1", "mandate-2", "mandate-3", "mandate-4", "mandate-5", "guarantees", "members", "repeatable",
    "timeline", "not-utopian",
    "sec-demil", "demil", "lemkin", "trade", "factions", "ddr", "demob", "isf",
    "movement", "evacuation",
    "egypt", "custodian", "assets",
    "holy-land-trust", "ledgers", "wb-why", "wb-both", "deathbed",
    "council", "econ-plan", "compact", "labor", "labor-transition",
    "sec-recon", "recon-why", "frameworks", "fw-telos-mandate", "fw-phylogeny", "fw-judeo-islamic", "fw-abrahamic", "multiple-truths", "precedent",
    "house", "house-pilots", "house-history", "house-wager",
    "wtf", "amorphous", "rubble", "two-state", "wager-1948", "decisive", "close", "references"],
  "sections": {
    "cover": ("cover", "Title, the three parts, author."),
    "core": ("lead", "The malformed bone, the moment, what is missing, and the architecture."),
    "telos": ("sec-telos", "Al-Farabi's Virtuous City as Gaza's telos, a new social contract, and its scope."),
    "coalition": ("sec-board", "The Board of Peace as incubator, the Virtuous City Convention, the Coalition for Canaan, its mandate, guarantees and members."),
    "continuity": ("timeline", "An incubation and three phases over roughly 30 years."),
    "security": ("sec-demil", "Demilitarization, DDR, and the ISF."),
    "movement": ("movement", "Freedom of movement: temporary evacuation and asylum."),
    "arab": ("egypt", "Egypt, the Reconstruction Custodian, and the Virtuous City Trust Fund."),
    "westbank": ("holy-land-trust", "The Holy Land Trust, its two ledgers, and why."),
    "economy": ("council", "The Virtuous City Council, the economic plan, a US compact, and the Palestinian Labor Movement."),
    "recon": ("sec-recon", "Five reconciliation frameworks, the Multiple Truths framework, and a precedent."),
    "wisdom": ("house", "The House of Wisdom and Peace."),
    "close": ("wtf", "What was all this for, and the close."),
    "references": ("references", "Sources named in the plan.")}}

PITCH = {"title": BRAND + " · Pitch", "order": [
    "cover", "lead", "missing", "vision", "arc", "p-telos", "p-board", "mandate", "guarantees", "timeline",
    "p-demil", "isf", "p-movement", "p-arab", "p-west-bank", "p-economy", "frameworks", "house", "wtf", "p-close"],
  "sections": {
    "cover": ("cover", "Title, the core thesis, and the architecture."),
    "telos": ("p-telos", "The telos."),
    "coalition": ("p-board", "The Board of Peace, the Coalition for Canaan, and its guarantees."),
    "continuity": ("timeline", "An incubation and three phases."),
    "security": ("p-demil", "Demilitarization and the ISF."),
    "movement": ("p-movement", "Freedom of movement."),
    "arab": ("p-arab", "Arab partners and trust funds."),
    "westbank": ("p-west-bank", "The Holy Land Trust."),
    "economy": ("p-economy", "Governance and economy."),
    "recon": ("frameworks", "Five frameworks."),
    "wisdom": ("house", "The House of Wisdom and Peace."),
    "close": ("wtf", "The close.")}}

FACES = {"eb-garamond": {"family": "EB Garamond", "href": "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap"},
         "amiri": {"family": "Amiri", "href": "https://fonts.googleapis.com/css2?family=Amiri&display=swap"},
         "frank-ruhl-libre": {"family": "Frank Ruhl Libre", "href": "https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;500;700&display=swap"}}


# the left footer names the slide's section (cover and the closing slides keep their own)
FOOT = {"cover": "The core thesis", "core": "The core thesis", "telos": "The telos", "coalition": "Coalition core", "continuity": "Coalition continuity",
        "security": "Security & stabilization", "movement": "Freedom of movement", "arab": "Arab partners & trust funds", "westbank": "The West Bank",
        "economy": "Governance & economy", "recon": "Rehumanization", "wisdom": "The House of Wisdom", "close": "The close", "references": "References"}
import re as _re
def foot_for(spec):
    starts = {start: k for k, (start, _) in spec["sections"].items()}; sec, out = "cover", {}
    for sid in spec["order"]:
        sec = starts.get(sid, sec); out[sid] = FOOT[sec]
    return out
FOOT_FULL = foot_for(FULL)

def write(dirname, spec):
    global S
    d = REPO / dirname
    (d / "slides").mkdir(parents=True, exist_ok=True)
    for f in (d / "slides").glob("*.html"): f.unlink()
    feet = {**foot_for(spec), **{k: v for k, v in FOOT_FULL.items() if k in spec["order"]}}
    for sid in spec["order"]:
        fn = SL.get(sid) or SL.get(sid + "-")
        S = SCALE.get(sid, 1.0)
        html = fn()
        if sid not in ("cover", "close", "p-close"):
            html = _re.sub(r'(<p style="position:absolute; left:128px; bottom:72px; width:800px;[^>]*>)[^<]*(</p>)', lambda m: m.group(1) + feet[sid].upper() + m.group(2), html)
        (d / "slides" / f"{sid}.html").write_text(html + "\n")
    deck = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-04T12:00:00Z"}, "title": spec["title"], "order": spec["order"],
            "sections": {k: {"description": desc, "start": start} for k, (start, desc) in spec["sections"].items()},
            "faces": FACES, "designSystems": []}
    (d / "deck.json").write_text(json.dumps(deck, indent=1, ensure_ascii=False) + "\n")

write("deck", FULL)
write("pitch", PITCH)
print(len(FULL["order"]), "full,", len(PITCH["order"]), "pitch")
