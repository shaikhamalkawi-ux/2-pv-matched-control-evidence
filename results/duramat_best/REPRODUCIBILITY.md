# DuraMAT BEST external comparability reproduction

This folder contains the complete public-data ledger set used for the Paper 2 AC3 external metrology/comparability stress test. Qatar restricted data are not stored here.

## Public source

- DOI: `10.21948/2462712`
- Admitted CSV SHA-256: `e6e88f3948008fd2ac6bdf52007b7cee16ee334f78db07c633826188fe4e8713`
- Admitted rows: `99`

Download the public file using `../../external_data/download_duramat_best.py` or the acquisition information in `../../external_data/ACQUISITION_NOTE_DURAMAT_BEST.md`.

## Reproduce

```bash
python results/duramat_best/reproduce_duramat_best_analysis.py \
  path/to/2019-2024-iv-curves-blind.csv \
  --out reproduced_duramat_best
```

The implementation reproduces the frozen `nrel_id × Side` scope and does not create a new endpoint. The prespecified corrected endpoint is `Pmax_VTIF_Corr`; because that source field is empty throughout the admitted resource, corrected directional inference is not made. `tracer_pmax` is retained only as a raw metrology/comparability sensitivity diagnostic.

## Claim boundary

The external case supports the distinction between a numerically calculable change and a scientifically interpretable direction. It does **not** establish module degradation, improvement, causal ageing, or a matched-control result for the Qatar modules.
