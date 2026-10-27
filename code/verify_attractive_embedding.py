"""Exact integer certificate for the 324-vertex attractive Kuramoto example.

Run: python -I code/verify_attractive_embedding.py   (prints to stdout only)
Requires numpy only. The proof is in signed_kuramoto_networks_inside_positive_ones.tex; this independently
constructs the graph, checks equilibrium, and verifies a complete integer
eigenbasis for twice the Jacobian at the displayed singular equilibrium.
No floating-point trigonometric or eigensolver computation is used.
"""

from collections import Counter
from itertools import product

import numpy as np


def determinant_integer(matrix):
    """Bareiss determinant, with exact Python integers and row pivoting."""
    a = [[int(x) for x in row] for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def certify(r):
    """Return the exact multiplicities of the eigenvalues of 2J at p on G_{6,r}."""
    m = 6
    vertices = list(product(range(m), range(6), range(r)))
    index = {v: k for k, v in enumerate(vertices)}
    edges = set()

    def add_edge(v, w):
        edge = tuple(sorted((index[v], index[w])))
        assert edge[0] != edge[1]
        assert edge not in edges
        edges.add(edge)

    for i, a, k, ell in product(range(m), range(6), range(r), range(r)):
        add_edge((i, a, k), (i, (a + 1) % 6, ell))
    internal_count = len(edges)
    for i in range(m):
        for j in range(i + 1, m):
            for a, k in product(range(6), range(r)):
                add_edge((i, a, k), (j, (a + 3) % 6, k))

    n = len(vertices)
    adjacency = np.zeros((n, n), dtype=np.int64)
    for v, w in edges:
        adjacency[v, w] = adjacency[w, v] = 1
    assert n == 6 * m * r and internal_count == 6 * m * r * r
    assert len(edges) == 6 * m * r * r + 6 * r * m * (m - 1) // 2
    assert np.array_equal(adjacency.sum(axis=1), np.full(n, 2 * r + m - 1))

    reached, pending = {0}, [0]
    while pending:
        v = pending.pop()
        for w in np.flatnonzero(adjacency[v]):
            w = int(w)
            if w not in reached:
                reached.add(w)
                pending.append(w)
    assert len(reached) == n

    # Phases are integer multiples of pi/3.  These lookup tables represent
    # 2 cos(theta) and 2 sin(theta)/sqrt(3), respectively, without rounding.
    phases = np.array([(a + (0 if i < 3 else 3)) % 6 for i, a, k in vertices])
    cosine_twice = np.array([2, 1, -1, -2, -1, 1], dtype=np.int64)
    sine_scaled = np.array([0, 1, 1, 0, -1, -1], dtype=np.int64)
    differences = (phases[None, :] - phases[:, None]) % 6
    force_scaled = (adjacency * sine_scaled[differences]).sum(axis=1)
    assert not np.any(force_scaled)
    twice_jacobian = adjacency * cosine_twice[differences]
    twice_jacobian -= np.diag(twice_jacobian.sum(axis=1))
    assert np.array_equal(twice_jacobian, twice_jacobian.T)
    assert not np.any(twice_jacobian.sum(axis=1))

    # Exact bases for the C=ss^T eigenspaces (eigenvalues 6 and 0).
    s = np.array([1, 1, 1, -1, -1, -1], dtype=np.int64)
    base_modes = [(s, 6)]
    for j in range(m - 1):
        vector = np.zeros(m, dtype=np.int64)
        vector[j] = 1
        vector[-1] = -int(s[j] * s[-1])
        assert np.dot(s, vector) == 0
        base_modes.append((vector, 0))

    # Ring eigenvectors: vector, cosine of frequency, parity of antipodal shift.
    # Store 2*cos(frequency) to keep every calculation integral.
    ring_modes = [
        (np.array([1, 1, 1, 1, 1, 1]), 2, 1),
        (np.array([2, 1, -1, -2, -1, 1]), 1, -1),
        (np.array([0, 1, 1, 0, -1, -1]), 1, -1),
        (np.array([2, -1, -1, 2, -1, -1]), -1, 1),
        (np.array([0, 1, -1, 0, 1, -1]), -1, 1),
        (np.array([1, -1, 1, -1, 1, -1]), -2, -1),
    ]
    clone_modes = [(np.ones(r, dtype=np.int64), True)]
    for k in range(r - 1):
        vector = np.zeros(r, dtype=np.int64)
        vector[k], vector[-1] = 1, -1
        clone_modes.append((vector, False))

    # A nonzero determinant in each factor proves that the tensor product
    # provides a full basis, independently of any numerical rank test.
    factor_determinants = [
        determinant_integer(np.column_stack([item[0] for item in modes]))
        for modes in (base_modes, ring_modes, clone_modes)
    ]
    assert all(factor_determinants)

    multiplicities = Counter()
    for (base, c_eigenvalue), (ring, twice_cos, parity), (clone, is_mean) in product(
        base_modes, ring_modes, clone_modes
    ):
        vector = np.kron(np.kron(base, ring), clone)
        internal_twice = -r * (2 - twice_cos) if is_mean else -2 * r
        cross_twice = -2 * c_eigenvalue if parity == 1 else 2 * c_eigenvalue - 4
        eigenvalue_twice = internal_twice + cross_twice
        assert np.array_equal(twice_jacobian @ vector, eigenvalue_twice * vector)
        multiplicities[eigenvalue_twice] += 1

    assert sum(multiplicities.values()) == n
    return n, len(edges), factor_determinants, multiplicities


def main():
    n, n_edges, factor_determinants, multiplicities = certify(9)
    assert n == 324 and n_edges == 3726
    assert multiplicities[0] == 5
    assert sum(count for value, count in multiplicities.items() if value < 0) == 319
    assert not any(value > 0 for value in multiplicities)
    # Threshold of the linear normal estimate r > 2(m-2) = 8 (Remark 12).
    _, _, _, mult8 = certify(8)
    _, _, _, mult7 = certify(7)
    assert max(mult8) == 0 and mult8[0] == 7          # two extra (normal) zero modes
    assert max(mult7) == 1 and mult7[1] == 2          # eigenvalue +1/2, twice: unstable

    print(f"Graph: {n} vertices, {n_edges} edges, degree 23, connected, simple.")
    print("Displayed phase state: exactly zero force (integer sine certificate).")
    print(f"Factor-basis exact determinants: {factor_determinants}")
    print("Complete integer eigenbasis verified for twice the Jacobian:")
    print(dict(sorted(multiplicities.items())))
    print("Inertia: 319 negative, 5 zero, 0 positive eigenvalues.")
    print("r=8: largest eigenvalue of 2J is 0 with multiplicity 7 (5 tangent + 2 normal): degenerate.")
    print("r=7: eigenvalue +1/2 of J with multiplicity 2: the cone point is unstable.")
    print("The proof of Lyapunov stability is analytic, not inferred from this spectrum.")


if __name__ == "__main__":
    main()
