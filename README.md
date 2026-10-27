# Signed Kuramoto networks inside positive ones

**An exact realisation theorem, stable non-manifold equilibria, and Sclosa's closed-manifold conjecture**

Unrefereed AI-assisted research candidate, version `1.0.0-candidate`.
DOI [10.5281/zenodo.23690073](https://doi.org/10.5281/zenodo.23690073) (concept DOI 10.5281/zenodo.23690072).
Creator: Anonymous. Text CC0-1.0; code MIT ([LICENSES.md](LICENSES.md)).
Release page: https://evidencepress.org/releases/signed-kuramoto-positive-networks/

Manuscript: [signed_kuramoto_networks_inside_positive_ones.pdf](signed_kuramoto_networks_inside_positive_ones.pdf) (18 pages), LaTeX source [signed_kuramoto_networks_inside_positive_ones.tex](signed_kuramoto_networks_inside_positive_ones.tex).

## In plain English

Picture many identical oscillators (clocks, pendulums, or generators) that nudge one another. If every link pulls neighbours *towards* each other (positive, attractive coupling), one might expect the resting states the network can settle into to be tidy. This package shows two things:

1. **Repulsion can be simulated by attraction.** Any network with links of strength +1 and −1 sits exactly inside a larger network whose links are all +1. Everything near any resting state, including whether it is stable, carries over unchanged.
2. **Stable resting states can form a cone.** Using (1), a 324-oscillator network with only attractive links has a whole continuum of stable resting states that, at one point, is shaped like a cone over a torus rather than a smooth surface.

The cone answers a question raised by D. Sclosa (Conjecture 1.3 of his 2023 paper). **Exactly which readings are refuted:** the published wording (the equilibrium set is a finite union of *closed* manifolds), the countable version of it, the version allowing *immersed* compact pieces, and pieces that are only closed relative to the equilibrium set or the stable set. **The literal arXiv v1 wording** ("a finite union of manifolds", with no "closed") **is true** for every graph, by the standard stratification of real algebraic sets; so is the version allowing manifolds with boundary. All phenomena occur at exact symmetric resonances and are destroyed by generic perturbation.

## Main results (see [CLAIMS.json](CLAIMS.json))

- **Theorem 1 (realisation).** Every ±1 signed simple graph H with maximum degree Δ is realised exactly on an invariant torus of a positive unweighted graph G(H, r), r > 4Δ, with 6nr vertices. Complete equilibrium germs, Lyapunov stability, Morse index and nullity transfer.
- **Theorem 2.** A connected 23-regular graph G_{6,9} on 324 vertices and 3726 edges has a stable equilibrium whose equilibrium germ is ℝ × C(S¹ × S¹). Neither the equilibrium set nor the stable set is a countable union of closed embedded manifolds or of immersed compact manifolds.
- **Theorem 3.** On K_n the equilibrium set is a finite (equivalently countable) union of closed embedded manifolds, or a countable union of immersed compact manifolds, if and only if n is odd or n ≤ 4.
- **Applications.** Stable cones ℝ × C(S^k × S^k) for every k ≥ 1 (Corollary 13), stable crossing tori on 120 vertices (Corollary 14), stable smooth continua of every dimension (Corollary 15), a 36-vertex weighted version (Remark 16).

## Reproduce (Python 3.12, pinned in `.python-version`; packages pinned in `requirements.txt`)

    shasum -a 256 -c SHA256SUMS
    uv run --no-project --python 3.12 --with-requirements requirements.txt \
        python -B -I code/reproduce.py --out /path/to/new/output --pdf
    uv run --no-project --python 3.12 --with-requirements requirements.txt \
        python -B -O negative_controls.py

Every script writes only inside `--out`. `reproduce.py` compares the exact certificate and the
edge list byte for byte with `checks/`; floating-point diagnostics are platform dependent and are
reported, not compared. The shipped scripts use `assert`, so run them without `-O`
(`negative_controls.py` uses explicit checks and is safe under `-O`). Release replay: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md).

## Contents

- `code/verify_attractive_embedding.py`: exact integer eigenbasis certificate at the cone point of G_{6,r} (r = 9, 8, 7).
- `code/kuramoto_checks.py`: G_{6,9} checks; realisation theorem on random signed graphs; repulsive K_m lifts (m = 4, 5, 6, 8); 36-vertex weighted variant; energy sampling.
- `code/make_figures.py`: construction figure (`figures/`).
- `code/reproduce.py`: runs everything into a new directory and compares with `checks/`.
- `negative_controls.py`: baseline plus nine semantic negative controls.
- `checks/`: outputs of the current revision. `checks/shipped_v1/`: outputs of the original submission, kept for comparison.
- `REVISION_RESPONSE.md`: point-by-point record of the objections raised in internal AI-assisted review and the changes made in response.
- `FINAL_FIXES.md`: fresh-context check of the four corrections made in the final editorial round.
- [STATUS.md](STATUS.md), [ASSURANCE.md](ASSURANCE.md), [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [PROVENANCE.md](PROVENANCE.md), [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [AI_INDEX.md](AI_INDEX.md), [ENVIRONMENT.txt](ENVIRONMENT.txt).

## Assurance boundary

Written proofs; exact integer certificates at explicit points; producer-side replay from a clean copy; internal AI-assisted review (five roles), two automated correctness reviews, a targeted proof audit, a verification re-review and a fresh-context check of the final corrections. This is **not** peer review, independent reproduction or formal verification. Novelty rests on a bounded literature search. See [ASSURANCE.md](ASSURANCE.md).
