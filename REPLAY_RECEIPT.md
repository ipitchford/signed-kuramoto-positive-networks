# Replay receipt (release 1.0.0-candidate, 27 October 2026)

Host: macOS 27 (Darwin, arm64). CPython 3.12.11; numpy 2.3.5, scipy 1.17.0, matplotlib 3.10.8 (exact pins in `requirements.txt`, run with `uv run --no-project --python 3.12 --with-requirements requirements.txt`). pdfTeX 1.40.29 (TeX Live 2026).

## Clean-copy replay

After the final corrections the package was copied to a fresh directory and run with

    python -B -I code/reproduce.py --out <new directory> --pdf

under the shared research queue (2 CPU, 2 GB). Every stage passed:

| Stage | Result |
|---|---|
| Exact certificate (`verify_attractive_embedding.py`, r = 9, 8, 7) | PASS; byte-identical to `checks/exact_kuramoto_certificate.txt` |
| Floating and random-graph checks (`kuramoto_checks.py`) | PASS; `kuramoto_edges.csv` byte-identical; `kuramoto_checks.json` also byte-identical on this host |
| Figure (`make_figures.py`) | PASS; PNG byte-identical to `figures/kuramoto_construction.png` |
| PDF build | PASS |

SHA-256 of the compared outputs:

- `checks/exact_kuramoto_certificate.txt` 45b2a441c00780d44222997efc8b4654c965c82c72e604dd9a527452f072e506
- `checks/kuramoto_edges.csv` f9e55cd8d790fe6f3f0eb232ecf21a065069a06676c45355349c8e749976664e
- `checks/kuramoto_checks.json` ea392bce0f8bfec75a985862af3c55dd07f9271909649277850771b2599d5a10

## Negative controls

`python -B -O negative_controls.py`: baseline passed (certificate reproduced, independent edge rule, independent spectra for r = 9, 8, 7, SHA256SUMS) and all nine controls were rejected: a tampered certificate, two verifier code bugs (positive instead of antipodal matchings; r = 8 in place of r = 9), a tampered edge list, a wrong edge rule, two false spectral claims, the old (incorrect) exponent of Corollary 13, and a one-byte change to the manuscript.

## Optimised mode

The scripts in `code/` use `assert`. `reproduce.py` starts each of them as a child process with `-I` and without `-O`, so their assertions stay active even when the driver itself is run with `-O`; the frozen-archive gate runs the driver in both modes. `negative_controls.py` uses explicit checks only.

## Scope

This is producer-side replay on the release host, not independent reproduction. Floating-point outputs may differ in the last digits on other platforms; only the exact certificate and the edge list are required to match byte for byte.
