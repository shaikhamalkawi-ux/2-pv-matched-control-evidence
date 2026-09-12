# DuraMAT live-source status — 2026-09-12

The measurement-interpretability audit was executed against the previously locked public DuraMAT BEST source file `2019-2024-iv-curves-blind.csv`, SHA-256 `e6e88f3948008fd2ac6bdf52007b7cee16ee334f78db07c633826188fe4e8713` (99 data rows).

A fresh GitHub Actions acquisition attempt on 2026-09-12 could not reproduce that binary from the provider URL: the HTTPS certificate chain reported an expired certificate, and a certificate-bypass `curl -k -L` attempt returned a 1,042-byte non-source response whose SHA-256 did not match the locked source. The workflow correctly rejected that response before analysis.

This is an upstream live-acquisition issue, not evidence against the locked analysis. No substitute binary was admitted and no raw source file is committed to this repository. Derived audit outputs in this directory are tied to the locked SHA-256 above.
