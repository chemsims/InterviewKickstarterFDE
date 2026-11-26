<!-- Findings from the 2026-11-25 Unit 6 session, checked against chemsims/thermodynamics main @ 4a6a0bb. The live site now serves branch unit9-entropy-9.1 @ a905934, so re-check line numbers. -->

# Handoff: Unit 6 Thermochemistry worksheet

Read `worksheets-handoff/HANDOFF-worksheets.md`, then finish the Unit 6 worksheet using `worksheets-handoff/draft/build.py`. Follow Tess's format, using her Unit 2 and Unit 3 PDFs in `worksheets-handoff/reference/`. Replace every guessed blank with the sim's own wording and numbers below. Look up each one in `thermodynamics/src` and give the file and line. Show me the PDF and a change list (blank → new value → file:line). Do not deploy and do not push.

Before you start, run `df -h /`. If less than about 20 GB is free, avoid large installs.

## Rule: use the sim's numbers, not textbook numbers
The sim's values differ from textbook values in a few places: water c = 4.2 (not 4.184), water ΔH_vap = 2230 J/g (not 2260), and C sublimation = 719 (not ~717). If the worksheet uses textbook values, students' answers won't match what they see on screen. Add a one-line note saying textbooks round these differently.

## Part 1: Heat transfer & calorimetry (`src/components/HeatLab.tsx`, `src/physics.ts`)
- Specific heats: water 4.2, iron 0.45, aluminum 0.897, lithium 3.58 J/g·°C (`physics.ts:2-7`)
- Sample mass 10–100 g (default 50). Water mass 20–120 g (default 60). Water starts at 20 °C. The burner has 3 settings, which heat the metal to 40, 70 or 100 °C.
- Formula as shown: −q_system = q_surrounding → −m_s × C_s × (T_f − T_i,s) = m_w × C_w × (T_f − T_i,w)
- Answer-key check: 50 g of iron at 100 °C into 60 g of water at 20 °C gives T_f = 26.6 °C and q = 1652 J
- Don't copy these:
  - The joule line displays "−1652 J = 1652 J" (bug, HeatLab.tsx:306).
  - The default burner setting is 40 or 100 °C depending on how the sim is opened, so the worksheet must name the setting.
  - The step text says "slider" but the control is arrow buttons.

## Part 2: Heating curves (`src/components/HeatingCurveLab.tsx`, `src/heatingCurve/`)
- Water: melts at 0 °C, boils at 100 °C, runs from −10 to 120 °C. c = 2.1 / 4.2 / 1.9 J/g·°C (solid / liquid / vapor). ΔH_f = 333 J/g, ΔH_v = 2230 J/g (`sim/substances.ts`)
- Ethanol liquid c = 2.44, acetone liquid c = 2.18
- Formulas as shown: "ΔH = Cₚ × (T₂ − T₁)", "ΔH_total = ΔH_f + ΔH_v + ΔH"
- Water total: 21 + 333 + 420 + 2230 + 38 = 3042 J. Ethanol 1475.5 J, acetone 999.7 J
- Mass is always 1 g and never shown, so the worksheet must state "1 g".
- Don't copy these:
  - steps.tsx:76 says liquid Cₚ is 4.2 for every substance (bug).
  - The heat capacity is labelled "Cw" for every substance.
  - The plateaus are not to scale.

## Part 3: Bond enthalpies (`src/components/BondEnthalpyLab.tsx`)
- Bond energies: H—H 436, Cl—Cl 242, H—Cl 431, C—H 414, C—C 347. C(s)→C(g) 719 (kJ)
- Formula as shown: "ΔH°rx = ΣΔH°bonds broken − ΣΔH°bonds formed" (+ ΣΔH°sublimation for C₂H₆)
- H₂ + Cl₂ → 2HCl: −184 = 436 + 242 − 2 × 431 (that is −92 kJ per mole of HCl)
- 2C + 3H₂ → C₂H₆: −85 = 3 × 436 − (347 + 6 × 414) + 2 × 719
- Don't copy these:
  - The "Breakind" typo (lines 1736, 1745, 1750).
  - "Forming the ___ bond" with the word missing; it should say C—C (line 1904).
  - The sim shows only "kJ", never kJ/mol.
  - The final −85 row appears before the C—H bonds are formed, so put any "calculate ΔH" blank before that point.
  - The sim has no Hess's law content, despite the 6.9 menu item.

## Part 4: Formation enthalpies (`src/components/FormationReactionLab.tsx`)
- Reaction: C₂H₆ + Cl₂ → C₂H₅Cl + HCl (all coefficients 1)
- "Exothermic (hypothetical)": C₂H₆ −85, Cl₂ 0, C₂H₅Cl −113, HCl −92, giving ΔH°rxn = −120 kJ/mol (lines 58-74)
- "Endothermic": C₂H₆ −85, Cl₂ 0, C₂H₅Cl +15, HCl +20, giving ΔH°rxn = +120 kJ/mol
- Formula: ΔH°rxn = ΣΔH°f(products) − ΣΔH°f(reactants)
- Don't copy these:
  - The endothermic values are made up and contradict the first set. Label them hypothetical.
  - Eₐ has no number.
  - The energy chart is not to scale.
  - "ΔH°rx" and "ΔH°rxn" are both used; pick one.

## Sim bugs to report to the team (separate from the worksheet)
Part 1: "−1652 J = 1652 J". Part 2: liquid Cₚ always shows 4.2. Part 3: "Breakind" typo, missing "C—C", no Hess's law. Part 4: the second dataset's values contradict the first.
