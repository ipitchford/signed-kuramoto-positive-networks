#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anonymous
"""Semantic negative controls for the signed-Kuramoto realisation package.

Run from the repository root with the pinned environment:

    python -B -O negative_controls.py

Every check below is an explicit comparison, so ``python -O`` disables nothing
here.  The shipped scripts in code/ use ``assert``; they are therefore run as
child processes WITHOUT -O, so their assertions stay active.

First an unmodified baseline must pass:
  * a fresh run of code/verify_attractive_embedding.py reproduces
    checks/exact_kuramoto_certificate.txt byte for byte;
  * an independent rebuild of G_{6,9} from the edge rule (eq. (5) of the paper)
    reproduces checks/kuramoto_edges.csv exactly;
  * an independent floating-point spectrum at the cone point gives 5 zero
    eigenvalues and no positive one (r = 9), 7 zeros (r = 8) and the
    eigenvalue +1/2 twice (r = 7);
  * SHA256SUMS verifies.
Then each control injects one plausible error (a tampered result, a code bug,
a false claim or a tampered file) and must be REJECTED.  The script exits
nonzero if the baseline fails or if any control is accepted.

The repository is never modified: all work happens in temporary copies.
"""
import hashlib
import shutil
import subprocess
import sys
import tempfile
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CERT = ROOT / "checks" / "exact_kuramoto_certificate.txt"
EDGES = ROOT / "checks" / "kuramoto_edges.csv"
VERIFY = ROOT / "code" / "verify_attractive_embedding.py"


def run_verifier(source_text, workdir):
    """Run a (possibly mutated) copy of the exact verifier, assertions active."""
    script = Path(workdir) / "verify_copy.py"
    script.write_text(source_text)
    res = subprocess.run([sys.executable, "-B", "-I", str(script)], capture_output=True, text=True)
    return res.returncode, res.stdout


def edge_rule(m=6, r=9, shift=3):
    """Independent rebuild of G(K_m^-, r) in the indexing of code/kuramoto_checks.py."""
    idx = lambda i, a, k: (i * 6 + a % 6) * r + k
    edges = set()
    for i, a, k, l in product(range(m), range(6), range(r), range(r)):
        u, v = idx(i, a, k), idx(i, a + 1, l)
        edges.add((min(u, v), max(u, v)))
    for i in range(m):
        for j in range(i + 1, m):
            for a, k in product(range(6), range(r)):
                u, v = idx(i, a, k), idx(j, a + shift, k)
                edges.add((min(u, v), max(u, v)))
    return sorted(edges)


def edges_csv(edges):
    return "vertex_u,vertex_v\n" + "".join(f"{u},{v}\n" for u, v in edges)


def cone_spectrum(r, m=6):
    """Floating spectrum of the Jacobian at F(0,0,0,pi,pi,pi) on G_{m,r}."""
    edges = edge_rule(m, r)
    n = 6 * m * r
    theta = np.array([(0.0 if i < m // 2 else np.pi) + a * np.pi / 3
                      for i in range(m) for a in range(6) for _ in range(r)])
    J = np.zeros((n, n))
    for u, v in edges:
        c = np.cos(theta[v] - theta[u])
        J[u, v] += c
        J[v, u] += c
        J[u, u] -= c
        J[v, v] -= c
    return np.linalg.eigvalsh(J)


def counts(ev, tol=1e-8):
    return int((ev > tol).sum()), int((np.abs(ev) <= tol).sum())


def sha_ok(root):
    for line in (root / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(None, 1)
        name = name.lstrip("*")
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
            return False
    return True


def main():
    failures = []
    report = []
    verifier = VERIFY.read_text()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # ---------------- baseline ----------------
        code, out = run_verifier(verifier, tmp)
        base_cert = code == 0 and out == CERT.read_text()
        base_edges = edges_csv(edge_rule()) == EDGES.read_text()
        p9, z9 = counts(cone_spectrum(9))
        p8, z8 = counts(cone_spectrum(8))
        ev7 = cone_spectrum(7)
        p7 = int((np.abs(ev7 - 0.5) < 1e-8).sum())
        base_spec = (p9, z9, p8, z8, p7, counts(ev7)[0]) == (0, 5, 0, 7, 2, 2)
        base_sha = (ROOT / "SHA256SUMS").exists() and sha_ok(ROOT)
        for name, ok in [("exact certificate reproduced byte for byte", base_cert),
                         ("independent edge rule reproduces kuramoto_edges.csv", base_edges),
                         ("independent spectra: r=9 (0 pos, 5 zero), r=8 (7 zero), r=7 (+1/2 twice)", base_spec),
                         ("SHA256SUMS verifies", base_sha)]:
            report.append(("BASELINE", name, ok))
            if not ok:
                failures.append("baseline: " + name)

        # ---------------- controls (each must be rejected) ----------------
        def control(name, rejected):
            report.append(("CONTROL", name, rejected))
            if not rejected:
                failures.append("control accepted: " + name)

        # 1. tampered result: claim 4 zero eigenvalues instead of 5
        tampered = CERT.read_text().replace("5 zero", "4 zero")
        control("tampered certificate (5 zero -> 4 zero) differs from fresh output", tampered != out)

        # 2. code bug: negative edges built as positive matchings (shift 3 -> 0)
        mutated = verifier.replace("(a + 3) % 6", "(a + 0) % 6")
        c2, o2 = run_verifier(mutated, tmp) if mutated != verifier else (0, out)
        control("verifier with positive instead of antipodal cross matchings fails", mutated != verifier and (c2 != 0 or o2 != out))

        # 3. code bug: certify the wrong clone count (r = 9 -> 8)
        mutated = verifier.replace("certify(9)", "certify(8)", 1)
        c3, o3 = run_verifier(mutated, tmp) if mutated != verifier else (0, out)
        control("verifier certifying r=8 in place of r=9 fails", mutated != verifier and (c3 != 0 or o3 != out))

        # 4. tampered edge list: one edge dropped
        lines = EDGES.read_text().splitlines(keepends=True)
        control("edge list with one edge removed is rejected by the edge rule", "".join(lines[:-1]) != edges_csv(edge_rule()))

        # 5. wrong construction: shift 2 instead of 3 does not give the shipped graph
        control("edge rule with shift 2 does not reproduce the shipped edge list", edges_csv(edge_rule(shift=2)) != EDGES.read_text())

        # 6. false claim: nullity 4 at the cone point of G_{6,9}
        control("claim 'nullity 4 at the cone point' contradicted (observed %d)" % z9, z9 != 4)

        # 7. false claim: the cone point of G_{6,7} is stable (no positive eigenvalue)
        control("claim 'G_{6,7} cone point has no positive eigenvalue' contradicted", counts(ev7)[0] != 0)

        # 8. false claim (corrected statement of Corollary 13): link S^{k+1} x S^{k+1} for m = 2k+4.
        #    lem:cone gives link S^{p-2} x S^{q-2} with p = q = m/2; at m = 6 the sphere dimension is 1.
        k = 1
        m = 2 * k + 4
        control("old Corollary 13 exponent k+1 disagrees with lem:cone (p-2 = %d)" % (m // 2 - 2), (k + 1) != m // 2 - 2)

        # 9. tampered file: one byte changed in a copy of the manuscript source
        copy = tmp / "pkg"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        tex = next(copy.glob("*.tex"))
        tex.write_bytes(tex.read_bytes().replace(b"324", b"325", 1))
        control("SHA256SUMS rejects a one-byte change in the manuscript", not sha_ok(copy))

    for kind, name, ok in report:
        verdict = ("PASS" if ok else "FAIL") if kind == "BASELINE" else ("REJECTED" if ok else "ACCEPTED")
        print(f"{kind:8s} {verdict:8s} {name}")
    if failures:
        print("NEGATIVE CONTROLS FAILED:", *failures, sep="\n  ")
        return 1
    print(f"All {sum(1 for k, _, _ in report if k == 'CONTROL')} controls rejected; baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
