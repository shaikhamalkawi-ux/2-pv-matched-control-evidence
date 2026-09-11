# Paper 2 — DuraMAT BEST Metrology-Comparability Transfer Protocol (FROZEN v1)

**Freeze date:** 2026-09-12 (Asia/Dubai)  
**Status:** Frozen before inspection of module-level Pmax outcomes.  
**Purpose:** independent stress test of the distinction between a calculable repeated-measurement change and a scientifically interpretable direction. This is not a Qatar matched-control replication and does not create an external matched control.

## 1. Prespecified scientific question
When the same PV specimen is measured at repeated epochs in the public NREL/DuraMAT BEST laboratory archive, does an apparent two-epoch numerical change remain admissible for directional interpretation once documented instrument/procedure comparability is enforced?

The transfer target is the **evidence-gating principle**: numerical change can be computed under weaker evidence than is required for physical directional interpretation.

## 2. Authoritative source
- Dataset: **BEST Field Degradation Research**.
- DOI: `10.21948/2462712`.
- Primary repeated-I–V resource: `2019-2024 IV Curves BLIND.csv`.
- Public metadata state that measurements include pre-deployment 2019 observations, some 2022 observations, and 2024 observations, and that LACCS-MSR, SPIRE 5600, and SPIRE 4600 systems are represented.

Exact CSV field names may be mapped after header/schema-only inspection. Outcome values may not be used to alter the scientific question, epoch contrasts, comparability hierarchy, or contribution gate.

## 3. Frozen analysis unit
The analysis unit is a uniquely identified physical module/specimen, not a technology average and not a Qatar-style field/control pair.

A repeated specimen is eligible only when:
1. the same specimen identifier is traceable at two or more admitted epochs;
2. the relevant maximum-power quantity is finite and its units are identifiable;
3. the measurement instrument/procedure metadata needed for the comparability state are present or explicitly marked unavailable.

No cross-specimen substitution is allowed to manufacture a missing baseline.

## 4. Frozen epoch contrasts
Primary contrast: **2019 → 2024** for specimens observed at both epochs.

Secondary chronological contrasts, reported separately when available:
- 2019 → 2022;
- 2022 → 2024.

No annualized degradation rate is computed. A two-epoch percent change is a repeated-measurement diagnostic only.

## 5. Numerical change
For specimen i and admitted pair of epochs a<b,

`delta_i(a,b) = 100 * (Pmax_i,b / Pmax_i,a - 1)`.

If repeated sweeps exist for the same specimen/epoch/instrument/procedure state, the specimen-epoch Pmax is the median of those repeated sweeps, provided the schema confirms that they are replicate measurements of the same state. No pooling across different instruments or incompatible procedure states is permitted merely to increase sample size.

## 6. Comparability states
Every numerical contrast receives one of the following prespecified states.

### C0 — not calculable
Specimen identity, epoch Pmax, units, or a required endpoint is missing/invalid. No numerical contrast is reported.

### C1 — calculable, comparability unresolved
A two-epoch numerical contrast is calculable, but instrument/procedure identity differs or the metadata do not establish a defensible measurement bridge. The number may be retained as a descriptive diagnostic but its sign is **not admitted** as physical degradation or improvement.

### C2 — comparable repeated measurement
The same specimen is measured under the same documented instrument/procedure state, or a source-documented metrological bridge explicitly establishes comparability between the two measurement systems. The sign may be described as a comparable repeated-measurement direction, but not automatically as field degradation because full uncertainty, correction, and causal attribution may remain incomplete.

### C3 — direction supported
Reserved for a case where the public source supplies enough repeatability/reproducibility, calibration/correction provenance, and uncertainty information to support a directional physical interpretation. C3 is not assumed to exist.

The hierarchy is cumulative; later evidence cannot repair a failed earlier prerequisite.

## 7. Instrument rule
Exact same-instrument/procedure pairs are the primary comparability-admitted set. Cross-instrument pairs are **not** promoted to C2 unless the public metadata or accompanying documentation provides an explicit bridge adequate for the quantity being compared. Similar device type, common laboratory ownership, or a commercial instrument label is not by itself a bridge.

## 8. Primary endpoints
Report without outcome-driven tuning:
1. number of repeated specimens in the 2019→2024 primary contrast;
2. counts and fractions in C0/C1/C2/C3;
3. distribution of naive numerical `delta` before the comparability gate;
4. distribution of C2-admitted repeated-measurement `delta`, if any;
5. number of **decision-changing cases**, defined prospectively as contrasts whose naive sign would invite a directional reading but whose evidence state is C0/C1, or whose eligible comparison changes when exact instrument/procedure matching is enforced;
6. whether any ordering by negative numerical change changes after comparability admission.

Secondary 2019→2022 and 2022→2024 contrasts use the same rules and are not pooled with the primary contrast.

## 9. Sensitivity checks
If the schema supports them without new assumptions:
- exact-instrument only versus any-instrument descriptive calculations;
- median-of-replicate sweeps versus first documented sweep within the same specimen/epoch/instrument state;
- leave-one-specimen-out summaries when at least four C2 specimens exist.

These checks are descriptive. They do not create a missing uncertainty budget.

## 10. Stop / downgrade rules
Do not admit the external case to the main manuscript if:
- specimen identity cannot be traced reproducibly across epochs;
- instrument identity cannot be mapped reproducibly;
- the resource does not contain at least one primary or secondary repeated-specimen contrast;
- outcome interpretation would require an undocumented cross-instrument normalization or bridge;
- no case materially changes scientific interpretation after the comparability gate.

If the dataset is scientifically useful but no decision changes, keep it in Supplement/GitHub only.

## 11. Contribution gate
A compact main-paper result is warranted only if the DuraMAT case buys new knowledge for Paper 2, for example:
A. at least one naive directional reading is blocked by the comparability gate;
B. exact instrument/procedure admission changes a sign, priority, or set of interpretable specimens;
C. the public archive provides a defensible C2/C3 example that clearly distinguishes calculability from interpretability; or
D. the public metadata establish a clear boundary showing that numerical repeated-measurement change is easier to compute than to interpret.

Otherwise the external analysis remains supplementary/reviewer evidence and AC2 stays the manuscript baseline.

## 12. Claim boundary
The DuraMAT case is a **metrology/comparability stress test**. It does not validate Qatar PERC-M7, SHJ-M1, SHJ-M5, or any Qatar numerical result; it does not create an external matched control; and it does not convert repeated laboratory change into a degradation rate.

The Qatar PERC-M7 structural/BOM non-equivalence remains the primary published gate evidence for Paper 2.

## 13. Frozen reproducibility outputs
- authoritative source URL/DOI/resource ID;
- downloaded-file SHA-256 and byte count;
- schema/header inventory before outcomes;
- specimen/epoch/instrument map;
- comparability-state ledger;
- primary and secondary contrast tables;
- decision-change ledger;
- contribution decision;
- code/environment hashes.
