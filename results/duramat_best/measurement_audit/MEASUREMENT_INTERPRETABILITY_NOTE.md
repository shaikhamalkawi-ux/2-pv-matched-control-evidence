# Measurement-Interpretability Audit

This audit is tied to the previously locked public DuraMAT BEST CSV with SHA-256 `e6e88f3948008fd2ac6bdf52007b7cee16ee334f78db07c633826188fe4e8713` (99 data rows). It is a post-baseline evidence audit, not a degradation estimate.

## Export-consistency check

Of 99 source rows, 97 contain usable sampled current and voltage vectors. Comparing the maximum sampled `I*V` value with `tracer_pmax` gives a median relative difference of +0.0067%, a 95th-percentile absolute difference of 0.287%, and a maximum absolute difference of 0.569%. This checks consistency of the public export only; it does not reconstruct the unavailable corrected endpoint and does not imply that `tracer_pmax` must equal the maximum sampled point exactly.

## Session-span check

Among 84 specimen-side/instrument/year groups, four span more than one day; the longest spans 321.9 days. These are repeated measurements within a year, not automatically same-session technical replicates. Any repeatability claim must therefore be tied to actual session metadata rather than year-level grouping alone.

## Conditional interpretation boundary

For the auxiliary multiplicative control comparison, write

`r_obs = d_field - d_control + eta`,

where `d_field` and `d_control` are physical log changes and `eta` is residual differential measurement bias. Under stated sensitivity bounds `|d_control| <= C` and `|eta| <= B`, the sign of `d_field` is guaranteed only when `|r_obs| > B + C`, with field-cohort sampling uncertainty handled separately. `B` and `C` are sensitivity axes, not measured laboratory uncertainty or confidence limits.

For the locked Qatar ratio-of-ratios diagnostics, the equivalent one-sided multiplicative sensitivity axes are approximately 0.733% (TOPCon-M2), 3.544% (SHJ-M1), 0.681% (TOPCon-M3), 0.037% (PERC-M-M4), 0.410% (PERC-M3), 0.904% (PERC-C-M4), and 3.110% (SHJ-M5).

The observed SHJ-M1 versus SHJ-M5 log-gap is 0.0042054. Under a worst-case model that permits an independent combined signed control-drift-plus-differential-measurement bound of equal magnitude for each configuration, guaranteed preservation of their observed order requires each bound to be strictly below 0.0021027 log units, approximately 0.2105% equivalent multiplicative change. This is a conditional robustness statement, not a measured uncertainty budget.

## Claim boundary

The audit does not change the Qatar calculation states, does not readmit PERC-M7, does not establish degradation or improvement, and does not isolate causal instrument effects in DuraMAT. Its value is to state what additional control/metrology evidence would be needed before a physical direction or follow-up ordering could be treated as robust.