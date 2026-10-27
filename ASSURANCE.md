# Assurance

| Dimension | State | Evidence |
|---|---|---|
| Written proofs | Complete for every stated result | Manuscript §§2–5 |
| Exact computation | Integer eigenbasis certificate of 2J at the cone point of G_{6,r}, r = 9, 8, 7 | `code/verify_attractive_embedding.py`, `checks/exact_kuramoto_certificate.txt` |
| Floating-point corroboration | Random signed graphs (296 equilibria), repulsive K_m lifts, weighted 36-vertex case, energy sampling | `code/kuramoto_checks.py`, `checks/kuramoto_checks.json` |
| Producer replay | Clean-copy rerun: certificate, edge list and JSON byte-identical; PDF rebuilt | [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md) |
| Negative controls | Baseline plus nine controls (tampered results, code bugs, false claims, tampered file), all rejected | `negative_controls.py` |
| Internal review | AI-assisted: editor, domain, methodology, perspective and devil's-advocate roles; two automated correctness reviews; targeted proof audit; verification re-review; fresh-context check of the final corrections | [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), `REVISION_RESPONSE.md`, `FINAL_FIXES.md` |
| Independent reproduction | None | — |
| External peer review | None | — |
| Formal verification | None; no proof assistant used | — |
| Novelty / priority | Bounded search only; see [RESEARCH_GATES.json](RESEARCH_GATES.json) | §7 of the paper |

The computations corroborate the proofs at explicit points; they do not replace the topological arguments or the nonlinear stability argument (Lemma 4 with Absil–Kurdyka).
Different AI roles and models are not independent human reviewers, and their agreement is not proof.

## Known limitations

- Every phenomenon sits at an exact resonance (unit weights, exact equal splits, exact symmetry); generic perturbation destroys it. Nothing here concerns heterogeneous networks such as power grids.
- The threshold r = 9 is sufficient, not shown sharp; r = 8 is open.
- The local cone homeomorphism (Lemma 7) is a self-contained derivation; an equivalent normal form may exist in the polygon-space literature.
- The invariance step of Theorem 1 is of a known coupled-cell type; the claimed novelty is the uniform normal bound and its quantitative consequences, within a bounded search.
- The coupled-cell literature (Stewart–Golubitsky–Pivato; Golubitsky–Stewart–Török; Golubitsky–Stewart) was checked at the level of main definitions and theorems only.
