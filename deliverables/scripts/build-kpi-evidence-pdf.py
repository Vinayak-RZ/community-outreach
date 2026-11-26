#!/usr/bin/env python3
"""Build the A4 KPI evidence report PDF from kpi-evidence-report.md.

Simple palette aligned with the A3 poster: one warm paper colour per page,
charcoal type, hairline rules. Calibri for structure, Georgia for body.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "deliverables" / "kpi-evidence-report.md"
OUT = ROOT / "deliverables" / "kpi-evidence-report.pdf"
FONTS = Path(r"C:\Windows\Fonts")

# One paper colour. Charcoal for type. Light grey for soft structure only.
PAPER = HexColor("#F4F1EC")
INK = HexColor("#2C2C2C")
MUTED = HexColor("#6E6E6E")
RULE = HexColor("#D6D2CB")
SOFT = HexColor("#EBE7E1")
CHARCOAL = HexColor("#3A3A3A")

MARGIN_X = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOT = 16 * mm
PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 2 * MARGIN_X
GAP = 3.5 * mm
GAP_SM = 2 * mm
GAP_LG = 5.5 * mm

FACE = "Calibri"
FACE_B = "Calibri-Bold"
FACE_I = "Calibri-Italic"
BODY = "Georgia"
BODY_B = "Georgia-Bold"
BODY_I = "Georgia-Italic"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(FACE, str(FONTS / "calibri.ttf")))
    pdfmetrics.registerFont(TTFont(FACE_B, str(FONTS / "calibrib.ttf")))
    pdfmetrics.registerFont(TTFont(FACE_I, str(FONTS / "calibrii.ttf")))
    pdfmetrics.registerFont(TTFont(BODY, str(FONTS / "georgia.ttf")))
    pdfmetrics.registerFont(TTFont(BODY_B, str(FONTS / "georgiab.ttf")))
    pdfmetrics.registerFont(TTFont(BODY_I, str(FONTS / "georgiai.ttf")))


PAGES = [
    {
        "name": "Reach",
        "lede": "Conversations on campus, and the form that took the same questions further.",
        "stats": [("50", "conversations"), ("211", "form responses"), ("43", "recorded and coded")],
    },
    {
        "name": "Depth",
        "lede": "Field time from the first meeting through to the night the posters went up.",
        "stats": [("11", "field sessions"), ("4.5 h", "audio and video"), ("88", "recordings"), ("3", "nights")],
    },
    {
        "name": "Record",
        "lede": "Datasets, transcripts and documents left behind by the work.",
        "stats": [("211", "survey rows"), ("43", "coded interviews"), ("88", "transcripts"), ("8", "feeding points mapped")],
    },
    {
        "name": "Output",
        "lede": "What went back to campus and to CCF.",
        "stats": [("8", "feeding points posted"), ("4", "asks to CCF"), ("2", "outputs")],
    },
    {
        "name": "Change",
        "lede": "What people knew beforehand, and what the posters put in front of them.",
        "stats": [("149", "of 211 unaware of CCF"), ("8", "points on the poster"), ("24 Nov", "poster drive")],
    },
]


def md_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = []
    i = 0
    while i < len(text):
        if text[i] == "`":
            j = text.find("`", i + 1)
            if j != -1:
                out.append(
                    f'<font face="{FACE}" size="8" color="#6E6E6E">{text[i + 1:j]}</font>'
                )
                i = j + 1
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


def strip_bold(text: str) -> str:
    return text.replace("**", "")


def parse_sections(path: Path) -> tuple[dict, dict[str, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: dict[str, list[str]] = {"title": "", "sub": [], "intro": []}
    sections: dict[str, list[str]] = {}
    current: str | None = None
    header_done = False

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("# "):
            header["title"] = line[2:].strip()
            continue
        if line.startswith("## "):
            current = line[3:].strip()
            header_done = True
            sections[current] = []
            continue
        if not header_done:
            if line.strip():
                header["sub"].append(line.strip())
            continue
        sections[current].append(line)

    # Keep course / dept / team as metadata; only the prose paragraph is the intro.
    subs = header["sub"]
    meta, intro = [], []
    for line in subs:
        if line.startswith("This report") or intro:
            intro.append(line)
        else:
            meta.append(line)
    header["sub"] = meta
    header["intro"] = intro
    return header, sections


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "kicker": ParagraphStyle(
            "kicker", parent=base["Normal"], fontName=FACE, fontSize=8,
            textColor=MUTED, leading=10, spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Normal"], fontName=BODY_B, fontSize=20,
            textColor=INK, leading=24, spaceBefore=0, spaceAfter=2,
        ),
        "lede": ParagraphStyle(
            "lede", parent=base["Normal"], fontName=BODY_I, fontSize=10,
            textColor=MUTED, leading=13.5, spaceAfter=0,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName=BODY, fontSize=10.2,
            textColor=INK, leading=14.8, alignment=TA_JUSTIFY, spaceAfter=7,
        ),
        "sources": ParagraphStyle(
            "sources", parent=base["Normal"], fontName=FACE, fontSize=7.3,
            textColor=MUTED, leading=9.8,
        ),
        "sources_head": ParagraphStyle(
            "sources_head", parent=base["Normal"], fontName=FACE, fontSize=7,
            textColor=MUTED, leading=9, spaceAfter=1,
        ),
        "stat_num": ParagraphStyle(
            "stat_num", parent=base["Normal"], fontName=BODY_B, fontSize=20,
            textColor=INK, leading=22, alignment=TA_LEFT,
        ),
        "stat_label": ParagraphStyle(
            "stat_label", parent=base["Normal"], fontName=FACE, fontSize=7.2,
            textColor=MUTED, leading=9.2, alignment=TA_LEFT,
        ),
        "cell": ParagraphStyle(
            "cell", parent=base["Normal"], fontName=BODY, fontSize=9.5,
            textColor=INK, leading=12.6,
        ),
        "cell_head": ParagraphStyle(
            "cell_head", parent=base["Normal"], fontName=FACE_B, fontSize=7.6,
            textColor=white, leading=10,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Normal"], fontName=BODY_B, fontSize=26,
            textColor=INK, leading=30, spaceAfter=5,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"], fontName=FACE, fontSize=9.5,
            textColor=MUTED, leading=13,
        ),
        "cover_body": ParagraphStyle(
            "cover_body", parent=base["Normal"], fontName=BODY, fontSize=10.8,
            textColor=INK, leading=16, alignment=TA_JUSTIFY,
        ),
        "toc": ParagraphStyle(
            "toc", parent=base["Normal"], fontName=BODY, fontSize=10,
            textColor=INK, leading=14.5,
        ),
        "toc_num": ParagraphStyle(
            "toc_num", parent=base["Normal"], fontName=FACE, fontSize=9.5,
            textColor=MUTED, leading=14.5,
        ),
    }


def stat_band(stats: list[tuple[str, str]], s: dict) -> Table:
    """Big numbers with one rule under them. Even column padding."""
    cells_num = [Paragraph(n, s["stat_num"]) for n, _ in stats]
    cells_lbl = [Paragraph(lbl, s["stat_label"]) for _, lbl in stats]
    data = [cells_num, cells_lbl]
    n = len(stats)
    widths = [CONTENT_W / n] * n
    t = Table(data, colWidths=widths)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 1),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, RULE),
        ("LINEBELOW", (0, 1), (-1, 1), 0.6, RULE),
    ]
    for i in range(1, n):
        cmds.append(("LINEBEFORE", (i, 0), (i, 1), 0.45, RULE))
    t.setStyle(TableStyle(cmds))
    return t


def md_table(rows: list[list[str]], s: dict) -> Table:
    header = [Paragraph(strip_bold(c), s["cell_head"]) for c in rows[0]]
    body = []
    for r in rows[1:]:
        body.append([Paragraph(md_inline(c), s["cell"]) for c in r])
    ncols = len(header)
    if ncols == 2:
        widths = [CONTENT_W * 0.34, CONTENT_W * 0.66]
    elif ncols == 3:
        widths = [CONTENT_W * 0.17, CONTENT_W * 0.61, CONTENT_W * 0.22]
    else:
        widths = [CONTENT_W / ncols] * ncols
    t = Table([header] + body, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), CHARCOAL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, CHARCOAL),
    ]
    for i in range(1, len(body) + 1, 2):
        cmds.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(cmds))
    return t


def section_flow(lines: list[str], s: dict) -> list:
    flow: list = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        if line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [c.strip() for c in raw.split("|")]
                if not all(set(c) <= {"-", ":"} for c in cells):
                    block.append(cells)
                i += 1
            if block:
                flow.append(Spacer(1, GAP_SM))
                flow.append(md_table(block, s))
                flow.append(Spacer(1, GAP))
            continue

        if line.startswith("Sources:"):
            body = line[len("Sources:"):].strip()
            flow.append(
                Table(
                    [
                        [Paragraph("Sources", s["sources_head"])],
                        [Paragraph(md_inline(body), s["sources"])],
                    ],
                    colWidths=[CONTENT_W],
                    style=TableStyle(
                        [
                            ("LINEABOVE", (0, 0), (-1, 0), 0.6, RULE),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, 0), 7),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
                            ("TOPPADDING", (0, 1), (-1, 1), 0),
                            ("BOTTOMPADDING", (0, 1), (-1, 1), 0),
                        ]
                    ),
                )
            )
            i += 1
            continue

        flow.append(Paragraph(md_inline(line), s["body"]))
        i += 1
    return flow


def page_bg(canvas, doc):
    """Same paper colour on every page. Thin rules only."""
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, PAGE_H - 14 * mm, PAGE_W - MARGIN_X, PAGE_H - 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont(FACE, 7)
    canvas.drawString(MARGIN_X, PAGE_H - 11 * mm, "KPI evidence report")
    canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 11 * mm, "EEC 399 · Group 23 · IIT Roorkee")
    canvas.line(MARGIN_X, 13 * mm, PAGE_W - MARGIN_X, 13 * mm)
    canvas.setFont(FACE, 7)
    canvas.drawString(MARGIN_X, 8.5 * mm, "Campus dogs: two sides of one street")
    canvas.setFillColor(INK)
    canvas.setFont(FACE, 8)
    canvas.drawRightString(PAGE_W - MARGIN_X, 8.5 * mm, str(doc.page))
    canvas.restoreState()


def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Foot bar only. No mid-page rule: that cut through the content.
    canvas.setFillColor(CHARCOAL)
    canvas.rect(0, 0, PAGE_W, 8 * mm, fill=1, stroke=0)
    canvas.restoreState()


def build() -> None:
    register_fonts()
    header, sections = parse_sections(MD)
    s = styles()

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOT,
        title="KPI evidence report · Campus dogs · Group 23",
        author="EEC 399 Group 23",
        subject="EEC 399 Community Outreach · Topic 3 · campus dogs",
    )

    cover_frame = Frame(
        MARGIN_X, MARGIN_BOT, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOT, id="cover"
    )
    body_frame = Frame(
        MARGIN_X, MARGIN_BOT, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOT, id="body"
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_bg),
            PageTemplate(id="Body", frames=[body_frame], onPage=page_bg),
        ]
    )

    story: list = []
    story.append(NextPageTemplate("Body"))

    story.append(
        Paragraph(
            "EEC 399 Community Outreach · Group 23 · Topic 3",
            s["kicker"],
        )
    )
    story.append(Spacer(1, 2.5 * mm))
    story.append(Paragraph("Campus dogs: two sides of one street", s["cover_title"]))
    story.append(Paragraph("KPI evidence report", s["lede"]))
    story.append(Spacer(1, GAP_LG))
    for meta in header.get("sub", []):
        # Skip the long course line; the kicker already carries it.
        if meta.startswith("EEC 399"):
            continue
        shown = meta.replace(", ", " · ") if meta.count(",") >= 3 else meta
        story.append(Paragraph(md_inline(shown), s["cover_sub"]))
        story.append(Spacer(1, 1.1 * mm))
    story.append(Spacer(1, GAP))

    intro = " ".join(t.strip() for t in header.get("intro", []) if t.strip())
    if intro:
        story.append(Paragraph(md_inline(intro), s["cover_body"]))
        story.append(Spacer(1, GAP_LG))

    key = [
        ("50", "conversations"),
        ("211", "form responses"),
        ("88", "recordings"),
        ("8", "feeding points"),
    ]
    story.append(stat_band(key, s))
    story.append(Spacer(1, GAP))

    toc_rows = [[Paragraph("Contents", s["sources_head"]), Paragraph("", s["sources_head"])]]
    for idx, page in enumerate(PAGES, start=2):
        toc_rows.append(
            [
                Paragraph(page["name"], s["toc"]),
                Paragraph(f"{idx}", s["toc_num"]),
            ]
        )
    toc = Table(toc_rows, colWidths=[CONTENT_W * 0.8, CONTENT_W * 0.2])
    toc.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ]
        )
    )
    story.append(toc)
    story.append(PageBreak())

    total = len(PAGES)
    for idx, page in enumerate(PAGES, start=1):
        name = page["name"]
        lines = sections.get(name, [])
        story.append(Paragraph(f"{idx} of {total}", s["kicker"]))
        story.append(Paragraph(name, s["h1"]))
        story.append(Paragraph(page["lede"], s["lede"]))
        story.append(Spacer(1, GAP_SM))
        story.append(stat_band(page["stats"], s))
        story.append(Spacer(1, GAP))
        story.extend(section_flow(lines, s))
        story.append(PageBreak())


    if story and isinstance(story[-1], PageBreak):
        story.pop()

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
