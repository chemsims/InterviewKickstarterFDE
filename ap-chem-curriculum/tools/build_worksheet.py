"""Build ChemSims-style Student Notes and Answer Key PDFs from a unit content file.

Usage:  python3 build_worksheet.py ../units/unit6/content.json [--out DIR]

The look follows Tess's Unit 1, Unit 2 and Reaction Rates worksheets: a cover
page with the mascot and a TOPIC/PAGE table, then one section per sim screen
with grey section bands (icon + caps title + one-line instruction), blanks to
fill, tables, graph frames and an EXPLORE box. The Answer Key is the same file
with every blank filled in coral bold.

Content format: see ../README.md ("Content file format").
"""
import argparse
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textfmt import FONT_DIR, HERE, rich  # noqa: E402

ASSETS = os.path.join(HERE, "assets")

for name, fn in [("Poppins", "Poppins-Regular.ttf"), ("Poppins-Bold", "Poppins-Bold.ttf"),
                 ("Poppins-SemiBold", "Poppins-SemiBold.ttf"), ("Poppins-Italic", "Poppins-Italic.ttf"),
                 ("Poppins-BoldItalic", "Poppins-BoldItalic.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Poppins", normal="Poppins", bold="Poppins-Bold", italic="Poppins-Italic",
                              boldItalic="Poppins-BoldItalic")
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")

DARK = colors.HexColor("#3d3d3d")
BAND = colors.HexColor("#e6e6e6")
PANEL = colors.HexColor("#efefef")
CORAL = colors.HexColor("#E8604C")
CORAL_HEX = "#E8604C"
GRID = colors.HexColor("#555555")

PAGE_W, PAGE_H = letter
MARGIN_X = 0.6 * inch
CONTENT_W = PAGE_W - 2 * MARGIN_X

body = ParagraphStyle("body", fontName="Poppins", fontSize=10.5, leading=21, textColor=colors.black)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=3)
small = ParagraphStyle("small", parent=body, fontSize=9, leading=12)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=12, alignment=TA_CENTER)
cell_left = ParagraphStyle("cell_left", parent=cell, alignment=TA_LEFT)
cell_head = ParagraphStyle("cell_head", parent=cell, fontName="Poppins-Bold")
band_title = ParagraphStyle("band_title", fontName="Poppins-Bold", fontSize=9.5, leading=11)
band_sub = ParagraphStyle("band_sub", fontName="Poppins", fontSize=9, leading=11)
key_note = ParagraphStyle("key_note", parent=body, fontSize=9.5, leading=13, textColor=CORAL,
                          fontName="Poppins-SemiBold")

BLANK_RE = re.compile(r"\{\{(.+?)\}\}")


def blanks(text, key, min_chars=12):
    """Replace {{answer}} with an underline (student) or the coral answer (key).

    The key's padding is measured so the answer spans about the same width as the student's line.
    """
    us = pdfmetrics.stringWidth("_", "Poppins", 10)
    nb = pdfmetrics.stringWidth("\u00a0", "Poppins", 10)
    out, last = [], 0
    for m in BLANK_RE.finditer(text):
        out.append(rich(text[last:m.start()]))
        ans = m.group(1)
        width = None
        if "|" in ans:
            ans, w = ans.rsplit("|", 1)
            if w.strip().isdigit():
                width = int(w)
        plain = re.sub(r"\*+", "", ans)
        aw = pdfmetrics.stringWidth(plain, "Poppins-Bold", 10) * 1.06  # bold + fallback-glyph margin
        n = width or max(min_chars, int(len(ans) * 1.25) + 4)
        if key:
            pad = "&nbsp;" * max(1, int((n * us - aw) / 2 / nb))
            out.append(f'<u>{pad}<font color="{CORAL_HEX}"><b>{rich(ans)}</b></font>{pad}</u>')
        else:
            out.append("_" * n)
        last = m.end()
    out.append(rich(text[last:]))
    return "".join(out)


def count_blanks(text):
    return len(BLANK_RE.findall(text or ""))


class Band(Flowable):
    """Grey rounded band with an icon, bold caps title and a one-line instruction."""

    def __init__(self, icon, title, subtitle):
        super().__init__()
        self.icon, self.title, self.subtitle = icon, title, subtitle
        self.width = CONTENT_W
        self.p1 = Paragraph(rich(title.upper() + ":"), band_title)
        self.p2 = Paragraph(rich(subtitle), band_sub) if subtitle else None

    def wrap(self, aw, ah):
        tw = self.width - 0.75 * inch
        h1 = self.p1.wrap(tw, ah)[1]
        h2 = self.p2.wrap(tw, ah)[1] if self.p2 else 0
        self.h = max(0.42 * inch, h1 + h2 + 12)
        return self.width, self.h + 8

    def draw(self):
        c = self.canv
        c.setFillColor(BAND)
        c.roundRect(0.18 * inch, 4, self.width - 0.18 * inch, self.h, 8, stroke=0, fill=1)
        ip = os.path.join(ASSETS, self.icon)
        s = 0.4 * inch
        c.drawImage(ip, 0, 4 + (self.h - s) / 2, s, s, mask="auto")
        tw = self.width - 0.75 * inch
        y = 4 + self.h - 6
        h1 = self.p1.wrap(tw, 100)[1]
        self.p1.drawOn(c, 0.6 * inch, y - h1)
        if self.p2:
            h2 = self.p2.wrap(tw, 100)[1]
            self.p2.drawOn(c, 0.6 * inch, y - h1 - h2)


class _Optional(Flowable):
    """Wraps an ungraded extra (the EXPLORE box): shown if it fits on the page, dropped otherwise."""

    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def wrap(self, aw, ah):
        w, h = self.inner.wrap(aw, ah)
        self.h = h + 4
        return w, self.h

    def draw(self):
        self.inner.drawOn(self.canv, 0, 0)

    def split(self, aw, ah):
        return [Spacer(0, 0)]  # an empty piece fits, so the box is dropped rather than moved


class GraphFrame(Flowable):
    """Empty axes for students to sketch on. Labels come from the content file."""

    def __init__(self, x_label, y_label, height=2.3 * inch, width=None, title=None, answer=None):
        super().__init__()
        self.xl, self.yl, self.h = x_label, y_label, height
        self.w = width or CONTENT_W * 0.62
        self.title = title
        self.answer = answer  # Answer Key only: written inside the grid so the key keeps the page breaks

    def wrap(self, aw, ah):
        return CONTENT_W, self.h + 0.45 * inch

    def draw(self):
        c = self.canv
        x0 = (CONTENT_W - self.w) / 2 + 0.25 * inch
        y0 = 0.35 * inch
        c.setStrokeColor(colors.HexColor("#cfcfcf"))
        c.setLineWidth(0.4)
        step = 0.25 * inch
        x = x0
        while x <= x0 + self.w + 0.1:
            c.line(x, y0, x, y0 + self.h)
            x += step
        y = y0
        while y <= y0 + self.h + 0.1:
            c.line(x0, y, x0 + self.w, y)
            y += step
        if self.answer:
            ap_ = Paragraph(blanks(self.answer, True), ParagraphStyle("ga", parent=key_note, fontSize=8.5,
                                                                      leading=10.5, backColor=colors.white))
            aw_, ah_ = ap_.wrap(self.w - 0.3 * inch, self.h)
            ap_.drawOn(self.canv, x0 + 0.15 * inch, y0 + self.h - ah_ - 0.1 * inch)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.4)
        c.line(x0, y0, x0 + self.w, y0)
        c.line(x0, y0, x0, y0 + self.h)
        p = Paragraph(rich(self.xl), ParagraphStyle("xl", parent=small, alignment=TA_CENTER))
        pw, ph = p.wrap(self.w, 40)
        p.drawOn(c, x0, y0 - ph - 4)
        c.saveState()
        c.translate(x0 - 8, y0 + self.h / 2)
        c.rotate(90)
        p = Paragraph(rich(self.yl), ParagraphStyle("yl", parent=small, alignment=TA_CENTER))
        pw, ph = p.wrap(self.h, 40)
        p.drawOn(c, -self.h / 2, 0)
        c.restoreState()


class Lines(Flowable):
    """Ruled writing lines; in the key, the answer is written on them, one text line per ruled line."""

    LH = 0.3 * inch

    def __init__(self, n, answer=None, key=False):
        super().__init__()
        self.n, self.answer, self.key = n, answer, key
        self.para = None
        if key and answer:
            st = ParagraphStyle("key_lines", parent=key_note, leading=self.LH)
            self.para = Paragraph(blanks(answer, True), st)

    def wrap(self, aw, ah):
        self.lines_n = max(self.n, 1)
        if self.para:
            self.para.wrap(CONTENT_W - 0.4 * inch, ah)
            if len(self.para.blPara.lines) > self.lines_n:
                # A key answer longer than the student's space: shrink it to fit the same space,
                # so the Answer Key keeps the Student Notes' page breaks.
                txt = blanks(self.answer, True)
                for fs in (9, 8.5, 8, 7.5, 7):
                    lead = max(fs * 1.15, self.lines_n * self.LH / max(1, len(self.para.blPara.lines)))
                    st = ParagraphStyle("key_small", parent=key_note, fontSize=fs, leading=fs * 1.2)
                    p = Paragraph(txt, st)
                    p.wrap(CONTENT_W - 0.4 * inch, ah)
                    if len(p.blPara.lines) * fs * 1.2 <= self.lines_n * self.LH - 2:
                        break
                self.para, self.squeezed = p, True
            self.lines_n = max(self.lines_n, 1)
            if not getattr(self, "squeezed", False):
                self.lines_n = max(self.lines_n, len(self.para.blPara.lines))
        self.h = self.lines_n * self.LH
        return CONTENT_W, self.h + 4

    def split(self, aw, ah):
        """At a page bottom, give up at most one writing line rather than spill onto a new page."""
        fit = int((ah - 4) // self.LH)
        need = len(self.para.blPara.lines) if self.para else 1
        if fit >= max(1, self.n - 1, need) and fit < self.lines_n:
            return [Lines(fit, self.answer, self.key)]
        return []

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#9a9a9a"))
        c.setLineWidth(0.6)
        for k in range(self.lines_n):
            y = self.h - (k + 1) * self.LH + 2
            c.line(0.2 * inch, y, CONTENT_W - 0.1 * inch, y)
        if self.para:
            pw, ph = self.para.wrap(CONTENT_W - 0.4 * inch, self.h)
            if getattr(self, "squeezed", False):
                self.para.drawOn(c, 0.25 * inch, self.h - ph + 2)
            else:
                fs = self.para.style.fontSize
                first_baseline = self.h - self.LH + 2 + 3
                self.para.drawOn(c, 0.25 * inch, first_baseline - ph + fs)


class _Dual(Flowable):
    """Takes its size and page splits from the student flowable, but draws the key flowable."""

    def __init__(self, stu, key):
        super().__init__()
        self.stu, self.key_fl = stu, key

    def wrap(self, aw, ah):
        self.w, self.h = self.stu.wrap(aw, ah)
        self.kw, self.kh = self.key_fl.wrap(aw, max(ah, 10 * inch))
        return self.w, self.h

    def getSpaceBefore(self):
        return self.stu.getSpaceBefore()

    def getSpaceAfter(self):
        return self.stu.getSpaceAfter()

    def draw(self):
        self.key_fl.drawOn(self.canv, 0, self.h - self.kh)

    def split(self, aw, ah):
        sp = self.stu.split(aw, ah)
        if not sp:
            return []
        if isinstance(self.stu, Lines):
            return [_Dual(sp[0], Lines(sp[0].n, self.key_fl.answer, True))]
        kp = self.key_fl.split(aw, ah)
        if len(kp) == len(sp):
            return [_Dual(a, b) for a, b in zip(sp, kp)]
        return sp  # rare: fall back to the student piece


class Worksheet:
    def __init__(self, data, key):
        self.d, self.key = data, key
        self._student_twin = Worksheet(data, False) if key else None
        self.toc = []  # (title, page)
        self.points = []  # (title, page, points)
        self.page_title = ""
        self.page_sub = ""

    # ---------- page decorations ----------
    def header_footer(self, c, doc):
        c.saveState()
        top = PAGE_H - 0.45 * inch
        r = 0.36 * inch
        cx, cy = MARGIN_X + r, top - r
        c.setFillColor(DARK)
        c.circle(cx, cy, r, stroke=0, fill=1)
        c.drawImage(os.path.join(ASSETS, "mascot_small.png"), cx - 0.16 * inch, cy - 0.29 * inch,
                    0.32 * inch, 0.59 * inch, mask="auto")
        x = MARGIN_X + 2 * r + 0.15 * inch
        c.setFont("Poppins-Bold", 15)
        c.setFillColor(colors.black)
        title = self.d["worksheet_title"].upper() + (" ANSWER KEY" if self.key else " STUDENT NOTES")
        c.drawString(x, top - 0.25 * inch, title)
        c.setLineWidth(0.8)
        c.line(x, top - 0.33 * inch, PAGE_W - MARGIN_X, top - 0.33 * inch)
        tp = Paragraph(rich(self.page_title), ParagraphStyle("pt", fontName="Poppins-BoldItalic", fontSize=11,
                                                             leading=13))
        tp.wrap(PAGE_W - MARGIN_X - x - 1.6 * inch, 30)
        tp.drawOn(c, x, top - 0.55 * inch - 3)
        if self.page_sub:
            c.setFont("Poppins-Italic", 8)
            c.setFillColor(colors.HexColor("#666666"))
            c.drawRightString(PAGE_W - MARGIN_X, top - 0.55 * inch, self.page_sub)
        c.setFillColor(colors.black)
        c.setFont("Poppins", 9)
        c.drawString(MARGIN_X - 0.2 * inch, 0.34 * inch, str(doc.page - 1))
        c.setFont("Poppins", 7.5)
        c.setFillColor(colors.HexColor("#777777"))
        c.drawRightString(PAGE_W - MARGIN_X, 0.34 * inch,
                          f"ChemSims.app · Unit {self.d['unit']}: {self.d['unit_title']}")
        c.restoreState()

    def cover(self, c, doc):
        c.saveState()
        c.setFont("Poppins", 11)
        c.drawString(MARGIN_X - 0.1 * inch, PAGE_H - 0.6 * inch, "Name: " + "_" * 58)
        c.drawString(MARGIN_X - 0.1 * inch, PAGE_H - 0.95 * inch,
                     "Class period: ________    Date started: ______________    Date finished: ______________")
        band_top = PAGE_H - 1.25 * inch
        band_h = 2.6 * inch
        c.setFillColor(DARK)
        c.rect(0, band_top - band_h, PAGE_W, band_h, stroke=0, fill=1)
        c.drawImage(os.path.join(ASSETS, "mascot_large.png"), 0.55 * inch, band_top - band_h + 0.3 * inch,
                    1.15 * inch, 2.1 * inch, mask="auto")
        words = self.d["worksheet_title"].upper().split()
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(t, "Poppins-Bold", 30) > PAGE_W - 2.6 * inch and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        size = 30 if len(lines) <= 3 else 24
        c.setFillColor(colors.white)
        c.setFont("Poppins-Bold", size)
        y = band_top - band_h / 2 + (len(lines) - 1) * size * 0.6 - size * 0.35
        for ln in lines:
            c.drawString(2.0 * inch, y, ln)
            y -= size * 1.2
        c.setFillColor(colors.black)
        c.setFont("Poppins", 22)
        c.drawCentredString(PAGE_W / 2, band_top - band_h - 0.45 * inch,
                            "Answer Key" if self.key else "Student Notes")
        c.setFont("Poppins", 10)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawCentredString(PAGE_W / 2, band_top - band_h - 0.72 * inch,
                            f"AP Chemistry Unit {self.d['unit']}: {self.d['unit_title']}  ·  Simulation: {self.d['sim_name']}")
        # TOC panel
        ptop = band_top - band_h - 0.95 * inch
        rows = self.toc_rows()
        ph = 0.75 * inch + 0.26 * inch * len(rows)
        c.setFillColor(PANEL)
        c.rect(0, ptop - ph, PAGE_W, ph, stroke=0, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Poppins-Bold", 15)
        c.drawString(1.1 * inch, ptop - 0.45 * inch, "TOPIC")
        c.drawString(PAGE_W - 2.1 * inch, ptop - 0.45 * inch, "PAGE")
        c.line(1.1 * inch, ptop - 0.5 * inch, 1.1 * inch + pdfmetrics.stringWidth("TOPIC", "Poppins-Bold", 15),
               ptop - 0.5 * inch)
        c.line(PAGE_W - 2.1 * inch, ptop - 0.5 * inch,
               PAGE_W - 2.1 * inch + pdfmetrics.stringWidth("PAGE", "Poppins-Bold", 15), ptop - 0.5 * inch)
        y = ptop - 0.78 * inch
        for t, pg in rows:
            fs = 10.5
            c.setFont("Poppins", fs)
            while pdfmetrics.stringWidth(t, "Poppins", fs) > PAGE_W - 4 * inch and fs > 7:
                fs -= 0.5
                c.setFont("Poppins", fs)
            c.drawString(1.2 * inch, y, t)
            c.setFont("Poppins", 10.5)
            c.drawCentredString(PAGE_W - 1.75 * inch, y, str(pg))
            y -= 0.26 * inch
        c.setFont("Poppins-Bold", 10)
        c.drawCentredString(PAGE_W / 2, 0.75 * inch, "ChemSims.app")
        c.setFont("Poppins", 8)
        c.drawCentredString(PAGE_W / 2, 0.58 * inch, "© ChemSims, 2026")
        c.restoreState()

    def toc_rows(self):
        if self.toc:
            return self.toc
        extra = [("Conclusion", "")] if self.d.get("conclusion") else []
        return [(p["title"], "") for p in self.d["pages"]] + extra + [("Self-Grading Record", "")]

    # ---------- blocks ----------
    def block(self, b, pts):
        t = b["type"]
        k = self.key
        out = []
        if t == "setup":
            out.append(Band("icon_explore.png", b.get("title", "Set up"),
                            b.get("subtitle", "Set the simulation exactly like this before you start")))
            for it in b["items"]:
                out.append(Paragraph(blanks(it, k), bullet, bulletText="•"))
                pts[0] += count_blanks(it)
        elif t == "notes":
            out.append(Band("icon_notes.png", b.get("title", "Guided notes"),
                            b.get("subtitle", "Fill in the blanks using the simulation")))
            for it in b["items"]:
                out.append(Paragraph(blanks(it, k), bullet, bulletText="•"))
                pts[0] += count_blanks(it)
        elif t in ("predict", "question"):
            icon = "icon_notes.png"
            title = b.get("title", "Predict" if t == "predict" else "Analyze")
            sub = b.get("subtitle", "Write your prediction BEFORE you run the simulation" if t == "predict"
                        else "Answer in complete sentences, using evidence from the simulation")
            out.append(Band(icon, title, sub))
            for q in b["items"]:
                prompt = q["prompt"]
                out.append(Paragraph(blanks(prompt, k), bullet, bulletText="•"))
                pts[0] += count_blanks(prompt)
                if q.get("lines", 2):
                    out.append(Lines(q.get("lines", 2), q.get("answer"), k))
                    pts[0] += q.get("points", 2 if t == "question" else 1)
        elif t == "equations":
            out.append(Band("icon_equations.png", b.get("title", "Equations"),
                            b.get("subtitle", "Fill in the equations from the simulation")))
            for it in b["items"]:
                out.append(Paragraph(blanks(it, k, min_chars=16), ParagraphStyle(
                    "eq", parent=body, fontSize=12, leading=26, leftIndent=24)))
                pts[0] += count_blanks(it)
        elif t == "table":
            out.append(Band("icon_equations.png", b.get("title", "Data table"),
                            b.get("subtitle", "Record what the simulation shows")))
            cols = b["columns"]
            data = [[Paragraph(rich(h), cell_head) for h in cols]]
            for row in b["rows"]:
                r = []
                for j, v in enumerate(row):
                    v = "" if v is None else str(v)
                    st = cell_left if (j == 0 and b.get("first_col_left")) else cell
                    if BLANK_RE.fullmatch(v.strip() or "x"):
                        ans = BLANK_RE.fullmatch(v.strip()).group(1).split("|")[0]
                        r.append(Paragraph(f'<font color="{CORAL_HEX}"><b>{rich(ans)}</b></font>' if k else "", st))
                        pts[0] += 1
                    else:
                        r.append(Paragraph(blanks(v, k, 6), st))
                        pts[0] += count_blanks(v)
                data.append(r)
            n = len(cols)
            cw = b.get("col_widths")
            if cw:
                tot = sum(cw)
                widths = [CONTENT_W * 0.96 * x / tot for x in cw]
            else:
                widths = [CONTENT_W * 0.96 / n] * n
            rh = b.get("row_height", 0.42) * inch
            tbl = Table(data, colWidths=widths, rowHeights=[None] + [rh] * (len(data) - 1), hAlign="CENTER")
            tbl.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.8, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4f4f4")),
                ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            out.append(Spacer(1, 4))
            out.append(tbl)
            if b.get("note"):
                out.append(Paragraph(blanks(b["note"], k), small))
        elif t == "calc":
            out.append(Band("icon_equations.png", b.get("title", "Calculate"),
                            b.get("subtitle", "Show your setup, numbers with units, and answer. Then check it against the simulation")))
            for q in b["items"]:
                out.append(Paragraph(blanks(q["prompt"], k), bullet, bulletText="•"))
                pts[0] += count_blanks(q["prompt"])
                out.append(Lines(q.get("lines", 4), q.get("answer"), k))
                pts[0] += q.get("points", 3)
        elif t == "graph":
            out.append(Band("icon_equations.png", b.get("title", "Graph"),
                            b.get("subtitle", "Sketch what the simulation shows and label it")))
            if b.get("prompt"):
                out.append(Paragraph(blanks(b["prompt"], k), bullet, bulletText="•"))
                pts[0] += count_blanks(b["prompt"])
            out.append(GraphFrame(b.get("x_label", ""), b.get("y_label", ""),
                                  height=b.get("height", 2.1) * inch, answer=b.get("answer") if k else None))
            pts[0] += b.get("points", 2)
        elif t == "explore":
            out.append(_Optional(Band("icon_explore.png", b.get("title", "Explore"), b["text"])))
        else:
            raise ValueError(f"unknown block type {t}")
        return out

    # ---------- story ----------
    def story(self):
        s = [NextPageTemplate("content"), PageBreak()]
        for i, p in enumerate(self.d["pages"]):
            pts = [0]
            s.append(_Mark(self, p["title"], p.get("sim_screen", "")))
            for b in p["blocks"]:
                fl = self.block(b, pts)
                if self.key:
                    # Lay the key out with the Student Notes' sizes, so both PDFs break pages identically
                    stu = self._student_twin.block(b, [0])
                    fl = [_Dual(a_, k_) for a_, k_ in zip(stu, fl)]
                # tables and graphs move as one piece; other blocks keep the band with their first item
                if b["type"] in ("table", "graph"):
                    s.append(KeepTogether(fl))
                elif len(fl) >= 2:
                    s.append(KeepTogether(fl[:2]))
                    s.extend(fl[2:])
                else:
                    s.extend(fl)
            s.append(_Points(self, p["title"], pts[0]))
            self._static_pts.append((p["title"], pts[0]))
            s.append(PageBreak())
        if self.key:
            stu = self._student_twin.closing()
            kc = self.closing()
            s.extend(_Dual(a_, k_) if type(a_) is type(k_) and not isinstance(a_, (_Mark, PageBreak)) else k_
                     for a_, k_ in zip(stu, kc))
            s.extend(kc[len(stu):])
        else:
            s.extend(self.closing())
        return s

    def closing(self):
        k = self.key
        s = []
        concl = self.d.get("conclusion", [])
        if concl:
            s.append(_Mark(self, "Conclusion", ""))
            s.append(Band("icon_notes.png", "Conclusion",
                          "Pull it together. Use numbers you recorded on the earlier pages as evidence"))
            for q in concl:
                s.append(Paragraph(blanks(q["prompt"], k), bullet, bulletText="•"))
                s.append(Lines(q.get("lines", 3), q.get("answer"), k))
            s.append(PageBreak())
        s.append(_Mark(self, "Self-Grading Record", ""))
        s.append(Band("icon_equations.png", "Self-grading record",
                      "Grade in a different color pen. Mark each item ✓ or ✗, then write the correction next to every ✗"))
        rows = [[Paragraph("<b>Page</b>", cell_head), Paragraph("<b>Topic</b>", cell_head),
                 Paragraph("<b>Points possible</b>", cell_head), Paragraph("<b>Points earned</b>", cell_head),
                 Paragraph("<b>Corrections made? (Y/N)</b>", cell_head)]]
        total = 0
        for title, page, p in self.points:
            rows.append([Paragraph(str(page), cell), Paragraph(rich(title), cell_left), Paragraph(str(p), cell),
                         Paragraph("", cell), Paragraph("", cell)])
            total += p
        rows.append([Paragraph("", cell), Paragraph("<b>TOTAL</b>", cell_left), Paragraph(f"<b>{total}</b>", cell),
                     Paragraph("", cell), Paragraph("", cell)])
        tbl = Table(rows, colWidths=[w * CONTENT_W * 0.96 for w in (0.08, 0.42, 0.15, 0.15, 0.2)],
                    rowHeights=[None] + [0.28 * inch] * (len(rows) - 1), hAlign="CENTER")
        tbl.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.8, GRID), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4f4f4"))]))
        s.append(tbl)
        s.append(Spacer(1, 4))
        s.append(Paragraph(rich("**Scoring:** each blank or table cell = 1 point · each prediction = 1 point · each "
                                "calculation = 3 points (setup, numbers with units, answer) · each analysis question "
                                "and each graph = 2 points."), small))
        s.append(Spacer(1, 2))
        s.append(Paragraph(rich("The question I got wrong that taught me the most, and why:"), body))
        s.append(Lines(2))
        s.append(Paragraph(rich("Graded by:  ☐ Myself    ☐ A classmate: ______________    ☐ My teacher"
                                "          Teacher initials: ________"), body))
        if k and self.d.get("key_notes"):
            s.append(PageBreak())
            s.append(_Mark(self, "Teacher Notes", "Not for students"))
            s.append(Band("icon_notes.png", "Teacher notes", "Sim values, known sim quirks, and where each answer comes from"))
            for n in self.d["key_notes"]:
                s.append(Paragraph(rich(n), ParagraphStyle("kn", parent=small, leading=13, leftIndent=12,
                                                           bulletIndent=2, spaceAfter=3), bulletText="•"))
        return s


class _Mark(Flowable):
    """Zero-size marker: sets the running page header and records the TOC page."""

    def __init__(self, ws, title, sub):
        super().__init__()
        self.ws, self.title, self.sub = ws, title, sub

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        pass

    def split(self, aw, ah):
        return []  # never start a page just for this marker

    def drawOn(self, canvas, x, y, _sW=0):
        pass

    def split(self, aw, ah):
        return []

    def identity(self, maxLen=None):
        return "mark"


class _Points(Flowable):
    def __init__(self, ws, title, pts):
        super().__init__()
        self.ws, self.title, self.pts = ws, title, pts

    """Zero-height marker at the end of a section. The Self-check score line is drawn in the footer
    of the page where the section ends, so it never pushes content onto a new page."""

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        pass


# Page-header + TOC bookkeeping is done in afterFlowable, so it works across both passes.
def _after_flowable(self, fl):
    ws = getattr(self, "_ws", None)
    if ws is None:
        return
    if isinstance(fl, _Mark):
        ws.page_title, ws.page_sub = fl.title, fl.sub
        if fl.title not in [t for t, _ in ws._toc_tmp]:
            ws._toc_tmp.append((fl.title, self.page - 1))
    elif isinstance(fl, _Points):
        pass
    elif ws._toc_tmp:
        # the last page any real content of the current section lands on gets its Self-check line
        ws._last_page[ws._toc_tmp[-1][0]] = self.page - 1


BaseDocTemplate.afterFlowable = _after_flowable


def build_unit(content_path, out_dir):
    with open(content_path) as f:
        data = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    base = f"Unit {data['unit']} - {data['worksheet_title']}"
    paths = []
    for key in (False, True):
        ws = Worksheet(data, key)
        fname = os.path.join(out_dir, f"{base} - {'Answer Key' if key else 'Student Notes'}.pdf")
        _build(ws, fname)
        paths.append(fname)
    return paths


def _build(ws, path):
    def make():
        doc = BaseDocTemplate(path, pagesize=letter, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                              topMargin=1.3 * inch, bottomMargin=0.7 * inch,
                              title=f"{ws.d['worksheet_title']} - {'Answer Key' if ws.key else 'Student Notes'}",
                              author="ChemSims")
        fr = Frame(MARGIN_X, 0.7 * inch, CONTENT_W, PAGE_H - 2.0 * inch, id="f", leftPadding=0, rightPadding=0)

        def on_content(c, d):
            ws.header_footer(c, d)

        doc.addPageTemplates([PageTemplate("cover", [Frame(0, 0, PAGE_W, PAGE_H)], onPage=ws.cover),
                              PageTemplate("content", [fr], onPage=on_content)])
        doc._ws = ws
        return doc

    # onPage runs when a page starts, before its flowables, so the running header can't know the
    # page's topic yet. Pass 1 records which topic starts on which page; pass 2 uses that for the
    # headers, the cover's TOC page numbers and the self-grading table.
    ws._toc_tmp, ws._last_page, ws._static_pts = [], {}, []
    make().build(ws.story())
    toc = ws._toc_tmp
    start = dict(toc)
    pts = [(t, start[t], n) for t, n in ws._static_pts]
    ws._selfcheck_by_page = {ws._last_page[t]: n for t, n in ws._static_pts if t in ws._last_page}
    # page -> (title, sub) for headers in pass 2
    ws.toc, ws.points = list(toc), list(pts)
    ws._title_by_page = _titles_by_page(toc, ws)
    ws._toc_tmp, ws._last_page, ws._static_pts = [], {}, []

    orig = ws.header_footer

    def hf(c, d):
        t = ws._title_by_page.get(d.page - 1)
        if t:
            ws.page_title, ws.page_sub = t
        orig(c, d)
        pts = ws._selfcheck_by_page.get(d.page - 1)
        if pts is not None:
            c.saveState()
            c.setFont("Poppins-SemiBold", 9)
            c.setFillColor(colors.HexColor("#444444"))
            c.drawRightString(PAGE_W - MARGIN_X, 0.56 * inch, f"Self-check:  ______ / {pts} points")
            c.restoreState()

    ws.header_footer = hf
    make().build(ws.story())
    ws.header_footer = orig


def _titles_by_page(toc, ws):
    subs = {p["title"]: p.get("sim_screen", "") for p in ws.d["pages"]}
    subs["Teacher Notes"] = "Not for students"
    out = {}
    starts = sorted(toc, key=lambda x: x[1])
    last_page = 400
    for i, (t, pg) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else last_page
        for q in range(pg, max(end, pg + 1)):
            out[q] = (t, subs.get(t, ""))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.content)), "pdf")
    for p in build_unit(a.content, out):
        print(p)
