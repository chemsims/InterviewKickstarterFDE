# Unit 4 Chemical Reactions: where every answer comes from

Two sims, read at their deployed commits:

- **Chemical Reactions** (`/home/user/chemical-reactions-webapp`, commit 73f1deb), referred to below as `CR:` with paths under `src/`.
- **Redox Reactions Lab** (`/home/user/unit4-redox-reactions`, commit 712dc82), referred to below as `RX:` with paths under `src/redox/`.

## Teaching order (worksheet order)

1. Balanced Reactions: atoms are conserved.
2. Limiting Reagent: moles and grams.
3. Precipitation: grams of a solid identify an unknown.
4. Redox Part 1: oxidation numbers classify reactions. It comes after Precipitation because it asks students to classify a precipitation reaction and an acid–base reaction.
5. Redox Part 2: half-reactions and electrons. It also has students balance MnO₄⁻/Fe²⁺, which Part 3 assumes they have done.
6. Redox Part 3: a titration that uses stoichiometry and redox together.

Within each sim, the sections follow the sim's own order: /balanced → /limiting → /precipitation, then ?part=1 → 2 → 3.

## Page 1: Balanced Reactions

| Item | Value | Source |
|---|---|---|
| Menu equations (unbalanced) | CH₄ + O₂ → CO₂ + H₂O, etc. | CR: pages/BalancedReactionScreen/BalancedReactionScreen.tsx:87-99 builds the labels from constants/reactions/balancedReactions.ts:38-93 |
| Coefficients | 1,2,1,2 · 2,2,1 · 1,3,2 · 2,6,4,3 · 4,7,4,6 | CR: constants/reactions/balancedReactions.ts:43-90 |
| Atom totals | C1 H4 O4 · H4 O2 · N2 H6 · N4 H12 O6 · N4 H12 O14 | Worked out from the coefficients and the molecule atoms in CR: helper/chemistry/molecules.ts:3-74 |
| Molecule totals | 3→3, 2→3, 4→2, 8→7, 11→10 | Sums of the coefficients |
| "reactants" / "products" | message text | CR: BalancedReactionScreen.tsx:268-271 |
| "Stoichiometric Coefficients … how many molecules" | message text | CR: BalancedReactionScreen.tsx:309-311 |
| "balanced … same amount of atoms on each side" | message text | CR: BalancedReactionScreen.tsx:315-318 |
| One scale per element; green check when balanced | scales | CR: BalancedReactionScreen.tsx:415-427; components/balanced-reaction/Scales/Scales.tsx:351-367; balancer `atomIsBalanced` at helper/chemistry/reactionBalancer.ts:61-65 |
| "could be smaller" | multiple-of-balanced message | CR: pages/BalancedReactionScreen/hooks/useBalancedReactionState.ts:281-287 |
| Only whole molecules can be added | molecule grid / beakers | CR: reactionBalancer.ts:17-35 |
| Demo step 9 (doubling) message | same as above | useBalancedReactionState.ts:282-287. It shows only in Guided mode; Free Explore uses the text at BalancedReactionScreen.tsx:249-256 |

## Page 2: Limiting Reagent

Setup facts:

- Each click adds 5 molecules: CR: pages/LimitingReagentScreen/LimitingReagentScreen.tsx:86-92.
- Guided mode advances at 12 or more molecules, so 3 clicks give 15: CR: pages/LimitingReagentScreen/hooks/useLimitingReagentState.ts:59, 320-323.
- Volume = 0.1 + (level − 0.1)/0.9 × 0.6 L, so the top of the slider is 0.70 L and the default (level 0.5) is 0.37 L: useLimitingReagentState.ts:62-76, 186. The label is shown with toFixed(2): LimitingReagentScreen.tsx:543 (formatValue).
- Molarity = count/190: useLimitingReagentState.ts:203-207. Moles = V × M: line 209. Excess needed = coefficient × n: lines 211-214. Theoretical mass = n × MM: lines 216-219. Actual mass = theoretical × yield: lines 221-224. Yield %: lines 226-229.
- Reaction constants: 2 NaHCO₃ (84), Na₂C₂O₄ 134, yield 0.98; NaOH 1 (40), NaNO₃ 85, yield 0.96: CR: constants/reactions/limitingReagentReactions.ts:13-56.
- Equation order shown, e.g. 2NaHCO₃(s) + H₂C₂O₄(aq) → 2H₂O(l) + 2CO₂(g) + Na₂C₂O₄(aq): LimitingReagentScreen.tsx:1-40 (buildReactionSegments).
- Displayed rounding: toFixed(2) for M, V, n, needed, masses and toFixed(0) for yield: LimitingReagentScreen.tsx:215-311. The equation panel uses the same values: components/limiting-reagent/LimitingEquationView/LimitingEquationView.tsx (fmt 2 decimals).

| Item | Value (15 molecules, 0.70 L) | Source / arithmetic |
|---|---|---|
| M | 15/190 = 0.0789 → shown 0.08 | above |
| n limiting | 0.70 × 0.078947 = 0.05526 → 0.06 | |
| NaHCO₃ needed | 2 × 0.05526 = 0.1105 → 0.11 | |
| Na₂C₂O₄ theoretical | 0.05526 × 134 = 7.405 → 7.41 g | |
| actual | 7.405 × 0.98 = 7.257 → 7.26 g; yield 98% | |
| NaOH needed | 0.05526 → 0.06 | |
| NaNO₃ theoretical | 0.05526 × 85 = 4.697 → 4.70 g | |
| actual | × 0.96 = 4.509 → 4.51 g; 4.51/4.70 = 96% | |

Notes text sources:

- "Stoichiometry": LimitingReagentScreen.tsx:128-131.
- aqueous / dissolved in water: lines 141-151.
- 6.02214076×10²³, Avogadro: lines 157-161.
- Molarity, mol/L: lines 201-208.
- Moles = V x M: line 229.
- Yield Percentage, Actual / Theoretical: lines 300-311.
- Limiting Reagent / Excess Reactant: lines 333-348.
- "accumulating … not taking place": line 329.

The 30-molecule early finisher gives 0.7 × 30/190 × 134 = 14.81 g. Free Explore allows up to 30 molecules (useLimitingReagentState.ts:60, 282-283).

## Page 3: Precipitation

Setup facts:

- Each pour adds 5 molecules: CR: pages/PrecipitationScreen/PrecipitationScreen.tsx:657, 697.
- Two-tap pour (the first click only picks the shaker up): lines 666, 706; components/shared/ShakingContainer/ShakingContainer.tsx:111-115.
- The CaCl₂ tooltip shows "N molecules": PrecipitationScreen.tsx:662.
- The "(X g) added" label: line 637.
- Volume = waterLevel, clamped to 0.3–0.7: pages/PrecipitationScreen/hooks/usePrecipitationState.ts:130-132, 343. The slider shows toFixed(3) (FillableBeaker default formatValue, components/shared/Beaker/FillableBeaker.tsx:134).
- M = count/190: usePrecipitationState.ts:350-353. n = V × M: lines 355-363. Grams of unknown = n × MM: lines 365-367. n(product) = coefficient × n(unknown): lines 369-374. Product mass: lines 376-380.
- Metal molar masses: Na 23, Li 7, K 39 (helper/chemistry/types.ts:167-171). The anion parts are 60 (CO₃) and 127 (I), with M₂ vs M: constants/reactions/precipitationReactions.ts:15-50; helper/chemistry/molarMass.ts:3-6. The metal table columns are "Compound | Molar Mass (g/mol)": components/precipitation/MetalTable/MetalTable.tsx:20-41.
- Metal is random: usePrecipitationState.ts:446 (selectReaction → getRandomMetal).
- Second pour is capped at unknown + 1 × round(20 × 0.5) = 20 total: usePrecipitationState.ts:519-531.

| Item | Value | Arithmetic |
|---|---|---|
| n(CaCl₂) | 0.7 × 20/190 = 0.0737 → 0.07 | |
| n(M₂CO₃) | 0.7 × 10/190 = 0.03684 | |
| grams M₂CO₃ | Na 106 → 3.905 → 3.91 · Li 74 → 2.726 → 2.73 · K 138 → 5.084 → 5.08 | |
| CaCO₃ | 0.03684 × 100 = 3.684 → 3.68 g | equation box: PrecipitationScreen.tsx:961-967 |
| student MM | 3.91/0.0368 = 106.2 · 2.73/0.0368 = 74.2 · 5.08/0.0368 = 138.0 | |
| after second pour | 0.7 × 20/190 × 100 = 7.37 g; label 7.4 g | label: PrecipitationScreen.tsx:770-776 |
| MI molar mass | Na 150, Li 134, K 166 | 127 + M |
| MI grams (10 molecules) | 5.53, 4.94, 6.12 → ÷ 0.0368 = 150.3, 134.2, 166.3 | |
| early finisher (15 M₂CO₃) | 0.7 × 15/190 × 100 = 5.53 g | |

Notes text sources:

- "solid (s)": PrecipitationScreen.tsx:175-177.
- "M is not a real element … 3 components": line 196.
- "filter and weigh": line 465.

The net ionic equation is not shown in the sim. Students write it from the sim's equation (AP 4.2).

## Page 4: Redox Part 1

- Oxidation numbers for every species: RX: chem/oxidation.ts:54-121.
- Ion challenges (MnO₄⁻ +7, Cr₂O₇²⁻ +6, H₂O₂ O −1): chem/oxidation.ts:124-137.
- Electron tally: chem/oxidation.ts:246-254. Zn: 2/2. CH₄: C 8 × 1 = 8 lost and O 2 × 4 = 8 gained. AgCl and HCl: 0/0.
- Classes (redox / precipitation / acidbase): chem/oxidation.ts:58, 78, 97.
- Notes text: "charge … ionic" at part1/OxidationLab.tsx:1081-1082. The rules list is at :172-196, and the narration rules at :1089, 1099, 1150. "oxidized / OIL RIG" is at :1115-1124. "always equal" is at :1140. "Every combustion reaction is a redox reaction" is at :1180.
- Calc: the Rule 4 sums are at narration :1159-1171 (C + 4(+1) = 0, C + 2(−2) = 0). The 4 O atoms come from the exercise at :134-145. N = +5 is at oxidation.ts:81.
- Precipitation and acid–base reasoning: OxidationLab.tsx:1208-1240.

## Page 5: Redox Part 2

- Half-reactions and electrons: RX: chem/halfReactions.ts:127-271.
- Lowest multipliers: :294-297. The guided reactions are zncu ×1/×1 (2 e⁻), cuag ×1/×2 (2 e⁻) and alcu ×2/×3 (6 e⁻). In femn, ox ×5 and red ×1 give 5 e⁻.
- Net equation order (ox left terms, then red left terms): :315-320. This gives 5Fe²⁺ + MnO₄⁻ + 8H⁺ → 5Fe³⁺ + Mn²⁺ + 4H₂O.
- Counts at 100 % use defaultEvents (8, 6, 4): :151, 178, 204. The model is eventModel :375-384 and stageCounts :424-444, labelled in part2/HalfReactionLab.tsx:90-110.
  - zncu: 8 Cu²⁺ (0 of 8 left), 8 Zn²⁺, 8 Cu, 16 e⁻.
  - cuag: redIn = 2 per event, so 12 Ag⁺; 6 Cu²⁺; 12 Ag; 12 e⁻.
  - alcu: 3 × 4 = 12 Cu²⁺; 2 × 4 = 8 Al³⁺; 12 Cu; 6 × 4 = 24 e⁻.
- Notes text in part2/steps.tsx: spectator ions :126-130, net ionic :135, product/reactant :146-156, coefficient :221, atoms and charge :228-231. The charge check for Al is at :271-272; for Ag⁺ it is at :228-231.
- Blue fade: :181-190. Blue Cu²⁺ formed (Cu + Ag⁺): :244-245.
- Free Explore picker includes femn: HalfReactionLab.tsx:416-428.

## Page 6: Redox Part 3

- Guided setup: 25.00 mL, 0.0200 M, endpoint 20.00 mL (400 drops). Sources: RX: chem/titration.ts:319-324 and part3/steps.tsx:26, 140-142.
- 1 drop = 0.05 mL: chem/titration.ts:7-8 and part3/TitrationLab.tsx:502.
- Endpoint = floor(equivalence drops) + 1: chem/titration.ts:155-157. The hidden concentration is set so the endpoint is exact: :302-311.
- Guided calculation: 0.0200 × 0.02000 = 4.00×10⁻⁴; × 5 = 2.00×10⁻³; ÷ 0.02500 = 0.0800 M (steps.tsx:206-245).
- Distractors: 0.0444 M is 2.00×10⁻³ / 0.045 (steps.tsx:109-116).
- Free Explore default samples (defaultEndpointMl): Fe 16, oxalic 25, peroxide 17.5 (titration.ts:65, 81, 94). The defaults are 0.02 M titrant and 25 mL sample (TitrationLab.tsx:82-83).
  - Oxalic: 0.0200 × 0.02500 = 5.00×10⁻⁴ × 5/2 = 1.25×10⁻³ / 0.025 = 0.0500 M.
  - Peroxide: 3.50×10⁻⁴ × 5/2 = 8.75×10⁻⁴ / 0.025 = 0.0350 M.
  - Show answer gives toFixed(4) of 0.04999 → 0.0500 and of 0.03499 → 0.0350.
- Ratios: Fe 5:1, oxalic 5:2, peroxide 5:2 (titration.ts:58-95).
- Notes text in part3/steps.tsx: titration :132, analyte and titrant :141-142, five Fe²⁺ and 5:1 :151, equivalence point and endpoint :182-184.
- Overshoot "too high": TitrationLab.tsx:270-278.
- Chart axes are "KMnO₄ added (mL)" and "moles in flask", with no numbers on the y axis: part3/TitrationChart.tsx:33, 109-120. The graph item asks for shape only.

## Conclusion and AP practice

- Conclusion 1: N 0 → −3 with 4 atoms, so 12 e⁻ gained. O −2 → 0 with 6 atoms, so 12 e⁻ lost.
- Conclusion 2: C in H₂C₂O₄ = (0 − 2 + 8)/2 = +3; C in HCO₃⁻ = +4 and stays +4 in CO₂; C₂O₄²⁻ is still +3. With MnO₄⁻, C goes +3 → +4 and Mn goes +7 → +2.
- MCQ: 0.0200 × 0.016 × 5 / 0.025 = 0.0640 M. Distractor (A): 3.2×10⁻⁴ / 0.025 = 0.0128.

## Values checked by hand (python)

```
lv(0.5)=0.3667 L; 15/190=0.078947; 0.7*0.078947=0.055263; *2=0.110526; *134=7.4053; *0.98=7.2572
*85=4.6974; *0.96=4.5095; 4.51/4.70=0.9596; 7.26/7.41=0.9798; 0.7*30/190*134=14.8105
0.7*20/190=0.073684; 0.7*10/190=0.036842; *106=3.9053; *74=2.7263; *138=5.0842; *100=3.6842
3.91/0.0368=106.25; 2.73/0.0368=74.18; 5.08/0.0368=138.04; 0.7*20/190*100=7.3684
MI: *150=5.53, *134=4.94, *166=6.12 -> /0.0368 = 150.3, 134.2, 166.3; 0.7*15/190*100=5.526
titration: unknown(fe,20)=0.07998 -> endpoint drop 400; ox 25 mL -> 0.04999 (500 drops); per 17.5 -> 0.03499 (350 drops); fe 16 -> 0.06398 (320)
0.02*0.02=4e-4; *5=2e-3; /0.025=0.08; 2e-3/0.045=0.0444; 0.0128 MCQ distractor
```

## Sim vs. textbook differences

- In Limiting Reagent and Precipitation, molarity is molecules ÷ 190 (the beaker grid). Molarity does not depend on the volume; only moles change with V. In a real solution, the same amount of solute in more water gives a lower M.
- Limiting Reagent yields are fixed constants (98%, 96%). There is no chemistry behind them.
- The sim's PbI₂ molar mass is 334 g/mol; the real value is 461 g/mol.
- Precipitation uses round molar masses (Na 23, Li 7, K 39; CaCO₃ 100). The worksheet uses these.
- Precipitation's minimum volume is 0.3 L (iOS used 0.1 L): usePrecipitationState.ts:124-132.

## Sim bugs and confusing text (not copied into the worksheet)

1. CR: constants/reactions/balancedReactions.ts:70-71. "Nitrogen Oxidation" (2N₂ + 6H₂O → 4NH₃ + 3O₂) actually reduces N (0 → −3). It is used as a conclusion question instead.
2. CR: BalancedReactionScreen.tsx:273. The formulas are called "Empirical Formulas", but they are molecular formulas (O₂, H₂, N₂).
3. CR: BalancedReactionScreen.tsx:406 says "Choose a Compound", and LimitingReagentScreen.tsx:508 and PrecipitationScreen.tsx:626 say "Choose a Substance". All three menus list reactions.
4. CR: components/balanced-reaction/ReactionDefinition/ReactionDefinition.tsx:200-201. Each coefficient box turns "correct" as soon as that coefficient matches, which hints at the answer.
5. CR: LimitingReagentScreen.tsx:186-193. The hard-coded "the solid H₂C₂O₄" (and "solid HNO₃") contradicts the (aq) state shown in the equation.
6. CR: useLimitingReagentState.ts:303-317 with ShakingContainer.tsx:117-123. Each click's onPour fires 420 ms later using the click-time molecule count and sets a non-functional `newCounts`, so rapid clicks overwrite each other and lose molecules.
7. CR: useLimitingReagentState.ts:216-224. Mass and yield come only from the "limiting" reactant. In Free Explore, too little NaHCO₃ still gives the full theoretical mass and 98%.
8. CR: LimitingReagentScreen.tsx / ProgressChart.tsx:163-178. The molecule counts are in a screen-reader-only table, so students cannot see the count. The worksheet uses the clicks instead.
9. CR: PrecipitationScreen.tsx:770-776. After reaction 1 (progress 0.5), the Macroscopic label shows productMass × 0.5 = 1.8 g, while the message (:312-340) and the equation box say 3.68 g.
10. CR: usePrecipitationState.ts:369-374 and PrecipitationScreen.tsx (n = 2 × n_MI box). n(PbI₂) = 2 × n(MI), but it should be ½ × n(MI). The PbI₂ molar mass is 334 (precipitationReactions.ts:116). PbI₂ numbers are not used.
11. CR: PrecipitationScreen.tsx:196. "alkaline metal" should be "alkali metal".
12. CR: usePrecipitationState.ts:493-497. The first M₂CO₃ pour has no stoichiometric cap (only the water cap of 40). Adding more M₂CO₃ than CaCl₂ still computes product from M₂CO₃.
13. RX: part3/steps.tsx:149. "You balanced this one in Part 2", but Guided Part 2 (part2/steps.tsx:30-50) never uses femn; only Free Explore does.
14. RX: part1/OxidationLab.tsx:1203-1206. The narration's Rule 5 says "Cl bonded to a metal is −1", but the rule list (:191-195) says "unless bonded to O or F". This is a minor mismatch.
15. RX: part3/TitrationLab.tsx:215-220. In Free Explore, the calculation lines fill in live from the burette reading, so the answer is visible during the titration. This is by design, but it weakens "calculate first".

## AP topics not covered by the sim

- **4.4 Physical and Chemical Changes:** not covered at all.
- **4.8 Introduction to Acid–Base Reactions:** only classification (HCl + NaOH in Part 1) and neutralization stoichiometry (HNO₃ + NaOH in Limiting Reagent). The sims have no Brønsted–Lowry proton-transfer treatment, conjugate pairs or amphoteric water.
- **4.6 Introduction to Titration:** only redox titration. There is no acid–base titration, indicator or pH curve.
- **4.2 Net Ionic Equations:** shown only for redox (Part 2). The Chemical Reactions screens show molecular equations; students write the precipitation net ionic equation themselves.
- **4.1 Introduction for Reactions:** evidence of reaction (precipitate, color change, gas) appears, but it is not discussed as a topic.
