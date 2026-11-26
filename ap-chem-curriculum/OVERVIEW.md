# Overview: AP Chemistry sim worksheets and lesson plans

**In short:** every AP Chemistry unit (1–9) has a printable Student Notes packet, a matching Answer Key and a lesson plan, all built on the ChemSims.app simulation for that unit. Files are in `output/`.

| Unit | AP unit | Simulation | Sections | Student pages | Class periods |
|---|---|---|---|---|---|
| 1 | Atomic Structure and Properties | Atomic Structure Sim | 8 | 19 | 6 |
| 2 | Compound Structure and Properties | AP Unit 2 sim | 8 | 19 | 6 |
| 3 | Properties of Substances and Mixtures | Properties of Substances & Mixtures Sim | 13 | 16 | 6 |
| 4 | Chemical Reactions | Chemical Reactions + Redox Reactions Lab | 6 | 15 | 6 |
| 5 | Kinetics | Reaction Rates Lab | 5 | 17 | 6 |
| 6 | Thermochemistry | Thermodynamics Lab, Parts 1–4 | 4 | 14 | 5 |
| 7 | Equilibrium | Equilibrium Lab | 10 | 22 | 6 |
| 8 | Acids and Bases | Acids & Bases | 7 | 17 | 5 |
| 9 | Applications of Thermodynamics | Thermodynamics Lab, Parts 91–94 | 7 | 21 | 6 |

Student page counts include the cover, the Conclusion page and the Self-Grading Record. Each Answer Key has the same pages plus one Teacher Notes page.

## How to use a unit

1. Print the Student Notes packet (one per student) and keep the Answer Key for yourself. On the site, students can't download answer keys.
2. Read the unit's lesson plan. Day 1 is your projected demo with a click-by-click script.
3. Students then work through the sim over the next periods and fill in the packet by hand, like a lab record.
4. On the last day, pick self-grading, peer grading or teacher grading (the plan lists pros, cons and risks of each).

## Before you teach: things to check

- **Nobody ran the sims in a browser while writing these.** Every answer comes from reading the deployed sim code and recomputing its numbers in Python. Run each sim once with the Answer Key beside you before class. If a number on screen differs from the key, trust the screen and tell us.
- **Unit 9's labs are only reachable by direct link** (`chemsims.app/sims/thermodynamics?part=91` to `94`). They aren't in the site's sim catalog (`lib/sims.ts`) or in the sim's own menu, so teachers can't assign them from the dashboard yet.
- **Units 1, 2 and 5 already had worksheets by Tess** (guided notes only). These new packets keep her blank wording where it matches the sim and add set-up, predictions, data tables, calculations and analysis. Tess's Unit 2 key disagrees with the sim in two places (HCN polarity; square-pyramidal angle); the new key follows the sim.
- **Sim bugs** found along the way are in `SIM-BUGS.md`, for the dev team.

## AP topics the sims don't cover

Each lesson plan's prep list tells the teacher to teach these with their usual lesson.

### Unit 1: Atomic Structure and Properties

- Orbital (box) diagrams, Hund's rule, Pauli exclusion; electron spin.
- Transition-metal configurations beyond Z = 18 in 1.5 (builder stops at Ar; Cr/Cu exceptions exist in code but unreachable) and transition-metal ions (4s removed first).
- Real PES energies (MJ/mol) and reading values from a to-scale PES.
- Mass spectra of molecules/diatomics; calculating isotope abundance from an average.
- Experimental composition methods (combustion analysis, gravimetric purity labs).
- Successive ionization energies; quantitative Coulomb's law.


### Unit 2: Compound Structure and Properties

All seven Unit 2 topics (2.1–2.7) have a screen. Gaps inside topics:
- 2.5/2.6: Lewis structures with more than one central atom (C₂H₄, CH₃OH, organic molecules); the builder is one central atom only (1843–1867).
- 2.7: σ/π and hybridization in multi-centre molecules; delocalized π systems beyond the resonance message.
- 2.1: bond dipole/dipole-moment magnitudes and percent ionic character are qualitative only.
- 2.2: F₂ anomaly is mentioned but not modelled; no quantitative Coulomb's-law energy (only ratios).
- 2.4: ductility (drawing into wire) is stated, not demonstrated; only the layer-slide test.


### Unit 3: Properties of Substances and Mixtures

All 13 CED topics (3.1–3.13) have a sim topic. Gaps inside topics:
- 3.4: gas density and molar mass from PV = nRT (d = PM/RT); stoichiometry with gases.
- 3.3/3.5: vapor pressure vs temperature curves, phase diagrams, Graham's law/effusion.
- 3.9: quantitative Rf calculation (the sim shows "relative movement" and says it is not a measured Rf).
- 3.11: real IR/UV-vis spectra; 3.11 calculates no energies.
- 3.12: energy per mole of photons.
- 3.13: %T / transmittance readout, calibration with real data scatter, sources of deviation.
The lesson plan's `prep` tells the teacher to use their usual lesson for these.


### Unit 4: Chemical Reactions

- **4.4 Physical and Chemical Changes:** not covered at all.
- **4.8 Introduction to Acid–Base Reactions:** only classification (HCl + NaOH in Part 1) and neutralization stoichiometry (HNO₃ + NaOH in Limiting Reagent). The sims have no Brønsted–Lowry proton-transfer treatment, conjugate pairs or amphoteric water.
- **4.6 Introduction to Titration:** only redox titration. There is no acid–base titration, indicator or pH curve.
- **4.2 Net Ionic Equations:** shown only for redox (Part 2). The Chemical Reactions screens show molecular equations; students write the precipitation net ionic equation themselves.
- **4.1 Introduction for Reactions:** evidence of reaction (precipitate, color change, gas) appears, but it is not discussed as a topic.


### Unit 5: Kinetics

- **5.2 (part):** method of initial rates, multi-reactant rate laws, overall order, units of k by order. Use initial-rate data tables.
- **5.4 Elementary Reactions** (molecularity; rate law from coefficients only for elementary steps).
- **5.7 Introduction to Reaction Mechanisms** (intermediates, summing steps).
- **5.8 Reaction Mechanism and Rate Law** (rate-determining step).
- **5.9 Steady-State Approximation** (fast reversible first step, substituting for intermediates).
- **5.10 Multistep Reaction Energy Profile** (two humps, intermediate valley, which Eₐ is rate-limiting).
- **5.11 Catalysis (part):** catalysts as a new reaction pathway that is consumed then regenerated; acid-base, surface and enzyme catalysis. The sim only shows "a catalyst lowers Eₐ".
- **5.5 (part):** orientation is only described in text; no orientation demo.
Teacher should use their usual lessons for these (about 2–3 periods), e.g. AP Classroom Topic Questions 5.4–5.11, a worked NO₂ + CO mechanism, and a two-hump energy diagram exercise. The lesson plan's prep item and AP practice question 2(e) point to this.


### Unit 6: Thermochemistry

- **6.9 Hess's Law**: listed in the Part 3 and Part 4 menus (`unit6/parts.ts:48,63`) but there is no Hess's law activity (`BondEnthalpyLab.tsx:1135-1137`). Lesson plan Day 4 reserves 20 minutes for the teacher's usual Hess's law lesson; Conclusion question 2 connects the same −92 kJ/mol from two paths to the state-function idea.
- Coffee-cup vs. bomb calorimetry and calorimeter heat capacity (part of 6.4) are not modelled: the sim's calorimeter is ideal (no heat to the cup or room). The AP FRQ part (d) touches heat loss.
- Thermochemical-equation stoichiometry (scaling ΔH with moles beyond the ÷2 for HCl) is only touched lightly.


### Unit 7: Equilibrium

- **7.6 Properties of the Equilibrium Constant**: no reversing, scaling or adding reactions. Covered only by a short calc on p. 1 that uses the sim's K = 10, labelled as not shown by the sim.
- **7.14 Free Energy of Dissolution**: nothing on ΔG°, ΔH°/ΔS° of dissolving.
- **7.5 Magnitude of K** (partial): K values are only 10, 1.0 and 0.1; no very large/very small K, no "x is small" approximation.
- **7.13 pH and Solubility** (partial): qualitative only; no pH value, no Ka/Kb link, no hydroxide salts.
- **7.11 Solubility** (partial): only 1:1 salts; no Ksp with exponents, no molar mass → g/L.
- Also missing: Kc ↔ Kp conversion, catalysts and inert-gas addition, Q from moles and volume.


### Unit 8: Acids and Bases

- **8.6 Molecular Structure of Acids and Bases** (bond polarity/strength, oxyacids, why HF is weak): not in the sim at all.
- **8.1** temperature dependence of Kw: the sim states Kw only at 25 °C (BUF:46).
- **8.5** indicator choice by pKa(In) and polyprotic titrations; **8.3** polyprotic acids.
- **8.10 Buffer capacity** is only qualitative (the limit is scripted, see above); comparing buffers of different total concentration is not possible.
- **8.4** reactions of a weak acid with a weak base, and the pH of a salt solution on its own (only seen at the titration EP).


### Unit 9: Applications of Thermodynamics

- **9.4 Thermodynamic and Kinetic Control:** only one sentence (GL:702-704) that ΔG° doesn't give the rate; no activation-energy/kinetic-control example. The handoff doc lists this as open item 2.
- **9.6 Coupled Reactions:** not present anywhere.
- **9.5 Free Energy and Equilibrium:** partly. ΔG° = −RT ln K and Q vs K appear in Part 94; Part 93 never shows K (the worksheet adds a calculation). No "ΔG° ≈ 0 → K ≈ 1" quantitative table.
- **9.2:** predicting the sign of ΔS for dissolving, or for reactions with phase changes beyond the three examples, is not in the sim.
- **9.3:** no real reaction combining ΔH° (kJ) with ΔS° (J/K); the worksheet's conclusion question supplies one from Part 92 data.
- The task brief listed "9.1–9.11"; the AP CED Unit 9 has ten topics (9.1–9.10). All ten are accounted for above.
