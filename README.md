# PV Matched-Control Evidence

Companion repository for the conference manuscript **Reserved PV Modules as Matched Controls: Calculation Eligibility, Downward-Signal Follow-Up, and Directional Interpretation**.

## Research question
When does an available reserved PV module support a matched-control calculation, when is the result useful only for follow-up prioritization, and when is the evidence strong enough to interpret a direction physically?

## Current Qatar result
The Qatar application separates three evidence states: calculation eligibility, conditional diagnostic / follow-up priority, and direction-supported interpretation. The manuscript does not equate a narrow cohort-resampling interval with metrological uncertainty and does not call a two-epoch difference a degradation rate by default.

## Independent public-data extension
An optional external metrology stress test is being prepared with the **NREL/DuraMAT BEST Field Degradation Research** dataset. The external dataset contains repeated I–V measurements from 2019, 2022, and 2024, including measurements from different laboratory systems. The purpose is to test whether apparently simple two-epoch interpretation changes when measurement/procedure comparability is enforced.

Primary public-data citation:

> NREL/DuraMAT BEST Field Degradation Research. DOI: 10.21948/2462712.

This external dataset is **not** a substitute matched-control experiment for the Qatar archive. It is used only to stress-test the broader evidence principle.

## Repository policy
- Qatar source workbook/BOM evidence and owner-held metrology records are not redistributed.
- No external module is declared a “matched control” without documented structural and procedural equivalence.
- Public external data are cited and downloaded from authoritative sources.
- Additional analysis enters the manuscript only if it changes or materially sharpens a scientific decision.

## Planned structure
- `src/` diagnostic and evidence-gate code
- `configs/` frozen analysis settings
- `tests/` arithmetic, gate, resampling, and priority checks
- `results/` disclosure-safe derived tables
- `supplement/` conference supplementary material
- `external_data/` DuraMAT provenance and transfer-test plan
- `restricted_data/` Qatar owner-data boundary

## Status
Public research companion. Manuscript authorship/affiliations will be synchronized after collaborator confirmation.
