"""Floating-point and exact-integer checks for the Kuramoto realisation paper.

Usage:  python -I code/kuramoto_checks.py --out OUTPUT_DIRECTORY

Everything is written inside OUTPUT_DIRECTORY (created if needed); nothing in
the source tree is modified.  The checks support the analytic proofs in
signed_kuramoto_networks_inside_positive_ones.tex; they do not replace them.

Sections
  1. The 324-vertex graph G_{6,9}: edge rule, integer Kronecker identity,
     trace powers, floating spectrum, invariance at random phases.
  2. Theorem 1 (realisation) on random signed graphs: counts, invariance,
     energy identity, invariance of TM, uniform normal bound, and the exact
     spectral transfer of Corollary 6 at many equilibria.
  3. Applications (Corollaries 9-11): lifted repulsive K_m for m = 4, 5, 6, 8.
  4. The 36-vertex weighted variant (Remark 13).
  5. Energy sampling near the cone vertex of G_{6,9} (numerical evidence only).
"""
from pathlib import Path
import argparse
import itertools
import json
import math

import numpy as np
from scipy.optimize import least_squares

SEED = 20261027


# ---------------------------------------------------------------- graph rule
def lift_graph(n, signed_edges, r, internal_weight=1.0):
    """Adjacency of the six-ring blow-up G(H, r) built from the edge rule.

    Vertices (i, a, k), i in V(H), a in Z_6, k in 1..r, indexed (i*6+a)*r+k.
    Internal: every (i,a,k) ~ every (i,a+1,l).  Cross: (i,a,k) ~ (j,a+d,k)
    with d = 0 for a positive and d = 3 for a negative base edge.
    """
    idx = lambda i, a, k: (i * 6 + a % 6) * r + k
    N = 6 * n * r
    A = np.zeros((N, N))
    for i in range(n):
        for a in range(6):
            for k in range(r):
                for l in range(r):
                    u, v = idx(i, a, k), idx(i, a + 1, l)
                    assert A[u, v] == 0
                    A[u, v] = A[v, u] = internal_weight
    for (i, j, s) in signed_edges:
        d = 0 if s > 0 else 3
        for a in range(6):
            for k in range(r):
                u, v = idx(i, a, k), idx(j, a + d, k)
                assert A[u, v] == 0 and u != v
                A[u, v] = A[v, u] = 1.0
    return A


def lift_phases(phi, r):
    return np.array([phi[i] + a * math.pi / 3
                     for i in range(len(phi)) for a in range(6) for k in range(r)])


def field(A, theta):
    return (A * np.sin(theta[None, :] - theta[:, None])).sum(axis=1)


def jacobian(A, theta):
    W = A * np.cos(theta[None, :] - theta[:, None])
    return W - np.diag(W.sum(axis=1))


def energy(A, theta):
    return 0.5 * float((A * (1 - np.cos(theta[None, :] - theta[:, None]))).sum())


def signed_matrix(n, signed_edges):
    S = np.zeros((n, n))
    for (i, j, s) in signed_edges:
        S[i, j] = S[j, i] = s
    return S


def tangent_projector(n, r):
    basis = np.zeros((6 * n * r, n))
    for i in range(n):
        basis[i * 6 * r:(i + 1) * 6 * r, i] = 1 / math.sqrt(6 * r)
    return basis


# ------------------------------------------------------------- section 1
def g69_checks():
    m, r = 6, 9
    edges = [(i, j, -1) for i in range(m) for j in range(i + 1, m)]
    A = lift_graph(m, edges, r)
    N = len(A)
    n_edges = int(A.sum() / 2)
    assert N == 324 and n_edges == 3726 and np.all(A.sum(axis=1) == 23)
    # connectivity by breadth-first search
    seen, todo = {0}, [0]
    while todo:
        v = todo.pop()
        for w in np.flatnonzero(A[v]):
            if int(w) not in seen:
                seen.add(int(w)); todo.append(int(w))
    assert len(seen) == N
    Ai = A.astype(np.int64)
    phase = np.array([(a + (3 if i >= 3 else 0)) % 6
                      for i in range(m) for a in range(6) for k in range(r)])
    twice_cos = np.array([2, 1, -1, -2, -1, 1], dtype=np.int64)
    j2 = Ai * twice_cos[(phase[None, :] - phase[:, None]) % 6]
    j2 -= np.diag(j2.sum(axis=1))
    c6 = np.zeros((6, 6), dtype=np.int64)
    sh3 = np.zeros((6, 6), dtype=np.int64)
    for a in range(6):
        c6[a, (a - 1) % 6] = c6[a, (a + 1) % 6] = 1
        sh3[a, (a + 3) % 6] = 1
    s = np.array([1, 1, 1, -1, -1, -1], dtype=np.int64)
    Gam = np.outer(s, s)
    I = np.eye(N, dtype=np.int64)
    Im = np.eye(m, dtype=np.int64)
    formula = (np.kron(np.kron(Im, c6), np.ones((r, r), dtype=np.int64)) - 2 * r * I
               + 2 * np.kron(np.kron(Im - Gam, sh3), np.eye(r, dtype=np.int64)) - 2 * I)
    assert np.array_equal(j2, formula)
    expected = {-20.: 5, -19.5: 2, -15.: 24, -14.: 1, -13.5: 10, -11.: 120,
                -9.: 120, -6.5: 10, -6.: 1, -5.: 24, -.5: 2, 0.: 5}
    traces, P = {}, np.eye(N, dtype=np.int64)
    for k in range(1, 5):
        P = P @ j2
        obs = int(np.trace(P))
        assert obs == sum(c * int(2 * v) ** k for v, c in expected.items())
        traces[str(k)] = obs
    eig = np.linalg.eigvalsh(j2 / 2)
    exact = np.array(sorted(v for v, c in expected.items() for _ in range(c)))
    spec_err = float(np.max(np.abs(eig - exact)))
    assert spec_err < 1e-12
    rng = np.random.default_rng(SEED)
    inv = 0.0
    for _ in range(12):
        phi = rng.uniform(-math.pi, math.pi, m)
        base = -np.sin(phi[None, :] - phi[:, None]).sum(axis=1)
        inv = max(inv, float(np.max(np.abs(field(A, lift_phases(phi, r)) - np.repeat(base, 6 * r)))))
    assert inv < 1e-12
    return A, {"vertices": N, "edges": n_edges, "degree": 23, "connected": True,
               "twice_jacobian_equals_integer_kronecker_formula": True,
               "exact_trace_powers_of_2J": traces,
               "spectrum_max_abs_error_bound": "below 1e-12 (observed value is platform dependent)",
               "spectrum_max_abs_error_observed": spec_err,
               "invariance_residual_observed": inv}


# ------------------------------------------------------------- section 2
def random_signed_graph(rng, n, p_edge, max_deg):
    while True:
        edges = []
        deg = [0] * n
        for i, j in itertools.combinations(range(n), 2):
            if rng.random() < p_edge and deg[i] < max_deg and deg[j] < max_deg:
                edges.append((i, j, int(rng.choice([-1, 1]))))
                deg[i] += 1; deg[j] += 1
        # require connectivity of H
        adj = {i: set() for i in range(n)}
        for i, j, _ in edges:
            adj[i].add(j); adj[j].add(i)
        seen, todo = {0}, [0]
        while todo:
            v = todo.pop()
            for w in adj[v] - seen:
                seen.add(w); todo.append(w)
        if len(seen) == n and edges:
            return edges, max(deg)


def base_field(S, phi):
    return (S * np.sin(phi[None, :] - phi[:, None])).sum(axis=1)


def base_jacobian(S, phi):
    W = S * np.cos(phi[None, :] - phi[:, None])
    return W - np.diag(W.sum(axis=1))


def base_energy(S, phi):
    return 0.5 * float((S * (1 - np.cos(phi[None, :] - phi[:, None]))).sum())


def descend(S, phi, steps=20000, h=0.05):
    for _ in range(steps):
        f = base_field(S, phi)
        phi = phi + h * f
        if np.max(np.abs(f)) < 1e-13:
            break
    return phi


def realisation_checks():
    rng = np.random.default_rng(SEED + 1)
    reports = []
    worst = {"invariance": 0., "energy": 0., "tm_leak": 0., "spectral_transfer": 0.,
             "normal_margin_min": math.inf}
    n_equilibria = 0
    for trial in range(10):
        n = int(rng.integers(4, 8))
        edges, Delta = random_signed_graph(rng, n, 0.6, 4)
        r = 4 * Delta + 1
        A = lift_graph(n, edges, r)
        S = signed_matrix(n, edges)
        degH = np.abs(S).sum(axis=1)
        # counts
        assert A.shape[0] == 6 * n * r
        assert int(A.sum() / 2) == 6 * n * r * r + 6 * r * len(edges)
        assert np.all(A.sum(axis=1) == np.repeat(2 * r + degH, 6 * r))
        e_minus = sum(1 for e in edges if e[2] < 0)
        T = tangent_projector(n, r)
        PT = T @ T.T
        PN = np.eye(len(A)) - PT
        for _ in range(5):
            phi = rng.uniform(-math.pi, math.pi, n)
            th = lift_phases(phi, r)
            worst["invariance"] = max(worst["invariance"], float(np.max(np.abs(
                field(A, th) - np.repeat(base_field(S, phi), 6 * r)))))
            worst["energy"] = max(worst["energy"], abs(
                energy(A, th) - (3 * n * r * r + 12 * r * e_minus + 6 * r * base_energy(S, phi))))
            J = jacobian(A, th)
            worst["tm_leak"] = max(worst["tm_leak"], float(np.max(np.abs(PN @ J @ PT))))
            mu = r / 2 - 2 * Delta
            lam = np.linalg.eigvalsh(PN @ J @ PN + 1e6 * PT)  # push TM out of the way
            normal_max = float(np.sort(lam)[len(A) - n - 1])
            worst["normal_margin_min"] = min(worst["normal_margin_min"], -mu - normal_max)
            assert normal_max <= -mu + 1e-9
        # equilibria: all 2^(n-1) aligned states and several descent minima
        eq = [np.array([0.] + [math.pi * b for b in bits])
              for bits in itertools.product([0, 1], repeat=n - 1)]
        for _ in range(4):
            eq.append(descend(S, rng.uniform(-math.pi, math.pi, n)))
        idx_counts = {}
        for phi in eq:
            if np.max(np.abs(base_field(S, phi))) > 1e-10:
                continue
            JH = base_jacobian(S, phi)
            th = lift_phases(phi, r)
            J = jacobian(A, th)
            assert np.max(np.abs(field(A, th))) < 1e-10
            tangent = np.linalg.eigvalsh(T.T @ J @ T)
            base = np.linalg.eigvalsh(JH)
            worst["spectral_transfer"] = max(worst["spectral_transfer"],
                                             float(np.max(np.abs(np.sort(tangent) - np.sort(base)))))
            full = np.sort(np.linalg.eigvalsh(J))
            # inertia of the lift equals inertia of the base (Corollary 6)
            tol = 1e-9
            assert int((full > tol).sum()) == int((base > tol).sum())
            assert int((np.abs(full) <= tol).sum()) == int((np.abs(base) <= tol).sum())
            key = f"index={int((base > tol).sum())},nullity={int((np.abs(base) <= tol).sum())}"
            idx_counts[key] = idx_counts.get(key, 0) + 1
            n_equilibria += 1
        reports.append({"n": n, "edges": len(edges), "negative_edges": e_minus,
                        "Delta": Delta, "r": r, "lift_vertices": 6 * n * r,
                        "equilibria_checked_by_inertia": idx_counts})
    assert worst["invariance"] < 1e-11 and worst["energy"] < 1e-8
    assert worst["tm_leak"] < 1e-11 and worst["spectral_transfer"] < 1e-9
    return {"graphs": reports, "equilibria_checked": n_equilibria,
            "max_invariance_residual": worst["invariance"],
            "max_energy_identity_error": worst["energy"],
            "max_TM_to_N_leak": worst["tm_leak"],
            "max_tangent_vs_base_eigenvalue_difference": worst["spectral_transfer"],
            "min_margin_below_normal_bound_-(r/2-2Delta)": worst["normal_margin_min"]}


# ------------------------------------------------------------- section 3
def balanced_point(m, rng, start=None, scale=None):
    """A balanced configuration near `start`, by least squares on Z = 0."""
    x0 = rng.uniform(-math.pi, math.pi, m) if start is None else start + scale * rng.standard_normal(m)
    fun = lambda x: np.array([np.cos(x).sum(), np.sin(x).sum()])
    sol = least_squares(fun, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    assert np.max(np.abs(fun(sol.x))) < 1e-13
    return sol.x


def repulsive_lift_checks():
    rng = np.random.default_rng(SEED + 2)
    out = {}
    for m in (4, 5, 6, 8):
        r = 2 * (m - 2) + 1
        edges = [(i, j, -1) for i in range(m) for j in range(i + 1, m)]
        A = lift_graph(m, edges, r)
        T = tangent_projector(m, r)
        PT = T @ T.T
        PN = np.eye(len(A)) - PT
        bound = m - 2 - r / 2
        rec = {"r": r, "vertices": 6 * m * r, "degree": 2 * r + m - 1,
               "normal_bound_m-2-r/2": bound, "points": []}
        pts = [("random balanced", balanced_point(m, rng)) for _ in range(3)]
        if m % 2 == 0:
            aligned = np.array([0.] * (m // 2) + [math.pi] * (m // 2))
            pts.append(("aligned balanced (cone point)", aligned))
            pts += [("balanced near cone point", balanced_point(m, rng, aligned, 0.05)) for _ in range(2)]
        for label, phi in pts:
            th = lift_phases(phi, r)
            J = jacobian(A, th)
            assert np.max(np.abs(field(A, th))) < 1e-11
            ev = np.sort(np.linalg.eigvalsh(J))
            normal = np.sort(np.linalg.eigvalsh(PN @ J @ PN - 1e6 * PT))[::-1][:1]
            nul = int((np.abs(ev) < 1e-9).sum())
            assert ev[-1] < 1e-9, "no positive eigenvalue"
            assert normal[0] <= bound + 1e-9
            rec["points"].append({"type": label, "zero_eigenvalues": nul,
                                  "largest_nonzero_eigenvalue": float(ev[ev < -1e-9][-1]),
                                  "largest_normal_eigenvalue": float(normal[0])})
        out[f"K{m}"] = rec
    # expected nullities (Corollaries 9-11)
    assert all(p["zero_eigenvalues"] == 3 for p in out["K5"]["points"])            # smooth, dim m-2
    assert [p["zero_eigenvalues"] for p in out["K4"]["points"] if p["type"].startswith("aligned")] == [3]
    assert [p["zero_eigenvalues"] for p in out["K6"]["points"] if p["type"].startswith("aligned")] == [5]
    assert [p["zero_eigenvalues"] for p in out["K8"]["points"] if p["type"].startswith("aligned")] == [7]
    for key in ("K6", "K8"):
        assert all(p["zero_eigenvalues"] == int(key[1:]) - 2
                   for p in out[key]["points"] if not p["type"].startswith("aligned"))
    return out


# ------------------------------------------------------------- section 4
def weighted36_check():
    m, K = 6, 9.0
    edges = [(i, j, -1) for i in range(m) for j in range(i + 1, m)]
    A = lift_graph(m, edges, 1, internal_weight=K)
    phi = np.array([0, 0, 0, math.pi, math.pi, math.pi])
    th = lift_phases(phi, 1)
    J = jacobian(A, th)
    assert np.max(np.abs(field(A, th))) < 1e-12
    ev = np.sort(np.linalg.eigvalsh(J))
    T = tangent_projector(m, 1)
    PT = T @ T.T
    PN = np.eye(36) - PT
    normal_max = float(np.sort(np.linalg.eigvalsh(PN @ J @ PN - 1e6 * PT))[-1])
    assert abs(normal_max - (m - 2 - K / 2)) < 1e-9 and ev[-1] < 1e-9
    vals, counts = np.unique(np.round(ev, 9), return_counts=True)
    return {"vertices": 36, "internal_weight": K, "zero_eigenvalues": int((np.abs(ev) < 1e-9).sum()),
            "largest_normal_eigenvalue": normal_max,
            "spectrum": {f"{v:g}": int(c) for v, c in zip(vals, counts)}}


# ------------------------------------------------------------- section 5
def energy_sampling(A):
    rng = np.random.default_rng(SEED + 3)
    th0 = lift_phases(np.array([0, 0, 0, math.pi, math.pi, math.pi]), 9)
    E0 = energy(A, th0)
    out = {"E_at_p": E0}
    for eps in (1e-1, 1e-2, 1e-3):
        worst = math.inf
        for _ in range(200):
            d = rng.standard_normal(len(th0))
            d *= eps / np.linalg.norm(d)
            worst = min(worst, energy(A, th0 + d) - E0)
        out[f"min_energy_increase_at_radius_{eps:g}"] = worst
        assert worst > -1e-9
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    A, g = g69_checks()
    report = {"seed": SEED, "G_6_9": g, "realisation_random_signed_graphs": realisation_checks(),
              "repulsive_complete_lifts": repulsive_lift_checks(), "weighted_36_vertex": weighted36_check(),
              "energy_sampling_near_cone_vertex": energy_sampling(A)}
    edges = np.argwhere(np.triu(A) > 0)
    np.savetxt(args.out / "kuramoto_edges.csv", edges, fmt="%d", delimiter=",",
               header="vertex_u,vertex_v", comments="")
    (args.out / "kuramoto_checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
