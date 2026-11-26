"""Build a unit lesson plan (PDF + Markdown) from the `lesson_plan` part of a unit content file.

Usage:  python3 build_lesson_plan.py ../units/unit6/content.json [--out DIR]

Every plan follows the same arc, which the user set for all units:
  1. Teacher demo: the teacher projects the sim, introduces the concept and walks
     through the first part of it while students take notes on page 1.
  2. Student sim work over several class periods: students run the sim
     themselves and fill in the paper worksheet as they go, like a lab record.
  3. Grading, teacher's choice: students self-grade (or peer-grade) with the
     answer key, or the teacher grades.
The shared sections (grading options, paper lab-sheet norms) are written here
once so every unit says the same thing; unit-specific parts come from the file.
"""
import argparse
import json
import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_worksheet as bw  # noqa: E402  (registers fonts)
from textfmt import rich  # noqa: E402

W = letter[0] - 1.3 * inch
H1 = ParagraphStyle("h1", fontName="Poppins-Bold", fontSize=20, leading=24, spaceAfter=2)
H1s = ParagraphStyle("h1s", fontName="Poppins", fontSize=11, leading=14, textColor=colors.HexColor("#555555"),
                     spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="Poppins-Bold", fontSize=13, leading=16, spaceBefore=12, spaceAfter=5,
                    textColor=colors.white, backColor=bw.DARK, borderPadding=(4, 6, 4, 6), keepWithNext=1)
H3 = ParagraphStyle("h3", fontName="Poppins-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=3,
                    keepWithNext=1)
P = ParagraphStyle("p", fontName="Poppins", fontSize=9.5, leading=13.5, spaceAfter=4)
B = ParagraphStyle("b", parent=P, leftIndent=14, bulletIndent=3, spaceAfter=2)
C = ParagraphStyle("c", parent=P, fontSize=8.5, leading=11.5, spaceAfter=0)
CB = ParagraphStyle("cb", parent=C, fontName="Poppins-Bold")
BOX = ParagraphStyle("box", parent=P, backColor=colors.HexColor("#f1f1f1"), borderPadding=6, spaceBefore=4,
                     spaceAfter=8)


def bullets(items, md, style=B):
    out = []
    for it in items:
        out.append(Paragraph(rich(it), style, bulletText="•"))
        md.append(f"- {it}")
    md.append("")
    return out


def table(rows, widths, md, header=True):
    data = [[Paragraph(rich(str(c)), CB if (header and i == 0) else C) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[W * w for w in widths], repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#888888")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")))
    t.setStyle(TableStyle(st))
    md.append("| " + " | ".join(str(c) for c in rows[0]) + " |")
    md.append("|" + "---|" * len(rows[0]))
    for r in rows[1:]:
        md.append("| " + " | ".join(str(c).replace("\n", " ") for c in r) + " |")
    md.append("")
    return t


def h2(text, md):
    md.append(f"## {text}\n")
    return Paragraph(rich(text), H2)


def h3(text, md):
    md.append(f"### {text}\n")
    return Paragraph(rich(text), H3)


def para(text, md, style=P):
    md.append(text + "\n")
    return Paragraph(rich(text), style)


def build(content_path, out_dir):
    with open(content_path) as f:
        d = json.load(f)
    lp = d["lesson_plan"]
    os.makedirs(out_dir, exist_ok=True)
    base = f"Unit {d['unit']} - {d['worksheet_title']} - Lesson Plan"
    md = []
    s = []
    days = lp["days"]
    n_days = len(days)
    mins = lp.get("period_minutes", 50)

    md.append(f"# AP Chemistry Unit {d['unit']}: {d['unit_title']} — Simulation Lesson Plan\n")
    s.append(Paragraph(rich(f"AP Chemistry Unit {d['unit']}: {d['unit_title']}"), H1))
    sub = (f"Simulation lesson plan · {d['sim_name']} · {n_days} class periods of about {mins} minutes · "
           f"Worksheet: “{d['worksheet_title']}” Student Notes + Answer Key")
    s.append(para(sub, md, H1s))

    # ---- at a glance
    s.append(h2("At a glance", md))
    glance = [["", ""],
              ["AP topics", "; ".join(lp["ap_topics"])],
              ["Simulation", f"{d['sim_name']} — {lp.get('sim_location', '')}"],
              ["Big idea", lp["essential_question"]],
              ["Time", f"{n_days} periods × ~{mins} min (1 teacher-demo day, "
                       f"{n_days - 2} student sim days, 1 grading and wrap-up day)"],
              ["Student product", "The paper worksheet, filled in by hand like a lab record, then graded"]]
    s.append(table(glance[1:], [0.2, 0.8], md, header=False))

    s.append(h2("Learning objectives", md))
    s.append(para("By the end of this unit, students will be able to:", md))
    s.extend(bullets(lp["objectives"], md))

    s.append(h2("Materials and preparation", md))
    mats = [f"One printed **{d['worksheet_title']} Student Notes** packet per student "
            "(print single-sided if students will tear out pages, double-sided otherwise)",
            "One device per student or per pair, signed in to ChemSims.app",
            "Teacher computer and projector for the demo",
            f"The **Answer Key** PDF, printed or ready to project. Students can't download it: the site "
            "blocks the Answer Key for student accounts",
            "Two pen colors per student: one to work in, one (green or red) for grading"] + lp.get("materials", [])
    s.extend(bullets(mats, md))
    s.append(h3("Before day 1 (about 20 minutes)", md))
    prep = ["Run the whole sim yourself once with the Answer Key beside you, so the numbers you see match it."] + \
        lp.get("prep", [])
    s.extend(bullets(prep, md))

    if lp.get("vocabulary"):
        s.append(h3("Key vocabulary", md))
        s.append(para(" · ".join(lp["vocabulary"]), md))
    if lp.get("prior_knowledge"):
        s.append(h3("Students should already know", md))
        s.extend(bullets(lp["prior_knowledge"], md))

    # ---- how the unit runs (shared)
    s.append(h2("How this unit runs", md))
    s.append(para(
        "**In short:** you show the sim first, students then work through it themselves over a few periods "
        "while they fill in the paper worksheet, and at the end the work is graded, by the students "
        "themselves or by you.", md))
    flow = [["Phase", "Who drives", "What happens"],
            ["1. Teacher demo (day 1)", "Teacher at the projector",
             "You open the sim, introduce the concept, and walk through the first part of it. Students watch, "
             "answer your questions out loud, and fill in the first worksheet page with you."],
            [f"2. Student sim work (days 2–{n_days - 1})", "Students, alone or in pairs",
             "Students run the sim themselves and fill in the worksheet as they go. They record settings, "
             "predictions, data and calculations on paper, like a lab notebook. You circulate."],
            [f"3. Grading and wrap-up (day {n_days})", "Students or teacher (your choice)",
             "Students self-grade with the answer key, or you collect and grade. Then a short class discussion "
             "and an exit ticket."]]
    s.append(table(flow, [0.24, 0.2, 0.56], md))
    s.append(h3("Paper lab-sheet norms (read these to students on day 1)", md))
    norms = ["The worksheet is your lab record. Write in pen or dark pencil, and don't erase: cross out with one "
             "line so your first thinking stays visible.",
             "Fill in **Set up** first and match the sim to it exactly. The answers depend on those settings.",
             "Write every **Predict** answer *before* you run that part of the sim. A wrong prediction loses no "
             "points; a blank one does.",
             "Copy numbers exactly as the sim shows them, with units.",
             "Show setup, numbers with units, and the answer for every **Calculate** item, then check it against "
             "the sim.",
             "At the bottom of each page, leave the **Self-check** score blank until grading day."]
    s.extend(bullets(norms, md))

    # ---- day by day
    s.append(PageBreak())
    s.append(h2("Day-by-day plan", md))
    for day in days:
        block = []
        title = f"Day {day['day']}: {day['title']}"
        block.append(h3(title, md))
        if day.get("goal"):
            block.append(para(f"**Goal:** {day['goal']}", md))
        if day.get("worksheet_pages"):
            block.append(para(f"**Worksheet pages:** {day['worksheet_pages']}", md))
        rows = [["Minutes", "Activity"]] + [[m[0], m[1]] for m in day["agenda"]]
        block.append(table(rows, [0.12, 0.88], md))
        s.append(KeepTogether(block[:2]))
        s.extend(block[2:])
        if day.get("demo_script"):
            s.append(para("**Demo script.** Do and say this at the projector:", md))
            rows = [["#", "On screen (you click)", "You say / ask", "Students write"]]
            for i, st in enumerate(day["demo_script"], 1):
                rows.append([str(i), st.get("do", ""), st.get("say", ""), st.get("students", "")])
            s.append(table(rows, [0.06, 0.32, 0.4, 0.22], md))
        if day.get("circulate"):
            s.append(para("**While students work, check for these:**", md))
            s.extend(bullets(day["circulate"], md))
        if day.get("checkpoint"):
            s.append(para(f"**Checkpoint before they move on:** {day['checkpoint']}", md, BOX))
        if day.get("early_finishers"):
            s.append(para(f"**Early finishers:** {day['early_finishers']}", md))
        if day.get("homework"):
            s.append(para(f"**Homework:** {day['homework']}", md))

    # ---- grading (shared)
    s.append(PageBreak())
    s.append(h2("Grading: your choice of self-grading or teacher grading", md))
    s.append(para(
        "**In short:** both options use the same answer key and the point values printed on the worksheet. "
        "Self-grading is faster and makes students study their mistakes. Teacher grading is more reliable. "
        "Pick per class, or mix them.", md))
    s.append(h3("Point values (printed on the worksheet's last page)", md))
    s.append(para("Each blank or table cell = 1 point · each prediction = 1 point · each calculation = 3 points "
                  "(setup, numbers with units, answer) · each analysis question and each graph = 2 points. Every "
                  "page shows its own total in its **Self-check** box.", md))
    s.append(h3("Option A: students self-grade (about 25 minutes)", md))
    a = ["Students put away the pen they worked in and take out a different color (green or red).",
         "Project the Answer Key one page at a time, or hand out printed copies to share.",
         "Students mark each item ✓ or ✗. For each ✗ they write the correct answer next to theirs, plus a few "
         "words on why.",
         "Predictions get the point if they were written down before the sim was run, right or wrong.",
         "Students total each page in its Self-check box, copy the totals to the Self-Grading Record on the last "
         "page, and write the question that taught them the most.",
         "Collect the packets. Spot-check 3–5 items per packet against the key, and initial the record."]
    s.extend(bullets(a, md))
    s.append(h3("Option B: you grade", md))
    bb = ["Collect the packets at the end of the last sim day.",
          "Grade with the same key and point values. Check the calculations and analysis questions closely; "
          "the blanks go quickly.",
          "Hand back with the Self-Grading Record filled in. Ask students to correct their ✗ items in a second "
          "color for partial credit back (a common choice is half the lost points)."]
    s.extend(bullets(bb, md))
    s.append(h3("Option C: peer grading", md))
    s.append(para("Students swap packets and grade with the key as in Option A, then return them; the owner "
                  "writes the corrections. The grader signs the record (“A classmate”).", md))
    s.append(h3("Pros, cons and risks", md))
    pc = [["", "Self-grading (A)", "Teacher grading (B)", "Peer grading (C)"],
          ["Pros", "Fast; students see every mistake right away and correct it while the sim is fresh; no "
                   "grading load for you",
           "Most accurate; you see each student's thinking; best for a recorded grade",
           "Students read someone else's reasoning; quicker than B"],
          ["Cons", "Students may mark generously or copy the key into blanks",
           "Takes your time (about 3–5 min per packet); feedback arrives days later",
           "Uneven grading; some students feel exposed"],
          ["Lower the risk by", "Requiring a different pen color, spot-checking, and grading for completion "
                                "plus corrections rather than raw accuracy",
           "Grading only the calculation and analysis items closely",
           "Anonymous swaps (numbers instead of names); you spot-check"]]
    s.append(table(pc, [0.16, 0.28, 0.28, 0.28], md))
    s.append(para("**A sensible default:** self-grade (A) for the practice grade, then use the exit ticket or a "
                  "short quiz for the recorded grade.", md, BOX))

    # ---- unit specifics
    if lp.get("misconceptions"):
        s.append(h2("Common misconceptions and how the sim helps", md))
        rows = [["Misconception", "What to do in the sim"]] + [[m["misconception"], m["sim_fix"]] for m in
                                                               lp["misconceptions"]]
        s.append(table(rows, [0.45, 0.55], md))
    if lp.get("sim_cautions"):
        s.append(h2("Sim cautions: tell students before they hit these", md))
        s.append(para("These are places where the sim's text or numbers can confuse students. The worksheet already "
                      "works around them; mention them during the demo.", md))
        s.extend(bullets(lp["sim_cautions"], md))
    if lp.get("differentiation"):
        s.append(h2("Differentiation", md))
        dd = lp["differentiation"]
        if dd.get("support"):
            s.append(h3("Support", md))
            s.extend(bullets(dd["support"], md))
        if dd.get("extension"):
            s.append(h3("Extension", md))
            s.extend(bullets(dd["extension"], md))
    if lp.get("exit_ticket"):
        s.append(h2("Exit ticket (last day)", md))
        for i, q in enumerate(lp["exit_ticket"], 1):
            s.append(para(f"**{i}.** {q['question']}", md))
            s.append(para(f"*Answer:* {q['answer']}", md, ParagraphStyle("ans", parent=P, leftIndent=14,
                                                                         textColor=bw.CORAL)))
    if lp.get("ap_practice"):
        s.append(h2("AP-style practice tied to the sim", md))
        for i, q in enumerate(lp["ap_practice"], 1):
            s.append(para(f"**{i}.** {q['question']}", md))
            s.append(para(f"*Answer:* {q['answer']}", md, ParagraphStyle("ans2", parent=P, leftIndent=14,
                                                                         textColor=bw.CORAL)))

    def onpage(c, doc):
        c.saveState()
        c.setFont("Poppins", 7.5)
        c.setFillColor(colors.HexColor("#777777"))
        c.drawString(0.65 * inch, 0.45 * inch, f"ChemSims.app · Unit {d['unit']} lesson plan · for teachers")
        c.drawRightString(letter[0] - 0.65 * inch, 0.45 * inch, str(doc.page))
        c.restoreState()

    pdf = os.path.join(out_dir, base + ".pdf")
    doc = SimpleDocTemplate(pdf, pagesize=letter, leftMargin=0.65 * inch, rightMargin=0.65 * inch,
                            topMargin=0.6 * inch, bottomMargin=0.7 * inch, title=base, author="ChemSims")
    doc.build(s, onFirstPage=onpage, onLaterPages=onpage)
    mdp = os.path.join(out_dir, base + ".md")
    with open(mdp, "w") as f:
        f.write("\n".join(md))
    return pdf, mdp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.content)), "pdf")
    for p in build(a.content, out):
        print(p)
