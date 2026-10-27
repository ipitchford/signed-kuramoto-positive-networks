# Response to reviewers: merged fix list

Reviewer IDs: **EIC** (editor), **METH** (methodology), **DOM** (domain), **PERSP** (perspective), **DA** (devil's advocate), **SOL** (independent correctness review).
Format: **R** = the reviewer's point, **A** = our response, **C** = the change made. Section, lemma and theorem numbers refer to the revised PDF.

## 1. Conjecture framing

1. **R** (DOM C1, METH M1, EIC M2, DA M1): "Refutes Conjecture 1.3" depends on an unquoted reading. arXiv v1 omits "closed".
   **A** Agreed. We checked both source texts. arXiv:2207.08182v1 reads "a finite union of manifolds". The SIADS version of record (22(4), p. 3269) reads "a finite union of closed manifolds".
   **C** §1.2 quotes both wordings word for word. Table 1 classifies five readings. The literal v1 reading is stated to be true by stratification, and the reading allowing boundaries is true by triangulation (both citing BCR). The refuted readings are: closed embedded (the published wording), relatively closed, and immersed compact pieces. The abstract no longer says "refutes" without qualification.
2. **R** (DA M1, Ignored path 1): Extend the obstruction to immersed or branched pieces.
   **A** Done, with a full proof.
   **C** New Lemma 9 (immersed-cover obstruction) is proved in full. It feeds Corollary 10, Theorem 3(iii) and Theorem 2.
3. **R** (EIC M2): Manifolds with boundary also fail.
   **A** *Rejected.* Compact manifolds with boundary or corners always suffice: every compact semialgebraic set is triangulable, and closed simplices are such manifolds.
   **C** Table 1 records this reading as true.

## 2. Structure and significance

4. **R** (EIC M1, DOM M2, DA M2 and Unexamined premise): Lead with the realisation theorem and add applications.
   **A** Agreed.
   **C** Theorem 1 is now the realisation theorem. Theorem 2 is presented as its application. The classification moved to Theorem 3 and §5 and is described as a short corollary that builds on Burns et al. New results: Corollary 5 (spectral transfer: Morse index and nullity), Corollary 13 (stable cones of every even order), Corollary 14 (stable crossing tori on 120 vertices) and Corollary 15 (stable smooth continua; prior work by Sclosa is credited). Each is certified in `kuramoto_checks.py`.
5. **R** (DOM M3, EIC minor): Confirm the Burns et al. section numbers.
   **A** Checked against the v3 PDF. §16 is "The singularities of V^max" and Theorem 16.1 gives the blow-up S_p = S^{d-2} × S^{d-2}.
   **C** The citation now gives the version, section and theorem. The text says Theorem 16.1 describes tangent directions, and that Lemma 7 gives a self-contained local homeomorphism (in the final round this is no longer claimed as new).
6. **R** (EIC M3, SOL §8): Check priority against coupled-cell, quotient-network and graph-cover theory.
   **C** §7.4 adds a paragraph comparing the work with Stewart–Golubitsky–Pivato, Golubitsky–Stewart–Török and Golubitsky–Stewart. It concedes that the invariance step is of the same type as their results and is not new. It limits the novelty claim to the normal bound, Lemma 4 and Corollary 5. It also states that the check was at the level of main definitions and theorems. A comparison table was added (SOL §8, PERSP R8).

## 3. Proofs

7. **R** (DA M3, SOL 2.1–2.2): Write out the energy inequality at degenerate points, and state Absil–Kurdyka precisely.
   **C** New Lemma 4 (normal coercivity) gives explicit constants ρ = μ/(8D) and μ/4, an explicit Hessian Lipschitz bound and Taylor's formula with integral remainder, and no nondegeneracy assumption. Its radial inequality replaces the implicit-function argument. §2.4 states the Absil–Kurdyka theorem, explains how it applies on the torus, and defines non-strict minima.
8. **R** (DA m3, METH m2, PERSP R7): Expand the proof of the cone lemma.
   **C** Lemma 7 is restated and its proof expanded: the graph over the base, an explicit homeomorphism and inverse, the submersion argument, and openness, density and connectedness, including for smaller neighbourhoods.
9. **R** (DA m1, EIC 9, SOL 3.2): "Sharp r = 9" is wrong. r = 8 is degenerate and r = 7 is unstable.
   **A** Sharpness is not proved.
   **C** Remark 12: r = 9 is *sufficient*. A proof is given that r ≤ 7 is unstable (positive eigenvalue +1/2). The case r = 8 is degenerate and stated as open. The exact certificate now checks r = 7 and r = 8.
10. **R** (DA m2, DOM m4, EIC 6, PERSP): The 36-vertex weighted claim is unproved.
    **C** Remark 16 now carries a proof (bound 4 − K/2, Lemma 4 with weighted degree). The case K = 9 is certified numerically.
11. **R** (METH m1): The scope of "generic lengths" is wrong.
    **C** §7.1 now reads: "no equal-sum partition of any sizes". Partitions with p or q ≤ 2 give singular points but not the obstruction.
12. **R** (SOL 1.1, 4): Lemma 8's hypotheses (U open and dense in W, finite-dimensional pieces, the interior O, the choice of X) are loose.
    **C** Lemma 8 restated as SOL proposed. The proof of Theorem 2 names X = E_G or X = S_G explicitly.
13. **R** (SOL 1.2): Name the point o.
    **C** §3.3 sets o = (0, vertex) and states that the link is ΣL.
14. **R** (SOL 1.4, EIC 4): Expand the n = 4 case.
    **C** §5 defines T_{12|34}, T_{13|24}, T_{14|23}, explains the identity conj(e_k) = e_{4−k}/e_4 and repeated roots, and lists the remaining aligned circles.
15. **R** (SOL 3.1, METH m3): Show that the stable set equals the equilibrium set near the vertex.
    **C** The proof of Theorem 2 states S_G ∩ O = E_G ∩ O.
16. **R** (DA m4, EIC 3): Clarify the role of homology.
    **C** §3.3 says homology only shows that o is not a manifold point.
17. **R** (DOM m1, m2, m3): Compactness; the count 2^{n−1}; the case Δ = 0.
    **C** Compactness and the 2^{n−1} count (up to global flip) are now stated. The Δ = 0 case is covered by the general statement and needs no change.
18. **R** (DA m6): K_{3,3}.
    **C** §5 states that smaller non-complete graphs are not determined.
19. **R** (DA Ignored path 3): Why Z_6?
    **A** Noted. The ±π/3 cancellation and the shift by 3 explain it, and the figure shows this. No separate proposition was added.

## 4. Computation and reproducibility

20. **R** (METH m6): Theorem 1 has no computational check.
    **C** `kuramoto_checks.py` §2 covers 10 random connected signed graphs and 296 equilibria (indices 0–5, nullities 1–2). It checks counts, invariance, the energy identity, J(TM) ⊂ TM, the normal bound and the spectral transfer (tangent minus base ≤ 1.3e−14). It also checks nearby balanced points of K_6.
21. **R** (METH m4): 3.5e−14 is a platform-dependent figure.
    **C** The paper now states a bound of 1e−12 and says the observed error is of order 1e−14 and depends on the platform. The JSON records both.
22. **R** (METH m5): reproduce.py overwrote the shipped evidence, Python was not pinned, and the Kuramoto checks were coupled to unrelated code.
    **C** `reproduce.py --out DIR` is required and refuses `checks/` and `figures/`. It compares results byte for byte with the shipped files. Python is pinned to 3.12 via `.python-version` and the README command. The Kuramoto checks are now separate (`kuramoto_checks.py`); unrelated code is not shipped.
23. **R** (SOL 5, DA m7, PERSP, EIC 8): Scripts are not linked or archived.
    **C** A Code and data declaration and §6 name all scripts. They ship in the bundle.
24. **R** (EIC 7): The PDF/PNG figure mismatch.
    **C** The adjacency-matrix figure was replaced by a construction figure built by `make_figures.py`.

## 5. Literature

25. **R** (DOM M1, PERSP): Missing synchronisation-landscape and identical-oscillator literature.
    **C** Added Taylor (0.9395), Ling–Xu–Bandeira (0.7929), Kassabov–Strogatz–Townsend (0.75), Townsend–Stillman–Strogatz (≈0.68), Wiley–Strogatz–Girvan, Watanabe–Strogatz, Ashwin–Burylko–Maistrenko and Ashwin–Swift. Every entry was checked against Crossref, and the thresholds against the arXiv abstracts. §7.3 places the density of 23/323 ≈ 0.071 relative to these results, and §7.2 distinguishes Watanabe–Strogatz degeneracy from the balance cone.
26. **R** (DOM M2): Kapovich–Millson and Farber.
    **C** Kapovich–Millson was added (DOI checked on Crossref). Farber was not added, because no verified record was obtained.
27. **R** (DOM m5, DA m5, METH m7): Years and arXiv IDs.
    **C** HSS: online 2025, issue 2026. Sclosa 2025: online 2024, with arXiv:2308.08311. Sclosa 2023: arXiv:2207.08182. arXiv IDs were added for Taylor, LXB, KST and TSS.
28. **R** (PERSP): Delabays–Coletta–Jacquod, Dörfler–Chertkov–Bullo, Okuda, Nixon et al., and Ising machines.
    **A** Delabays–Coletta–Jacquod was added in the final round (see §7). Others *not added.* They were outside the requested list and we did not verify them. The power-grid caveat is stated explicitly in §1 and §7.1.

## 6. Readability

29. **R** (PERSP R1, EIC 1): The abstract.
    **C** Rewritten. It opens with why the question matters, gives one sentence per result, includes the robustness caveat, and drops the list of methods.
30. **R** (PERSP R3, R5, R6, R4, R9, R10): Intuition, why stability is surprising, a construction figure, a roadmap, notation, and practical meaning.
    **C** Added "The picture", "Why a stable singularity is surprising", an early "caveat about scope", the roadmap, Figure 1 and the practical note after the proof of Theorem 2. Notation was changed: θ⋆ for the equilibrium, \mathrm{i} for the imaginary unit, Γ for the Gram matrix.
31. **R** (PERSP R2, DOM m6, EIC 2): The Status paragraph and evaluative status wording.
    **C** Removed. A Declarations section was added (author Anonymous, AI provenance). The shipped files contain no such wording, and internal audit folders are not shipped.

## 7. Final editorial round (27 October 2026)

A targeted proof audit, an independent correctness review and a traceability re-review found the following; each was corrected before release.

- Corollary 13 (stable cones): the germ is R × C(S^k × S^k) for m = 2k+4 (the previous S^{k+1} exponent was wrong); abstract and introduction now agree.
- Corollary 14 (crossing tori): Lemma 7's chart and Morse part is now stated and proved for p, q ≥ 2 (two crossing lines when p = q = 2); "transversally" replaced by a clean intersection along the aligned circle; explicit open-and-closed argument added. The same argument was added to Corollary 15.
- Proposition 11: conclusion (c) is restated with the bound −(r/2 − m + 2).
- Lemma 9 (immersed covers): the dimension step now uses invariance of dimension on the open set f^{-1}(G); the lemma is applied to both the equilibrium set and the stable set in Theorem 2, whose statement now covers both.
- Remark 16: weighted version of Lemma 4 stated and proved (D_w = 2K+5).
- Novelty wording: the local homeomorphism of Lemma 7 is no longer claimed as new; the realisation priority claim is stated conditionally; the comparison table now agrees with the priority paragraph.
- Figure 1(c) labels enlarged; files renamed to match the title; Delabays–Coletta–Jacquod (J. Math. Phys. 58, 032703, 2017) cited.

## 8. Not done (out of scope for one round)

- The minimal vertex count, settling r = 8, robustness and unfolding, noise simulations, and an extension to the Sakaguchi model (all reviewers' extension lists). Each is stated as open or left out.
- An exhaustive topology-literature search for the Baire / invariance-of-domain argument (SOL §6). The novelty claim for Theorem 3 is phrased as an application.
