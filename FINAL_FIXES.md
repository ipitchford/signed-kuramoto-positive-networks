# Final fixes: independent check

27 October 2026

This was an AI-assisted check, by a fresh-context Claude subagent, of these four items only. It is not a full review and not human peer review.

## 1. cor:cones germ and its consistency with the abstract and introduction

**Fix:** the germ is now stated as R x C(S^k x S^k) for m = 2k+4.

**PASS.** With p = q = m/2 = k+2, lem:cone gives the link S^{p-2} x S^{q-2} = S^k x S^k and a regular part of dimension d = m-2 >= 4, which matches the corollary. The abstract ("stable cones over S^k x S^k for every k >= 1") and the introduction ("R x C(S^k x S^k) ... from G_{2k+4,r}") say the same thing.

## 2. cor:crossing: lem:cone with p = q = 2, the tangent planes and the clopen argument

**Fix:** lem:cone now covers p, q >= 2, its connectedness claims are restricted to p, q >= 3, and cor:crossing gives a direct tangent-plane check.

**PASS.** The chart, Morse-lemma and graph steps hold for p, q >= 2; when p = 2 the slice is one-dimensional and the Morse lemma still applies. Connectedness is claimed only for p, q >= 3, and the case p = q = 2 is stated separately (two crossing lines, four components). At (0,0,pi,pi), only T_{13|24} and T_{14|23} pass through the point. Their tangent planes {(a,b,a,b)} and {(a,b,b,a)} meet exactly in the diagonal, which is the tangent line of the aligned circle, so the intersection is clean. The clopen argument holds: by prop:sharper(a), F(B_4) is open, because B_4 is compact and lies at positive distance from the non-balanced aligned circles. It is also compact, and so closed in a Hausdorff space.

## 3. prop:sharper(c) bound and the (m,r) = (6,9) remark

**Fix:** conclusion (c) is now stated with the bound -(r/2 - m + 2), not the bound from thm:realisation.

**PASS.** The statement and proof use the bound computed directly, -(r/2 - m + 2), by way of the proof of cor:spectral. The remark's arithmetic is right: with Delta = 5 for K_6 and r = 9, -(r/2 - 2 Delta) = -(4.5 - 10) = +11/2.

## 4. lem:immersed Step 1, and its use in thm:stable for both E_G and S_G

**Fix:** Step 1 now derives d_j = d by invariance of dimension, and thm:stable now applies lem:immersed to both E_G and S_G.

**PASS.** In Step 1, G is open in V and V is open in U, so G is a nonempty open subset of the d-manifold U. G is also homeomorphic, through f_j restricted to the ball, to the nonempty open set f_j^{-1}(G) in the d_j-manifold B_k, so invariance of dimension gives d_j = d. The proof of thm:stable applies both lemmas with X = E_G and with X = S_G, using W = E_G ∩ O = S_G ∩ O, which is open in each X. The theorem's statement covers immersed compact covers of S_G.
