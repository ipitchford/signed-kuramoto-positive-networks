# Review summary (public, AI-assisted)

All review in this package is internal and AI-assisted. It is not peer review. This summary keeps the substantive objections and their dispositions; the point-by-point record is `REVISION_RESPONSE.md`.

## Round 1: five review roles and an automated correctness review

Main objections and what changed:
- The refutation of Conjecture 1.3 depended on an unquoted reading; arXiv v1 omits "closed". **Changed:** both wordings quoted verbatim; five readings classified; the literal v1 reading stated to be true.
- Extend the obstruction to immersed or branched pieces. **Changed:** new Lemma 9.
- Manifolds with boundary also fail. **Rejected, with reason:** compact semialgebraic sets are triangulable, so this reading is true.
- Lead with the realisation theorem; priority against coupled-cell theory. **Changed:** Theorem 1 is the realisation; the invariance step is conceded to be of known type.
- Energy inequality at degenerate points; precise Absil–Kurdyka statement. **Changed:** Lemma 4 with explicit constants.
- "Sharp r = 9" was wrong. **Changed:** r = 9 sufficient, r ≤ 7 unstable, r = 8 open.
- Reproducibility: unpinned Python, evidence overwritten by the reproduction script. **Changed:** pinned environment; `--out` required; byte comparison.
- Missing synchronisation-landscape literature. **Changed:** added and verified.

## Round 2 (final, 27 October 2026): proof audit, second correctness review, re-review

The re-review traced every required change to the manuscript and found three minor issues. The proof audit and the correctness review found:
- **Corollary 13 was wrong as stated** (sphere exponent off by one). Corrected to ℝ × C(S^k × S^k) for m = 2k+4.
- **Lemma 9 (immersed covers): a material gap.** Invariance of domain was misapplied in the dimension step. Repaired with invariance of dimension on an open set; the lemma is now also applied to the stable set.
- **Corollary 14 used Lemma 7 outside its hypotheses (p = q = 2),** and "transversally" was false in the ambient torus. Lemma 7's chart part now covers p, q ≥ 2; the intersection is described as clean; an explicit open-and-closed argument was added (also to Corollary 15).
- **Proposition 11(c) imported the wrong spectral constant.** Restated with −(r/2 − m + 2).
- Weighted coercivity in Remark 16 was an unstated extension. Now stated and proved.
- Novelty wording: the local homeomorphism is no longer claimed as new; the realisation priority claim is conditional; the comparison table now agrees with the priority paragraph.
- Re-review items: figure labels enlarged, files renamed, Delabays–Coletta–Jacquod cited.

A fresh-context AI check then confirmed that the four corrected items hold (`FINAL_FIXES.md`). No counterexample to the main construction was found by any review.
