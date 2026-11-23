#!/usr/bin/env python3
"""Build a clean Q&A PDF of unique offline interview questions for Topic 3."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    KeepTogether,
    NextPageTemplate,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "unique-interview-qa.pdf"

# Fonts
pdfmetrics.registerFont(TTFont("Georgia", r"C:\Windows\Fonts\georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", r"C:\Windows\Fonts\georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", r"C:\Windows\Fonts\georgiai.ttf"))
pdfmetrics.registerFont(TTFont("Calibri", r"C:\Windows\Fonts\calibri.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Bold", r"C:\Windows\Fonts\calibrib.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Italic", r"C:\Windows\Fonts\calibrii.ttf"))

# Palette — cool ink on paper, not purple/cream/terracotta
INK = HexColor("#1C2421")
MUTED = HexColor("#5A6A63")
RULE = HexColor("#C5D0C9")
ACCENT = HexColor("#1F5C4A")
ACCENT_SOFT = HexColor("#E8F1ED")
PAPER = HexColor("#F7F6F2")
BAND = HexColor("#163D33")
NUMBER_BG = HexColor("#214F42")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


# Curated from Luna (10) + Opus (10): best 10 distinct angles
ITEMS = [
    {
        "q": (
            "When a dog fouls a corridor or a mess back area, who actually cleans it? "
            "Is that written into anyone's duties, or does it just end up with you?"
        ),
        "ask": "Hostel cleaning staff and mess back-area workers",
        "why": (
            "Surfaces the unpaid labour behind \"coexistence\" — work done by people "
            "whose opinion rarely appears as either \"side\" of the street."
        ),
        "a": (
            "A strong answer names a role (cleaner, mess helper) and whether the duty "
            "is formal or informal. Fieldwork already shows hygiene as a lived problem "
            "(survey: 54% ticked hygiene/waste; P-HYG in 11/36 interviews), including "
            "fouling in bathrooms and tipped bins. Cleaning staff (I21) describe dirt "
            "in bathrooms and offices with no permanent fix. A useful answer also says "
            "whether complaining upward changes anything, or whether the work is simply "
            "absorbed into an already invisible shift. That turns coexistence from a "
            "student opinion into a labour question."
        ),
        "source": "analysis/synthesis.md F2; analysis/interview-coding.md I21, P-HYG; survey-analysis.md §3",
    },
    {
        "q": (
            "Is there anything you would like to do about a dog at night but are not "
            "allowed to? Who told you that, and what happens to you if you do it anyway?"
        ),
        "ask": "Night-shift security guards (bhawan and road posts)",
        "why": (
            "Treats guards as people under rules, not as opinion-givers — and exposes "
            "the operational limit competitors miss when they only ask \"what should be done.\""
        ),
        "a": (
            "Expect answers that land between \"we can only shoo and report upward\" "
            "(already heard from a bhawan guard, I08) and \"we were told not to kill "
            "them\" (girls' bhawan guard, I17). The valuable part is the chain of "
            "authority: who issued the limit, whether it is written, and what personal "
            "risk (complaint, job, being labelled cruel) stops action. Pair this with "
            "who receives the report and whether anything comes back. That maps why "
            "hotspots persist even when guards see them every night."
        ),
        "source": "analysis/interview-coding.md I08, I13, I17; synthesis.md F3",
    },
    {
        "q": (
            "Suppose the institute gave you a feeding spot you actually liked — not one "
            "next to the garbage. What would it need to have for you to stop feeding at "
            "hostel doors completely? And what would never make you stop?"
        ),
        "ask": "Regular student feeders and staff feeders",
        "why": (
            "Asks feeders for their own non-negotiable, instead of debating whether "
            "feeding is good or bad — the angle that separates persuasion from policing."
        ),
        "a": (
            "A useful answer lists concrete conditions: distance from doors and bins, "
            "fixed times, water, shade, a board that is actually readable, and who "
            "enforces it. Fieldwork already finds zones exist but fail: next to garbage "
            "(I04), poorly marked with \"a tiny board\" (I10/I35), and feeding outside "
            "them (I13). CCF says spots are already in quiet areas (I24) — so the "
            "dispute is use and enforcement, not existence. The second half of the "
            "question (\"what would never make you stop\") reveals whether door-feeding "
            "is convenience, attachment to a specific dog, or distrust of the "
            "administration. Without that limit, zone policy is theatre."
        ),
        "source": "analysis/synthesis.md F5; interview-coding.md I04, I10, I13, I24, I35",
    },
    {
        "q": (
            "When a student brings you a dog complaint, whose problem do you say it is — "
            "Security's, CCF's, or Estate's? And when it is passed on, who passes it back to you?"
        ),
        "ask": "Wardens first; then the same wording to Security and to a CCF office-bearer",
        "why": (
            "Asking three offices the same sentence maps responsibility dumping from "
            "all sides, instead of collecting three separate wish-lists."
        ),
        "a": (
            "Prospective pattern: each office can name another. Guards report upward "
            "but cannot relocate (I08); CCF frames aggressive cases as exceptional and "
            "points at outside dogs / broken gate 7 (I24); sterilisation itself is "
            "contested between CCF and the CMO notes (\"handled through security "
            "guards\"). A crisp answer names the next desk and whether a ticket, email, "
            "or verbal handoff ever returns with an outcome. If three interviews "
            "produce a closed loop with no owner, that loop is itself the finding — "
            "and it belongs on the poster as an organisational gap, not as blame."
        ),
        "source": "analysis/synthesis.md conflicts table; interview-coding.md I08, I24; project-brief CMO notes",
    },
    {
        "q": (
            "If \"managed coexistence\" happened tomorrow, which floor, corridor, or route "
            "would you personally want the dogs gone from? Would you still call that coexistence?"
        ),
        "ask": "Students who already chose managed coexistence (the survey majority)",
        "why": (
            "Stress-tests whether the polite 85.8% majority quietly means \"not near me\" "
            "— a distinction no tick-box survey can catch."
        ),
        "a": (
            "A candid answer often draws a hard line at rooms, washrooms, mess doors, "
            "or a named night route (MAC–Rajiv, MNC–Govind, library path), while "
            "accepting dogs on open roads. That matches the strong finding: the fight "
            "is over space, not presence (181/211 chose a managed boundary; even "
            "mostly-negative respondents mostly chose coexistence options). Students "
            "already say \"fine on roads near MAC/MNC/SAC but not in hostels\" (I01, I04, "
            "I32). If the person still calls their personal exclusion zone "
            "\"coexistence,\" ask them to define the residual shared space. The "
            "answerable proposal writes that boundary down — hostels closed, zones "
            "enforced — rather than arguing about belonging in the abstract."
        ),
        "source": "analysis/synthesis.md F1; survey-analysis.md §3–4.2; interview-coding.md I01, I04, I32",
    },
    {
        "q": (
            "Have you changed your timetable — leaving the lab early, skipping the library, "
            "or avoiding a route after dark — because of dogs? Do you know anyone who has, "
            "but wouldn't say so on a form?"
        ),
        "ask": "Students with late lab/library hours; use the \"friend\" version so fear can be reported without self-exposure",
        "why": (
            "Measures the cost of fear in academic hours and mobility, not only in "
            "bites — and the friend framing lets people speak about a group pattern "
            "without naming themselves."
        ),
        "a": (
            "Expect detours, waiting for company, or cutting late sessions on named "
            "routes. Interviews already record night avoidance after bites or packs "
            "(I03, I06, I12, I29, I33 — including a 2 a.m. pack of 5–6). Survey: 61.1% "
            "felt unsafe or chased, and that group rates the problem far higher "
            "(mean 4.36 vs 2.22). Injuries that are not bites — falls while fleeing "
            "(I08, I28, I30) — also change behaviour. A strong answer names the route, "
            "the hour, and what was traded away (lab time, library, walking alone). "
            "That is Depth evidence competitors rarely quantify."
        ),
        "source": "analysis/synthesis.md F3; survey-analysis.md §4.1; interview-coding.md I03, I06, I12, I33",
    },
    {
        "q": (
            "How often do new puppies turn up that weren't born here? Where do they "
            "appear, and who do you think leaves them?"
        ),
        "ask": "Guards at gates and along the boundary wall; long-serving campus staff; feeders/caretakers",
        "why": (
            "Dumped animals from outside puncture both the sterilisation claim and the "
            "gate-control claim at once — an angle most teams never open."
        ),
        "a": (
            "A high-value answer gives frequency, place (wall gap, gate, Himalaya side), "
            "and time of day. A caretaker/feeder already describes puppies dumped at "
            "night and gaps in railing/wall plus broken gate 7 (I25); CCF likewise "
            "blames outside dogs via gate 7 (I24); a MAC guard blames roughly 8–10 "
            "outside dogs (I11). The Nehru Road gate guard says outside dogs are not "
            "let in at the gate (I14) — so the wall, not the booth, may be the leak. "
            "Treat numbers as unverified until geotagged photos of gaps and a dated "
            "count exist. The question's job is to turn \"population rising\" from mood "
            "into a boundary-and-dumping hypothesis."
        ),
        "source": "analysis/synthesis.md F4 and conflicts (gate control); interview-coding.md I11, I14, I24, I25",
    },
    {
        "q": (
            "Can you point to a dog on this route right now and tell us whether it is "
            "sterilised? Show us how you know — the ear notch, a record, or just that you recognise it."
        ),
        "ask": "CCF volunteers, on a walk along a night hotspot route",
        "why": (
            "Converts \"~90 females neutered\" from a claimed number into something a "
            "sceptic can check in the field."
        ),
        "a": (
            "A convincing answer uses a visible marker (ear notch, cited by a CCF "
            "volunteer as the mark of a treated dog — I23) or a written register, not "
            "recognition alone. CCF office-bearer claims roughly 90 females, \"almost "
            "all\" / \"all\" neutered, while unsure of the exact count (I24); an MNC "
            "guard describes litters of 8–10 every 6–8 months (I13); a caretaker says "
            "sterilisation never reaches 100% (I25). Outside dogs may be unneutered "
            "even if campus females are treated. The interview itself can become an "
            "ear-notch count on 3–4 routes in one evening — exactly the test "
            "synthesis.md recommends — and honesty about \"I don't know\" is a valid, "
            "publishable result."
        ),
        "source": "analysis/synthesis.md sterilisation conflict + R4; interview-coding.md I13, I23, I24, I25",
    },
    {
        "q": (
            "At 2 a.m., if a dog blocks a route or someone is bitten, who should be "
            "contacted first — and why does that person currently feel like the wrong one?"
        ),
        "ask": "Late-hour students, night guards, wardens, and hospital/medical staff",
        "why": (
            "Reveals the post-incident chain that technology alone cannot fix, and "
            "why fear persists after the chase ends."
        ),
        "a": (
            "Prospective answers often split: call a friend first, then a guard, then "
            "wait for morning for a physician. A bitten student already described "
            "waiting until morning to see a physician (I12); CMO notes say the first "
            "dose should be within 2 days; a guard mentions many costly injections "
            "(I13). There is no campus-wide 24×7 \"if bitten\" notice in the collected "
            "evidence. The second clause (\"why the wrong one\") surfaces missing "
            "night coverage, unclear hospital access, or fear of being blamed. A "
            "great outcome of asking this is a one-page route card for every bhawan "
            "(recommendation R5) — Output evidence, not just another opinion."
        ),
        "source": "analysis/synthesis.md F7, R5; interview-coding.md I12, I13; CMO notes in project-brief",
    },
    {
        "q": (
            "How much cooked food leaves this mess as waste each night, where does it go, "
            "and at what time? If that stopped tomorrow, which dogs would leave first?"
        ),
        "ask": "Mess managers and back-area mess workers (ask privately before asking in front of a manager)",
        "why": (
            "Treats institute food waste — not only student feeders — as the hidden "
            "attractor, which competitors usually skip."
        ),
        "a": (
            "A useful answer gives timing, destination (open bin, covered bin, feeder "
            "pickup), and whether non-veg waste is separate. Interviews already link "
            "open bins and mess leftovers to dog presence (C-WASTE in 6/36; canteen "
            "worker on bins with non-veg waste, I20; students on overturned bins, "
            "I04/I12). Survey free text even records a fix that worked: raised "
            "dustbins stopped dogs entering one bhawan (row 112). CCF says a feeder "
            "takes mess leftovers to set spots (I24) — so waste is already part of "
            "the feeding system. If certain packs arrive on a waste clock, changing "
            "that clock may move dogs more than another awareness poster. Ask whether "
            "technology helps here: usually no — lids, height, and a schedule do."
        ),
        "source": "analysis/synthesis.md F5, R1; survey-analysis.md §6.2 row 112; interview-coding.md I04, I12, I20, I24",
    },
]


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverKicker",
            fontName="Calibri",
            fontSize=9,
            leading=12,
            textColor=HexColor("#A8C4B8"),
            alignment=TA_LEFT,
            spaceAfter=8,
            tracking=1.2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Georgia",
            fontSize=28,
            leading=34,
            textColor=white,
            alignment=TA_LEFT,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Calibri",
            fontSize=11,
            leading=16,
            textColor=HexColor("#D5E6DE"),
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverNote",
            fontName="Calibri-Italic",
            fontSize=9.5,
            leading=14,
            textColor=HexColor("#B7CDBF"),
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="PageHeader",
            fontName="Calibri",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="QNum",
            fontName="Calibri-Bold",
            fontSize=9,
            leading=11,
            textColor=ACCENT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Question",
            fontName="Georgia",
            fontSize=12.5,
            leading=17,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaLabel",
            fontName="Calibri-Bold",
            fontSize=8,
            leading=10,
            textColor=ACCENT,
            spaceBefore=2,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaBody",
            fontName="Calibri",
            fontSize=9,
            leading=12.5,
            textColor=MUTED,
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="AnswerLabel",
            fontName="Calibri-Bold",
            fontSize=8.5,
            leading=11,
            textColor=ACCENT,
            spaceBefore=4,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Answer",
            fontName="Calibri",
            fontSize=9.8,
            leading=13.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Source",
            fontName="Calibri-Italic",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
            spaceBefore=2,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Footer",
            fontName="Calibri",
            fontSize=7.5,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="IntroTitle",
            fontName="Georgia",
            fontSize=16,
            leading=20,
            textColor=INK,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="IntroBody",
            fontName="Calibri",
            fontSize=10,
            leading=14,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        )
    )
    return styles


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BAND)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # subtle left rule
    canvas.setFillColor(HexColor("#2A6B56"))
    canvas.rect(0, 0, 6 * mm, PAGE_H, fill=1, stroke=0)
    # bottom accent strip
    canvas.setFillColor(HexColor("#0F2A24"))
    canvas.rect(0, 0, PAGE_W, 22 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#A8C4B8"))
    canvas.setFont("Calibri", 8)
    canvas.drawString(
        MARGIN,
        10 * mm,
        "EEC 399 · Group 23 · Private team use · Do not publish interviewee names",
    )
    canvas.restoreState()


def draw_inner(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # top rule
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, PAGE_H - 12 * mm, PAGE_W - MARGIN, PAGE_H - 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Calibri", 8)
    canvas.drawString(MARGIN, PAGE_H - 10 * mm, "Campus dogs · Unique offline interview Q&A")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 10 * mm, f"{doc.page}")
    # bottom
    canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    canvas.setFont("Calibri", 7.5)
    canvas.drawCentredString(
        PAGE_W / 2,
        7 * mm,
        "Prospective answers are grounded in repo analysis — verify quotes against audio before citing.",
    )
    canvas.restoreState()


def qa_block(styles, n, item):
    bits = []
    bits.append(Paragraph(f"QUESTION {n:02d}", styles["QNum"]))
    bits.append(Paragraph(item["q"], styles["Question"]))
    bits.append(Paragraph("ASK OF", styles["MetaLabel"]))
    bits.append(Paragraph(item["ask"], styles["MetaBody"]))
    bits.append(Paragraph("WHY THIS CUTS THROUGH", styles["MetaLabel"]))
    bits.append(Paragraph(item["why"], styles["MetaBody"]))
    bits.append(Paragraph("PROSPECTIVE ANSWER", styles["AnswerLabel"]))
    bits.append(Paragraph(item["a"], styles["Answer"]))
    bits.append(Paragraph(f"Evidence trail: {item['source']}", styles["Source"]))
    bits.append(Spacer(1, 4 * mm))
    # divider via thin paragraph of rule-like text
    bits.append(
        Paragraph(
            "<font color='#C5D0C9'>────────────────────────────────────────</font>",
            ParagraphStyle(
                "Rule",
                fontName="Calibri",
                fontSize=8,
                leading=10,
                textColor=RULE,
                alignment=TA_CENTER,
                spaceAfter=6,
            ),
        )
    )
    return KeepTogether(bits)


def build():
    styles = make_styles()
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Unique Offline Interview Q&A — Campus Dogs",
        author="EEC 399 Group 23",
    )

    cover_frame = Frame(
        MARGIN,
        30 * mm,
        PAGE_W - 2 * MARGIN,
        PAGE_H - 55 * mm,
        id="cover",
    )
    inner_frame = Frame(
        MARGIN,
        16 * mm,
        PAGE_W - 2 * MARGIN,
        PAGE_H - 32 * mm,
        id="inner",
    )

    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
            PageTemplate(id="inner", frames=[inner_frame], onPage=draw_inner),
        ]
    )

    story = []
    # Cover content
    story.append(Paragraph("EEC 399  ·  COMMUNITY OUTREACH  ·  TOPIC 3", styles["CoverKicker"]))
    story.append(
        Paragraph(
            "Ten questions<br/>competitors are<br/>unlikely to ask",
            styles["CoverTitle"],
        )
    )
    story.append(
        Paragraph(
            "Offline interview prompts for campus dogs — with prospective answers "
            "drawn from the group's survey (n = 211), 36 coded interviews, and synthesis.",
            styles["CoverSub"],
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        Paragraph(
            "Selected from 20 drafts (10 GPT Luna + 10 Claude Opus). "
            "Answers are prospective patterns grounded in repo evidence — not invented quotes. "
            "Use roles, not names. Check audio before citing any line.",
            styles["CoverNote"],
        )
    )
    story.append(Spacer(1, 14 * mm))
    story.append(
        Paragraph(
            "IIT Roorkee  ·  Group 23  ·  \"Two sides of one street\"",
            styles["CoverSub"],
        )
    )

    story.append(NextPageTemplate("inner"))
    story.append(FrameBreak())

    # Intro page
    story.append(Paragraph("How to use this sheet", styles["IntroTitle"]))
    story.append(
        Paragraph(
            "These are face-to-face prompts for a second wave of interviews. Each question "
            "is meant to open a gap the first survey and the generic interview script did not: "
            "invisible labour, rules guards cannot break, feeder non-negotiables, office "
            "ping-pong, the personal meaning of \"coexistence,\" the academic cost of fear, "
            "dumped puppies, field-checkable sterilisation, the 2 a.m. contact chain, and "
            "mess-waste timing. Ask one or two per sitting. Prefer silence after the question "
            "over leading follow-ups.",
            styles["IntroBody"],
        )
    )
    story.append(
        Paragraph(
            "Course frame (from the deck): enquiry, not charity; both sides of the street; "
            "a question the other teams on this topic did not think of; honesty about what "
            "could not be verified. Relative grading rewards primary contact and sceptical evidence.",
            styles["IntroBody"],
        )
    )
    story.append(
        Paragraph(
            "Privacy: anonymise by role. Do not put names on this sheet in the field. "
            "Do not promise fixes you cannot deliver.",
            styles["IntroBody"],
        )
    )
    story.append(Spacer(1, 4 * mm))

    for i, item in enumerate(ITEMS, start=1):
        story.append(qa_block(styles, i, item))

    # Closing note
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("After you ask them", styles["IntroTitle"]))
    story.append(
        Paragraph(
            "Log role, place, time, and whether consent was recorded. Code new answers "
            "against the existing codebook in analysis/interview-coding.md. If three offices "
            "name each other with no owner, that loop is a finding. If an ear-notch walk "
            "contradicts a sterilisation claim, report both. If technology is offered as a "
            "fix, ask what physical change it replaces — the synthesis so far says mostly "
            "doors, bins, walls, zones, and records matter more than apps.",
            styles["IntroBody"],
        )
    )

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
