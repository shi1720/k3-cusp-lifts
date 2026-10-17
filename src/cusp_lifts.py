"""Exact labelled lifts in 2U + <-2d>. All production arithmetic is integral.

Coordinates are (x1,y1,x2,y2,z); norm = 2*x1*y1+2*x2*y2-2*d*z*z.
The two negative E8 summands are fixed and omitted from certificates.
"""
from math import gcd, isqrt
from functools import reduce


def egcd(a, b):
    """Return g,s,t with s*a+t*b=g>=0."""
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r, old_s, s, old_t, t = r, old_r-q*r, s, old_s-q*s, t, old_t-q*t
    if old_r < 0:
        return -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def threshold(S):
    """Smallest positive T such that T*(T+1)>=S; no floating point."""
    if S < 0:
        raise ValueError('S must be nonnegative')
    t = max(1, (isqrt(1+4*S)-1)//2)
    return t + (t*(t+1) < S)


def centered(a, m):
    a %= m
    return a if 2*a <= m else a-m


def pair(d, v, w):
    return v[0]*w[1]+v[1]*w[0]+v[2]*w[3]+v[3]*w[2]-2*d*v[4]*w[4]


def div(d, v):
    return reduce(gcd, [abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3]), abs(2*d*v[4])])


def height(v):
    return max(map(abs, v))


def mm(A, B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def transform(v, P, Q):
    M = [[v[0], v[2]], [-v[3], v[1]]]
    N = mm(mm(P, M), Q)
    return [N[0][0], N[1][1], N[0][1], -N[1][0], v[4]]


def certificate(d, m, a):
    if not all(type(x) is int for x in (d,m,a)) or d < 1 or m < 1 or d % (m*m) or gcd(a,m) != 1:
        raise ValueError('require d>0, m>0, m^2|d and gcd(a,m)=1')
    a = centered(a,m)
    D = d//(m*m)
    S = D*a*a
    T = threshold(S)
    y = min(T, S//T)
    w = S-T*y
    seed = [m, m*S, 0, 0, a]
    P, Q = [[1,0],[y,1]], [[T,1],[-1,0]]
    c = transform(seed, P, Q)
    g, s, t = egcd(m,a)
    assert g == 1
    u, v = -t, s  # m*v-a*u=1
    b = [u, -D*a*a*u+2*m*D*a*v, 0, 0, v]
    basis = [c, transform(b,P,Q), transform([0,0,1,0,0],P,Q), transform([0,0,0,1,0],P,Q)]
    return {'d':d,'m':m,'a':a,'D':D,'S':S,'T':T,'y':y,'w':w,'seed':seed,'P':P,'Q':Q,'c':c,'kernel_basis':basis,'bezout':[u,v]}


def labels(d, unoriented=False):
    """Generate (m,a), using square-divisor search, no factorization oracle."""
    for m in range(1,isqrt(d)+1):
        if d % (m*m):
            continue
        for a in range(m):
            if gcd(a,m)==1 and (not unoriented or a <= (-a)%m):
                yield m,a


def exact_fixed_z(d,m,a):
    """Minimum height in 2U+<-2d> at centered z=a (small inputs only).

    Enumerates pairs with a product table. Divisibility m is checked exactly.
    Search stops at the certified chart upper bound.
    """
    a = centered(a,m)
    S = (d//(m*m))*a*a
    B = 2*d*a//m
    for T in range(1,threshold(S)+1):
        products = {}
        for x in range(-T,T+1):
            for y in range(-T,T+1):
                products.setdefault(x*y, []).append((x,y))
        for p, pairs in products.items():
            if S-p not in products:
                continue
            for x,y in pairs:
                for u,w in products[S-p]:
                    if reduce(gcd,[x,y,u,w,B]) == 1:
                        return m*T, [m*x,m*y,m*u,m*w,a]
    raise ArithmeticError('certified witness was not found')
