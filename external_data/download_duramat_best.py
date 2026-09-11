"""Download the public NREL/DuraMAT BEST repeated I-V dataset.

Authoritative project DOI: 10.21948/2462712
Resource: 2019-2024 IV Curves BLIND.csv

The downloaded file is an external metrology/comparability stress-test source.
It must not be treated as a Qatar matched-control dataset without documented
structural and procedural equivalence.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import urllib.request

URL = (
    "https://datahub.duramat.org/dataset/7cdfed1b-7571-4b28-958e-c62e8f67139b/"
    "resource/4b1b201a-d866-4f52-ac6f-6989f7a376df/download/"
    "2019-2024-iv-curves-blind.csv"
)
OUT = Path("2019-2024-iv-curves-blind.csv")


def main() -> None:
    urllib.request.urlretrieve(URL, OUT)
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"saved: {OUT}")
    print(f"bytes: {OUT.stat().st_size}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
