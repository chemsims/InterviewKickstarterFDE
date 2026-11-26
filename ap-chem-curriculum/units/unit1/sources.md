# Unit 1 Atomic Structure and Properties: sources

Sim: "Atomic Structure Sim" (chemsims.app/sims/unit1), deployed commit `7d2af55`, checkout `/home/user/unit1armarildosim`.
All paths below are relative to `src/`. `T` = `units/unit-1-atomic-structure/topics`. `PT` = `domain/chemistry/periodic-table.ts`.

Shared: atomic masses H 1.008 (PT:37), C 12.011 (PT:116), N 14.007 (PT:132), O 15.999 (PT:148), Na 22.99 (PT:195), Mg 24.305 (PT:211), Al 26.982 (PT:227), Cl 35.45 (PT:291), K 39.098 (PT:322). Avogadro 6.02214076e23 (`domain/chemistry/constants.ts:1`), displayed as 6.022 × 10²³. Subshell capacities s2 p6 d10 f14 (`constants.ts`, `SUBSHELL_CAPACITIES`). Step navigation buttons "Next"/"Previous"/"Start Free Explore" (`shared/components/SimulationShell/SimulationFooter.tsx:69-112`).

## Topic 1.1 Moles and Molar Mass (`T/topic-1-1-moles`)
| Item | Value | Source |
|---|---|---|
| Default substance / mass | H₂O, mass = one molar mass (18.015 g, shown 18.0 g) | `state.ts:264-279`, display `components/MolesPanels.tsx:141,193` (1 dp) |
| Mass range | 0 to 2 × M (H₂O 0–36.0 g), step 0.1; ± buttons 1.0 g | `state.ts:281-289`, `MolesPanels.tsx:613-662` |
| Substance resets mass | selecting a substance sets mass = M | `GuidedSimulation.tsx:416-431` |
| Mass control only on step 6 | `interactive={isInteractiveStep}` | `GuidedSimulation.tsx:491-498` |
| Equations n = m/M, N = n × Nₐ, Nₐ = 6.022 × 10²³ mol⁻¹ | | `MolesPanels.tsx:926-944` |
| Notes: "We measure mass, then use the mole to connect mass to amount of substance" | mass / mole | `MolesPanels.tsx:1034-1037` |
| "The molar mass tells how many grams correspond to one mole" | molar mass / one | `MolesPanels.tsx:1046` |
| "To find moles, divide the sample mass by the molar mass" | divide / molar mass | `MolesPanels.tsx:1059` |
| "One mole always contains 6.022 × 10²³ particles" | | `MolesPanels.tsx:1071` |
| "Each factor cancels the previous unit…" | cancels | `MolesPanels.tsx:1082` |
| NaCl in "formula units", H₂O "molecules" | | `state.ts:206-254` (`particleTerm`) |
| Step 2 table: "2 x 1.0", "16.0", total 18.0 g mol⁻¹ | | `MolesPanels.tsx:405-423` (atomic masses to 1 dp) |
| Calc 1 / step 3: 18.0 g ÷ 18.0 = 1.00 mol | sim 18.015/18.015 = 1.00 | `calculations.ts:308-323`, `MolesPanels.tsx:962-976` |
| Step 6 rows | H₂O 18.0 g: 18.0, 1.00, 6.022 × 10²³; H₂O 36.0 g: 2.00 mol, 1.203 × 10²⁴; NaCl 36.0 g: 58.4, 0.62, 3.71 × 10²³ formula units | worked from constants; display 4 s.f., max 3 decimals (`shared/components/science/scientific-format.ts:105-130`) |
| Try-it prompts | CO₂ one molar mass; double mass; equal masses H₂O/NaCl | `MolesPanels.tsx:361-378` |

## Topic 1.2 Mass Spectra (`T/topic-1-2-mass-spectra`)
| Item | Value | Source |
|---|---|---|
| Isotope data | Ne 19.992/20.994/21.991 at 90.48/0.27/9.25 %; Mg 23.985/24.986/25.983 at 78.99/10.0/11.01; B 10.013/11.009 at 19.9/80.1; Si 27.977/28.976/29.974 at 92.23/4.67/3.1 | `domain/chemistry/isotopes.ts:8-28` |
| Default element Ne; element buttons only on step 6 | | `state.ts:18`, `components/MassSpectraPanels.tsx:79-89` |
| Slider renormalizes others to 100 % | | `state.ts:64-99` |
| Abundance shown 1 dp, fraction 4 dp (zeros stripped), contributions 3 dp | 90.5/0.3/9.3; 0.9048/0.0027/0.0925; 18.089/0.057/2.034 | `calculations.ts:178-188`, `MassSpectraPanels.tsx:184-193, 440-455` |
| Peak at m/z = mass number | 20, 21, 22 | `MassSpectraPanels.tsx:145-150` |
| Relative abundance = amount of one isotope ÷ total amount × 100 | | `MassSpectraPanels.tsx:160-173` |
| Average = Σ(mᵢ × fᵢ), Ne 20.180 amu | | `MassSpectraPanels.tsx:495-541`, `domain/chemistry/isotopes.ts:43-50` |
| Notes text (isotopes; different m/z; m/z ≈ isotope mass; tallest = most abundant; weighted average; not whole number) | | `MassSpectraPanels.tsx:135, 176, 581-611` |
| Step 6 averages | Ne 20.180, Mg 24.305, B 10.811 (Si 28.086) | worked from isotopes.ts |
| Dominant isotope | ²⁰Ne, ²⁴Mg, ¹¹B | `calculations.ts:151` |
| y-axis 0–100 % relative abundance (to scale), x = m/z | | `shared/components/charts/MassSpectrumChart.tsx:49-52, 195-205` |
| Try-it prompts | | `MassSpectraPanels.tsx:223-235` |

## Topic 1.3 Elemental Composition (`T/topic-1-3-elemental-composition`)
| Item | Value | Source |
|---|---|---|
| Molecular example CH₂O: C 40.0, H 6.7, O 53.3 g; formula-unit example Mg 60.3, O 39.7 g | | `state.ts:47-72` |
| Mode toggle "Molecular"/"Formula unit" resets example | | `state.ts:136-145`, `ElementalCompositionPanels.tsx:1085-1110` |
| Sample-mass slider 1–200 g, rescale + round to 0.1 g | | `state.ts:112-134, 155-165`, `ElementalCompositionPanels.tsx:380-405` |
| Equations: % by mass; mass = %/100 × total; n = m/M; ratio = moles ÷ smallest | | `ElementalCompositionPanels.tsx:1204-1262` |
| Notes text | definite proportions; 100.0 g; convert to moles; smallest; lowest whole-number; molecular molar mass; formula units | `ElementalCompositionPanels.tsx:159, 204, 749-750, 1386-1438` |
| Table: moles 3.33/6.65/3.33; ratios 1.00/2.00/1.00 → CH₂O | | `domain/chemistry/empirical-formula.ts:51-107`; display `calculations.ts:301-319` |
| Glucose: 180.16 g/mol, EFM 30.026, "6.00 rounds to 6", C₆H₁₂O₆ | | `calculations.ts:228-232, 328-355`, `ElementalCompositionPanels.tsx:711-738` |
| MgO: 2.48 / 2.48 mol → 1:1 | | worked from PT |
| Free Explore element boxes 0.1–200 g, "Reset to Example" | | `ElementalCompositionPanels.tsx:509-545` |

## Topic 1.4 Mixtures (`T/topic-1-4-mixtures`)
| Item | Value | Source |
|---|---|---|
| Atomic masses C = 12, O = 16 on this topic | M(CO) 28.00, M(CO₂) 44.00 | `calculations.ts:95-98, 242-267` |
| Default CO 14 g, CO₂ 22 g ("50-50 mol example"); presets Pure CO 36/0, Pure CO₂ 0/36, Mystery 9/27 | | `state.ts:47-92` |
| Step 1 shows CO only | `includeSecondComponent: stepIndex > 0` | `GuidedSimulation.tsx:44-47` |
| Mass fractions: CO 42.9 % C / 57.1 % O; CO₂ 27.3 % C / 72.7 % O | | `MixturePanels.tsx:1070-1087` |
| Contributions 6.0/8.0/6.0/16.0 g; totals 12.0 C, 24.0 O; 36.0 g | | `MixturePanels.tsx:1090-1113, 1140-1158` |
| %C 33.3, %O 66.7 | | `MixturePanels.tsx:1116-1133` |
| f(CO₂) 0.611, Likely composition 38.9 : 61.1 | | `calculations.ts:313-373`, `MixturePanels.tsx:1173-1235` |
| Mystery: 31.2 % C, 68.8 % O, 25.0 : 75.0; "Is the sample pure? No" | | worked from constants; `MixturePanels.tsx:1159-1163` |
| Notes text (one kind of molecule; fixed composition; mixture; vary; twice, 32 g O, Law of Multiple Proportions; intermediate) | | `MixturePanels.tsx:1307-1360` |

## Topic 1.5 Electron Configuration (`T/topic-1-5-electron-config`)
| Item | Value | Source |
|---|---|---|
| Default Cl, distance 3, comparison charge 17 | | `state.ts:17-25` |
| Nuclear-charge slider changes the element | | `state.ts:72-85` |
| Relative pull = Z / n², labels strong ≥7, moderate ≥2.5, else weaker | 17.00/4.25/1.89 | `calculations.ts:167, 192`; display `ElectronConfigPanels.tsx:134-180` |
| Rules Z = protons, e⁻ = p⁺, nucleus = p⁺ + n⁰, F ∝ q₁q₂/r² | | `ElectronConfigPanels.tsx:271-290` |
| Guide text (proton count; opposite charges attract; closer; subshells; Aufbau lowest; superscript; core inner / valence highest occupied; proton count stays) | | `ElectronConfigPanels.tsx:32-75` |
| Neutrons = round(atomic mass) − Z | Cl 18, Mg 12, S 16 | `calculations.ts:183`, shown `ElectronConfigPanels.tsx:988` |
| Valence = electrons in highest n | Cl 7, Cl⁻ 8, Mg 2, S 6 | `domain/chemistry/electron-config.ts:85-99` |
| Configurations | Aufbau fill | `electron-config.ts:43-78`, `constants.ts` AUFBAU_ORDER |
| Charge options (Cl: −1, +1, +5, +7) | | `state.ts:87-98`, PT:296 |
| Try-it (Mg²⁺, S valence, 1s²…3p⁵) | | `ElectronConfigPanels.tsx:77-83, 400-412` |

## Topic 1.6 PES (`T/topic-1-6-pes`)
| Item | Value | Source |
|---|---|---|
| Species Na, Na⁺, Mg, Mg²⁺, Al, Ne; default Na | | `state.ts:19-37`; selector always visible `PesPanels.tsx:105` |
| Peak height = electron count | | `domain/chemistry/pes.ts:19-28` |
| Binding energy model Z/n² + offset; ions × (1 + 0.1·charge) | (not used for answers) | `pes.ts:62-65`, `calculations.ts:217-224` |
| Peak list, tallest, lowest/highest binding | Na 1s,2s,2p,3s (4, 2p, 3s); Na⁺ 1s,2s,2p (3, 2p, 2p); Mg 4, 2p, 3s; Al 5, 2p, 3p; Ne 3, 2p, 2p | `calculations.ts:70-129`; Live Summary `PesPanels.tsx:1151-1161` |
| "3 peaks higher" ion shift for Na⁺ | | `calculations.ts:124-127`, `PesPanels.tsx:1141-1143` |
| Rules atom + hν → ion + e⁻; E_B = energy required to remove an electron | | `PesPanels.tsx:212-219` |
| Guide text (energy pattern; arranged/interact; peak per subshell; height; position/remove; inner more strongly; 3s removed, less shielding, higher) | | `PesPanels.tsx:34-72` |
| Axis "Higher binding energy" arrow to the left, "Relative intensity" | | `PesPanels.tsx:426-444` |
| Challenge prompts | | `PesPanels.tsx:322-327` |

## Topic 1.7 Periodic Trends (`T/topic-1-7-periodic-trends`)
| Item | Value | Source |
|---|---|---|
| Paths Across Period 3 / Down Group 1 / Down Group 17; default Na, compare Na/Mg/Cl | | `state.ts:28-65` |
| Zeff = Z − core (= valence for neutral main-group) | Na 1, Mg 2, Al 3, P 5, S 6, Cl 7 | `calculations.ts:221-243`; shown `PeriodicTrendsPanels.tsx:267-271, 704-731` |
| Radius (pm) | Na 190, Mg 145, Al 118, P 98, S 88, Cl 79 | PT:203, 219, 235, 267, 283, 299 |
| First IE (kJ/mol) | 496, 738, 578, 1012, 1000, 1251 | PT:204, 220, 236, 268, 284, 300 |
| EA (kJ/mol, rounded) | 53, 0, 42, 72, 200, 349 | PT:205, 221, 237, 269, 285, 301; rounding `calculations.ts` formatPropertyValue |
| Electronegativity | 0.93, 1.31, 1.61, 2.19, 2.58, 3.16 | PT:202, 218, 234, 266, 282, 298 |
| Ionic radii | Na⁺ 102, Mg²⁺ 72, Cl⁻ 181 (also Al³⁺ 54, S²⁻ 184, P³⁻ 212, Li⁺ 76, K⁺ 138, F⁻ 133, Br⁻ 196) | `calculations.ts:139-150` |
| Property preview on step 1 (radius, IE, EN) | | `PeriodicTrendsPanels.tsx:404-431` |
| Guide text (Zeff ≈ nuclear − shielding; protons increase; closer/smaller; shrink/expand; remove; added electron / bond; stronger) | | `PeriodicTrendsPanels.tsx:55-93` |
| Equations Zeff ≈ Z − S; M(g) → M⁺(g) + e⁻; X(g) + e⁻ → X⁻(g) | | `PeriodicTrendsPanels.tsx:515-605` |
| Try-it challenges (Cl, F, K) | | `calculations.ts:152-179`, `PeriodicTrendsPanels.tsx:667-694` |

## Topic 1.8 Ionic Compounds (`T/topic-1-8-ionic-compounds`)
| Item | Value | Source |
|---|---|---|
| Default Na + Cl; metals Li Na K Mg Ca Al; nonmetals F Cl Br O S N P; Al–Cl, Al–Br blocked | | `state.ts:23-49, 116-118` |
| Charges = first common ion | Na⁺, Mg²⁺, Al³⁺, Ca²⁺, Cl⁻, O²⁻, N³⁻ | `domain/chemistry/ionic-compounds.ts:29-53`, PT commonIonCharges |
| Ratio by LCM, formula, name | NaCl 1:1, MgCl₂ 1:2, Na₂O 2:1, Al₂O₃ 2:3, Ca₃N₂ 3:2; names from ANION_NAMES | `ionic-compounds.ts:18-27, 79-118` |
| Electrons transferred = total + charge (Al₂O₃: 6) | | `calculations.ts` analyzeIonicCompounds (`electronTransferCount = totalPositiveCharge`) |
| Guide text (outer/reactivity; attraction/nuclei; left/losing; right/gaining; positive/negative; neutral/equal; formula; same column) | | `components/IonicCompoundPanels.tsx:48-86` |
| Analogous LiCl/NaCl/KCl; most reactive metal = lowest IE (K 419); strongest nonmetal = highest EN | | `calculations.ts` buildAnalogousCompounds, getMostReactiveMetal; PT:331 |

## Values checked by hand (python, scripts in scratchpad `u1/verify.py`, `u1/verify2.py`)
- M(H₂O) = 2(1.008) + 15.999 = 18.015; 36.0/18.015 = 1.9983 → 2.00 mol; × 6.02214076e23 = 1.2034e24 → "1.203 × 10²⁴" (student 2.00 × 6.022e23 = 1.204e24).
- M(NaCl) = 58.44; 36.0/58.44 = 0.6160 → 0.62; × NA = 3.710e23 → "3.71 × 10²³"; student 36.0/58.4 × 6.022e23 = 3.712e23 → 3.71.
- 9.0 g H₂O → 0.4996 mol → 3.009e23 (exit ticket).
- Ne: 19.992(0.9048) + 20.994(0.0027) + 21.991(0.0925) = 18.089 + 0.057 + 2.034 = 20.180. Mg 24.305; B 1.993 + 8.818 = 10.811; Si 28.086. Equal B: (10.013 + 11.009)/2 = 10.511. Equal Mg thirds: 24.985.
- JS toFixed(9.25, 1) = "9.3" (exact binary tie rounds up), 0.27 → "0.3", 90.48 → "90.5".
- CH₂O: 40.0/12.011 = 3.3303; 6.7/1.008 = 6.6468; 53.3/15.999 = 3.3315; ratios 1.000/1.996/1.000. EFM = 30.026; 180.16/30.026 = 6.0001.
- MgO: 60.3/24.305 = 2.4810; 39.7/15.999 = 2.4814.
- Slider drift (re-implemented `scaleCompositionToSampleMass`): drag 100 → 50 g one step at a time gives C 20.0, H 2.5, O 27.5 (H 5.0 %), formula CHO; drag to 200 g gives C 80.0, H 16.7, O 103.3, formula CH₃O; typing "50" (passes 5 g) gives H 6.0 %.
- Mixture 14/22 g: C 6.0 + 6.0 = 12.0; O 8.0 + 16.0 = 24.0; 33.33 %/66.67 %; f(CO₂) = (66.667 − 57.143)/(72.727 − 57.143) = 0.611 = 22/36. Rounded-input version 0.615. Mystery 9/27: C 11.221, O 24.779, 31.17 %/68.83 %, f = 0.750.
- Cl relative pull 17/1 = 17.00, 17/4 = 4.25, 17/9 = 1.89.
- Neutrons: round(35.45) − 17 = 18; round(24.305) − 12 = 12; round(32.06) − 16 = 16.
- Al₂O₃: lcm(3,2) = 6 → 2:3; 2(+3) + 3(−2) = 0. Ca₃N₂: lcm(2,3) = 6 → 3:2.
- EA rounding: 52.867 → 53, 41.762 → 42, 72.037 → 72, 200.41 → 200, 348.575 → 349.

## Sim vs. textbook differences
- Atomic radii are calculated radii (Na 190, K 243 pm), larger than common textbook values (Na 186, K 227 pm).
- Topic 1.4 uses C = 12, O = 16; other topics use 12.011, 15.999.
- PES binding energies are a model (relative units), not MJ/mol; peaks evenly spaced.
- Valence electrons for cations counted as the highest occupied shell (Mg²⁺ = 8).
- EA reported as positive energy released; Mg, N, Ar shown as 0.
- Mg average atomic mass 24.305 from isotopes; Si 28.086 from isotopes vs 28.085 in the sim's table.

## Sim bugs and confusing text (not copied into the worksheet)
1. Topic 1.3 sample-mass slider rounds each element to 0.1 g on every change, so composition drifts and the empirical formula changes (CHO, CH₃O) — contradicts the step's own "law of definite proportions" message. `T/topic-1-3-elemental-composition/state.ts:112-134, 163-165`.
2. Topic 1.1: equations show "2.00 mol × 6.022 × 10²³ = 1.203 × 10²⁴" because moles/particles use unrounded molar mass while the screen shows rounded values. `T/topic-1-1-moles/components/MolesPanels.tsx:979-992`.
3. Topic 1.6: in overlay mode, ion and neutral peaks are placed at the same x (position chosen per subshell, evenly spaced), so the claimed shift is not visible. `T/topic-1-6-pes/components/PesPanels.tsx:520-545`. Step 2 "Peak position" metric shows raw model numbers (e.g. 2.83). `PesPanels.tsx:1086-1088`.
4. Topic 1.7 step 5: Ar electronegativity shown as "0" (undefined value forced to 0). `T/topic-1-7-periodic-trends/components/PeriodicTrendsPanels.tsx:1550-1561`.
5. Topic 1.8: group pattern text drops the "1" for ±1 charges: "Group 1 metals repeat a + charge pattern." `T/topic-1-8-ionic-compounds/calculations.ts` getGroupPatternText + formatChargeLabel (lines ~328-336, 396-404).
6. Topic 1.3 Free Explore Try-it "Change sample mass while keeping percentages fixed" but Free Explore has no sample-mass control (only element boxes). `ElementalCompositionPanels.tsx:257` vs `:77-79`.
7. Topic 1.5 step 2: "Nuclear charge for comparison" slider silently changes the element (Cl → other atom). `T/topic-1-5-electron-config/state.ts:72-85`. Cl charge buttons offer +1, +5, +7 as "ions". `PT:296`.
8. Topic 1.5: relative pull for Cl's valence shell labelled "weaker" (1.89) while the guide calls Cl's outer shell "almost full"; not wrong, but the label set is arbitrary thresholds. `calculations.ts:192`.
9. Tess's existing worksheet typos ("alaways", "dive", "sheilding"; two pages numbered 6) were not copied.

## AP topics not covered by the sim
- Orbital (box) diagrams, Hund's rule, Pauli exclusion; electron spin.
- Transition-metal configurations beyond Z = 18 in 1.5 (builder stops at Ar; Cr/Cu exceptions exist in code but unreachable) and transition-metal ions (4s removed first).
- Real PES energies (MJ/mol) and reading values from a to-scale PES.
- Mass spectra of molecules/diatomics; calculating isotope abundance from an average.
- Experimental composition methods (combustion analysis, gravimetric purity labs).
- Successive ionization energies; quantitative Coulomb's law.
