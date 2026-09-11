# DuraMAT BEST schema mapping and instrument bridge — PRE-OUTCOME v1

This addendum was fixed after schema/header and source-document inspection but before any module-level outcome summary, ranking, or sign-count analysis.

## Exact migrated official source
- DOI: `10.21948/2462712`
- Dataset ID: `7cdfed1b-7571-4b28-958e-c62e8f67139b`
- Resource ID: `4b1b201a-d866-4f52-ac6f-6989f7a376df`
- HERO DataRepo ID: `production-duramatdh-app`
- Migrated API root: `https://hero.nlr.gov/data-repo/api/v1/production-duramatdh-app`
- Expected resource byte count from HERO metadata: `5,186,428`.

The legacy CKAN download route currently resolves to the new SPA shell and is not treated as the source binary.

## Frozen column mapping
- physical specimen identifier: `nrel_id`
- measurement timestamp: `measdatetime`
- instrument/platform label: `tracer`
- measurement side: `Side`
- technology: `Technology`
- field/control descriptor: `Control-Field` (descriptive only; it does **not** create the Qatar matched-control design)
- primary power endpoint: `Pmax_VTIF_Corr`
- secondary raw-power sensitivity: `tracer_pmax`
- source correction flag/context: `corrected_to_temperature`
- source correction factor: `Correction Factor`

`Pmax_VTIF_Corr` is primary because the source itself supplies the corrected endpoint; the choice is fixed before outcome summaries. `tracer_pmax` is retained only as a raw-measurement sensitivity.

## Frozen specimen-side and epoch scope
Comparisons are performed only within the same physical **`nrel_id × Side`** unit. Front, rear, and mono measurements are never pooled or substituted for one another. If one side is absent at an endpoint, that specimen-side contrast is not calculable even when another side exists for the same physical module.

The prespecified contrasts remain 2019→2024 (primary), 2019→2022, and 2022→2024 (secondary). Rows from 2018 and 2020 are retained in the source archive and lineage ledger but are excluded from these contrasts because those epochs were not prespecified. They are not used to fill a missing endpoint.

Within a specimen-side-year-instrument state, repeated sweeps are summarized by the median only when they refer to the same documented measurement state. No averaging across different instruments is used to manufacture comparability.

## Instrument bridge fixed before outcomes
A 2024 NREL PV Lifetime report documents that Spire 4600 has lower absolute accuracy than Spire 5600 and describes systematic offsets from temperature control, uniformity, spectral match, and aperture area. It further states that control modules were measured on both platforms to derive a correction factor and that Spire 4600 data plotted in that report were corrected for the simulator offset. Therefore:

- exact same instrument/procedure remains the cleanest C2 admission route;
- Spire 4600 ↔ Spire 5600 may be treated as source-documented bridged comparability **only when the DuraMAT record itself identifies/applies the relevant source correction state/factor**;
- LACSS-MSR ↔ either Spire platform remains C1 unless a separate source-documented bridge is located;
- no bridge is inferred from common laboratory ownership alone.

## Accidental transport-probe exposure note
During migration debugging, a metadata/download endpoint returned the CSV header plus an initial source row when only transport behavior was being tested. The scientific question, epoch contrasts, comparability hierarchy, primary/secondary power mapping, and contribution gate had already been frozen. No observed value from that accidental preview is used to change eligibility rules, thresholds, endpoints, or the analysis plan.
