# Unit 5 Kinetics: sources for every answer

Sim: Reaction Rates Lab, `/home/user/reactionratewebapp` at deployed commit `dfbe5a5`. All paths below are under `src/`.
Tess's Reaction Rates Student Notes and Answer Key (`chemtutor-static-tutor/public/sims/reaction-rates/static/media/`) were read. The guided-note blanks keep her wording and answers. The new parts are the set-ups, data tables, calculations and analysis.

## How the controls work (needed for every Set Up box)
| Fact | Source |
|---|---|
| Starting values 0.70 M / 0.35 M, 10 s / 15 s | `context/AppContext.tsx:101-102` |
| ▲ ▼ change the active concentration by 0.10 M (`step*100` on a 0–100 scale, then /100) | `components/SliderVert/SliderVert.tsx:68,129` |
| ◀ ▶ change the active time by 1 s (`step*10` on a 0–200 scale, then /10) | `components/SliderHoriz/SliderHoriz.tsx:77,147` |
| Limits: c₂ ≥ 0.14 M and c₁ − c₂ ≥ 0.13 M; t₂ − t₁ ≥ 2.5 s; t ≤ 20 s | `components/ChartTime/ChartTime.tsx:120-133`, `SliderVert.tsx:48-53`, `SliderHoriz.tsx:56-60` |
| After the reaction ends, the arrows scrub the time indicator 1 s per click (◀ = back) | `SliderHoriz.tsx:81`, `SliderVert.tsx:72` |
| [A] at the indicator is shown inside the bottom panel row: values[12] (zero), values[9] (first/second) = curValC | `pages/ReactionRates/zero/index.tsx:187`; `first/index.tsx` getFormula; `second/index.tsx:178` |
| Values button: c₁ c₂ / t₁ t₂; prints "-" for 0 | `layout/WatchMenu.tsx:33-38` |
| Values carry between screens (one shared context; the page change only resets step and reaction) | `hooks/useFunctions.ts:23-37` |
| Which control is active per step (stepsActions `canvaTimeSliderC/T`) | `zero/constants.ts:161-317`, `first/constants.ts` stepsActions, `second/constants.ts:187-` |
| Menu screens unlock only after they are visited | `layout/ChapterMenu.tsx:113` |
| Explore mode button | `layout/NavMenu.tsx:256-275` |

## Page 1: Zero order (run 1: c₁ 0.90, t₁ 0, c₂ 0.25, t₂ 13)
| Blank / cell | Value | Source |
|---|---|---|
| k = 0.050 M/s (calc, notes) | −(0.25−0.90)/(13−0) | formula `zero/index.tsx:151-157`; text "k=${val[0]}M/s" with toFixed(3) `zero/constants.ts:15-17`, `zero/index.tsx:241` |
| t½ = 9.00 s | A₀/(2k), A₀ = (t₁c₂−t₂c₁)/(t₁−t₂) = 0.90 | `zero/index.tsx:161-163`; text `zero/constants.ts:20-23` |
| rate, concentration, time / k / Half-life, half | sim wording | `zero/constants.ts:15-23` |
| constant, k, straight line, −k | sim wording | `zero/constants.ts:31-33` |
| Run 1 table: 0.25, 0.45, 0.60, 0.75, 0.90 at 13, 9, 6, 3, 0 s; rate 0.05 | [A] = 0.90 − 0.05t | `components/ConcentrationPlotView/ConcentrationEquation.ts:42-52`; row `zero/index.tsx:183-187` |
| Run 2 (C→D, t₂ 20): k 0.03, t½ 13.85 | 0.65/20 = 0.0325 → JS toFixed(2) "0.03"; 0.90/0.065 | worked from `zero/index.tsx:151-163` (run in node) |
| Run 3 (E→F, c₁ 1.00, t₂ 20): k 0.04, t½ 13.33 | 0.75/20 = 0.0375 → "0.04"; 1.00/0.075 | same |

## Page 2: First order (c₁ 0.60, c₂ 0.15, t = t₁ = 10, hidden t₂ = 20)
| Blank | Value | Source |
|---|---|---|
| k = 0.139 (text), 0.14 (panel) | (ln0.60 − ln0.15)/10 | `first/index.tsx:155-161`; text `first/constants.ts:16-19` |
| t½ = 5.00 s | ln2/k | `first/index.tsx:160`; text `first/constants.ts:25-29` |
| start rate 0.08 | k·c₁ | `first/index.tsx:161` |
| rate, concentration (rate law) | sim wording | `first/constants.ts:16-18` |
| k[A]¹ | "rate=k[A]^1" | `first/constants.ts:21-22` |
| curve, A | | `first/constants.ts:40-42` |
| faster, more, higher | | `first/constants.ts:46-47` |
| straight line, −k (ln[A] vs t) | Tess's key p. 2; panel eq. k = (ln[A₀]−ln[Aₜ])/t (image `assets/ReactionRates/math/first/0.png`) | |
| Table [A] 0.60, 0.45, 0.30, 0.20, 0.15 at elapsed 0, 2, 5, 8, 10 | graph model A(t) = a₀e^(−k t), k = ln(c₂/c₁)/(t₁−t₂), a₀ = c₁e^(k t₁), clock 10→20 s | `components/ChartTime/ChartTime.tsx:81-86`, `ConcentrationEquation.ts:99-131` |
| ln[A] −0.51, −0.80, −1.20, −1.61, −1.90 | ln of the 2-decimal readings | calculated |
| slope −0.139 | (−1.90 + 0.51)/10 | calculated |

## Page 3: Second order (c₁ 1.00, c₂ 0.25, t = 10, hidden t₂ = 20)
| Blank | Value | Source |
|---|---|---|
| k = 0.300 (text), 0.30 (panel) | (1/0.25 − 1/1.00)/10 | `second/index.tsx:149-157`; text `second/constants.ts:13-14` |
| t½ = 3.33 s | 1/(k[A]₀) | `second/index.tsx:156`; text `second/constants.ts:20-23` |
| second half-life 6.67 s | 1/(0.30×0.50) | calculated (textbook formula, same one the sim uses) |
| k[A]² | | `second/constants.ts:16-18` |
| steeper curve, A | | `second/constants.ts:31-32` |
| a lot faster, much higher | | `second/constants.ts:35` |
| 0.81, 0.64, 0.1, 0.17 | sim's own example (implied k = 1) | `second/constants.ts:41-43` |
| straight line, k (1/[A] vs t) | "k=(1/[A]-1/[A0])/t … 1/[A] vs t is a straight line … slope is k" | `second/constants.ts:50-53` |
| Table [A] 1.00, 0.63, 0.40, 0.29, 0.25; 1/[A] 1.00, 1.59, 2.50, 3.45, 4.00 | model 1/[A] = 1/a₀ + kt with a₀ = 1/(1/c₁ − k t₁) | `ChartTime.tsx:88-93`, `ConcentrationEquation.ts:158-171` |

## Page 4: Reaction comparison
| Blank | Value | Source |
|---|---|---|
| Graph order top→bottom zero, first, second | chartTimeItem0/1/2 use zeroOrder/firstOrder/secondOrder, stacked in a column | `comparison/index.tsx` ConcentrationPlotView `order={0,1,2}`; `comparison/*.module.scss` `.chartTimeCol {flex-direction: column}` |
| Shapes straight line / curve / steeper curve | | `comparison/constants.ts:18` |
| Rate laws, integrated forms | cards `comparison/index.tsx:194-213` (second order card typo corrected, see bugs); Tess's key p. 4 |
| same start, same end, lowest = second, highest = zero at 5.0 s | every curve: A₀ = 1, reaches 0.10 at 20 s (localStorage keys never written, so defaults c₁ 1, c₂ 0.1, t 0→20). At 5 s: 0.775 / 0.562 / 0.308 | `components/ConcentrationPlotView/ReactionComparisonViewModel.ts:10-20,106-152` |
| Time readout under the buttons, 1 s per click | | `comparison/index.tsx` handleSpinDown/Up and the "Time:" label |

## Page 5: Energy profile (Kinetics; reaction choice "Zero Order Reactions")
| Blank | Value | Source |
|---|---|---|
| Collision theory, energy, orientation | | `kinetics/constants.ts:13-17` |
| activation energy (Eₐ) | | `kinetics/constants.ts:20` |
| Arrhenius equation, higher | | `kinetics/constants.ts:25,34` |
| frequency factor, natural logarithm base, 8.314, Kelvin | | `kinetics/constants.ts:29-31` |
| energy diagram, reaction profile | | `kinetics/constants.ts:54` |
| exothermic, higher, released | | `kinetics/constants.ts:59-62`; zero choice draws reactants 0.5 > products 0.2 `components/EnergyProfileChart/constants.ts:72-80` |
| activation energy (hump), Catalysts, lower | | `kinetics/constants.ts:71,76-78` |
| Eₐ in panel = "9e3", R = 8.31, T₁ = 400 | val_Ea = [9,8,6][reaction] | `kinetics/index.tsx:158-170,348` |
| slope −1083 | −9000/8.31 = −1083.0 | text `kinetics/constants.ts:95` |
| k₂ = 1.8, 2.1, 3.7 (1st, 2nd, 3rd catalyst used) | ln_below | `kinetics/index.tsx:349` |
| k₁ at 550 K: 0.9, 1.0, 1.8 | k₂·exp((9000/8.31)(400−550)/(400·550)), toFixed(1) | `kinetics/index.tsx:158-170` (run in node) |
| T₂ = 550 K after 5 clicks from 425 | burner resets to 425 (`valueFire: 425` in stepsActions 19, 25, 30); ±125/1000 of 400–600 K = 25 K per click | `components/CanvasBeaker/Burner/Burner.tsx:15-23,114` |
| 8000 J, 6000 J | | `kinetics/constants.ts:126,149` |
| kinetic energy line, below (at 425 K), kinetic, up | text; line height 0.6 + 0.35(T−400)/200 | `kinetics/constants.ts:90-91,104-106`; `EnergyProfileChartInput.ts` getCurrentEnergy; `EnergyProfileChart.tsx:126-133` |
| 550 K: line above orange hump, below gray | line 0.8625; catalyzed peak 0.80 (maxReducedPeak, Catalyst.A because reaction index 0 → catalyst 1); original peak 0.90 | `kinetics/index.tsx:414`, `EnergyProfileChartInput.ts:58-62`, `EnergyProfileChart/constants.ts:72-80` |
| gray original / orange catalyzed | | `EnergyProfileChart.tsx:73-80` |
| ratio k(550)/k(400) = 2.09 | e^0.7384 | calculated |
| Beaker times at 550 K (~3.5 s to the "Perfect!" step, ~10.5 s to finish) | +gasSpeed²/15 % per 0.5 s; gasSpeed = (T/100 − 4)·5 + 1 | `kinetics/index.tsx:310`; `components/CanvasBeaker/Chamber/ChamberF.tsx:362-368,408-426` |

## Explore mode (Explore boxes only, no graded answers)
Default order Second, 0.70/0.35 M, 0→10 s; k shown to 3 decimals; y-axis label ln[A] / 1/[A] by order (`pages/ReactionRates/explore/index.tsx:12-16,41-48,51-60,236`).

## Values checked by hand
Every number above was recomputed in node, copying the sim's JS formulas and `toFixed` rounding (script: `u5calc.js` in the session scratchpad), and spot-checked in python:
- Zero run 1: k = 0.65/13 = 0.0500 → "0.05", "0.050"; A₀ = (0·0.25 − 13·0.90)/(0−13) = 0.90; t½ = 0.90/0.10 = 9.00. [A](3) = 0.75, (6) = 0.60, (9) = 0.45.
- Zero run 2: 0.65/20 = 0.0325 → toFixed(2) "0.03"; t½ 13.846 → "13.85". Run 3: 0.75/20 = 0.0375 → "0.04"; t½ = 1.00/0.075 = 13.33.
- First: ln0.60 = −0.5108, ln0.15 = −1.8971; k = 0.13863 → "0.14"/"0.139"; t½ = 5.000; rate = 0.0832 → "0.08". Graph k = ln(4)/10 identical. A(elapsed 2) = 0.4547 → 0.45, A(8) = 0.1980 → 0.20; ln0.45 = −0.799, ln0.20 = −1.609.
- Second: k = 3.00/10 = 0.30; t½ = 3.333; 1/(0.30·0.50) = 6.667; rate = 0.30·0.0625 = 0.0188 → "0.02". A(12) = 0.625 → "0.63" (JS gives 0.63), A(15) = 0.40, A(18) = 0.2941 → 0.29; 1/0.63 = 1.587, 1/0.29 = 3.448.
- Comparison: k = 0.045, 0.1151, 0.45; at 5 s: 0.775, 0.562, 0.308; all three reach 0.100 at 20 s.
- Arrhenius: 9000/8.31 = 1083.03; (1/400 − 1/550) = 6.818×10⁻⁴; product 0.7384; e^0.7384 = 2.093. k₁ = 1.8/2.093 = 0.860 → "0.9"; 2.1/2.093 = 1.004 → "1.0"; 3.7/2.093 = 1.768 → "1.8".
- AP practice: 0.60/8 = 0.075 M; 0.30·0.25 = 0.075 M/s; extension e^((3000/8.31)/550) = 1.93.
- Beaker at 550 K: gasSpeed 8.5, 4.817 %/tick → 30 % after 7 ticks (3.5 s), 100 % after 21 ticks (10.5 s).

## Sim vs. textbook differences
- The panel uses R = 8.31; the step text and textbooks use 8.314 (`kinetics/index.tsx:161` vs `kinetics/constants.ts:30`). The worksheet uses 8.31 in calculations so numbers match the panel.
- Eₐ is in J with no "per mole" (panel "9e3", text "8000 J"); AP uses J/mol.
- Zero order t½ uses [A]₀ extrapolated to t = 0, not the starting concentration (`zero/index.tsx:161-163`). The worksheet starts at t = 0 so they are equal.
- First/second order use the first time value as the reaction length t (`first/index.tsx:159`, `second/index.tsx:155`), while the graph runs from t₁ to t₂ (`ChartTime.tsx:83,90`).
- No units are shown for first and second order k; the worksheet adds s⁻¹ and M⁻¹s⁻¹.
- The two-temperature Arrhenius form in the panel is ln(k₁/k₂) = (Eₐ/R)((T₁−T₂)/(T₁T₂)) (`assets/ReactionRates/math/kinetics/2.png`), equivalent to the AP form.

## Sim bugs and confusing text (not copied into the worksheet)
1. "a different reaction, which has a fixed rate constant" (zero/constants.ts:44,65; first:62,83; second:60,81): k is never fixed; the constants `reactionBRateConstant`/`reactionCRateConstant` (`ConcentrationPlotView/constants.ts:41,44`) are unused. "Notice how the final concentration varies as you adjust the final time" (zero/constants.ts:53) does not happen. "You picked a reaction with a rate constant ${val[2]}" shows the previous run's k.
2. Zero order: "This happens at a variable rate" (zero/constants.ts:28,58,78); zero order rate is constant.
3. First/second order: panel k divides by t₁ (`first/index.tsx:159`, `second/index.tsx:155`) but the graph uses t₂ − t₁ (`ChartTime.tsx:83,90`). They disagree unless t₂ = 2t₁; t₂ is hidden and inherited from the previous screen.
4. First order: "t½=In(1)/k" (first/constants.ts:29) should be ln(2)/k (the value is correct); "In" (capital i) for ln in the equation images and the graph label (`first/index.tsx:311`).
5. First order bottom row: rate = k·c₁ stays fixed while [A] in the parentheses changes when scrubbing (`first/index.tsx:161`), so "0.08 = 0.139(0.15)¹" is shown. Second order uses k·[A]ₜ² instead (`second/index.tsx:157`), inconsistent with first.
6. Second order 1/[A] box: CanvasTime draws the reactant line from c₁ down to a fudged c₂ (`components/ChartInA/ChartInA.tsx:72-74`, `Canvas/CanvasTime.tsx:175-180`), so 1/[A] appears to fall. ln[A] box is also not to scale (same fudge).
7. Comparison: "the constants k are the ones we already got from the previous reactions" (comparison/constants.ts:11) is false; cards are hard-coded k 0.07/0.07/0.14 (`comparison/index.tsx:194-213`) (they match only the sim's default settings), while the curves use k 0.045/0.115/0.45. First order card "[A]₀e^-kt" exp1 "1.0e^0.07" lacks the minus; second order card "[A₀]([A₀]kt+1)" lacks the "/" (line 210). `shuffledOrder` is unused, so the graphs are always zero/first/second top to bottom.
8. Kinetics step 9 text (kinetics/constants.ts:48): turVal has only 2 entries (`kinetics/index.tsx:191-194`), so it reads "Eₐ is 9J and k is -0.16 when the temperature is undefinedK".
9. Kinetics step 16 "Eₐ was reduced to ${val[0]}J" shows "9J" (constants.ts:90); steps 24/29 hard-code 8000 J / 6000 J; the panel's Eₐ never changes with the catalyst (`kinetics/index.tsx:348`). Step 18 hard-codes "k went up to 1.3 when T is 400K" (constants.ts:100) while the panel shows 1.5 at 425 K. Step 17 slope −1083 is hard-coded (matches only the Zero Order choice).
10. Kinetics panel holds k₂ (at the burner temperature) fixed per catalyst and back-calculates k₁ at 400 K, so "k at 400 K" changes with the burner (`kinetics/index.tsx:158-163`).
11. The catalyzed hump depends on the reaction choice, not the catalyst used (`kinetics/index.tsx:414`): all three catalysts draw the same hump. The beaker conversion runs on a timer whose speed depends only on temperature (`ChamberF.tsx:426`, `kinetics/index.tsx:310`), so products form even when the kinetic energy line is below the hump, and catalysts do not speed up the beaker. `canReactToC` is never used.
12. "First Order Reactions" choice draws an endothermic profile (reactants 0.2, products 0.4; `EnergyProfileChart/constants.ts:82-90`) but the text says exothermic (kinetics/constants.ts:59).
13. Text says "Use the flame slider"; the burner is changed with ◀ ▶ (25 K per click) and its temperature appears only in the equation panel (on-screen label is screen-reader only, `Burner.tsx:29-31`).
14. Values button prints "-" when a time is 0 (`WatchMenu.tsx:37`). Typo "Half-lie" only in code comments; "reaciton" typo is in Tess's PDF only.
15. Kinetics energy-profile and ln(k) vs 1/T charts have no numbers (not to scale); the ln(k) chart line uses Eₐ 12000/10000/8000 (`kinetics/index.tsx:424-431`), not the panel's 9000.

## AP topics not covered by the sim
- **5.2 (part):** method of initial rates, multi-reactant rate laws, overall order, units of k by order. Use initial-rate data tables.
- **5.4 Elementary Reactions** (molecularity; rate law from coefficients only for elementary steps).
- **5.7 Introduction to Reaction Mechanisms** (intermediates, summing steps).
- **5.8 Reaction Mechanism and Rate Law** (rate-determining step).
- **5.9 Steady-State Approximation** (fast reversible first step, substituting for intermediates).
- **5.10 Multistep Reaction Energy Profile** (two humps, intermediate valley, which Eₐ is rate-limiting).
- **5.11 Catalysis (part):** catalysts as a new reaction pathway that is consumed then regenerated; acid-base, surface and enzyme catalysis. The sim only shows "a catalyst lowers Eₐ".
- **5.5 (part):** orientation is only described in text; no orientation demo.
Teacher should use their usual lessons for these (about 2–3 periods), e.g. AP Classroom Topic Questions 5.4–5.11, a worked NO₂ + CO mechanism, and a two-hump energy diagram exercise. The lesson plan's prep item and AP practice question 2(e) point to this.
