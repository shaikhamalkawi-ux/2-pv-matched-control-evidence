# Paper 2 — DuraMAT BEST comparability stress test

## Source lock
- DOI: `10.21948/2462712`
- Source bytes: `5186428`
- Source SHA-256: `e6e88f3948008fd2ac6bdf52007b7cee16ee334f78db07c633826188fe4e8713`
- Data rows: `99`

## Frozen primary endpoint
The prespecified primary endpoint was `Pmax_VTIF_Corr`. It is populated in **0/99** rows in the admitted public resource, and `Correction Factor` is also populated in **0/99** rows. Therefore the primary 2019→2024 corrected-power comparison is **C0 / not calculable** for all **9** repeated specimen-side candidate units. The analysis does not switch endpoints after observing this result.

## Prespecified raw `tracer_pmax` sensitivity
- Primary 2019→2024: **9** same-instrument Spire 5600 specimen-side contrasts; median raw change **−2.430%**, range **−9.447% to −1.012%**. These are raw repeated-measurement diagnostics, not degradation rates and not C3 direction claims.
- Secondary 2019→2022: 11 C2 same-instrument and 11 C1 cross-instrument contrasts. Four specimen-side units have both alternatives; **1** changes sign under the comparability gate.
- Secondary 2022→2024: 12 C2 same-instrument and 4 C1 cross-instrument contrasts. Two specimen-side units have both alternatives; **1** changes sign under the comparability gate.
- Prespecified first-sweep vs median-of-replicates sensitivity changes sign in **2** exact-instrument secondary contrasts and in 0 primary 2019→2024 contrasts.

## Decision-changing examples
| Contrast | Specimen-side | Cross-instrument C1 raw change | Same-instrument C2 raw change | Effect of gate |
|---|---|---:|---:|---|
| 2019→2022 | M1812-0010 rear | −0.752% | 0.000% | Negative sign is not retained |
| 2022→2024 | M1812-0011 rear | −0.329% | +0.665% | Sign reverses |

## Contribution decision
**Admit a compact external boundary result to Paper 2 AC3.** The public archive independently demonstrates the paper's core distinction: a numerical repeated-measurement change can be easy to calculate while physical direction remains evidence-gated. Instrument choice can even reverse the raw sign in otherwise identical specimen-side comparisons. The result does not replace the Qatar PERC-M7 structural gate, does not create an external matched control, and does not establish degradation or improvement.
