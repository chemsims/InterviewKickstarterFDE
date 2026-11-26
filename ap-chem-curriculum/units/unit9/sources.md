# Unit 9 sources: Applications of Thermodynamics

Sim: Thermodynamics Lab, repo `thermodynamics`, branch `unit9-entropy-9.1` at **a905934** (the deployed commit).
Paths below are relative to `thermodynamics/src/`. Abbreviations:
`ES` = `heatingCurve/entropySteps.tsx`, `ESub` = `heatingCurve/sim/entropySubstances.ts`,
`EL` = `components/EntropyLab.tsx`, `AEL` = `components/AbsoluteEntropyLab.tsx`,
`GL` = `components/GibbsLab.tsx`, `EC` = `components/ElectrochemLab.tsx`.

## How the labs are reached (checked)

- `App.tsx:110-124`: part 91 → EntropyLab, 92 → AbsoluteEntropyLab, 93 → GibbsLab, 94 → ElectrochemLab.
  `App.tsx:38-43` sets the tab title to "Unit 9: Applications of Thermodynamics" for parts 91–94.
- `unit6/labRoute.ts:4-10,19-27`: `?part=91..94` are accepted; `&mode=freeExplore` opens Free Explore, anything else is Guided.
- The deployed bundle `chemtutor-static-tutor/public/sims/thermodynamics/assets/index-CLx7aX4_.js` contains the text of all four labs
  (checked strings: "Pinch to change ice size", "Choose a Compound", "Favorable at high T", "Move one more step",
  "Equilibrium has been disturbed", "ec-time-slider", "Ice mass", "-379.7", "Arrow keys adjust", "would stop partway").
- **Not exposed in any menu:** the sim home page lists only parts 1–4 (`unit6/homeSimCards.ts:8-37`), and the menu drawer maps
  only `UNIT6_PARTS` (`components/Unit6MenuDrawer.tsx:90`, `unit6/parts.ts`). The site catalog
  `chemtutor-static-tutor/lib/sims.ts:427-443` lists thermodynamics parts 1–4 only and `AP_UNIT_SIMS["ap-unit-9"]` is `[]`
  (`lib/sims.ts:838`). The comment at `lib/sims.ts:422-423` says ElectrochemLab is "unbuilt", which is out of date.
- URL used in the worksheet: `chemsims.app/sims/thermodynamics?part=9N` (same base + `?part=N` form as `lib/sims.ts:431-441`).

## Page 1: Entropy and Melting (part 91)

| Item | Answer | Source |
|---|---|---|
| First Law "destroyed" | slide 1 | ES:30-35 |
| "increasing", "100%" efficiency | slide 3 | ES:45-52 |
| Entropy = disorder; "ways" to arrange | slides 4–5 | ES:54-67 |
| Smaller box = "decrease" | slides 6–7 | ES:68-81 |
| Symbol S, S° per "mole", units J/°C | slide 8 | ES:83-89 |
| Choose a Substance gate | slide 9 | ES:91-95; EL:2210 |
| ΔS = q/T, T in kelvin, reversible | slide 12 | ES:113-120 |
| Melting began: ΔS "positive"; molecules "disperse" | ES:186-209 (cases 3, 4) |
| Ice mass default 7 g, range 5–20 g | EL:1659, 2454, 2474 |
| Water ΔH_fus 333 J/g, T_melt 0 °C | ESub:18, 23; narration ES:157 |
| 273 offset | EL:1356 (`C_TO_K = 273`) |
| Fusion row "ΔSf = q/T = m(ΔHf)/T", shows 2331 / 273 = 7(333)/273 | EL:1466-1474, 2545-2558 |
| q = 2331 J, T = 273 K, ΔS = 9 | worked: 7 × 333 = 2331; 2331/273 = 8.538 → round 9 (EL:1468 `round0`) |
| "Entropy increased by 9 J/°C for the melting process" | ES:276-286 (case 10, dSf) |
| Explore 15 g → 18 | 15 × 333/273 = 18.30 → 18 |

## Page 2: Heating, Boiling and Total Entropy (part 91)

| Item | Answer | Source |
|---|---|---|
| "average" of initial and final temperature | ES:172-183 (case 2) |
| "Sensible Heat", Cw = specific heat | ES:289-300 (case 11) |
| Cw "at gaseous state" | ES:237-248 (case 7) |
| ΔH_vap water 2230 J/g | ESub:24; narration ES:211-222 (case 5) |
| Vaporization began, entropy "increase" | ES:314-325 (case 13) |
| Entropy increases with temperature, solid→liquid→gas, "decrease" in reverse | ES:250-274 (cases 8, 9) |
| Equations shown | EL:2578-2627 |
| Liquid leg ΔS = q/T_avg | EL:1495-1502 (`sensLive`) |
| Vapor-leg value shows one decimal under 1 | EL:1497 |
| Total = ΔSf + ΔSv + Σ sensible, rounded | EL:1513-1524 |
| Substance data | water ESub:12-25, ethanol 26-39, acetone 40-53 |
| Next substance after a finished run | EL:2763-2769 |

Values (7 g; J/K, sim prints J/°C), all from `check.py` (below):

| Substance | ΔSf = m·ΔHf/Tm | ΔS liquid = m·c_l·(Tb−Tm)/T_avg | ΔSv = m·ΔHv/Tb | ΔS vapor | Total |
|---|---|---|---|---|---|
| Water | 2331/273 = 8.54 → 9 | 2940/323 = 9.10 → 9 | 15610/373 = 41.85 → 42 | 266/383 = 0.69 → 0.7 | 9+42+9.10+0.69 = 60.8 → 61 |
| Ethanol | 728/159 = 4.58 → 5 | 3279.4/255 = 12.86 → 13 | 5887/351 = 16.77 → 17 | 266/361 = 0.74 → 0.7 | 35.6 → 36 |
| Acetone | 686/178 = 3.85 → 4 | 2304.3/253.5 = 9.09 → 9 | 3626/329 = 11.02 → 11 | 231/339 = 0.68 → 0.7 | 24.8 → 25 |

Narration totals (ES:131-145, rounded legs) agree: 61, 36, 25.

## Page 3: Absolute Entropy and Entropy of Reaction (part 92)

| Item | Answer | Source |
|---|---|---|
| "Entropy" / "Gibbs Free Energy" of formation for every compound | AEL:707-712 (step 2), 714-724 |
| ΔG°f of pure element = 0 | AEL:1184 |
| Multiplied by number of "moles" → 3(130.6) | AEL:1175-1179, 860-869 |
| Difference products − reactants = of "reaction" | AEL:709-711 |
| NH₃: all "gaseous", more "molecules" on reactant side | AEL:728-735 |
| Changes with number of "molecules", "temperature", state | AEL:744-750 |
| Equations ΔS°rx, ΔG°rx | AEL:1042, 1066 |
| S° / ΔG°f data | NH₃ AEL:116-117, 128-129; HCl 163-164, 171-172; NaOH 206-208, 215-216 |
| ΔS°rx, ΔG°rx formula in code | AEL:241-246 |

Worked: NH₃ 2(192.5) − [191.5 + 3(130.6)] = 385.0 − 583.3 = −198.3; ΔG = 2(−16.7) = −33.4.
HCl 2(186.9) − (130.6 + 223.1) = 373.8 − 353.7 = +20.1; ΔG = 2(−95.3) = −190.6.
NaOH 2(64.5) − (102.6 + 205.2 + 130.6) = 129.0 − 438.4 = −309.4; ΔG = 2(−379.7) = −759.4.

## Page 4: Gibbs Free Energy and Favorability (part 93)

| Item | Answer | Source |
|---|---|---|
| Round values −2500/+25, +5000/+16, −5000/−16, +2500/−25; verdicts | GL:67-70 |
| Sign table | GL:74-79 |
| T start 298 K, slider 278–340 K, step 1 | GL:81-83, 1144-1153 |
| ΔH° slider 500–10000 (rounds 1, 4) / 3000–7000 (2, 3), step 100; ΔS° bounds | GL:402-405, 940, 150-167 |
| Slider seeded with round value; release locks | GL:338-341, 412-432 |
| ΔG° = ΔH° − TΔS° ("TΔS°") | GL:689-695, 1250 |
| "thermodynamically favored", "spontaneous", "fast"/"slow" | GL:698-705 |
| "exergonic" / "endergonic" | GL:831, 867 |
| ΔH° and ΔS° stayed "fixed", only "T" | GL:838-845 |
| "equilibrium" partway sentence | GL:876-882 |
| ΔG° box empty in round 1 until complete | GL:925-938 |
| Start / Now strip, "ΔG° = 0 at 312.5 K" | GL:1278-1294 |
| Temperature carries round 2 → 3 | GL:442-454 |

Worked: −2500 − 298(25) = −9950; 5000 − 298(16) = +232; 5000 − 320(16) = −120; crossover 5000/16 = 312.5 K;
−5000 − 320(−16) = +120; −5000 − 298(−16) = −232; 2500 − 298(−25) = +9950.
K (worksheet calc, not shown by sim): e^(9950/(8.314·298)) = 55.5; e^(232/(8.314·298)) = 1.098; round 2 at 320 K: 1.046.
Round 3 slider bounds at 320 K: min ⌊5000/320⌋+1 = 16, max ⌈5000/278⌉−1 = 17 → default 16 accepted. Round 2 at 298 K: 15–16.

## Pages 5–7: Electrochemistry (part 94, Zn/Cu)

| Item | Answer | Source |
|---|---|---|
| Reaction option text, E° Zn −0.76, Cu +0.34, n = 2, M(Zn) 65.38 | EC:74-89 |
| R = 8.314, F = 96485, T = 298 | EC:55-57 |
| Step gates (pick 0, Zn²⁺ 8, Cu²⁺ 9, submerge 13, voltmeter 19, thermo 27, run 31, disturb 32, reverse 37, battery 41, amps 42, time 43) | EC:171-184 |
| "battery" | EC:1481-1485 (step 1) |
| Reduction gains / oxidation loses | EC:1507-1513 (step 4) |
| "reversible", "Equilibrium" | EC:1525-1541 (steps 6–7) |
| 1.00 M each, Q = 1.00 | EC:1551-1566 (steps 9–10) |
| Anode Zn oxidized, cathode Cu reduced | EC:1577-1602 (steps 12–13) |
| Salt bridge keeps solutions "neutral" | EC:1604-1611 (step 14) |
| Half-reactions, cell notation | EC:1623-1652 (steps 16–18) |
| Electrons from "negative" side (anode) | EC:1653-1660 (step 19) |
| "Cell Potential" Ecell / E°cell | EC:1662-1673 (step 20) |
| 96485 C/mol | EC:1693-1701 (step 23) |
| ΔG = 0 equilibrium; <0 forward; >0 reverse | EC:1720-1728 (step 26) |
| T = 298 K; K huge → more "products" | EC:1738-1746 (step 28) |
| Ecell = E°cell at "standard" conditions | EC:1747-1754 (step 29) |
| Slope = ΔG; at bottom "0" | EC:1755-1762 (step 30) |
| E°cell, ΔG° strip text ("−212 kJ = −(2)(96485)(1.10)") | EC:2083-2105, 148-151 |
| K display (fmtExp → 1.6×10³⁷) | EC:127-137, 244; step 28 narration |
| Voltmeter 0.00 at equilibrium | EC:716-722 |
| Disturbance: lnQ += ln 2.5 | EC:395, 1363 |
| ΔG positive, Ecell negative | EC:1780-1795 (steps 33–34) |
| Reverse view: roles swap, E° = −1.10 | EC:1805-1828 (steps 36–37), 2045-2056, 302 |
| Galvanic / Electrolytic / non-spontaneous | EC:1837-1860 (steps 38–40) |
| q = I × t "charge", moles "e⁻" | EC:1879-1887 (step 44) |
| Electrode "coating" | EC:1905-1912 (step 47) |
| I slider 1–10 A step 0.5; t slider 100–3600 s step 100 | EC:923-925, 1320-1322 |
| Faraday chain and rounding | EC:627-646, 2165-2245 |
| Mass–time graph shape (Zn up, Cu down, schematic) | EC:2489-2561 |
| G-vs-Q graph schematic axis | EC:2286-2300 |

Worked: E° = 0.34 − (−0.76) = 1.10 V. ΔG° = −2(96485)(1.10) = −212 267 J → −212 kJ. ln K = 212267/(8.314·298) = 85.675; K = 1.62×10³⁷ (displayed 1.6×10³⁷).
Disturbed: E = −(8.314·298/(2·96485))·ln 2.5 = −0.0118 V → −0.01; ΔG = RT ln 2.5 = +2.27 kJ → 2. Reverse view flips signs: +0.01 V, −2 kJ.
Faraday 5.0 A × 1800 s: q = 9000 C; 9000/96485 = 0.09328 mol e⁻ (shown 0.093); /2 = 0.04664 mol Zn (shown 0.047); × 65.38 = 3.049 → 3.05 g.
Cu lost (worksheet question; Cu molar mass 63.55 supplied by the worksheet, not the sim): 0.04664 × 63.55 = 2.96 g.
Hypothetical Nernst (labeled not in sim): Q = 200, E = 1.10 − 0.012841·ln 200 = 1.032 V.
Explore Sn/Cu: E° = 0.48 V, ΔG° = −92.6 → −93 kJ, K = 1.7×10¹⁶; Sn mass at 9000 C = 0.04664 × 118.71 = 5.54 g (EC:99-104).

## Conclusion / AP practice

- NH₃: ΔH° = ΔG° + TΔS° = −33.4 + 298(−0.1983) = −92.49 kJ; T = 92.49/0.1983 = 466.4 K; K(298) = e^(33400/2477.6) = 7.2×10⁵.
- HCl (extension): ΔH° = −190.6 + 298(0.0201) = −184.6 kJ (Unit 6 bond-enthalpy result: −184 kJ).
- Exact liquid-water ΔS (extension): 7 × 4.2 × ln(373/273) = 9.18 J/K vs the sim's 9.10.
- Time for 1.00 g Zn at 5.0 A: 1.00/65.38 × 2 × 96485 / 5.0 = 590 s.

## Values checked by hand

Script `scratchpad/u9/check.py` (python3), output summarized:

```
water 7 g: Sf 8.538→9 | Sv 41.85→42 | Sl 9.102 | Sg 0.695 | total 61
ethanol 7 g: 4.579→5 | 16.772→17 | 12.86 | 0.737 | 36
acetone 7 g: 3.854→4 | 11.021→11 | 9.09 | 0.681 | 25
water 15 g: 18 / 90 / 19.5 / 1.49 → 129 (deck says 130)
NH3 dS −198.3 dG −33.4 | HCl +20.1 −190.6 | NaOH −309.4 −759.4
Gibbs: −9950, +232, −120 (320 K), +120 (320 K), −232, +9950; crossover 312.5 K
K(−9950, 298) = 55.5; K(−232, 298) = 1.098; K(−120, 320) = 1.046
ZnCu E 1.10 dG −212.267 kJ lnK 85.675 K 1.62e37 ; SnCu 0.48 −92.626 1.72e16 ; AlAg 2.46 −712.059 6.56e124
disturbed E −0.01176 V, dG +2.27 kJ
Faraday 5.0 A 1800 s: 9000 C, 0.0933, 0.0466, 3.05 g (65.38 × 0.047 = 3.073)
Nernst Q=200: 1.032 V
```

## Sim vs. textbook differences

- Entropy units J/°C (ES:85-88; EL:2611 comments) vs J/K. Same magnitude.
- 273 instead of 273.15 (EL:1356; ES:133).
- Heating-leg ΔS uses q/T_avg (EL:1388-1392) instead of m·c·ln(T₂/T₁): 9.10 vs 9.18 J/K for water.
- Water c(liquid) 4.2 (4.184), c(vapor) 1.9 (≈2.0), ΔH_vap 2230 J/g (2260) (ESub:21-24).
- Part 91 default mass 7 g; the deck's 18/90/130 J/°C are for 15 g, and 15 g actually gives 129 in the sim's own rounding.
- Part 92 table heads S° as "ΔS°f" (AEL:999); ΔG°f NH₃ −16.7 (tables −16.4/−16.45), NaOH −379.7 (−379.5). S° values match tables within 0.3.
- Part 93 uses J/mol and J/(mol·K) for a hypothetical reaction (GL:1322-1324); AP problems usually mix kJ and J/K.
- Part 93 shows all-or-nothing conversion although K ≈ 1.05–1.10 in rounds 2–3 (docs/UNIT-9-3-4-QA-HANDOFF.md open item 1).
- Part 94 rounds ΔG° to whole kJ and K to 2 significant figures; the "ΔG = ΔG° + RT ln Q" row prints kJ values next to R = 8.314 J (EC:2124-2128).

## Sim bugs and confusing text (not copied into the worksheet)

1. Part 91 narration calls the heat of vaporization "Heat of Fusion" (ES:216, case 5).
2. Part 91 says ΔSv "for the melting process" (ES:229-230, case 6).
3. Part 91 "more noticeable in the graph at the top" (ES:192), but the graph is temperature vs energy (EL:477, 2643).
4. Part 91 end-of-run "Next chapter" button and Next on the last substance open Unit 6 Part 3 (bond enthalpies) (EL:2774, 2959), not Part 92.
5. Part 91 "Ice mass" label is used for ethanol and acetone too (EL:2450).
6. Part 92 narration gives ΔG°f in "J" (AEL:1184, 1209-1211) and the beaker callout labels S° values "kJ" (AEL:852-857); staircase says "J/mol·K" (AEL:1335).
7. Part 92 step 4 explanation for a negative ΔS says all components are gaseous (AEL:728-735) — wrong for NaOH (Na(s), NaOH(s)).
8. Part 92 step 5 "All those scenarios make the disorder of the system to rise" (AEL:744-750) — the NH₃ and NaOH cases decreased.
9. Part 92 last slide: ΔG negative "because the reaction is spontaneous ... without the help of any outside source of energy" (AEL:752-757) — causality reversed; contradicts Part 93's kinetics caveat.
10. Part 94 Al/Ag: half-reaction text uses n as each ion's charge ("Ag+3", EC:1519-1531), Q labels both ions as n+ (EC:2036-2045) and Q has no exponent; the concentration model (EC:247-253) ignores the 3:1 stoichiometry.
11. Part 94 step 21 reads E° for Zn as "0.76" (Math.abs, EC:1670) — drops the minus sign.
12. Part 94 step 25 mixes ΔG and ΔG° (EC:1702-1709); step 20 "measures electricity" (EC:1656).
13. Part 94 step 45-46: "a mol of Cu(s) is being consumed" is fine for Zn/Cu but wrong for Al/Ag; "This value also represents the grams of Cu(s) consumed" (EC:1902) — equal moles, not grams.
14. Part 94 step 47 "coating with Zn+2 ions" (EC:1910) — it is coated with zinc metal.
15. Part 94 Faraday chain prints 3.05 = 65.38 x 0.047 (mass computed from unrounded moles, EC:627-646).
16. Part 94 voltmeter keeps showing −0.01 V in the reversed-perspective screens while the strip shows +0.01 V (EC:718-722 vs the strip call at EC:1251-1263).
17. Typos students see: "in order words" (EC:1483), "The are many ways" (EC:1784), "Associated to" (EC:1474), "Same as Enthalpy, the Entropy is too usually expressed" (ES:98).
18. `lib/sims.ts:422-423` (site repo) says the ElectrochemLab is unbuilt; it is in the deployed bundle.

## AP topics not covered by the sim

- **9.4 Thermodynamic and Kinetic Control:** only one sentence (GL:702-704) that ΔG° doesn't give the rate; no activation-energy/kinetic-control example. The handoff doc lists this as open item 2.
- **9.6 Coupled Reactions:** not present anywhere.
- **9.5 Free Energy and Equilibrium:** partly. ΔG° = −RT ln K and Q vs K appear in Part 94; Part 93 never shows K (the worksheet adds a calculation). No "ΔG° ≈ 0 → K ≈ 1" quantitative table.
- **9.2:** predicting the sign of ΔS for dissolving, or for reactions with phase changes beyond the three examples, is not in the sim.
- **9.3:** no real reaction combining ΔH° (kJ) with ΔS° (J/K); the worksheet's conclusion question supplies one from Part 92 data.
- The task brief listed "9.1–9.11"; the AP CED Unit 9 has ten topics (9.1–9.10). All ten are accounted for above.
