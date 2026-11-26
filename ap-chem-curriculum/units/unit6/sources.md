# Unit 6 Thermochemistry: sources for every answer

Sim: **Thermodynamics Lab** (chemsims.app/sims/thermodynamics), checked out at the deployed commit
`a905934` (branch `unit9-entropy-9.1`, 2026-11-17) in `/home/user/thermodynamics`. All paths below are
relative to `/home/user/thermodynamics/src/`. Unit 6 = Parts 1–4 (`?part=1..4`); Parts 91–94 are Unit 9
and are not used.

Yesterday's notes (`prior-findings-2026-11-25.md`, made against `main @ 4a6a0bb`) were re-checked line
by line against `a905934`. Every value still holds; most line numbers moved (e.g. the "−1652 J = 1652 J"
line is now `HeatLab.tsx:1146-1155`, not :306). The newer commit also confirmed some new quirks (listed below).

## Part 1 · Heat Transfer & Calorimetry (`components/HeatLab.tsx`, `physics.ts`)

| Worksheet item | Answer | Source |
|---|---|---|
| Menu name | "Part 1 · Simulation 1" / "Heat transfer and calorimetry" | `unit6/parts.ts:16-18`; kicker format `components/Unit6MenuDrawer.tsx:109` |
| Mode buttons | "Guided" / "Free Explore" | `components/lab/LabModeSwitch.tsx:23,37` |
| Metal picker | "Choose a Metal"; iron default, order iron → aluminum → lithium | `HeatLab.tsx:1160`, `:197`, `:54` |
| Mass buttons | ◀ ▶, ±5 g, 10–100 g, default 50 g | `HeatLab.tsx:1083-1101`, `:198` |
| Water slider | 20–120 g, step 1, default 60 g; water starts at 20 °C | `HeatLab.tsx:1271-1281`, `:199-200` |
| Burner | 3 positions (0/1/2); metal T = 40 + flame × (100 − 40) → 40, 70, 100 °C | `HeatLab.tsx:1217-1234`, `:87`, `:288-291` |
| Burner reset to lowest | initial state 0, and reset to 0 whenever `metalId` changes | `HeatLab.tsx:203`, `:206-208` |
| Notes: "Energy cannot be **destroyed** or **created**. Energy is **transferred**." | quoted | `HeatLab.tsx:998` |
| Notes: c values 0.45 / 0.897 / 3.58 / 4.2 | constants; shown in bubble (step 1) and formula line | `physics.ts:2,5-7`; `HeatLab.tsx:1007-1011`, `:1135` |
| Notes: metal = **system**, water = **surroundings** | quoted | `HeatLab.tsx:1052-1053` |
| Notes: **hot** → **cold**; metal **loses**, water **gains** until T_f | quoted (two lines combined) | `HeatLab.tsx:1044`, `:1450-1451` |
| Equations | "−q_system = q_surrounding"; "−mₛ × Cₛ × (T_f − T_i,s) = m_w × C_w × (T_f − T_i,w)" | `HeatLab.tsx:1119-1126` |
| Formula number line (Set Up check) | "−50 × 0.45 × ( □ − 100) = 60 × 4.2 × ( □ − 20)" | `HeatLab.tsx:1127-1145` |
| T_f (displayed, 1 dp) | Fe 26.6, Al 32.1, Li 53.2 °C | worked from `physics.ts:13-25` (equilibriumTemp), displayed via `HeatLab.tsx:1131` |
| q (right-hand box, rounded) | Fe 1652, Al 3046, Li 8373 J | `HeatLab.tsx:308`, `:1153` |
| Calc 1 (T_f before drop) | 7290 ÷ 274.5 = 26.6 °C | worked from `physics.ts:21-24` |
| Calc 2 (q from rounded T_f) | 60 × 4.2 × 6.6 = 1663 J; accept 1650–1665 | worked; sim shows 1652 (unrounded T_f 26.557) |
| Graph | "Time (s)" vs "Temperature"; curves converge exponentially to T_f (to scale, real data) | `components/temperature-chart/EquilibriumLineChart.tsx:50-51`; `HeatLab.tsx:409-431` |
| Run starts by itself after the drop | auto-start effect | `HeatLab.tsx:389-394` |
| Explore values (40 °C burner, iron) | T_f 21.6 °C, q 413 J | worked from `physics.ts:13-25` |

## Part 2 · Heating Curves & Phase Changes (`components/HeatingCurveLab.tsx`, `heatingCurve/`)

| Worksheet item | Answer | Source |
|---|---|---|
| Menu name | "Energy diagrams, phases, and reaction enthalpy" | `unit6/parts.ts:29` |
| Substance picker | "Choose a Substance"; water default | `HeatingCurveLab.tsx:1915`, `:1337` |
| Mass = 1 g (never shown) | `massG: 1` for all three | `heatingCurve/sim/substances.ts:25,39,53` |
| "ΔH = Cₚ × (T₂ − T₁)", T₁ **initial**, T₂ **current**, Cₚ depends on **substance** and **physical state**, solid water **2.1** | quoted | `heatingCurve/steps.tsx:36-48`; value `substances.ts:30` |
| Liquid water Cₚ **4.2** | shown in liquid phase | `steps.tsx:64-69`; `substances.ts:31` |
| ΔH_f "enthalpy of **fusion**", energy to **melt**, water **333** J | quoted | `steps.tsx:88-95`; `substances.ts:33` |
| Phase change: T **constant**, ΔH = Cₚ(T₂ − T₁) is **zero**, energy breaks **intermolecular forces** | quoted | `steps.tsx:103-109` |
| ΔH_v "enthalpy of **vaporization**" **2230** J; vapor Cₚ **1.9** | quoted | `steps.tsx:117-125`; `substances.ts:32,34` |
| Equations | "ΔH = C (T₂ − T₁)", "ΔH_total = ΔH_f + ΔH_v + ΔH" | `HeatingCurveLab.tsx:2211`, `:2222-2223`; formula popup `:2570` |
| Leg values water | 21, 333, 420, 2230, 38; total 3042 J | `heatingCurve/sim/heatingModel.ts:30-34`; displayed total line `heatingModel.ts:155` via `HeatingCurveLab.tsx:2226` ("3042 = 333 + 2230 + (21 + 420 + 38)") |
| Melting / boiling points (thermometer) | water 0/100; ethanol −114/78; acetone −95/56 °C | `substances.ts:28-29,42-43,56-57`; readout `HeatingCurveLab.tsx:2082` |
| Liquid Cₚ ethanol / acetone | 2.44 / 2.18 | `substances.ts:45,59` |
| ΔH_f / ΔH_v ethanol | 104 / 841 J | `substances.ts:47-48`; bubble `steps.tsx:95,121` |
| ΔH_f / ΔH_v acetone | 98 / 518 J | `substances.ts:61-62` |
| ΔH_total ethanol | 24 + 104 + 468.48 + 841 + 38 = 1475.5 J | worked from `substances.ts:36-49`, rounded by `heatingModel.ts:24-26` |
| ΔH_total acetone | 21.5 + 98 + 329.18 + 518 + 33 = 999.7 J | worked from `substances.ts:50-63` |
| Graph axes | "Heat (J)" / "Temperature"; schematic equal-size legs (not to scale) | `HeatingCurveLab.tsx:422`, `:73-82` (SCHEM_VERTS) |
| Q3 condensing −2230 J | reverse of boiling; AP reasoning (sim shows heating only) | worked from `substances.ts:34` |

## Part 3 · Bond Enthalpies (`components/BondEnthalpyLab.tsx`)

| Worksheet item | Answer | Source |
|---|---|---|
| Menu name | "Bond enthalpies, formation, and Hess's law" | `unit6/parts.ts:40` |
| Compound picker | "Choose a Compound": HCl, C2H6 (NaOH commented out) | `BondEnthalpyLab.tsx:2809-2817`, `:65-69` |
| "Energy is involved in the **breaking** of atoms' bonds." | quoted | `:1720` |
| H—H **436** kJ "per mole of bonds" | quoted | `:1728`; callout `:298`; table `:2312-2315` |
| Cl—Cl **242** kJ | callout `:338`; table `:2322-2325` (bubble text with this value has the "Breakind" typo, `:1736,1745`) |
| Forming H—Cl **released** **431** kJ | quoted | `:1770`; callouts `:434,454`; table `:2332-2335` |
| Breaking bonds **costs** energy; forming bonds **returns** it | quoted (info panel) | `:3030` |
| Equation (HCl) | "ΔH°rx = ΣΔH°bonds broken − ΣΔH°bonds formed" | `:1511` |
| Calc 1 | 436 + 242 − 2 × 431 = −184 kJ; −92 kJ per mol HCl | sim row `:1586-1589`; bubbles `:1776-1778`, `:1786-1787` |
| C₂H₆: "Energy is required to change **physical state** of molecules." | quoted | `:1836` |
| C(s) → C(g) **719** kJ per mole | quoted | `:1845`; table `:2418-2421` |
| Forming C—C released **347** kJ | quoted | `:1892`; table `:2370-2373` |
| C—H 414 kJ (given in prompt) | callout `:696`; table `:2360-2363` (shown from step 4 only) |
| Equation (C₂H₆) | "… + ΣΔH°sublimation" | `:1504-1505` |
| Calc 2 | 3 × 436 − (347 + 6 × 414) + 2 × 719 = −85 kJ | sim row `:1663-1666`; bubble `:1924-1927` |
| Q formation: −85 kJ is "enthalpy of formation of 1 mole of C₂H₆" | quoted | `:1934-1938` |
| Diagrams (Explore) | images `assets/part_3_graphs/graphC2H6(12).png`, `graphHCI(4).png` | imported `:19,31` |

## Part 4 · Enthalpy of Formation (`components/FormationReactionLab.tsx`)

| Worksheet item | Answer | Source |
|---|---|---|
| Menu name | "Part 4" / "Formation Enthalpies" | `unit6/parts.ts:54-55` |
| Reaction | C₂H₆ + Cl₂ → C₂H₅Cl + HCl | header `:1225-1229` |
| Reaction type picker / default | "Reaction type": Exothermic (default) / Endothermic | `:1788-1795`, `:846` |
| ΔH°f exothermic set | C₂H₆ −85, Cl₂ 0, C₂H₅Cl −113, HCl −92 | `:64-67`, rendered `:2040-2045` |
| ΔH°f endothermic set | −85, 0, +15, +20 | `:70-73` |
| Equation | "ΔH°rx = ΔH°f products − ΔH°f reactants" | `:2048-2050` |
| Calc exo | (−113 + −92) − (−85 + 0) = −120 kJ/mol | sim row `:1292-1296`; bubble `:1599`; info `:2155-2156` |
| Calc endo | (15 + 20) − (−85 + 0) = +120 kJ/mol | sim row `:1300-1304`; bubble `:1616`; info `:2158-2159` |
| Notes: "With sufficient **energy**, reactants will turn into products!" | quoted | `:1352` |
| Notes: flame slider → **Activation Energy** | quoted | `:1386` |
| Notes: burner never moves the reactant or product **plateaus**; from tabulated **ΔH°f** values | quoted | `:1446-1448` |
| Notes: Cl₂ ΔH°f = **0**, **element** in standard state | 0 from table `:65`; "element" is the AP definition (the sim gives no reason) |
| Graph | exothermic: products below reactants; endothermic: above; Eₐ label has no number | geometry `:131-133`, `:165-167`; Eₐ / ΔH°rxn labels `:527-541` |
| Q: endothermic set hypothetical | HCl +20 contradicts −92 (Part 3 `BondEnthalpyLab.tsx:1787` and exo set `:67`) | |

## Values checked by hand

All checked with python (`check.py` in the session scratchpad):

```
Part 1  T_f = (mₛcₛTₛ + m_w c_w T_w)/(mₛcₛ + m_w c_w), c_w = 4.2, m_w = 60, T_w = 20, mₛ = 50, Tₛ = 100
  Fe: 7290/274.5   = 26.5574 → 26.6 °C;  q = 60·4.2·6.5574 = 1652 J (left side 1652 J)
  Al: (4485+5040)/(44.85+252) = 32.0869 → 32.1 °C; q = 3046 J
  Li: (17900+5040)/(179+252)  = 53.2251 → 53.2 °C; q = 8373 J
  from rounded T_f: Fe 60·4.2·6.6 = 1663.2; Al 3049.2; Li 8366.4 (accept range given in key)
  Fe at 40 °C burner: 21.6 °C, 413 J;  Al at 40 °C: 23.0 °C (used in "circulate")
  ΔT iron 100 − 26.6 = 73.4; water 6.6;  m·c: iron 22.5 J/°C, water 252 J/°C
Part 2  water: 2.1·10 = 21; 333; 4.2·100 = 420; 2230; 1.9·20 = 38 → 3042 J; 2230/333 = 6.70
  ethanol: 2.4·10 = 24; 104; 2.44·192 = 468.48; 841; 1.9·20 = 38 → 1475.48 → 1475.5 J
  acetone: 2.15·10 = 21.5; 98; 2.18·151 = 329.18; 518; 1.65·20 = 33 → 999.68 → 999.7 J
Part 3  436 + 242 − 2·431 = −184; /2 = −92
  3·436 = 1308; 347 + 6·414 = 2831; 2·719 = 1438; 1308 − 2831 + 1438 = −85
Part 4  (−113 − 92) − (−85 + 0) = −205 + 85 = −120;  (15 + 20) − (−85) = +120
Conclusion  333 J/g × 18.0 g/mol = 5994 J/mol ≈ 6.0 kJ/mol
AP FRQ  60·4.2·12.1 = 3049 J;  50·0.897·(32.1 − 100) = −3045 J
AP MCQ  (A) 436 + 242 − 431 = 247;  (B) −184;  (C) −92;  (D) +184
Exit ticket 60·4.2·12.1 = 3049 J
```

## Sim vs. textbook differences

| Quantity | Sim | Typical textbook | Source |
|---|---|---|---|
| c(water, liquid) | 4.2 J/g·°C | 4.184 | `physics.ts:2`, `substances.ts:31` |
| c(ice) / c(steam) | 2.1 / 1.9 | 2.09 / 2.01 | `substances.ts:30,32` |
| ΔH_vap water | 2230 J/g | 2257–2260 J/g | `substances.ts:34` |
| ΔH_fus water | 333 J/g | 333–334 J/g | `substances.ts:33` |
| C(s) → C(g) | 719 kJ/mol | 717 kJ/mol | `BondEnthalpyLab.tsx:1845,2421` |
| C—H / C—C | 414 / 347 | 413–414 / 347–348 | `:2363,2373` |
| ΔH°f C₂H₅Cl, HCl (exo set) | −113, −92 | −112, −92.3 | `FormationReactionLab.tsx:65-66` |
| ΔH°f C₂H₅Cl, HCl (endo set) | +15, +20 | (invented) | `:70-71` |
| Units | reaction ΔH as "kJ"; ΔH°f table has no unit | kJ/mol | throughout |

## Sim bugs and confusing text (not copied into the worksheet)

**Part 1 (HeatLab.tsx)**
- Bottom formula line renders "− 1652 J = 1652 J": a literal "− " (`:1147`) in front of a box that holds a positive `Math.round(qLeft)` (`:307`, `:1149`). Lines `:1146-1155`.
- Burner default changes with how you get there: starts at 0 (40 °C) (`:203`), reset to 0 on every metal change, including the Next → aluminum/lithium flow (`:206-208`, `:1466`); Guided Reset and switching to Guided set 2 (100 °C) (`:485`, `:504`); re-selecting Part 1 in the menu sets 2 (`:536`). No readout: the Low/Medium/High label is commented out (`:1235-1241`).
- Bubble says "Pinch the slider" (`:1016`) but the control is ◀ ▶ buttons (`:1083-1101`); the slider is commented out (`:1245-1255`).
- Bubble says "press play to graph" (`:1061-1063`) but the graph auto-starts after the drop (`:389-394`).
- Mass and water readouts are commented out (`:1288-1290`); values visible only in the formula line.

**Part 2 (HeatingCurveLab.tsx, heatingCurve/)**
- While still solid, the bubble says "Once [substance] melts, Cₚ changes to 4.2 J/g·°C" for every substance (`heatingCurve/steps.tsx:76`); ethanol is 2.44, acetone 2.18.
- Heat capacity labelled "Cw" for every substance and phase (`heatingCurve/sim/heatingModel.ts:107-139`, shown at `HeatingCurveLab.tsx:2211`).
- Mass (1 g) never displayed; ΔH_f / ΔH_v shown as "333 J" etc. with no "per gram" (`steps.tsx:95,121`).
- Step 0 text ("Both a change in temperature and a change of phase require enthalpy… Select a substance.") and the placeholder row "□ = 4.2 ( □ − □ )" are unreachable in Guided mode: the lab starts at step 1 (`HeatingCurveLab.tsx:1338`) and Back is disabled at step ≤ 1 (`:2365`). Not used.
- Heating curve is schematic: every leg is the same size (`:49-52`, `:73-82`).

**Part 3 (BondEnthalpyLab.tsx)**
- "Breakind" typo at `:1736`, `:1745`, `:1750`, `:1885`.
- "Forming the [empty] bond released about 347 kJ" (`:1904`); should say C—C. Also "Now C—H bond released about 414 kJ. Swipe to do it." (`:1914-1917`) is ungrammatical.
- If Cl₂ is broken first, the bubble says "Now rearrange them to make the products" even though H₂ is still whole (`:1733-1738`).
- The HCl enthalpy diagram draws one 431 arrow though two H—Cl bonds form (`assets/part_3_graphs/graphHCI(4).png`).
- Results appear before students can calculate: −184 in the bubble as soon as the second H—Cl forms (`:1776-1778`); −85 in the calc row as soon as step 4 begins, before any C—H is formed (`:1660-1667`). C—H = 414 appears only in step 4 (`:2363`).
- Reaction enthalpies given as "kJ" only; picker label "C2H6" without subscripts (`:73`, `:2817`).
- 6.9 Hess's Law menu item opens the intro screen only; NaOH tour commented out (`:1128-1138`).

**Part 4 (FormationReactionLab.tsx)**
- The sim labels the **exothermic** set "hypothetical" (`:1634`, `:1650`, `:2130`, `:2155`) and the endothermic set not; the endothermic values (+15, +20) are the invented ones and contradict Part 3's HCl −92 (`:70-73`).
- Calc row shows "0 = □ − □" at step 1 and "−205 = □ − □" / "+35 = □ − □" at step 2, i.e. the products' sum in the ΔH°rx position (`:1254-1273`).
- Reactants written "(0 − 85)" meaning 0 + (−85) (`:1295`, `:1303`).
- Endothermic run: bubble announces "Enthalpy of reaction has been reached! It's 120 kJ (absorbed)" during the climb, before the activation energy (`:1404-1409`).
- Eₐ has no numeric value; plateau gaps differ for |ΔH| = 120 (exo 32 units `:131-133`, endo 44.2 units `:165-167`), so the diagram is not to scale.
- Mixed notation ΔH°rx (`:2049`) and ΔH°rxn (`:1599`).

## AP topics not covered by the sim

- **6.9 Hess's Law**: listed in the Part 3 and Part 4 menus (`unit6/parts.ts:48,63`) but there is no Hess's law activity (`BondEnthalpyLab.tsx:1135-1137`). Lesson plan Day 4 reserves 20 minutes for the teacher's usual Hess's law lesson; Conclusion question 2 connects the same −92 kJ/mol from two paths to the state-function idea.
- Coffee-cup vs. bomb calorimetry and calorimeter heat capacity (part of 6.4) are not modelled: the sim's calorimeter is ideal (no heat to the cup or room). The AP FRQ part (d) touches heat loss.
- Thermochemical-equation stoichiometry (scaling ΔH with moles beyond the ÷2 for HCl) is only touched lightly.
