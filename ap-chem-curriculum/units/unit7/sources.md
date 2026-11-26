# Unit 7 Equilibrium: sources for every answer

Sim: **Equilibrium Lab** (chemsims.app/sims/equilibrium), source `/home/user/equilibriumweb`, deployed commit `5dbe7de`.
All paths below are relative to `/home/user/equilibriumweb/src/`. Abbreviations:

- `AQ` = `features/lessons/aqueous/lesson.tsx`
- `GA` = `features/lessons/gaseous/lesson.tsx`
- `SO` = `features/lessons/solubility/lesson.tsx`
- `PR` = `data/presets/index.ts`
- `SOLV` = `components/l/equilibrium/aqueous/equilibriumSolver.ts` (bisection ICE solver used by aqueous and gaseous)
- `SSIM` = `components/l/equilibrium/solubility/simulation.ts` (Ksp quadratic solver)

Module order and URLs: `data/subUnits.ts:55–268`; `/home/user/chemtutor-static-tutor/lib/sims.ts:445–471`.

How the sim runs (applies to every page):

- Each module loads its own preset when entered, both from the URL and from Next across a module boundary:
  `features/lessons/core/subUnitTransitions.ts:16–18` → `restoreDefaultSubUnit` (`features/lessons/aqueous/useAqueousLessonController.tsx:201–218`) → `PR:486–505`.
- Equilibrium is reached at simulation progress 1 (exponential interpolation, exactly equal to the ICE equilibrium at progress 1): `components/l/equilibrium/aqueous/simulationConcentrations.ts:148–186`, `SSIM:172–201`.
- Table tab (ICE table, `toFixed(2)`): aqueous/gaseous `components/l/equilibrium/aqueous/ConcentrationTimeGraph.tsx:371–380, 334–358, 721` and `aqueous/IceTable.tsx:25–35`; solubility `components/l/equilibrium/solubility/ConcentrationTimeGraph.tsx:326`, `solubility/IceTable.tsx:6–15`.
- Q panel (2 significant figures, second numerator term adjusted): `components/l/equilibrium/displayNumbers.ts:38–93, 141–162`; `aqueous/EquationPanel.tsx:45–60, 171–178`; `solubility/EquationPanel.tsx:31–41, 118`.

---

## Page 1: Equilibrium (Aqueous · Equilibrium)

| Item | Answer | Source |
|---|---|---|
| Predict | forward (only reactants present) | reasoning; `AQ:364–375` ("Add reactant to make it start") |
| Notes: reversible, equilibrium | quoted | `AQ:207–209` |
| Notes: forward, reverse | quoted | `AQ:208–209` |
| Notes: same rate | quoted | `AQ:252–253` |
| Table: three reactions | A+B⇌C+D; 3A+2B⇌C+2D; 2A+3B⇌C+4D | `AQ:22–26` (dropdown `AQ:229–238`) |
| Table: Q expressions | products over reactants, coefficients as powers | `aqueous/EquationPanel.tsx:73–100`; `simulationConcentrations.ts:178–183` |
| Coefficient sums | 2/2, 5/3, 5/5 | from `AQ:22–26` |
| Calc: K = 10 | `EQUILIBRIUM_CONSTANT_K = 10` | `AQ:16` |
| Calc: K reverse 0.10, K doubled 100 | worked: 1/10; 10² | not shown by the sim (AP 7.6), uses `AQ:16` |
| Question: dynamic | "both forward and reverse reactions have the same rate" | `AQ:252–253`, `AQ:480–483` |

## Page 2: Reaction Quotient (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Module resets reaction to A + B ⇌ C + D | preset `selectedReaction: 0` | `PR:22–34` |
| Water level does not matter | concentrations never use the slider | `components/l/equilibrium/aqueous/AqueousBeaker.tsx:139–148, 341–343` (visual only) |
| 0.30 max, 0.02 per shake, snaps to max | `CONCENTRATION_INCREMENT = 0.02`, `CONCENTRATION_MAX = 0.3` | `AQ:17–18`; `useAqueousLessonController.tsx:493–522` |
| Predict: Q = 0 < K | [C] = [D] = 0 | `simulationConcentrations.ts:181–183` |
| Notes: product / reactant / stoichiometric coefficient | quoted | `AQ:277–279` |
| Notes: Q and K same at equilibrium | quoted | `AQ:290–291` |
| Notes: larger | quoted | `AQ:303–304` |
| Notes: Kc | quoted | `AQ:327–328` |
| Notes: favored | quoted | `AQ:436–438` |
| Equations: Q = [C][D]/([A][B]), K = 10 | | `aqueous/EquationPanel.tsx:73–113`; `AQ:16` |
| Calc: x = 0.228; [A] = [B] = 0.072; [C] = [D] = 0.23 | √10 = 3.162; x = 0.30·3.162/4.162 | `SOLV:206–332` run with A = B = 0.30, K = 10 |
| Table (ICE, 2 dp) | I 0.30 0.30 0.00 0.00; C −0.23 −0.23 +0.23 +0.23; F 0.07 0.07 0.23 0.23 | Table tab, `aqueous/IceTable.tsx:25–35` |
| Graph | Q rises from 0, levels on K line | `aqueous/QTimeGraph.tsx:441–495` (no tick labels → shape only) |
| Free Explore sliders 0–0.3, step 0.01 | | `routes/_authenticated/l/equilibrium/aqueous.tsx:263–298` |
| FE: Q = 4 (forward), Q = 25 (reverse), both end 0.072/0.228 | 0.2²/0.1² = 4; 0.25²/0.05² = 25 | `SOLV` with each start |

## Page 3: Le Chatelier's Principle (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Start state | [A]₀ = 0.30, [B]₀ = 0.26302, rxn 0 | `PR:36–48` (line 45) |
| First equilibrium | A 0.0880, B 0.0510, C = D 0.2120 (Table 0.09, 0.05, 0.21, 0.21; Q panel 0.088, 0.051, 0.21) | `SOLV`; frozen at `AQ:530–538` (line 533) |
| Shake C, D to 0.30 | phase-2 max = 0.30 − C_eq = 0.088 (≈5 shakes, min 0.05) | `useAqueousLessonController.tsx:496–499`; `AQ:20, 607–620` |
| Predict | reverse; [A] up | `AQ:646–648` |
| Notes: counteract | quoted | `AQ:524–525` |
| Notes: reverse / reactants | quoted | `AQ:646–648` |
| Notes: equal / constant | quoted | `AQ:692–693` |
| Calc: Q = 20 > K | 0.30² / (0.088 × 0.051) = 20.05; panel shows "20" | `simulationConcentrations.ts:181–183` |
| Table row "right after" | 0.09, 0.05, 0.30, 0.30 | Table tab Initial row in phase 2 (`aqueous/ConcentrationTimeGraph.tsx:97–100, 334–358`) |
| Table row "new equilibrium" | x = −0.0207: A 0.1087, B 0.0717, C = D 0.2793 → 0.11, 0.07, 0.28, 0.28 | `SOLV` |
| Question: K unchanged | 0.28²/(0.11 × 0.07) = 10.2 ≈ 10 | worked from table |
| Question: partial undo | 0.21 → 0.30 → 0.28 | above |
| FE "Add A" slider | 0–0.3 | `aqueous.tsx:263–271` |

## Page 4: Partial Pressure (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Reactions | 3A+4B⇌C+2D; A+2B⇌4C+3D; 4A+2B⇌C+2D | `GA:16–20` |
| Kp = 10 | `DEFAULT_EQUILIBRIUM_K = 10` | `GA:22` |
| Pump 0.043/pump, max 1.5, min 0.745 | | `GA:26–28`; `features/lessons/gaseous/useGaseousLessonController.tsx:470–479` |
| A/B switch | `MoleculeSwitch` | `components/l/equilibrium/gaseous/GaseousBeaker/GaseousBeaker.tsx:146–150` |
| Notes: partial pressures | quoted | `GA:331–332` |
| Notes: Kp, pressure | quoted | `GA:343` |
| Notes: Q = Kp, lower | quoted | `GA:456–458` |
| Equations: Q = P_C·P_D²/(P_A³·P_B⁴), Kp = 10 | panel uses Pa, Pb, Pc, Pd | `aqueous/EquationPanel.tsx:79–99`; `GA:22` |
| Calc: x = 0.2741; ΔP = −0.82, −1.10, +0.27, +0.55; final 0.68, 0.40, 0.27, 0.55 | | `SOLV` with P_A = P_B = 1.5, powers 3,4,1,2, K = 10 |
| Calc: Q check 10.1 | 0.0817/0.00805 | worked from 2-dp values |
| Table (ICE) | I 1.50 1.50 0.00 0.00; C −0.82 −1.10 +0.27 +0.55; F 0.68 0.40 0.27 0.55 | Table tab |
| Question: scale tips to reactants | angle = 15·log₁₀(Q/K), clamped; Q = 0 → −15° (left/reactant basket down) | `components/l/equilibrium/aqueous/EquilibriumDisplay.tsx:90–101, 213–216` |
| FE sliders 0–1.5 | | `routes/_authenticated/l/equilibrium/gaseous.tsx:307–342` |

## Page 5: Pressure Changes (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Start (preset) | P₀: A 1.5, B 1.376; eq A 0.7367, B 0.3583, C 0.2544, D 0.5089 (Table 0.74, 0.36, 0.25, 0.51) | `PR:93–120` |
| Piston slider all the way down | V = 60/124.8 = 0.4808 → ×2.08; all the way up V = 1.519 | `GaseousBeaker/AirBeaker.tsx:219–230` (calcGridHeight), beaker height = 0.7·280·1.1 = 215.6 (`GaseousBeaker.tsx:126, 158`; width 280 `routes/.../gaseous.tsx:96`); pressures ÷ V in `useGaseousLessonController.tsx:499–524` |
| Required change | \|V − 1\| ≥ 0.25 | `GA:29, 583–592` |
| Predict | 3 vs 7 gas moles → forward | `GA:16` |
| Notes: increases / reactants / decreases | quoted (rxn 0, V < 1 branch) | `GA:618–631` |
| Notes: forward consumes | quoted | `GA:663–673` (`(7 > 3) !== (V < 1)` → "forward", "consumes") |
| Calc: new P 1.53, 0.75, 0.53, 1.06; Q = 0.534 | 10 × 2.08⁻⁴ = 0.534 | worked; equals sim Q (python) |
| Table | I 1.53 0.75 0.53 1.06; C −0.22 −0.30 +0.07 +0.15; F 1.31 0.45 0.60 1.21 | `SOLV` x = 0.0749 |
| Question: Kp stays 10 | K only changes in `onTemperatureChange` | `useGaseousLessonController.tsx:526–545` |
| FE piston up: Q = 53 > Kp → reverse | 10 × (1/1.519)⁻⁴ … | worked (python: 53.27) |

## Page 6: Temperature Changes (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Start (preset) | A 1.0876, B 0.4194, C 0.4634, D 0.9268 (Table 1.09 0.42 0.46 0.93), Kp 10 | `PR:122–153` |
| "+ Heat" on products | `showHeat: true` for every gaseous step | `GA:247`; `components/l/equilibrium/aqueous/EquationAnimation.tsx:442–446` |
| Kp formula | Kp = 10 × 10^(−T), slider 0–1, step 0.01, clamp 0.001–10000 | `useGaseousLessonController.tsx:531, 542`; `GaseousBeaker/Burner.tsx:206–213`; `GA:23–25` |
| Full right → Kp = 1.0 | 10 × 10⁻¹ = 1.0, panel "1.0" | above |
| Must reach ≥ 0.40 | `TEMPERATURE_CHANGE_REQUIRED_PHASE3` | `GA:30, 851–860` |
| Notes: consume / endothermic | quoted | `GA:802–804` |
| Notes: exothermic / endothermic | quoted | `GA:836` |
| Calc: Q = 10 > Kp = 1.0 → reverse | pressures unchanged at the moment K changes | `GA:186–196` (phase 3 starts from phase-2 equilibrium) |
| Table | I 1.09 0.42 0.46 0.93; C +0.15 +0.20 −0.05 −0.10; F 1.24 0.62 0.41 0.83 | `SOLV` K = 1, x = −0.0503 |
| Question check | 0.41·0.83²/(1.24³·0.62⁴) = 1.00 | worked |
| FE middle slider ≈ Kp 3.2 | 10 × 10^(−0.5) | formula above |

## Page 7: Ionic Compounds

| Item | Answer | Source |
|---|---|---|
| Reactions AB, CD, EF (only letters/colours differ) | | `SO:28–53`, dropdown `SO:368–384` |
| Notes: precipitation reactions / dissolve | quoted | `SO:353–354` |
| Notes: solubility | quoted | `SO:400` |
| Notes: ions / net-ionic | quoted ("turns into ions") | `SO:410–411` |
| Notes: solids / liquids | quoted | `SO:431–432` |
| Table: aqueous, gaseous Q forms | [A][B]/[AB]; P_A·P_B/P_AB | `components/l/equilibrium/solubility/EquationsRecap.tsx` (recap screen, step 5 `SO:416–419`) |
| Table: salt Q | [A⁺][B⁻] | `solubility/EquationPanel.tsx:55–85` (AB struck out from step 6, `SO:254`) |
| CaF₂ question | Ksp = [Ca²⁺][F⁻]² | not in the sim (labelled) |

## Page 8: Solubility Product (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Ksp = 0.1 | `DEFAULT_K = 0.1`, preset `currentK: 0.1` | `SO:55`; `PR:177` |
| 125 mg per shake; 1875 to equilibrium; 2500 max | | `features/lessons/solubility/useSolubilityLessonController.tsx:438–460`; `SO:56–57, 273–279, 494–520, 604–627` |
| Notes: Ksp, solubility product | quoted | `SO:443–445` |
| Notes: higher | quoted | `SO:455–456` |
| Notes: same rate | quoted | `SO:465–467` |
| Notes: 1875 mg | `PHASE_1_DISSOLVE_MAX` in text | `SO:595–597` |
| Notes: capacity / saturated | "reached its capacity" | `SO:640–641`; "saturated" is in `SO:954` |
| Calc: s = √0.1 = 0.316 → 0.32 M | | `SSIM:90–104` with ion1 = ion2 = 0 |
| Table | I 0.00 0.00; C +0.32 +0.32; Eq 0.32 0.32 | `solubility/IceTable.tsx` |
| Graph: Q to K line, flat with extra solid | | `solubility/QTimeGraph.tsx:204–230`; extra solid doesn't change ICE (`SO:183`: ICE uses solid = 100) |
| Question on "maximum amount of ions" | | sim wording `SO:477` |
| FE slider 0–2500, step 125 | | `routes/_authenticated/l/equilibrium/solubility.tsx:248–257` |

## Page 9: Common Ion Effect (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| XB: 4 shakes = 500 mg → [B⁻] = 0.12 | ion2Added = s2/500 × 0.12 | `SO:58, 61, 170`; shake 125 mg `useSolubilityLessonController.tsx:465–475` |
| AB: 1375 mg to equilibrium (11 shakes) | `PHASE_2_SOLID1_MAX` | `SO:59, 281–287` |
| Notes: soluble / common-ion effect / B⁻ | quoted | `SO:688–690` |
| Notes: doesn't (X⁺) | quoted | `SO:704–712` |
| Notes: 1375 / less | quoted | `SO:827–833` |
| Calc: s = 0.2619 → 0.26; [B⁻] 0.3819 → 0.38 | (−0.12 + √0.4144)/2 | `SSIM:90–104` with ion2 = 0.12 |
| Table | I 0.00 0.12; C +0.26 +0.26; Eq 0.26 0.38 | Table tab |
| Question: 17 % drop | (0.3162 − 0.2619)/0.3162 = 0.172 | worked |
| FE: 250 mg common ion → [B⁻]₀ 0.06, s = 0.288 | | `SSIM`; sliders `solubility.tsx:259–280` |

## Page 10: pH Effect (+ Free Explore)

| Item | Answer | Source |
|---|---|---|
| Start (preset) | s1 = 2000, s2 = 500, h = 0 → [A⁺] 0.2619, [B⁻] 0.3819 | `PR:291–298`; `SO:170, 183, 188–195` |
| Each H⁺ shake removes 0.045 M B⁻; max 6; 6th auto-starts dissolving | | `SO:63–64, 188–195, 934–945`; animation `useSolubilityLessonController.tsx:327–392` |
| Notes: H⁺ | quoted | `SO:905–906` |
| Notes: HB(aq) | "to form H{ion2}(aq)" | `SO:907–908` |
| Notes: reducing Q | quoted | `SO:918–921` |
| Notes: saturated / forward | quoted | `SO:953–956` |
| Table: Q after 0–5 shakes | 0.10, 0.088, 0.076, 0.065, 0.053, 0.041 (panel, 2 sf) | 0.2619 × (0.3819 − 0.045h); display check below |
| Calc (a): 0.012/0.26 ≈ 0.045 M | sim constant 0.045 | `SO:63` |
| Calc (b): [B⁻] = 0.112 → 0.11, Q = 0.029 | | worked |
| Calc 2: x = 0.1381; [A⁺] = 0.400, [B⁻] = 0.250 | exact: [A⁺] − [B⁻] = 0.15, product 0.1 → (0.15 + 0.65)/2 = 0.40 | `SSIM:90–107` (solid 100) |
| Graph: U-shaped curve, dot moves left | parabolas, min at pH 8, dot from pH 11 left at constant y | `components/l/equilibrium/solubility/SolubilityPhCurve.tsx:7–27, 55–62`; no tick labels (`:151–159`) → shape only |
| Question | [A⁺] 0.26 → 0.40 | above |
| FE: 1000 mg, 6 additions → solid limited to 0.075 M, all dissolves, Q = 0.063 < Ksp | solid = s1/2000 × 0.15 | `SO:65, 185–187`; sliders `solubility.tsx:283–301` |

## Conclusion and lesson-plan numbers

All reuse the values above (Q = 20, 0.53, 0.029; Kp 10 → 1.0; s 0.32 → 0.26 → 0.40). Exit ticket 1: 0.5²/0.1² = 25 > 10. AP practice (a): 0.25·0.51²/(0.74³·0.36⁴) = 0.0650/0.00681 = 9.55 (rounded data).

---

## Values checked by hand

Python scripts (scratchpad `calc.py`, `disp.py`) re-implemented `SOLV` (bisection), `SSIM` (quadratic), the AirBeaker volume formula, the Kp temperature formula and the 2-sig-fig display. Results:

```
Aqueous A=B=0.30, K=10:           x=0.22792  A=B=0.07208  C=D=0.22792
Le Chatelier preset A=0.30,B=0.26302: eq A=0.08803 B=0.05105 C=D=0.21197 (Q=10.0)
  add C,D to 0.30:                Q=20.03 ; new eq A=0.10873 B=0.07175 C=D=0.27930
FE (0.1,0.1,0.2,0.2): Q=4.0 -> same eq 0.0721/0.2279 ; FE (0.05,0.05,0.25,0.25): Q=25 -> same eq
Gas 3A+4B<=>C+2D, PA=PB=1.5, Kp=10: x=0.27414  A=0.6776 B=0.4034 C=0.2741 D=0.5483
Gas preset PA=1.5,PB=1.376:       A=0.7367 B=0.3583 C=0.2544 D=0.5089 (matches PR:103 exactly)
Piston: L=215.6-86=129.6; V(s)=(1.296 s+60)/124.8 -> s=0:0.4808  s=12:0.6054 (matches PR:151)  s=100:1.5192
Compressed x2.08: 1.5324 0.7452 0.5292 1.0584, Q=0.5343 (=10*2.08^-4) ; eq 1.3077 0.4456 0.6041 1.2082
Expanded x1/1.519: Q=53.27 ; eq 0.5372 0.3055 0.1500 0.3001
Preset V=0.6054 from eq: eq 1.0876 0.4194 0.4634 0.9268 (matches PR:140 exactly)
Temperature K=1.0: eq 1.2386 0.6207 0.4131 0.8261 (x=-0.0503)
Ksp=0.1: s=0.31623 ; with 0.12 B-: s=0.26187, [B-]=0.38187
pH: h=0..6 Q0 = 0.1000 0.0882 0.0764 0.0646 0.0529 0.0411 0.0293 ; h=6 -> x=0.13813, [A+]=0.4000 [B-]=0.2500
FE pH 1000 mg: x=min(0.1381, 0.075)=0.075 -> 0.3369, 0.1869, Q=0.0630
FE common ion 250 mg: [B-]0=0.06, s=0.28765
```

ICE tables at `toFixed(2)` (what the Table tab shows):

```
quotient  I 0.30 0.30 0.00 0.00 | C -0.23 -0.23 +0.23 +0.23 | F 0.07 0.07 0.23 0.23
LeChat-2  I 0.09 0.05 0.30 0.30 | C +0.02 +0.02 -0.02 -0.02 | F 0.11 0.07 0.28 0.28
gas1      I 1.50 1.50 0.00 0.00 | C -0.82 -1.10 +0.27 +0.55 | F 0.68 0.40 0.27 0.55
pressure  I 1.53 0.75 0.53 1.06 | C -0.22 -0.30 +0.07 +0.15 | F 1.31 0.45 0.60 1.21
temp      I 1.09 0.42 0.46 0.93 | C +0.15 +0.20 -0.05 -0.10 | F 1.24 0.62 0.41 0.83
```

Q panel as displayed (emulating `displayNumbers.ts`; 2nd numerator term adjusted):

```
quotient eq   Q 10   (0.23)(0.23)/(0.072)(0.072)
LeChat start  Q 10   (0.21)(0.214)/(0.088)(0.051)     <- D shows 0.214
LeChat added  Q 20   (0.30)(0.30)/(0.088)(0.051)
gas eq        Q 10   (0.27)(0.55)^2/(0.68)^3(0.40)^4
pressure start Q 10  (0.25)(0.522)^2/...              <- P_D shows 0.522 (true 0.509)
pressure comp Q 0.53 (0.53)(1.03)^2/(1.5)^3(0.75)^4    <- P_D 1.03 (true 1.06)
temp eq K=1   Q 1.0  (0.41)(0.79)^2/(1.2)^3(0.62)^4    <- P_D 0.79 (true 0.83)
Ksp water     Q 0.10 (0.32)(0.313)                    <- [B-] 0.313 although [A+]=[B-]
common ion    Q 0.10 (0.26)(0.385)
pH h=0..6     Q 0.10 0.088 0.076 0.065 0.053 0.041 0.029 ; [B-] shown 0.385 0.34 0.292 0.25 0.204 0.158 0.11
pH end        Q 0.10 (0.40)(0.25)
```

Because of the adjusted term, the worksheet takes data from the Table tab, and from the Q panel only for Q itself or for unadjusted terms ([A], [B], [A⁺], P_A, P_B, P_C).

Rounded-value Q checks: 0.28²/(0.11·0.07) = 10.18; 0.27·0.55²/(0.68³·0.40⁴) = 10.15; 0.41·0.83²/(1.24³·0.62⁴) = 1.003; 1.31/0.45/0.60/1.21 → 9.53.

## Sim vs. textbook differences

- Reactions and species are hypothetical (A, B, C, D, AB, XB). K = 10 (aqueous) and Kp = 10 (gaseous) for every reaction; Ksp = 0.1 is orders of magnitude larger than real "slightly soluble" salts.
- No units anywhere in the sim; the worksheet adds M and atm.
- The water-level sliders (aqueous `AqueousBeaker.tsx:139–148`, solubility step 11) are cosmetic. In reality more water dissolves more grams of salt; the sim always dissolves 1875 mg.
- Temperature changes K by a made-up rule, Kp = 10 × 10^(−slider) (`useGaseousLessonController.tsx:531`), not van 't Hoff; there is no temperature value.
- Volume changes scale all partial pressures by 1/V (correct for ideal gases); the volume itself is never displayed.
- The pH effect is modelled as removing a fixed 0.045 M of B⁻ per H⁺ "shake" (`SO:63`). No pH value, no Ka, no HB concentration. The solubility-vs-pH curve is two hand-tuned parabolas with a minimum at pH 8 (`SolubilityPhCurve.tsx:7–17`).
- Only 1:1 salts; no Ksp with powers (e.g. CaF₂).
- Kc and Kp are never linked (no Kp = Kc(RT)^Δn).
- The ICE "x" for the gaseous reactions is a 7th-degree equation; the worksheet gives x and asks students to use the coefficients (AP would not ask students to solve it).
- The mg amounts (1875, 1375) are not proportional to molar solubility (ratio 0.733 vs. 0.828).

## Sim bugs and confusing text (not copied into the worksheet)

1. `GA:886–888`: after raising the temperature the text says "The endothermic reaction will now take place! It is said that the **forward** reaction is being favored." The forward reaction is exothermic (`GA:836`, "+ Heat" on products), K drops, and the sim actually runs the reverse (`GA:904–907`). Worksheet says reverse.
2. `GA:635–645`: when the volume is *increased*, the text still ends "The system will consume moles to relieve pressure." It should produce moles.
3. `GaseousBeaker.tsx:97–104` + `gaseousBeakerSettings.ts:15`: the flame slider handle starts at 0.5 (middle) but the lesson state starts at temperature 0 / Kp = 10 (`PR:152`). Dragging the handle slightly left of where it started (e.g. to 0.45) still lowers Kp and counts as "raised" (≥ 0.40, `GA:30`).
4. Presets on every module boundary (`subUnitTransitions.ts:16–18`): the reaction chosen in Equilibrium (`AQ:218–243`) is reset to reaction 0 in Reaction Quotient, yet step 9 says "You chose a reversible reaction" (`AQ:341`). Le Chatelier starts from [B]₀ = 0.26302 (`PR:45`), not from the student's own run; Pressure and Temperature modules likewise start from saved numbers; the solubility reaction choice (`SO:368`) is reset to AB.
5. `displayNumbers.ts:38–93`: the Q panel adjusts the second product term so the displayed product equals the rounded Q, producing values like [B⁻] = 0.313 next to [A⁺] = 0.32 in pure water, [D] = 0.214 next to [C] = 0.21, P_D = 0.79 where the true value is 0.83.
6. pH module: the Table tab still shows the common-ion ICE values (`solubility/ConcentrationTimeGraph.tsx:326` uses `iceValues`, not `phase3IceValues`), and the red dot on the pH curve moves horizontally at constant "solubility" (`SolubilityPhCurve.tsx:22–27, 55–62`), which visually contradicts "more dissolves".
7. `SO:477`: "Ksp being the maximum amount of ions that can be in a solution" (Ksp is the product of ion concentrations). Used as a question to correct, not copied as fact.
8. `SO:595–597`: "you could only dissolve 1875mg of" + reaction name renders without a space ("1875mg ofAB(s)").
9. `GA:539`: "The reaction will counteract by consuming more moles of gas, or producing fewer moles of gas" (the two halves say the same thing; should be "or producing more"). `GA:691`: missing word ("still lower the equilibrium value"). `AQ:303`: "the the reactants". Missing spaces in solubility strings, e.g. `SO:918–919` ("presence of" + ion name with no space).
10. `components/l/equilibrium/solubility/EquationsRecap.tsx`: recap shows "AB(aq) → A(aq) + B(aq)" with a one-way arrow for an equilibrium.
11. Aqueous Q graph y-range is fixed 0–12 in phases 1 and 3 (`aqueous/QTimeGraph.tsx:456`); the gaseous expanded-volume free explore (Q ≈ 53) and other large Q values need the free-explore auto axis.
12. Rapid shaking can lose increments: `chemicalAdded` animates from a stale `currentConcentration` (`useAqueousLessonController.tsx:493–548`). "Shake until it stops" still ends at the maximum because of the snap at `:501–520`.
13. Equilibrium module (`AQ:199–256`) has no simulation: the beaker and graphs stay empty; it is three text screens and a dropdown.

## AP topics not covered by the sim

- **7.6 Properties of the Equilibrium Constant**: no reversing, scaling or adding reactions. Covered only by a short calc on p. 1 that uses the sim's K = 10, labelled as not shown by the sim.
- **7.14 Free Energy of Dissolution**: nothing on ΔG°, ΔH°/ΔS° of dissolving.
- **7.5 Magnitude of K** (partial): K values are only 10, 1.0 and 0.1; no very large/very small K, no "x is small" approximation.
- **7.13 pH and Solubility** (partial): qualitative only; no pH value, no Ka/Kb link, no hydroxide salts.
- **7.11 Solubility** (partial): only 1:1 salts; no Ksp with exponents, no molar mass → g/L.
- Also missing: Kc ↔ Kp conversion, catalysts and inert-gas addition, Q from moles and volume.
