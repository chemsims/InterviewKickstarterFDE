# Unit 3 sources: Properties of Substances and Mixtures

Sim: Properties of Substances & Mixtures Sim, deployed commit `7d2af55` (checkout `/home/user/unit1armarildosim`).
Served at chemsims.app/sims/unit1 under `/unit/unit-3/topic/3.N` (Guided) and `…/free-explore`.
All paths below are relative to `src/units/unit-3-properties-of-substances-and-mixtures/topics/`. `T3.N/` means the
`topic-3-N-…` folder (e.g. `T3.4/` = `topic-3-4-ideal-gas-law/`). `TP` = `components/TopicPanels.tsx`.

Screen counts (topic.meta.ts `slideCount`): 3.1, 3.2, 3.4, 3.5 = 6; 3.3, 3.6, 3.7 = 5; 3.8–3.13 = 4.

## p. 1 · 3.1 Intermolecular Forces
| Item | Value | Source |
|---|---|---|
| Screen defaults (Screen 1 phase-change, 2 dispersion-size, 3 polarity-series, 4 hydrogen-bonding, 5 dispersion-shape) | | T3.1/calculations.ts:623 (`getDefaultCompareSetIdForStep`), compare sets T3.1/state.ts:390-454 |
| Methane bp | −161.5 °C | T3.1/state.ts:114 |
| Methanol bp | 64.7 °C | T3.1/state.ts:174 |
| n-pentane / neopentane bp | 36.1 / 9.5 °C | T3.1/state.ts:271, :290 |
| Dispersion score CH₄ / Cl₂ / I₂ | 3.8 / 5.9 / 9.9 | worked from `calculateDispersionScore` T3.1/calculations.ts:210 with electronCount/polarizability/contactArea at T3.1/state.ts:105-107, 224-226, 243-245: 0.65 + 0.42√e + 0.65p + 1.25c, rounded to 0.1 |
| CH₃Cl + CH₃Cl dominant force | Dipole-dipole (6.2 vs dispersion 5.6) | T3.1/calculations.ts:293 (3.8 + 1.9×1.25 = 6.2); LDF from :342-345 |
| Methanol + water dominant force | H bonding (7.3 vs dipole-dipole 6.0, LDF 4.1) | T3.1/calculations.ts:317 (6.4 + 1.775×0.5 = 7.3) |
| CH₃F + CH₃F: no H bond; dipole-dipole 6.1 | | `hydrogenBondDonor: false` T3.1/state.ts:150; note text :156; model limitation T3.1/calculations.ts:510-511 |
| Notes: "temporary fluctuating dipoles", "larger contact area" | | T3.1/TP:55-56 |
| Notes: "Molecular geometry decides…" | | T3.1/TP:62 |
| Notes: "donor H directly bonded to N, O, or F" / "acceptor" | | T3.1/TP:69-70 |
| Notes: weaker attractions → higher vapor pressure | | T3.1/TP:77 |
| Shape/contact-area answer | | challenge text T3.1/state.ts:476-477 |

## p. 2 · 3.2 Properties of Solids
| Item | Value | Source |
|---|---|---|
| Classification labels | Ionic solid / Covalent network solid / Molecular solid / Metallic solid / Alloy | T3.2/calculations.ts:55-61 |
| NaCl solid / molten conductivity | "no conductivity" / "conducts" | T3.2/calculations.ts:223-245 |
| Diamond hardness | very high | T3.2/state.ts:204 (network3dProfiles) |
| Sucrose melting point | moderate for a molecular solid | T3.2/state.ts:450 |
| Copper malleability (Pure metal) | high | T3.2/calculations.ts:310-313 (pure-metal branch of `getMetalMechanicalProfile`, :265) |
| Steel ductility (Interstitial) | reduced | T3.2/calculations.ts:276-281; choosing Interstitial switches the solid to steel T3.2/state.ts:757-770 |
| Notes (fixed ions, like charges, between molecules, electrons, block) | | T3.2/TP:55-56, 70, 76-77 |
| Allowed solids per screen | | T3.2/TP:1169-1191 |

## p. 3 · 3.3 Solids, Liquids, and Gases
| Item | Value | Source |
|---|---|---|
| Screen 4 default: argon, T 50, V 20 | | T3.3/calculations.ts:91-165 (`GUIDED_STEP_DEFAULTS`), slider ranges T3.3/state.ts:114-129, unit labels "T"/"V" T3.3/TP:237, 246 |
| Speed / spacing / collision labels | T 50,V 20: moderate / shorter / moderate (score 6.85); T 50,V 90: moderate / larger / low (3.7); T 85,V 20: faster / shorter / high (8.4) | worked from `buildGasMetrics` T3.3/calculations.ts:285-311, labels :313-333 |
| Gas Property tile | "no definite shape or volume; fills the available container" | T3.3/calculations.ts:447-458 |
| Notes (long-range, close, neighbors, similar) | | T3.3/TP:57, 64, 71 |
| Ice takes more volume | | T3.3/calculations.ts:507 |

## p. 4 · 3.4 Ideal Gas Law
| Item | Value | Source |
|---|---|---|
| R | 0.08206 L·atm, 8.314 L·kPa, 62.36 L·mmHg (also torr) | T3.4/calculations.ts:20-22, display :1584-1594 |
| Screen defaults | | T3.4/calculations.ts:165-247; initial state T3.4/state.ts:438 |
| Screen 1: P₂ = (1)(100)/50 = 2 atm | 2 atm | Boyle solver T3.4/calculations.ts:434-438 |
| Screen 2: V₂ = 50×600/300 | 100 L | Charles solver T3.4/calculations.ts:564-575 |
| Screen 3: P₂ = 1×450/300 | 1.5 atm | Gay-Lussac solver T3.4/calculations.ts:729-740 |
| Screen 4: P = 1×0.08206×298/50 | 0.489 atm; 49.551 kPa (sim) | T3.4/calculations.ts:944-965 |
| Screen 5 air-like mixture 0.78/0.21/0.01, 1 atm → P(O₂) | 0.21 atm | T3.4/state.ts:522-526, mixture math T3.4/calculations.ts:1401-1440 |
| Two gas 2/1 mol, 3 atm → P(O₂) | 1.0 atm | T3.4/state.ts:505-510; preset keeps total pressure T3.4/state.ts:792-806 |
| °C→K | +273.15 | T3.4/calculations.ts:879 |

## p. 5 · 3.5 Kinetic Molecular Theory
| Item | Value | Source |
|---|---|---|
| Constants | N_A 6.02214076e23, R 8.314462618 | T3.5/calculations.ts:10-12 |
| Molar masses He / Ar / N₂ | 4.0026 / 39.948 / 28.014 | T3.5/state.ts:113, 139, 152 |
| Screen defaults (He vs Ar 800 m/s; N₂ 400/800 K; N₂ 300/600 K) | | T3.5/state.ts:781-829 |
| KE(He, 800 m/s) | 2.13 × 10⁻²¹ J; Ar 2.12 × 10⁻²⁰ J; ratio 9.98 | worked: m = 4.0026e-3/6.022e23 (T3.5/calculations.ts:82-87) |
| Average KE 400 / 800 K | 4.99 / 9.98 kJ/mol | T3.5/calculations.ts:429 (1.5RT) |
| v_rms N₂ 300 / 600 K | 517 / 731 m/s | T3.5/calculations.ts:111-113 |
| Notes / graph wording (squared, equal KE not speed, √T, peak height not count, volume does not shift) | | T3.5/TP:82, 87, 93, 98, 104 |

## p. 6 · 3.6 Deviation from Ideal Gas Law
| Item | Value | Source |
|---|---|---|
| R | 0.082057366 | T3.6/state.ts:68 |
| a, b from critical constants | N₂ a 1.349, b 0.0386; CO₂ a 3.608, b 0.0428 | T3.6/state.ts:209-222, Tc/Pc :86-87, :116-117 |
| Presets | Ordinary N₂ 1 mol 300 K 24.6 L; Attractions visible CO₂ 320 K 1 L; Extreme compression N₂ 300 K 0.1 L | T3.6/state.ts:148-182; step→preset T3.6/state.ts:421-430 |
| Results | 1 / 1 atm, Z 0.999 (Approximately equal); 26.3 / 23.8 atm, Z 0.907 (Lower); 246 / 266 atm, Z 1.081 (Higher) | worked from `evaluateRealGasState` T3.6/calculations.ts:152-259; display 3 sig figs :361-363, Z toFixed(3) :676-679, direction ±2 % :630-637 |
| Notes | | T3.6/TP:69, 74 |

## p. 7 · 3.7 Solutions and Mixtures
| Item | Value | Source |
|---|---|---|
| Sucrose / glucose molar mass | 342.3 / 180.16 | T3.7/state.ts:83, 90 |
| Screen defaults | | T3.7/calculations.ts:406-516 (0.25 mol/85.575 g/500 mL; 0.4 M/250 mL :484; 0.12 mol/0.3 M glucose :495; compare 0.5 M, 250/750 mL :510) |
| 85.575/342.3 = 0.250 mol; 0.500 M; 1.000 M at 250 mL | | worked |
| 0.400 × 0.250 = 0.100 mol; 6.02 × 10²² | | N_A T3.7/calculations.ts:10; 3-sig format :39 |
| 0.120/0.300 = 0.400 L = 400 mL | | worked |
| A: 0.125 mol, 7.53 × 10²²; B: 0.375 mol, 2.26 × 10²³ | | worked |
| Notes ("final solution volume", equal M ≠ equal N) | | T3.7/TP:1370, 1397; topic.meta.ts slide 2 guide |

## p. 8 · 3.8 Representations of Solutions
| Item | Value | Source |
|---|---|---|
| Screen 1 default: NaCl, target 6, volume 2 | | T3.8/calculations.ts:907-916 |
| Represented units = round(6 × 2 / 4) = 3; at 4 → 6 | | T3.8/calculations.ts:145-153; MODEL_VOLUME_MAX 4 T3.8/state.ts:97 |
| Waters = 16 × volume → 32, 64 | | T3.8/state.ts:99; T3.8/calculations.ts:137 |
| Na⁺/Ca²⁺ → "O end, δ−"; Cl⁻ and methanol O → "One H, δ+" | | T3.8/calculations.ts:565-566; display T3.8/TP:1610 |
| Interaction type "Ion-dipole" / "Hydrogen bond" | | T3.8/TP:1571-1575 |
| Ca²⁺:Cl⁻ 1:2; 2D exercise text | | T3.8/state.ts:172; T3.8/TP:1928, 1934, 1940 |

## p. 9 · 3.9 Separation
| Item | Value | Source |
|---|---|---|
| Filter grades | coarse 45 % Cloudy, medium 75 % Slightly cloudy, fine 100 % Clear | T3.9/calculations.ts:77-106 |
| Sample 1 analyte profiles (A low, B medium, C high polarity) | | T3.9/state.ts:130-158; order table :159 (index 0 = A,B,C); reset increments sample T3.9/state.ts:447-470 |
| Relative movement = round(100·m/(m+s)), m = mobileAt3 + strength − 3 | strength 3: 80/50/29; strength 5: 86/63/44 | T3.9/calculations.ts:134-140; display T3.9/TP:650 |
| Notes | | T3.9/TP:2336, 2346; distillation L-rich T3.9/calculations.ts:226-235, :418-420 |

## p. 10 · 3.10 Solubility
| Item | Value | Source |
|---|---|---|
| Outcome categories and new attractions | NaCl/water appreciable, ion–dipole; NaCl/hexane very low; glucose/water high, glucose–water H bonds; I₂/hexane appreciable, dispersion | T3.10/calculations.ts:70-157 (lines 74, 92, 103, 152) |
| Liquid pairs: one / two liquid phases | | T3.10/calculations.ts:170-192, label :262 |
| Notes | | T3.10/TP:1090, 1102, 1107; T3.10/state.ts:206 |
| Screen defaults | | T3.10/state.ts:505-552 |

## p. 11 · 3.11 Spectroscopy
| Item | Value | Source |
|---|---|---|
| Ranges & families | UV 100–400 nm, Vis 400–780 nm (electronic); IR 780 nm–1 mm (vibrational); MW 1 mm–1 m (rotational) | T3.11/state.ts:68-114 |
| What changes | | T3.11/calculations.ts:138, 145, 149, 154 |
| lower→upper / outgoing | | T3.11/calculations.ts:52-69 |
| Notes | | T3.11/TP:1317, 1327, 1332 |
| Energy ranking question | not computed by 3.11 (T3.11/calculations.ts:385); answered from 3.12's E = hc/λ | |

## p. 12 · 3.12 Photons
| Item | Value | Source |
|---|---|---|
| c, h, tolerance | 299,792,458 m/s; 6.62607015e-34 J·s; 0.5 % | T3.12/calculations.ts:11-15 |
| Screen photons 500 nm / 600 nm / 750 THz / 600 nm; gap 486 nm | | T3.12/state.ts:613-633, defaults :563-611 |
| 500 nm → 3.97 × 10⁻¹⁹ J; 600 nm → 5.00 × 10¹⁴ s⁻¹ (499.65 THz, shown "500 THz"), 3.31 × 10⁻¹⁹ J; 750 THz → 4.97 × 10⁻¹⁹ J; 486 nm → 4.09 × 10⁻¹⁹ J; mismatch −19.0 % | | worked; 3-sig display T3.12/calculations.ts:172-183 |
| Notes | | T3.12/TP:1264, 1269, 1274 |

## p. 13 · 3.13 Beer–Lambert
| Item | Value | Source |
|---|---|---|
| Allura Red ε = 540 × 496.42/10 = 26,806.7 at λmax 504 nm | | T3.13/state.ts:75-82 |
| Defaults 25 µM, 1 cm, 504 nm; Screen 4 at 600 nm | | T3.13/state.ts:479-527 |
| A = εbc | 25 µM 0.670; 12.5 µM 0.335; 50 µM 1.340; 2 cm 1.340; 0.5 cm 0.335; 600 nm 0.0324 (ε 1296) | T3.13/calculations.ts:116-157; display toFixed(3) or 4 if <0.1 :530 |
| Band model | right σ 39 nm | T3.13/state.ts:81; Gaussian T3.13/calculations.ts:131-135 |
| Limits 0–50 µM, 0.1–2 cm, 400–700 nm | | T3.13/state.ts:218, 245, 255 |
| "A has no unit" | | T3.13/TP:1267 |

## Conclusion, exit tickets, AP practice
- I₂ in water: weak dipole-induced dipole, T3.10/calculations.ts:117-122.
- N₂ 24.6 L vs 0.100 L: P_ideal 1.00 / 246 atm, Z 0.999 / 1.081 (p. 6 rows).
- 504 nm photon: 6.62607015e-34 × 299792458 / 5.04e-7 = 3.94 × 10⁻¹⁹ J.
- Exit ticket: 0.100 × 0.08206 × 300 / 2.00 = 1.23 atm; ×450/300 = 1.85 atm. 0.536/26,807 = 2.00 × 10⁻⁵ M.
- AP MC: v_rms He 300 K 1367, N₂ 300 K 517, N₂ 600 K 731, CO₂ 600 K 583 m/s (M = 44.01).
- AP FRQ: CO₂ 1 L 320 K: 26.3 atm, Z 0.907; at 10 L Z = 0.991 (T3.6 model). Beer–Lambert: 0.402/0.0268 = 15.0 µM; 2.00 cm → 0.804.

## Values checked by hand
All numbers were recomputed with Python (`verify.py` in the session scratchpad) using the sim's constants:
```
dispersion score: CH4 3.8, Cl2 5.9, I2 9.9, CH3Cl 5.6, CH3OH 4.7, CH3F 4.5
CH3Cl+CH4: LDF 4.6 > dipole-induced 4.3 (Dispersion wins); CH3Cl+CH3Cl: dd 6.2 > LDF 5.6
CH3OH+H2O: H-bond 7.3, dd 6.0, LDF 4.1; CH3F self: dd 6.1 > LDF 4.5
3.3 collision score: (5.5+8.2)/2 = 6.85; (5.5+1.9)/2 = 3.7; (8.6+8.2)/2 = 8.4
P = 1*0.08206*298/50 = 0.48908 atm; 1*8.314*298/50 = 49.551 kPa
n = 745*2.5/(62.36*300.15) = 0.09951 mol
KE He 800 m/s = 2.1269e-21 J; Ar = 2.1227e-20 J; ratio 9.98
1.5*8.314462618*400 = 4989 J/mol; *800 = 9978
vrms N2 300 = 517, 600 = 731; He 300 = 1367; CO2 600 = 583
3.6: N2 24.6 L Pi 1.0007 Pr 1.0000 Z 0.9993; CO2 1 L Pi 26.258 Pr 23.826 Z 0.9074;
     N2 0.1 L Pi 246.17 Pr 266.03 Z 1.0807; CO2 10 L Z 0.9906; CH4 459 K 0.15 L Z 1.0000
3.7: 85.575/342.3 = 0.25; 0.1*N_A = 6.022e22; 0.12/0.3 = 0.4; 0.125*N_A = 7.528e22; 0.375*N_A = 2.258e23
3.8: round(6*2/4) = 3; 16*2 = 32
3.9: strength 3 -> 0.800/0.500/0.286; strength 5 -> 0.857/0.625/0.444
3.12: 500 nm 3.9729e-19 J; 600 nm 4.9965e14 Hz, 3.3107e-19 J; 750 THz 4.9696e-19 J; 486 nm 4.0873e-19 J
3.13: eps 26806.68; A(25 uM) 0.6702; eps(600) 1295.7, A 0.0324; 0.402/26806.68 = 1.4996e-5 M
```

## Sim vs. textbook differences
- Three R values: 0.08206 (3.4), 0.082057366 (3.6), 8.314462618 J (3.5). 3.4 uses 62.36 for torr and mmHg alike.
- 3.6 van der Waals a, b are derived from Tc/Pc (CO₂ a = 3.61, b = 0.0428) vs textbook tables (3.59, 0.0427).
- 3.11 visible range is 400–780 nm (many textbooks: 400–700 nm).
- 3.13 ε comes from EU E(1 %, 1 cm) specs; the spectral band shape is an educational model.
- 3.1 boiling points are real literature values; "dispersion score" and force "scores" are invented model numbers.
- 3.3 slider units "T" and "V" are relative 0–100, not K or L.

## Sim bugs and confusing text (not copied into the worksheet)
- T3.1/calculations.ts:561, 567, 573: shows "deg C" instead of °C; vapor-pressure readout says "higher when boiling point is −161.5 deg C".
- T3.1 Screen 3 default pair (chloromethane + methane) shows Dispersion as dominant (score 4.6 vs 4.3), which reads oddly on a "Dipoles" screen (T3.1/calculations.ts:623-640 default set; scores :306, :342-345).
- T3.1/state.ts:310, 329: Na⁺ and Cl⁻ ions each carry `meltingPointC: 801` (NaCl's melting point assigned to individual ions).
- T3.4/state.ts:579: `setGasPressureUnit` changes only the unit label, not the value (1 atm → 1 kPa). Temperature unit does convert (T3.4/state.ts:715).
- T3.2/calculations.ts:265-313: alloy mechanical values are overridden by generic text ("moderately increased") instead of brass's own "higher than pure copper" (T3.2/state.ts:540-555).
- T3.8/calculations.ts:145-153: entered "formula units at 4 model units" is silently rounded; target 6 at volume 2 shows 3 units.
- T3.9/state.ts:447-470: every reset reshuffles which dye letter is most polar ("sample N"), so class answers differ unless everyone records sample 1.
- T3.10/calculations.ts:136-157: iodine/ethanol is "moderate" (score 3) but iodine/hexane is "appreciable" (score 2) — word order and score order disagree.
- unit.meta.ts description still says "Scaffolded … for later … builds" though all 13 topics are built.

## AP topics not covered by the sim
All 13 CED topics (3.1–3.13) have a sim topic. Gaps inside topics:
- 3.4: gas density and molar mass from PV = nRT (d = PM/RT); stoichiometry with gases.
- 3.3/3.5: vapor pressure vs temperature curves, phase diagrams, Graham's law/effusion.
- 3.9: quantitative Rf calculation (the sim shows "relative movement" and says it is not a measured Rf).
- 3.11: real IR/UV-vis spectra; 3.11 calculates no energies.
- 3.12: energy per mole of photons.
- 3.13: %T / transmittance readout, calibration with real data scatter, sources of deviation.
The lesson plan's `prep` tells the teacher to use their usual lesson for these.
