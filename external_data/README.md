# External data record — NREL/DuraMAT BEST Field Degradation Research

Authoritative source:
- Project: BEST Field Degradation Research
- DOI: `10.21948/2462712`
- Dataset page: https://datahub.duramat.org/dataset/best-field-degradation-research
- Repeated I–V resource: `2019-2024 IV Curves BLIND.csv`

The public dataset contains repeated laboratory I–V measurements for modules in the NREL BEST bifacial field, with measurements before deployment (2019) and later measurements including 2022 and 2024. The metadata state that some measurements were taken with the low-uncertainty LACCS-MSR system and others with SPIRE systems.

## Prespecified transfer question
Does the interpretation or prioritization of a two-epoch PV change differ when measurement/procedure comparability is explicitly enforced?

## Guardrails
1. Do not call any external module a Qatar-style matched control without documented equivalence.
2. Treat the external dataset as a metrology/comparability stress test, not as replication of the Qatar experiment.
3. Preserve instrument/procedure identity in every comparison.
4. If a cross-instrument comparison is not defensible from metadata, classify it as not admitted rather than forcing normalization.
5. Add the external example to the manuscript only if it changes or materially clarifies a scientific decision; otherwise retain it as supplementary/reviewer evidence.
