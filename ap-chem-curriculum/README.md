# AP Chemistry simulation worksheets and lesson plans

One worksheet (Student Notes + Answer Key) and one lesson plan for each of the nine AP Chemistry units,
built on the ChemSims.app simulations.

## What's here

| Folder | What it holds |
|---|---|
| `OVERVIEW.md` | **Start here.** All nine units at a glance, how to use them, what to check before teaching, AP topics the sims miss |
| `SIM-BUGS.md` | Every sim bug found while writing the worksheets, by unit, for the dev team |
| `units/unitN/content.json` | Everything for unit N: worksheet pages, answer key, lesson plan. **Edit this, then rebuild.** |
| `units/unitN/sources.md` | Where every answer comes from in the sim code (file:line), values checked by hand, and sim bugs found |
| `output/worksheets/` | Printable PDFs: `Unit N - <title> - Student Notes.pdf` and `... - Answer Key.pdf` |
| `output/lesson-plans/` | `Unit N - <title> - Lesson Plan.pdf` and an editable `.md` copy |
| `tools/` | The two builders, fonts (Poppins, OFL) and the mascot/icons from Tess's Unit 2 worksheet |

Rebuild everything:

```bash
python3 tools/build_all.py
```

## How every lesson plan runs

1. **Teacher demo (day 1).** The teacher projects the sim, introduces the concept, and walks through the first
   part of it with a scripted demo. Students fill in the first worksheet page along with the teacher.
2. **Student sim work (several periods).** Students run the sim themselves and fill in the paper worksheet as
   they go, like a lab record: set-up, prediction, data table, calculations, guided notes, analysis.
3. **Grading (last day).** The teacher's choice: students self-grade (or peer-grade) in a second pen color with
   the answer key, or the teacher grades. Each section ends with a Self-check score in its page footer; the
   packet ends with a Conclusion page and a Self-Grading Record page.

The Answer Key is laid out from the Student Notes' measurements, so both PDFs have the same page breaks and
page numbers (the key adds one Teacher Notes page at the end). A key answer longer than the student's writing
space is printed smaller to fit. An EXPLORE box that doesn't fit at the end of a section is left out (it carries
no points).

## Rules every worksheet follows (from the Unit 6 thermochemistry review)

1. **Use the sim's numbers, not textbook numbers.** Where the sim rounds differently (e.g. water c = 4.2, not
   4.184), the worksheet uses the sim's value so students' answers match what's on screen. The Answer Key's
   Teacher Notes page lists each difference.
2. **Every answer is traceable.** Each blank's answer is quoted from the sim's code or worked out from its
   constants; `sources.md` gives the file and line.
3. **Name the settings.** If the result depends on a setting (a default that changes, a slider position, a
   chosen substance), the page's Set Up box tells students exactly what to choose.
4. **Don't copy sim bugs.** Typos, wrong labels, contradicting values and text students never see are left
   out of the worksheet and listed in `sources.md` and the lesson plan's "Sim cautions".
5. **Don't ask students to read numbers off graphs that aren't to scale.** Ask for shape and direction instead.
6. **Put "calculate" items before the sim reveals the answer**, so students compute first and then check.
7. **Label made-up data as hypothetical** when the sim uses invented values.
8. **Gaps are stated, not papered over.** If an AP topic in the unit isn't in the sim, the lesson plan says so
   and tells the teacher what to use instead.

## Content file format

`content.json` (UTF-8, plain Unicode chemistry text: H₂O, ΔH°, →, ⇌, 10⁻³; `**bold**` and `*italic*` work).

```jsonc
{
  "unit": 6,
  "unit_title": "Thermochemistry",          // AP unit name
  "worksheet_title": "Thermochemistry",     // shown on the cover and every page header
  "sim_name": "Thermodynamics Lab",
  "pages": [                                 // one worksheet section per sim screen/part
    {
      "title": "Heat Transfer & Calorimetry",   // page header + cover table of contents
      "sim_screen": "Part 1 · Guided mode",     // small grey text, top right
      "blocks": [ /* see block types below, in the order students meet them */ ]
    }
  ],
  "conclusion": [ { "prompt": "...", "answer": "...", "lines": 3 } ],
  "key_notes": [ "Teacher-only notes printed at the end of the Answer Key" ],
  "lesson_plan": { /* see below */ }
}
```

**Blanks:** write `{{answer}}` anywhere in text. Students see an underline sized to the answer; the key shows
the answer in coral. `{{answer|20}}` forces a 20-character line.

**Block types**

| type | fields | renders as |
|---|---|---|
| `setup` | `items: [str]` | SET UP band: exact sim settings to use |
| `predict` | `items: [{prompt, answer, lines}]` | PREDICT band + writing lines (1 pt each) |
| `notes` | `items: [str with {{blanks}}]` | GUIDED NOTES bullets (1 pt per blank) |
| `equations` | `items: [str with {{blanks}}]` | EQUATIONS band, large type |
| `table` | `columns: [str]`, `rows: [[str]]`, optional `col_widths`, `row_height` (inches), `first_col_left`, `note` | DATA TABLE; a cell that is exactly `{{x}}` is a blank cell (1 pt) |
| `calc` | `items: [{prompt, answer, lines, points}]` | CALCULATE band + work lines (3 pts default) |
| `graph` | `prompt`, `x_label`, `y_label`, `answer`, `height` (inches) | GRAPH band + blank axes (2 pts) |
| `question` | `items: [{prompt, answer, lines, points}]` | ANALYZE band + lines (2 pts default) |
| `explore` | `text` | EXPLORE box (no points) |

Any band's `title`/`subtitle` can be overridden.

**`lesson_plan`**

```jsonc
{
  "period_minutes": 50,
  "ap_topics": ["6.1 Endothermic and Exothermic Processes", "..."],
  "sim_location": "ChemSims.app → Simulations → Thermodynamics Lab (Parts 1–4)",
  "essential_question": "...",
  "objectives": ["..."],
  "materials": ["extra items only; the shared ones are added automatically"],
  "prep": ["teacher prep steps beyond 'run the sim once'"],
  "vocabulary": ["..."],
  "prior_knowledge": ["..."],
  "days": [
    { "day": 1, "title": "Teacher demo: ...", "goal": "...", "worksheet_pages": "Cover + p. 1",
      "agenda": [["0–5", "Warm-up: ..."], ["5–35", "Demo (script below)"], ["35–50", "..."]],
      "demo_script": [ { "do": "what to click", "say": "what to say/ask", "students": "what students write" } ] },
    { "day": 2, "title": "Student sim work: ...", "worksheet_pages": "pp. 1–2",
      "agenda": [["..", ".."]], "circulate": ["what to check"], "checkpoint": "...",
      "early_finishers": "..." },
    { "day": 5, "title": "Grading and wrap-up", "agenda": [["..", ".."]] }
  ],
  "misconceptions": [ { "misconception": "...", "sim_fix": "..." } ],
  "sim_cautions": ["sim quirks to warn about, in plain words"],
  "differentiation": { "support": ["..."], "extension": ["..."] },
  "exit_ticket": [ { "question": "...", "answer": "..." } ],
  "ap_practice": [ { "question": "...", "answer": "..." } ]
}
```

The shared sections (how the unit runs, paper lab-sheet norms, the three grading options with pros, cons and
risks) are written by `tools/build_lesson_plan.py`, so they read the same in every unit.
