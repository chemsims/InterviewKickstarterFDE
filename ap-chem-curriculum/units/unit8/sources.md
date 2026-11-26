# Unit 8 Acids and Bases: sources for every answer

Sim: **Acids & Bases** (chemsims.app/sims/acids-bases), deployed commit `bb81d6b` (branch `remove-acids-quizzes-clean`).
All paths are relative to `/home/user/acidsbaseschemsimsemetei/src/`. Abbreviations:

- `SUB` = `helper/acidsBases/substances.ts`
- `ENG` = `helper/acidsBases/simulationEngine.ts`
- `INTRO` = `components/AcidsBases/guide/introGuideSteps.ts`
- `STORE` = `components/AcidsBases/guide/useGuideStore.ts`
- `GIS` = `pages/AcidsBases/intro/GuidedIntroScreen.tsx`
- `EQD` = `components/AcidsBases/ui/EquationDisplay.tsx`
- `BUF` = `components/AcidsBases/guide/bufferGuideSteps.ts`
- `BDS` = `pages/AcidsBases/buffers/hooks/useBufferDerivedState.ts`
- `BSM` = `helper/acidsBases/BufferSaltModel.ts`
- `BEN` = `pages/AcidsBases/buffers/BufferEquationsNew.tsx`
- `BBOT` = `pages/AcidsBases/buffers/hooks/useBufferBottles.ts`
- `TM` = `pages/AcidsBases/titration/hooks/useTitrationModel.ts`
- `TS` = `pages/AcidsBases/titration/TitrationScreen.tsx`
- `TST` = `components/AcidsBases/guide/titrationStatements.ts`
- `TMP` = `pages/AcidsBases/titration/components/TitrationMathPanel.tsx`
- `TGS` = `pages/AcidsBases/titration/hooks/useTitrationGuideState.ts`

## Shared constants

| Value | Where |
|---|---|
| Kw = 1×10⁻¹⁴ | SUB:10 |
| HCl, HI, HBr strong acids; KOH, LiOH, NaOH strong bases | SUB:140–175 |
| HA Ka = 7.3×10⁻⁵ (pKa 4.14) | SUB:178–183 |
| HF Ka = 4.5×10⁻⁴; HCN Ka = 9×10⁻⁵ | SUB:185–197 |
| B⁻ Kb = 4×10⁻⁵ (pKb 4.40, conj. acid HB); F⁻ Kb = 1.3×10⁻⁵; HS⁻ Kb = 1×10⁻³ | SUB:200–219 |
| Salts: MA (for HA), HBX (for B⁻) | SUB:182, 204 |
| Weak acid pH: exact quadratic x = (−Ka + √(Ka² + 4KaM))/2 | ENG:47–54 |
| Weak base pH: same quadratic with Kb; pH = 14 − pOH | ENG:61–69 |
| Strong acid pH = −log M; strong base pH = 14 + log M | ENG:20–26 |
| Titration pH (strong excess / Henderson-Hasselbalch / EP hydrolysis / excess titrant) | ENG:200–296 |

## Page 1 Strong Acids and Bases (Introduction screen)

| Blank / answer | Value | Source |
|---|---|---|
| Arrhenius acid → hydrogen ions (H⁺); base → hydroxide (OH⁻) | quoted | INTRO:30 |
| Brønsted-Lowry: donate / accept | quoted | INTRO:34 |
| Lewis base donates an electron pair | quoted | INTRO:38 |
| strong acids dissociate entirely, go to completion | quoted | INTRO:46 |
| both at 10⁻⁷, pH 7 | quoted | INTRO:51 |
| higher [H⁺] → lower pH, more acidic | quoted | INTRO:71 |
| pH = −log[H⁺], pOH = −log[OH⁻], pH + pOH = 14 | quoted | INTRO:55, 59; EQD:127–131 |
| Each shake adds 1/14; max 14 shakes; Next after 7 | | STORE:276, 303, 332 |
| Beaker molarity = 0.1 × fraction added (water level not used) | 7 shakes 0.050 M; 14 shakes 0.100 M | GIS:271–279 |
| HCl 7 shakes: pH 1.3, pOH 12.7, [H⁺] 5.0×10⁻², [OH⁻] 2.0×10⁻¹³ | worked: −log 0.05 = 1.301 | ENG:22, display EQD:133–173 (pH 1 dp, conc. 2 s.f.) |
| HCl 14 shakes: pH 1.0, pOH 13.0, [H⁺] 1.0×10⁻¹, [OH⁻] 1.0×10⁻¹³ | −log 0.1 | ENG:22 |
| KOH 14 shakes: pH 13.0, pOH 1.0 | 14 + log 0.1 | ENG:26 |
| pH meter shows 1 decimal | | `components/AcidsBases/interactive/PHMeter.tsx:220` |
| pH vs. moles graph shape (shape only; no tick labels) | | `components/AcidsBases/charts/ConcentrationBarChart.tsx:104–122, 214–283` |
| Explore: every strong acid pH 1.0 / base 13.0 | same formula for all | ENG:20–26 |

## Page 2 Weak Acids and Weak Bases (Introduction)

| Blank / answer | Value | Source |
|---|---|---|
| dissociate partially, go to equilibrium | quoted | INTRO:80 |
| H₃O⁺ and H⁺ interchangeably; H₂O written as reactant | quoted | INTRO:85 |
| double arrow | quoted | INTRO:139 |
| B⁻ acts as a proton acceptor | quoted | INTRO:152 |
| HA + H₂O ⇌ H₃O⁺ + A⁻; B⁻ + H₂O ⇌ HB + OH⁻ | as drawn | `components/AcidsBases/interactive/ReactionEquation.tsx:78–102` |
| HA 0.10 M: pH 2.6, [H⁺] 2.7×10⁻³, [OH⁻] 3.8×10⁻¹² | x = 2.666×10⁻³, pH 2.574 | worked from SUB:181 with ENG:47–54 |
| % ionization 2.7% | 2.666×10⁻³/0.10 | worked |
| B⁻ 0.10 M: pH 11.3, [OH⁻] 2.0×10⁻³, [H⁺] 5.1×10⁻¹² | x = 1.980×10⁻³, pOH 2.703, pH 11.297 | worked from SUB:203 with ENG:61–69 |
| Explore: HF pH 2.2, HCN 2.5 | 2.188, 2.529 | worked from SUB:188, 195 |

## Page 3 Weak Acid Equilibrium and Ka (Buffers, part 1)

| Blank / answer | Value | Source |
|---|---|---|
| Ka for an acid, Kb for a base | quoted | BUF:38 |
| higher Ka → more H⁺, more acidic | quoted | BUF:42 |
| water is a pure liquid (not in Ka) | quoted | BUF:125 |
| conjugate base; conjugate acid-base pair | quoted | BUF:129 |
| Kw = 10⁻¹⁴ at 25 °C; Kw = Ka × Kb | quoted | BUF:46, 54 |
| Ka = [H⁺][A⁻]/[HA], pKa = −log(Ka) | shown | BEN:225–235, 263–270; BUF:59 |
| Water at default 0.5 → 11 rows → 19 × 11 = 209 slots | rowsFloat = 11.00002 | `helper/acidsBases/beakerMath.ts:1–21`; BDS:58–66; `helper/acidsBases/particles/types.ts:40–45`; BufferScreen.tsx:102, 240–241 |
| 5 particles per shake, capped at 43 | | BBOT:139–140; BufferScreen.tsx:244 |
| Next needs ≥ 20 particles | | `pages/AcidsBases/buffers/hooks/useGuideNavigation.ts:141` |
| [HA] start = 43/209 = 0.206 M (shown to 3 decimals) | 0.20574 | BDS:66, 78; BEN:47–59 |
| [H⁺] = [A⁻] = 3.8×10⁻³; [HA] eq 0.202; pH 2.42 | x = 3.839×10⁻³, 0.2019, pH 2.4158 | BDS:78–86, `useScientificConcentrations.ts:59–75`; ENG:47–54 |
| pKa 4.14 (summary shows 4.137) | −log 7.3×10⁻⁵ = 4.1367 | SUB:93; BEN:220, 267 |
| Kb(A⁻) = 1.4×10⁻¹⁰ | 1×10⁻¹⁴/7.3×10⁻⁵ = 1.37×10⁻¹⁰ | SUB:85; BEN:305–311 shows Kw = Ka × Kb |
| “plenty of HA remaining” | quoted | BUF:159 |
| buffer range shaded ±1 on fraction graph; not yet a buffer | | `pages/AcidsBases/buffers/BufferCharts.tsx:564–567`; BUF:168 |
| Explore: HF equilibrium pH 2.03 | x = 9.40×10⁻³ at 0.2057 M | worked |

## Page 4 Making and Testing an Acid Buffer

| Blank / answer | Value | Source |
|---|---|---|
| resist a change in pH; conjugate base | quoted | BUF:75 |
| 0.50; pH = pKa; ±1 | quoted | BUF:164, 172 |
| highest effectiveness | quoted (“higher effectiveness”) | BUF:176 |
| salt that ionizes completely | quoted | BUF:180, 184 |
| pH went up when MA added; A⁻ traps H⁺ | quoted | BUF:189 |
| pH = pKa + log([A⁻]/[HA]) | quoted | BUF:138; BEN:288–300 |
| Salt max = (43 + 4) − 4 = 43 particles, 5 per shake → 9 shakes; auto-advance | | BSM:81; BDS:89–97, 112–117; `useBufferAutoAdvance.ts:48–52` |
| At max salt [A⁻] = [HA] = 0.206 → pH = pKa = 4.14 | ratio 1 | BSM:93–106, 134–143 |
| Buffer range 3.14–5.14 | 4.14 ± 1 | BUF:172 |
| Hypothetical ratios 10/1, 1/10 → 5.14, 3.14 | | worked (labelled hypothetical) |
| HCl test ends at pH 2.64 | pKa − 1.5 (scripted) | BDS:141–157, 166–176 |
| H⁺ + A⁻ → HA; “doesn't go down immediately” | quoted | BUF:204 |
| “reached its limit … pH has gone down significantly” | quoted | BUF:87 |
| Graph: straight diagonal water line vs. buffer line (shape only, no ticks) | | `buffers/components/BufferPhMolesChart.tsx:139–152, 177–178` |

## Page 5 A Weak Base Buffer

| Blank / answer | Value | Source |
|---|---|---|
| higher Kb → more OH⁻, more basic | quoted | BUF:96 |
| HB is the conjugate acid; Kb large → Ka small | quoted | BUF:226, 230 |
| pOH = pKb when equal | from HH | BUF:235; BEN:288–300 |
| HB reacts with free OH⁻ to make more B⁻ | quoted | BUF:297 |
| Water resets to 0.5 when weak base is chosen | | BufferScreen.tsx:552–566 |
| B⁻ equilibrium: [OH⁻] 2.85×10⁻³, pOH 2.55, pH 11.45 | at 0.2057 M | worked from SUB:203, ENG:61–69 |
| pKb 4.40 (summary 4.398); buffer pOH 4.40, pH 9.60 | | SUB:124; BSM ratio 1 |
| KOH limit: pOH 2.90, pH 11.10 | pKb − 1.5 (scripted) | BDS:141 |
| “pOH went up” | quoted | BUF:282 |

## Page 6 Strong Acid–Strong Base Titration

| Blank / answer | Value | Source |
|---|---|---|
| salt and water; neutralization | quoted | TST:32 |
| H⁺ + OH⁻ → H₂O | quoted | TST:38 |
| equivalence point; pH 7 | quoted | TST:41 |
| excess H⁺ before EP; basic after | quoted | TST:52, 76 |
| Rows default 11 → V = 0.15 + (11−7)(0.5/8) = 0.400 L | | TM:20–25, 35, 80 |
| Max substance = ceil(19 × 11/3) = 70 particles (14 shakes of 5); auto-advance at max | | TM:16, 59, 75; TGS:437–440 |
| M = 70/209 = 0.335 M; n = 0.134 mol | 0.33493; 0.13397 | TM:81–84; TS:713 |
| Titrant default 0.35 M (range 0.2–0.5) | | TM:12–14 |
| V(EP) = n/M = 0.383 L | 0.38278 | ENG:188–195; TM:86–89 |
| Starting pH 0.48 (meter 0.5) | −log 0.33493 = 0.4750 | ENG:22 |
| Halfway (35 of 70 taps): V 0.191 L, pH 0.95 | 0.067 mol left / 0.5914 L = 0.1133 M | TM:91–95; ENG:231–239 |
| EP pH 7.00 | | ENG:264–266 |
| End: 70 more taps → V = 2 × 0.383 = 0.766 L; pH 13.06 (HCl + KOH) / 0.94 (KOH + HCl) | excess 0.134 mol / 1.1655 L = 0.1149 M | TM:63–64, 96–97; ENG:282–295 |
| KOH start 13.5 (meter) | 14 + log 0.3349 = 13.525 | ENG:26 |
| Math panel shows n, V, M to 3 decimals, pH 2 decimals, after first drop | | TMP:80–114, 165 |

## Page 7 Weak Acid and Weak Base Titrations

| Blank / answer | Value | Source |
|---|---|---|
| spectator ions | quoted | TST:189 |
| buffer region | quoted | TST:202 |
| max buffer capacity, pH = pKa, halfway | quoted | TST:215 |
| titration ends at the equivalence point (lab) | quoted | TST:137 |
| HA start pH 2.31 (guide message, 2 dp) | x = 4.903×10⁻³ at 0.3349 M | TST:196; ENG:47–54 |
| Halfway stop: round(70 × 0.5) = 35 taps, V 0.191 L, pH 4.14 | HH, ratio 1 | TM:65, 69–71; ENG:246–250 |
| HA EP: V 0.383 L, pH 8.69 (guide shows 8.69) | [A⁻] 0.1711 M, Kb 1.37×10⁻¹⁰, [OH⁻] 4.84×10⁻⁶, pH 8.685 | ENG:268–274; TGS:111–121; TST:221 |
| B⁻ start pH 11.56, guide pOH 2.44 | [OH⁻] 3.66×10⁻³ | TST:231 |
| B⁻ halfway pH 9.60; EP pH 5.18 | pOH = pKb; [HB] 0.1711 M, Ka 2.5×10⁻¹⁰, pH 5.184 | ENG:253–257, 275–278 |
| Weak post-EP runs until pH ≥ 13.0 (acid) or ≤ 1.0 (base), ~115 of 140 taps, V ≈ 0.697 L | | TGS:61–62, 360–362 |

## Values checked by hand

All numbers were recomputed with python (`scratchpad/u8/calc.py`), using the sim's formulas:

```
Intro (M = 0.1 × shakes/14):
  HCl 0.05 M: pH 1.3010, pOH 12.699 -> [OH-] 2.0e-13 ; 0.10 M: pH 1.000
  KOH 0.10 M: pH 13.000
  HA  0.10 M: x = 2.6656e-3, pH 2.5742, % ion 2.67 ; sqrt shortcut pH 2.568
  HF  0.10 M: pH 2.1880 ; HCN 0.10 M: pH 2.5294
  B-  0.10 M: [OH-] 1.9801e-3, pOH 2.7033, pH 11.2967 ; [H+] 5.05e-12
Buffers (rows: (0.5-0.31818)/(0.681818-0.31818) = 0.500003 -> 11.00002 -> 11; 19*11 = 209):
  C = 43/209 = 0.205742
  HA: [H+] 3.8391e-3, [HA] 0.20190, pH 2.4158, pKa 4.1367, limit 2.6367
  HF: pH 2.0269 ; HCN: pH 2.3708
  B-: [OH-] 2.8488e-3, pOH 2.5453, pH 11.4547, pKb 4.3979, buffer pH 9.6021, limit pH 11.1021
Titration: V = 0.15 + 4*(0.5/8) = 0.400 L; max = ceil(209/3) = 70; C = 0.334928; n = 0.133971 mol
  Veq = 0.133971/0.35 = 0.382775 L
  HCl start pH 0.4750; 35 taps: Vt 0.191388, excess 0.113269 M, pH 0.9459; end Vt 0.765550, pH 13.0605 / 0.9395
  KOH start pH 13.5250
  HA start pH 2.3091; half pH 4.1367; EP [A-] 0.171149 M, pH 8.6850; 69 taps pH 5.976 (< EP, so the EP stop is at 70)
  B- start pH 11.5611 (pOH 2.4389); half pH 9.6021; EP pH 5.1844
  weak post-EP reaches pH 13.0 / 1.0 at tap 115 of 140, Vt 0.69720 L
FRQ extension: after 0.100 L KOH: pH = 4.1367 + log(0.035/0.0990) = 3.685
```

## Sim vs. textbook differences

- **HCN Ka = 9×10⁻⁵** in the sim (SUB:195; the code comment itself says the real value is ~6.2×10⁻¹⁰).
- **F⁻ Kb = 1.3×10⁻⁵** (SUB:210), but the sim's HF Ka 4.5×10⁻⁴ implies Kb(F⁻) = 2.2×10⁻¹¹. **HS⁻ Kb = 1×10⁻³** (SUB:217); textbook Kb(HS⁻) ≈ 1×10⁻⁷. The worksheet uses only HA and B⁻ for graded answers.
- **Introduction concentrations ignore the water level**: 14 shakes always gives 0.10 M (GIS:271–279).
- **Introduction bars are not to scale**: bar heights are fixed shares by `substanceAddedPerIon` (e.g. HA shows 50% HA, 25% H⁺, 25% A⁻) (`ConcentrationBarChart.tsx:83–100`), while real HA at 0.10 M is 2.7% ionized.
- **Buffer “limit” is scripted**: the strong-acid/strong-base test always ends 1.5 pH units past the buffer pH (BDS:141), so buffer capacity is not calculated from moles.
- **Titration volumes are large** (0.400 L sample, 0.383 L titrant); the code comment says 11 rows = 0.35 L but the equation gives 0.400 L (TM:22).
- **Indicator** is a single generic color that blends linearly with pH/7 (TS:382–410); no transition range or pKa(In).
- Pre-EP weak titration pH uses Henderson-Hasselbalch from the first drop (ENG:242–250); textbooks would also use HH there, so this matches except for very small additions.
- Concentrations are “particles ÷ grid slots”, i.e. invented units; we treat them as M as the sim's labels do.

## Sim bugs and confusing text (not copied into the worksheet)

1. **Titration math panel, weak acid before EP**: [H⁺] box = (n(HA) − n(KOH))/(V total), which is leftover HA, not [H⁺]; shown next to the HH pH, so “4.14 = −log 0.113” appears (TS:713–721; TMP:153–170).
2. **Weak-base fraction-of-species curve is reversed**: uses 10^(pKb − pOH) instead of 10^(pOH − pKb), so B⁻ appears to vanish at high pH (`pages/AcidsBases/buffers/BufferCharts.tsx:478–485`). Contradicts BUF:261 (“much more B⁻ than HB”).
3. **Wrong conjugate acids** for F⁻ and HS⁻: equation shows “F” and “HS” instead of HF and H₂S (`ReactionEquation.tsx:98`; SUB:207–218). Titration salt for B⁻ shows as “HBCl” (`ReactionEquation.tsx:58–62`).
4. **Weak acid called “dissociates completely”**: the set-water-level message is reused for weak acids (INTRO:104 via STORE:88–93, step intro-25).
5. **“moles of strong acid you added”** shown after the strong *base* (INTRO:127, step intro-20).
6. **Base-buffer text**: “When OH⁻ and B⁻ are the same, then pOH = pKb” (should be HB and B⁻) (BUF:265); dev note “(assuming cationic conjugate)” and “reverse reaction” (BUF:216).
7. **?mode=explore** only hides the guide and highlight blocking (`components/AcidsBases/guide/freeExplore.ts`, `HighlightOverlay.tsx:47, 188, 238`); the screens never read it, so bottles stay locked (Intro bottles unlock by step: GIS:523–548; Buffers bottles need `requiresAction` steps: BBOT:121–127). Not run in a browser; from code reading.
8. Intro bar label for B⁻'s conjugate shows “HB⁺” (`ConcentrationBarChart.tsx:99`) while the equation shows “HB”.
9. Typo “that's the concept of pOH exists” (INTRO:59); duplicated text for `acidBufferLimitReached` dynamic text (BUF:208–211, unused).
10. Hard-coded fallback weak-base EP pH 5.32 (TGS:60) differs from the computed 5.18; only used if the computation fails.

## AP topics not covered by the sim

- **8.6 Molecular Structure of Acids and Bases** (bond polarity/strength, oxyacids, why HF is weak): not in the sim at all.
- **8.1** temperature dependence of Kw: the sim states Kw only at 25 °C (BUF:46).
- **8.5** indicator choice by pKa(In) and polyprotic titrations; **8.3** polyprotic acids.
- **8.10 Buffer capacity** is only qualitative (the limit is scripted, see above); comparing buffers of different total concentration is not possible.
- **8.4** reactions of a weak acid with a weak base, and the pH of a salt solution on its own (only seen at the titration EP).
