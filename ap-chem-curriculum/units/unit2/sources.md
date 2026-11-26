# Unit 2 — Compound Structure and Properties: sources

Sim: `/home/user/chemtutor-static-tutor/public/sims/unit2/index.html` (deployed copy, served at `/sims/unit2`).
All line numbers below are `index.html:line`. Two engines share the page: Bonds & Solids (screens 1–5,
lines 523–1795) and Molecular Structure (screens 6–8, lines 1797–2649). The shell (tabs, guide) is 2651–2767.

Defaults when a tab is opened (boot code 1781–1785, 2643–2646): Bonds = Cl–Cl; Energy = H₂ at r = 340 pm;
Ionic = NaCl, empty grid, Solid; Lattice = "Same charges, different sizes"; Metals = Pure copper; Lewis = CO₂;
VSEPR predictor = H₂O (first in `MOLS`, 2008); 3-D = CH₄. Clicking a tab moves the guide to that tab's first
step without re-running its loader (2726–2733).

## Page 1 — Bonds (Topic 2.1)

| Item | Value | Source |
|---|---|---|
| Notes: nuclei / electrons / time | "positive nuclei pulling on negative electrons… where the bonding electrons spend their time" | 1733 |
| Notes: EN, nonmetals, δ−/δ+ | step 2 text | 1734 |
| Notes: metal, nonmetal, cation, anion, ionic | step 3 text | 1735 |
| Notes: metals, valence electrons, sea, metallic | step 5 text | 1737 |
| Notes: continuum; "metal + nonmetal is the better test" | step 4 text | 1736 |
| Notes: 0.4 cut-off for nonpolar | `d < 0.4 ? "nonpolar"` | 711; caption 875 |
| EN values (Pauling) | Cl 3.16, H 2.20, F 3.98, Na 0.93, Mg 1.31, O 3.44, Cu 1.90, Zn 1.65, Al 1.61, Ca 1.00, C 2.55 | 667–686 |
| ΔEN column | Cl–Cl 0.00, H–Cl 0.96, H–F 1.78, Na–Cl 2.23, Mg–O 2.13, Na–Na 0.00, Cu–Zn 0.25 | worked from EN at 667–686 with `classify` 710 (rounded to 0.01), shown by 838 |
| Bond type rule | metal+metal metallic; metal+nonmetal ionic; else nonpolar if ΔEN < 0.4, else polar | 711; names 707 |
| Particles column | "Cl₂ molecule, pair shared equally"; "H–Cl bond: δ+ on H, δ− on Cl"; "Na⁺ and Cl⁻ ions; charges balance as NaCl"; "Mg²⁺ and O²⁻ … MgO"; "Na⁺ cations in a sea of shared valence electrons"; "Cu⁺ and Zn²⁺ cations in one electron sea (a mixture of metals: an alloy)" | 760–772 (Cu⁺ from `seaQ` 956, Zn q = 2 at 674) |
| Calc: Al–O → 2 Al³⁺ : 3 O²⁻, Al₂O₃ | give 3, take 2, gcd 1 → nm 2, nx 3 | `ionCount` 747–750, line text 948–950, formula 736–741 |
| H–F analysis | polar covalent; "Metal + nonmetal is the better test for ionic" | 1736, 873–874 |
| Al–Cl note (Explore box / key notes) | "ΔEN is only 1.55 here. Bonds like this have some covalent character, but AP classifies metal + nonmetal as ionic." | 867 |
| Properties to expect | ionic / molecular text | 843–848 |
| Demo: ΔEN bar labels | shared equally / shared unequally / transferred | 976–980 |

## Page 2 — Energy (Topic 2.2)

| Item | Value | Source |
|---|---|---|
| Notes 1–3 | step texts | 1741–1743 |
| "Breaking bonds always absorbs energy; forming bonds releases it" | Quick-check caption | 1063 |
| shorter, stronger / bigger | 1745, 1746 |
| Bond data (r₀ pm, De kJ/mol) | H₂ 74/436; C–C 154/348; C=C 134/614; C≡C 120/839; Cl₂ 199/243; Br₂ 228/193; I₂ 151 at 267 | 994–1004 |
| PE formula (Morse) | `Vm = De((1−e^{−a(r−re)})² − 1)` | 1009 |
| Home key → r₀; Shift+arrow ±10 pm, arrow ±2 | 1044–1048 |
| Pull apart target | rMax − 20 = 430 pm (H₂ rmax 450) | 1057, 995 |
| Table 1 PE | 430 → −1, 124 → −268, 74 → −436, 54 → −338 kJ/mol | worked from 1009 with H₂ constants (995); display rounding `fmt` 537 |
| Net-force readouts | zones bottom (±4 pm) / close / pull (V < −0.03De) / far; text at 1079 | 1014, 1079 |
| Calc: 0.50 mol × 436 = 218 kJ; 2.0 × 436 = 872 kJ | worked from 995 |
| Calc: 614/348 = 1.76; 614 − 348 = 266 | worked from 997–998 |
| Halogen trend explanation | "The smaller the atoms, the closer the shared pair sits…" | 1070, 1746 |

## Page 3 — Ionic (Topic 2.3)

| Item | Value | Source |
|---|---|---|
| Notes 1–2 (cations, anions, checkerboard, opposite, attraction, repulsion) | 1749–1750 |
| 4 neighbours flat / 6 in 3-D | 1190, 1203, 1314, 1439 |
| "a current needs charge that can MOVE" | 1751 |
| hammer: SAME charge, cracks | 1211 |
| Like-charge rejection | 1186 |
| Grid 5 × 8 = 40 sites, even so neutral | 1158–1159 |
| State readouts (Ions / Conducts) | 1359–1360; bulb on unless solid 1372 |
| Melting points NaCl 801, KBr 734, MgO 2852; MgO `sol:false` | 1153–1157 |
| MgO won't dissolve (reason text) | 1213, 1216 |
| Explain-it answers A/D/B/C | 1443–1445 |

## Page 4 — Lattice (Topics 2.2–2.3)

| Item | Value | Source |
|---|---|---|
| Notes / equation wording ("|q₊ × q₋| ÷ r", separate one mole into gaseous ions) | 1756 |
| Doubling → four times | 1757 |
| r = r₊ + r₋, ion centres | 1758; card label 1511, 1537 |
| Radii (pm), U (kJ/mol), mp (°C) | NaF 102+133, 923, 993; NaCl 102+181, 786, 801; NaBr 102+196, 747, 747; NaI 102+220, 704, 661; KCl 138+181, 715, 770; KBr 138+196, 682, 734; MgO 72+140, 3791, 2852; CaO 100+140, 3401, 2613 | 1459–1468 |
| Hint ratio `|q₊q₋|/r ÷ NaCl` | 1.20, 1.00, 0.95, 0.88, 0.89, 0.85, 5.34, 4.72 | `coul` 1477, displayed 1541 (2 dp) |
| Rankings | NaF>NaCl>NaBr>NaI; MgO>CaO>NaCl>KBr; NaBr>KCl>NaI>KBr | sorted by U, 1484; explanations 1470–1475 |
| KCl melts above NaBr note | 1492–1497 |

## Page 5 — Metals (Topic 2.4)

| Item | Value | Source |
|---|---|---|
| Notes text | steps 1761–1765 |
| 50 sites (5 × 10), Zn max 20 = 40% | 1551, 1560, 1574, 1622 |
| Densities Cu 8.96, Zn 7.14 mix by atom %; Fe 7.87; steel ≈ 7.85 | 1668–1670 |
| Composition / malleability readouts | 1665–1667, 1672–1673 |
| Brass slides "a bit harder"; steel stuck text | 1605, 1601 |
| Battery: drift toward + terminal | 1618 |
| Slip-gap holes (i = 1, drawn darker) | 1575, 1688 |
| Alloy pairs and radii; ratio % | Ni 124/Cu 128 = 97%; C 77/Fe 126 = 61%; Sn 140/Cu 128 = 109%; N 71/Fe 126 = 56%; Ag 144/Au 144 = 100% | 1709, ratio `Math.round(ra/rh*100)` 1713 |
| Calc: 8.96×0.80 + 7.14×0.20 = 8.60; 8.96×0.60 + 7.14×0.40 = 8.23 | worked from 1669 |

## Page 6 — Lewis (Topics 2.5–2.6)

| Item | Value | Source |
|---|---|---|
| Notes: valence map, count rule, centre atom, octets, formal charge, resonance, exceptions | steps 2608–2614 |
| Valence e⁻ | `EL.v` 1826–1839; total 1870 (central + terminals − charge) |
| CO₂ 16, NO₃⁻ 24, BF₃ 24, SO₂ 18, SF₆ 48 | worked from 1870 |
| Accepted structures | `ans[0]`: CO₂ [2,2],0,[2,2]; NO₃⁻ [2,1,1],0,[2,3,3]; BF₃ [1,1,1],0,[3,3,3]; SO₂ [2,1],1,[2,3]; SF₆ six single, 0, F 3 LP | 1851–1864 |
| Formal charge formula | `v − 2·LP − bonds` | 2041–2044 |
| FCs: CO₂ all 0; O≡C–O: C 0, O(triple) +1, O(single) −1; NO₃⁻ N +1, O(single) −1; SO₂ S +1, O(single) −1 | worked from 2041–2044 |
| Electrons around central: CO₂ 8, NO₃⁻ 8, BF₃ 6, SO₂ 8, SF₆ 12 | 2037–2039 |
| Resonance counts 2 (SO₂), 3 (NO₃⁻) | `res` 1854, 1856; caption 2265 |
| Exceptions accepted (B 6, expanded period 3+) | 2254–2263 |
| "Valid — but not the best" for O≡C–O (`ans[1]`) | 1851, 2269–2272 |

## Page 7 — VSEPR (Topic 2.7)

| Item | Value | Source |
|---|---|---|
| Notes | steps 2618–2622 |
| Shapes table (EDG, MG, angle text) | `SHAPES` 1879–1893 (5-3 linear 180° row included) |
| Lone pairs equatorial / trans | 2329, 2333 |
| Predictor domains line | 2388 |
| Predictor answers H₂O, SF₄, XeF₄, ClF₃, CO₂ | lone pairs from `ans[0][1]` 1848–1866, key 1873, `SHAPES`; angle option text 1896 |

## Page 8 — 3-D (Topic 2.7)

| Item | Value | Source |
|---|---|---|
| Notes | steps 2626–2631 |
| Readout lines | 2447–2453 |
| Hybridization; 5/6-domain "not assigned at AP level" | 1879–1893 (5th field), 1899 |
| σ/π: CO₂ 2σ+2π, HCN 2σ+2π, others σ only | 2450–2453 with `ans[0][0]` |
| Polarity (threshold 0.15 on `dipole`) | CH₄ 0.00 non; NH₃ 0.94 polar; H₂O 1.52 polar; CO₂ 0.00 non; HCN 0.84 polar; BF₃ 0 non; SF₄ 1.40 polar; XeF₄ 0 non | worked from 2436–2442 and directions 1907–1924, 2459 |
| Arc angles: CH₄ 109.5, NH₃ 107, H₂O 104.5, BF₃ 120 | 1910–1914 via 2534–2557 |
| CO₂/H₂O dipole text | 2629, 2576–2578 |

## Conclusion
Values reused from pages 1–8 (NaCl 801, MgO 2852 °C at 1154–1156; MgO 5.34× NaCl from 1477; U 3791/786 at 1461, 1466).

## Values checked by hand

Python (`scratchpad/u2/check.py`, `mol.py`) re-implemented the sim's formulas:

```
classify: Cl–Cl 0.00 nonpolar; H–Cl 0.96 polar; H–F 1.78 polar; Na–Cl 2.23 ionic; Mg–O 2.13 ionic;
          Na–Na 0.00 metallic; Cu–Zn 0.25 metallic; C–H 0.35 nonpolar; Al–O 1.83 ionic; Al–Cl 1.55 ionic; N–O 0.40 polar
Morse H2 (De 436, a 0.0194, re 74): V(430) = −0.87 → "−1"; V(340) = −4.99; V(124) = −267.9 → −268;
          V(74) = −436; V(54) = −338.0; zone(124) pull (−268 < −13.1); zone(54) close
lattice |q+q−|/r ÷ (1/283): NaF 1.20, NaBr 0.95, NaI 0.88, KCl 0.89, KBr 0.85, MgO 5.34, CaO 4.72
brass 8.96(1−x)+7.14x: x=0.20 → 8.596 → 8.60; x=0.40 → 8.232 → 8.23
alloy ratios: 97, 61, 109, 56, 100 %
Lewis valence: H2O 8, CO2 16, HCN 10, BF3 24, SO2 18, NO3− 24, CO3 2− 24, OCN− 16, PCl5 40, SF4 34,
          ClF3 28, XeF2 22, SF6 48, BrF5 42, XeF4 36 (all equal to electrons used by ans[0])
formal charges from ans[0]: SO2 S +1, O −1; NO3− N +1, O −1 ×2; OCN− O −1; rest 0
dipole magnitudes: H2O 1.52, NH3 0.94, HCN 0.84, SO2 1.38, O3 0.51, SF4 1.40, ClF3 0.82, BrF5 1.02, others 0.00
template angles: NH3 107.0°, CH4 109.47°, H2O 104.5°, 3-1 bent 119°; 5- and 6-domain lone-pair shapes 90/120 exactly
energy: 0.50×436 = 218; 2.0×436 = 872; 614/348 = 1.764; 614−348 = 266; 839 < 3×348 = 1044
```

## Sim vs. textbook differences

- Bond energies: C–C 348 (often 347), Cl₂ 243 (often 242) kJ/mol (997, 1001). The PE curves are Morse fits, not measured curves (990).
- Lattice energies: NaCl 786 (often 787–790), MgO 3791 (often 3795–3850), CaO 3401 (1459–1468).
- Radii: Shannon ionic radii (1457); Cu 132 pm on Bonds (675) but 128 pm in the alloy check (1709); C 76 vs. 77 pm (677, 1709).
- Brass density is a linear average by atom % (1669); real brass densities (≈ 8.4–8.7 g/cm³) depend on mass %.
- The sim classifies any metal + nonmetal as ionic regardless of ΔEN (711) and calls ΔEN < 0.4 nonpolar (so C–H is "nonpolar covalent").
- Bent (3 domains, 1 LP) arc shows 119° (1911); SO₂'s real angle is ≈119°, so this is fine; the readout says "slightly less than 120°".
- SO₂: the sim's only accepted structure is the octet form with formal charges +1/−1 (1854); many textbooks prefer the expanded-octet form with all-zero formal charges.
- Hybridization for 5/6 domains is not given ("not assigned at AP level", 1899), matching the current CED.

## Sim bugs and confusing text (not copied into the worksheet)

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

## AP topics not covered by the sim

All seven Unit 2 topics (2.1–2.7) have a screen. Gaps inside topics:
- 2.5/2.6: Lewis structures with more than one central atom (C₂H₄, CH₃OH, organic molecules); the builder is one central atom only (1843–1867).
- 2.7: σ/π and hybridization in multi-centre molecules; delocalized π systems beyond the resonance message.
- 2.1: bond dipole/dipole-moment magnitudes and percent ionic character are qualitative only.
- 2.2: F₂ anomaly is mentioned but not modelled; no quantitative Coulomb's-law energy (only ratios).
- 2.4: ductility (drawing into wire) is stated, not demonstrated; only the layer-slide test.
