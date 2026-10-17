"""Independent integer verifier. Does not import the certificate constructor."""
from fractions import Fraction
from math import gcd
from functools import reduce

def det(A):
    A = [[Fraction(x) for x in row] for row in A]
    ans = Fraction(1)
    for i in range(len(A)):
        k = next((j for j in range(i, len(A)) if A[j][i]), None)
        if k is None:
            return 0
        if i != k:
            (A[i], A[k]) = (A[k], A[i])
            ans = -ans
        pivot = A[i][i]
        ans *= pivot
        for j in range(i + 1, len(A)):
            factor = A[j][i] / pivot
            for l in range(i + 1, len(A)):
                A[j][l] -= factor * A[i][l]
    if not ans.denominator == 1:
        raise AssertionError()
    return int(ans)

def verify(C):
    def integral_tree(x):
        if isinstance(x, dict):
            return all(isinstance(k, str) and integral_tree(v) for k, v in x.items())
        if isinstance(x, list):
            return all(integral_tree(v) for v in x)
        return type(x) is int
    try:
        if not integral_tree(C):
            return False
        (d, m, a, D, S, T, y, w) = (C[k] for k in ('d', 'm', 'a', 'D', 'S', 'T', 'y', 'w'))
        if not all((type(x) is int for x in (d, m, a, D, S, T, y, w))):
            raise AssertionError()
        if not (d > 0 and m > 0 and (D > 0) and (d == m * m * D) and (gcd(a, m) == 1) and (abs(2 * a) <= m)):
            raise AssertionError()
        if not (S == D * a * a and T >= 1 and (T * (T + 1) >= S) and (T == 1 or (T - 1) * T < S)):
            raise AssertionError()
        if not (S == T * y + w and 0 <= y <= T and (0 <= w <= T)):
            raise AssertionError()
        c = C['c']
        basis = C['kernel_basis']
        if not (len(c) == 5 and len(basis) == 4 and all((len(v) == 5 for v in basis))):
            raise AssertionError()
        if not all((type(x) is int for v in basis + [c] for x in v)):
            raise AssertionError()
        G = [[0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, -2 * d]]

        def pairing(v, w):
            return sum((v[i] * G[i][j] * w[j] for i in range(5) for j in range(5)))
        if not c == [m * T, m * y, m, m * w, a]:
            raise AssertionError()
        if not pairing(c, c) == 0:
            raise AssertionError()
        if not reduce(gcd, map(abs, c)) == 1:
            raise AssertionError()
        Gc = [sum((G[i][j] * c[j] for j in range(5))) for i in range(5)]
        if not reduce(gcd, map(abs, Gc)) == m:
            raise AssertionError()
        if not 2 * d * c[4] // m % (2 * d) == 2 * d * a // m % (2 * d):
            raise AssertionError()
        if not max(map(abs, c)) == m * T:
            raise AssertionError()
        (P, Q) = (C['P'], C['Q'])
        if not det(P) == det(Q) == 1:
            raise AssertionError()

        def action(v):
            X = [[v[0], v[2]], [-v[3], v[1]]]
            out = [[sum((P[i][j] * X[j][k] * Q[k][l] for j in range(2) for k in range(2))) for l in range(2)] for i in range(2)]
            return [out[0][0], out[1][1], out[0][1], -out[1][0], v[4]]
        E = [[int(i == j) for i in range(5)] for j in range(5)]
        F = [action(e) for e in E]
        if not all((pairing(F[i], F[j]) == G[i][j] for i in range(5) for j in range(5))):
            raise AssertionError()
        if not det([list(row) for row in zip(*F)]) == 1:
            raise AssertionError()
        if not (C['seed'] == [m, m * S, 0, 0, a] and action(C['seed']) == c):
            raise AssertionError()
        if not basis[0] == c:
            raise AssertionError()
        expected = [[0, 0, 0, 0], [0, -2 * D, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
        if not [[pairing(v, w) for w in basis] for v in basis] == expected:
            raise AssertionError()
        B = [list(row) for row in zip(*basis)]
        cof = [(-1) ** i * det(B[:i] + B[i + 1:]) for i in range(5)]
        normal = [x // m for x in Gc]
        if not (cof == normal or cof == [-x for x in normal]):
            raise AssertionError()
        (u, v) = C['bezout']
        if not m * v - a * u == 1:
            raise AssertionError()
        return True
    except (AssertionError, KeyError, TypeError, ZeroDivisionError, ValueError, IndexError, StopIteration):
        return False
if __name__ == '__main__':
    import json, sys
    total = 0
    with open(sys.argv[1]) as f:
        for line in f:
            total += 1
            if not verify(json.loads(line)):
                raise SystemExit(f'Invalid certificate {total}')
    print(f'Verified {total} certificates')
