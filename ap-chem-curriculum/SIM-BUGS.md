# Sim bugs found while writing the worksheets

Collected from each unit's `units/unitN/sources.md` (section "Sim bugs and confusing text"). Each item was found by reading the deployed sim source; none were confirmed in a browser. The worksheets work around all of them. File paths are relative to each sim repo at the commit shown.


## Unit 1: Atomic Structure and Properties — Atomic Structure Sim
Source: chemsims/Unit1ArmarildoSim @ 7d2af55 · served at `/sims/unit1 (topics 1.1–1.8)`

1. Topic 1.3 sample-mass slider rounds each element to 0.1 g on every change, so composition drifts and the empirical formula changes (CHO, CH₃O) — contradicts the step's own "law of definite proportions" message. `T/topic-1-3-elemental-composition/state.ts:112-134, 163-165`.
2. Topic 1.1: equations show "2.00 mol × 6.022 × 10²³ = 1.203 × 10²⁴" because moles/particles use unrounded molar mass while the screen shows rounded values. `T/topic-1-1-moles/components/MolesPanels.tsx:979-992`.
3. Topic 1.6: in overlay mode, ion and neutral peaks are placed at the same x (position chosen per subshell, evenly spaced), so the claimed shift is not visible. `T/topic-1-6-pes/components/PesPanels.tsx:520-545`. Step 2 "Peak position" metric shows raw model numbers (e.g. 2.83). `PesPanels.tsx:1086-1088`.
4. Topic 1.7 step 5: Ar electronegativity shown as "0" (undefined value forced to 0). `T/topic-1-7-periodic-trends/components/PeriodicTrendsPanels.tsx:1550-1561`.
5. Topic 1.8: group pattern text drops the "1" for ±1 charges: "Group 1 metals repeat a + charge pattern." `T/topic-1-8-ionic-compounds/calculations.ts` getGroupPatternText + formatChargeLabel (lines ~328-336, 396-404).
6. Topic 1.3 Free Explore Try-it "Change sample mass while keeping percentages fixed" but Free Explore has no sample-mass control (only element boxes). `ElementalCompositionPanels.tsx:257` vs `:77-79`.
7. Topic 1.5 step 2: "Nuclear charge for comparison" slider silently changes the element (Cl → other atom). `T/topic-1-5-electron-config/state.ts:72-85`. Cl charge buttons offer +1, +5, +7 as "ions". `PT:296`.
8. Topic 1.5: relative pull for Cl's valence shell labelled "weaker" (1.89) while the guide calls Cl's outer shell "almost full"; not wrong, but the label set is arbitrary thresholds. `calculations.ts:192`.
9. Tess's existing worksheet typos ("alaways", "dive", "sheilding"; two pages numbered 6) were not copied.


## Unit 2: Compound Structure and Properties — AP Unit 2 sim
Source: chemtutor-static-tutor public/sims/unit2/index.html · served at `/sims/unit2`

1. **SO₂ expanded-octet structure gets a wrong message** (2273–2275): O=S=O with one lone pair on S passes all checks (10 e⁻ allowed for S, FC sum 0) but matches no `ans`, so the sim says "formal charges are higher than they need to be" — its formal charges are all 0, i.e. lower. Should be accepted (or explained as a resonance/expanded form).
2. **Free Explore gives away the Lewis count** (2029): in `?mode=explore` the valence total is shown before the student counts.
3. **3-D bond-angle arc vs. readout** (1915–1922, 2534–2557): SF₄, ClF₃, BrF₅ arcs show exact 90°/120° while the readout says "slightly less than".
4. **VSEPR predictor accepts the ideal angle** for lone-pair molecules (2400–2405), e.g. 109.5° for H₂O is marked right.
5. **Sea-electron counts differ between screens**: Metals screen puts one electron per core for every metal including Zn (1568–1569); Bonds screen gives Zn²⁺ two (956, 962).
6. **Radius mismatches** between screens (Cu 132 vs. 128 pm, C 76 vs. 77 pm; 675/677 vs. 1709).
7. **Lewis "Show answer"** fills in the full structure and count (2280–2285); not a bug, but it bypasses the worksheet.
8. Lewis step 2 says "Read the counter: 4 of 16 placed" (2609); the counter shows "?" unless the count was checked in step 1 (2183).
9. Energy step 6 mentions F₂ breaking the trend (1746), but F₂ is not in the sim's data (1000–1003); students cannot check it.
10. The Worksheets menu still downloads Tess's older "Molecular Structure" PDFs (197–198); that key lists HCN as nonpolar and square pyramidal as 90°, which disagree with the sim (2459–2465 gives HCN polar; 1891 gives "slightly less than 90°").


## Unit 3: Properties of Substances and Mixtures — Properties of Substances & Mixtures Sim
Source: chemsims/Unit1ArmarildoSim @ 7d2af55 · served at `/sims/unit1 (topics 3.1–3.13)`

- T3.1/calculations.ts:561, 567, 573: shows "deg C" instead of °C; vapor-pressure readout says "higher when boiling point is −161.5 deg C".
- T3.1 Screen 3 default pair (chloromethane + methane) shows Dispersion as dominant (score 4.6 vs 4.3), which reads oddly on a "Dipoles" screen (T3.1/calculations.ts:623-640 default set; scores :306, :342-345).
- T3.1/state.ts:310, 329: Na⁺ and Cl⁻ ions each carry `meltingPointC: 801` (NaCl's melting point assigned to individual ions).
- T3.4/state.ts:579: `setGasPressureUnit` changes only the unit label, not the value (1 atm → 1 kPa). Temperature unit does convert (T3.4/state.ts:715).
- T3.2/calculations.ts:265-313: alloy mechanical values are overridden by generic text ("moderately increased") instead of brass's own "higher than pure copper" (T3.2/state.ts:540-555).
- T3.8/calculations.ts:145-153: entered "formula units at 4 model units" is silently rounded; target 6 at volume 2 shows 3 units.
- T3.9/state.ts:447-470: every reset reshuffles which dye letter is most polar ("sample N"), so class answers differ unless everyone records sample 1.
- T3.10/calculations.ts:136-157: iodine/ethanol is "moderate" (score 3) but iodine/hexane is "appreciable" (score 2) — word order and score order disagree.
- unit.meta.ts description still says "Scaffolded … for later … builds" though all 13 topics are built.


## Unit 4: Chemical Reactions — Chemical Reactions + Redox Reactions Lab
Source: chemical-reactions-webapp @ 73f1deb; unit4-redox-reactions @ 712dc82 · served at `/sims/chemical-reactions, /sims/redox`

1. CR: constants/reactions/balancedReactions.ts:70-71. "Nitrogen Oxidation" (2N₂ + 6H₂O → 4NH₃ + 3O₂) actually reduces N (0 → −3). It is used as a conclusion question instead.
2. CR: BalancedReactionScreen.tsx:273. The formulas are called "Empirical Formulas", but they are molecular formulas (O₂, H₂, N₂).
3. CR: BalancedReactionScreen.tsx:406 says "Choose a Compound", and LimitingReagentScreen.tsx:508 and PrecipitationScreen.tsx:626 say "Choose a Substance". All three menus list reactions.
4. CR: components/balanced-reaction/ReactionDefinition/ReactionDefinition.tsx:203, 224. Each coefficient box turns "correct" as soon as that coefficient matches, which hints at the answer.
5. CR: LimitingReagentScreen.tsx:186-193. The hard-coded "the solid H₂C₂O₄" (and "solid HNO₃") contradicts the (aq) state shown in the equation.
6. CR: useLimitingReagentState.ts:303-317 with ShakingContainer.tsx:117-123. Each click's onPour fires 420 ms later using the click-time molecule count and sets a non-functional `newCounts`, so rapid clicks overwrite each other and lose molecules.
7. CR: useLimitingReagentState.ts:216-224. Mass and yield come only from the "limiting" reactant. In Free Explore, too little NaHCO₃ still gives the full theoretical mass and 98%.
8. CR: LimitingReagentScreen.tsx / ProgressChart.tsx:176-195. The molecule counts are in a screen-reader-only table, so students cannot see the count. The worksheet uses the clicks instead.
9. CR: PrecipitationScreen.tsx:770-776. After reaction 1 (progress 0.5), the Macroscopic label shows productMass × 0.5 = 1.8 g, while the message (:312-340) and the equation box say 3.68 g.
10. CR: usePrecipitationState.ts:369-374 and PrecipitationScreen.tsx (n = 2 × n_MI box). n(PbI₂) = 2 × n(MI), but it should be ½ × n(MI). The PbI₂ molar mass is 334 (precipitationReactions.ts:116). PbI₂ numbers are not used.
11. CR: PrecipitationScreen.tsx:196. "alkaline metal" should be "alkali metal".
12. CR: usePrecipitationState.ts:519-522. The first M₂CO₃ pour has no stoichiometric cap (only the water cap of 40). Adding more M₂CO₃ than CaCl₂ still computes product from M₂CO₃.
13. RX: part3/steps.tsx:149. "You balanced this one in Part 2", but Guided Part 2 (part2/steps.tsx:30-50) never uses femn; only Free Explore does.
14. RX: part1/OxidationLab.tsx:1199-1206. The narration's Rule 5 says "Cl bonded to a metal is −1", but the rule list (:191-195) says "unless bonded to O or F". This is a minor mismatch.
15. RX: part3/TitrationLab.tsx:212-220. In Free Explore, the calculation lines fill in live from the burette reading, so the answer is visible during the titration. This is by design, but it weakens "calculate first".


## Unit 5: Kinetics — Reaction Rates Lab
Source: reactionratewebapp @ dfbe5a5 · served at `/sims/reaction-rates`

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


## Unit 6: Thermochemistry — Thermodynamics Lab, Parts 1–4
Source: thermodynamics @ a905934 (unit9-entropy-9.1) · served at `/sims/thermodynamics?part=1–4`

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


## Unit 7: Equilibrium — Equilibrium Lab
Source: equilibriumweb @ 5dbe7de · served at `/sims/equilibrium`

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


## Unit 8: Acids and Bases — Acids & Bases
Source: acidsbaseschemsimSemetei @ bb81d6b (remove-acids-quizzes-clean) · served at `/sims/acids-bases`

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


## Unit 9: Applications of Thermodynamics — Thermodynamics Lab, Parts 91–94
Source: thermodynamics @ a905934 (unit9-entropy-9.1) · served at `/sims/thermodynamics?part=91–94 (direct link only)`

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
