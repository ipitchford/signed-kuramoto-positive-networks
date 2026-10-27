# Agent navigation

## Identity

- Release slug: `signed-kuramoto-positive-networks`. Version `1.0.0-candidate`, tag `v1.0.0-candidate`. DOI 10.5281/zenodo.23690073; concept DOI 10.5281/zenodo.23690072.
- Repository: https://github.com/ipitchford/signed-kuramoto-positive-networks. Release page: https://evidencepress.org/releases/signed-kuramoto-positive-networks/
- Title: *Signed Kuramoto networks inside positive ones: an exact realisation theorem, stable non-manifold equilibria, and Sclosa's closed-manifold conjecture*. Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md)).
- Manuscript: [PDF](signed_kuramoto_networks_inside_positive_ones.pdf) (18 pages) and [LaTeX source](signed_kuramoto_networks_inside_positive_ones.tex). Figure: [figures/kuramoto_construction.pdf](figures/kuramoto_construction.pdf) (illustration only).
- Machine-readable claims: [CLAIMS.json](CLAIMS.json). Overview for humans: [README.md](README.md).
- Assurance limits: [ASSURANCE.md](ASSURANCE.md). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REVISION_RESPONSE.md](REVISION_RESPONSE.md), [FINAL_FIXES.md](FINAL_FIXES.md).
- Provenance: [PROVENANCE.md](PROVENANCE.md). Sources: [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json).
- Citation: [CITATION.cff](CITATION.cff) and [Zenodo metadata](.zenodo.json). Licences: [LICENSES.md](LICENSES.md), [PUBLIC_DOMAIN.md](PUBLIC_DOMAIN.md).

## Model in one paragraph

Homogeneous Kuramoto flow on a finite simple graph G: dθ_u/dt = Σ_{v∼u} sin(θ_v − θ_u), the negative gradient of E_G(θ) = Σ_edges [1 − cos(θ_v − θ_u)]. A signed graph H carries σ_ij ∈ {±1}. The lift G(H, r) has vertices (i, a, k), a ∈ ℤ_6, k ≤ r: every clone in ring group a joins every clone in group a ± 1, and a base edge joins (i, a, k) to (j, a + d_ij, k), with d = 0 for positive and d = 3 for negative edges. The torus F(φ)_{i,a,k} = φ_i + aπ/3 is invariant and carries the signed flow exactly. G_{m,r} = G(K_m^−, r).

## Scientific map

Each line: claim, status, paper location, evidence.

- **Realisation.** Germs, Lyapunov stability, Morse index and nullity transfer for r > 4Δ. *Proved.* Theorem 1, Lemma 4, Corollary 5. Checked on 10 random signed graphs and 296 equilibria by [code/kuramoto_checks.py](code/kuramoto_checks.py) ([checks/kuramoto_checks.json](checks/kuramoto_checks.json)).
- **Stable cone on 324 vertices.** Germ ℝ × C(S¹ × S¹); stable; no countable closed or immersed compact cover of the equilibrium set or the stable set. *Proved; spectrum exact.* Theorem 2, §4.2. [code/verify_attractive_embedding.py](code/verify_attractive_embedding.py), [checks/exact_kuramoto_certificate.txt](checks/exact_kuramoto_certificate.txt) (319 negative, 5 zero).
- **Sclosa's Conjecture 1.3.** Refuted: closed embedded pieces (finite or countable; the published wording), immersed compact pieces, relatively closed pieces. True: the literal arXiv v1 wording (manifolds not necessarily closed) and compact manifolds with boundary. Table 1, Theorem 3.
- **Complete-graph classification.** Closed or immersed compact cover iff n odd or n ≤ 4. *Proved.* Theorem 3, §5.
- **Applications.** Stable cones ℝ × C(S^k × S^k), m = 2k + 4 (Corollary 13); crossing tori on G_{4,5} (Corollary 14); smooth continua of every dimension (Corollary 15); 36-vertex weighted version (Remark 16). Checked at explicit points in [code/kuramoto_checks.py](code/kuramoto_checks.py).
- **Threshold.** r = 9 sufficient; r ≤ 7 unstable; r = 8 open. Remark 12; certificate covers r = 7, 8.

Do not read:
- the literal arXiv v1 wording of the conjecture as refuted (it is true);
- any phenomenon as robust to generic perturbation, or as a statement about power grids;
- r = 9 as sharp;
- Lemma 7's local homeomorphism or the invariance step of Theorem 1 as new;
- the computations as replacing the topological or stability proofs;
- internal AI-assisted review as peer review.

## Code

- [code/verify_attractive_embedding.py](code/verify_attractive_embedding.py): exact integer eigenbasis of 2J at the cone point of G_{6,r}, r = 9, 8, 7.
- [code/kuramoto_checks.py](code/kuramoto_checks.py): floating-point checks (G_{6,9}, random signed graphs, K_m lifts, weighted case, energy sampling); writes the edge list.
- [code/make_figures.py](code/make_figures.py): construction figure. [code/reproduce.py](code/reproduce.py): driver with byte comparison.
- [negative_controls.py](negative_controls.py): baseline and nine semantic negative controls.

## Replay

Python 3.12 with the pins in [requirements.txt](requirements.txt); the code uses `assert`, so do not pass `-O` to it:

```sh
shasum -a 256 -c SHA256SUMS
python -B -I code/reproduce.py --out OUT --pdf     # about 30 s
python -B -O negative_controls.py                  # under 1 minute
```

Results of the release replay: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). Environment: [ENVIRONMENT.txt](ENVIRONMENT.txt). CI: [.github/workflows/replay.yml](.github/workflows/replay.yml).

## Useful next research questions

- Is the cone point of G_{6,8} stable (degenerate normal Hessian)?
- What is the smallest positive unweighted graph with a stable non-manifold continuum?
- Does K_{3,3} or another small non-complete graph already violate the closed reading?
- Does the realisation extend to the Kuramoto–Sakaguchi model?
