# Research and claim audit — 17 October 2026

## Question and selection

The target is ICERM's *Moduli of K3 surfaces*, November 9–13, 2026, Providence, Rhode Island. Its public application is for workshop participation, with a CV and personal statement. It is not an AI conference in Seoul, has no stated proceedings-paper track, and does not publish a paper template in the inspected application. The research question was therefore chosen in the arithmetic of polarized K3 boundary components.

The working question is how to construct a small integral representative and an embedded saturated orthogonal quotient for a supplied isotropic discriminant label. Full cusp classification, geometric compactifications, and generic isotropic-vector existence were excluded as novelty claims.

## Search and inspected sources

Search families included:

- K3 moduli zero-dimensional cusps, primitive isotropic vectors, square divisors, discriminant labels, and Scattone.
- Small isotropic representatives, coordinate height, two hyperbolic planes, and lattice algorithms.
- Small zeros with congruence conditions and sublattice avoidance.
- Exact quadratic-form software and factorization-free isotropic-vector construction.

Primary sources inspected:

1. F. Scattone, *On the compactification of moduli spaces for algebraic K3 surfaces*, Memoirs AMS 70(374), 1987. Bibliographic information and chapter structure were checked; a complete freely accessible copy was not obtained. DOI: https://doi.org/10.1090/memo/0374
2. V. Gritsenko, K. Hulek, G. K. Sankaran, *Moduli of K3 Surfaces and Irreducible Symplectic Manifolds*, arXiv:1012.4155v2; Handbook of Moduli I, 2013, 459–526. Full PDF inspected, especially Lemma 7.5 and Remarks 8.8–8.9. https://arxiv.org/abs/1012.4155
3. V. Alexeev, P. Engel, *Compact moduli of K3 surfaces*, arXiv:2101.12186v3. Full PDF obtained and scope inspected. https://arxiv.org/abs/2101.12186
4. S. Ma, *On the 0-dimensional cusps of the Kähler moduli of a K3 surface*, arXiv:0812.4132v2. Full PDF obtained; its Kähler-moduli/FM-partner setting differs from the polarized period lattice here. https://arxiv.org/abs/0812.4132
5. L. Fukshansky, *Heights and quadratic forms: Cassels' theorem and its generalizations*, Contemporary Mathematics 587 (2013), 77–94. Full PDF obtained and scope inspected. https://arxiv.org/abs/1204.1938
6. P. Bandi, A. Ghosh, *Small solutions of quadratic forms with congruence conditions*, arXiv:2008.08568v2. Full PDF obtained and introduction/main-results scope inspected. https://arxiv.org/abs/2008.08568
7. L. Fukshansky, S. Jeong, *Integral zeros of quadratic polynomials avoiding sublattices*, arXiv:2409.10867v2. Full PDF obtained and main-results scope inspected. https://arxiv.org/abs/2409.10867
8. P. Castel, *Solving quadratic equations in dimension 5 or more without factoring*, Open Book Series 1 (2013), 213–234. Publisher PDF inspected. https://doi.org/10.2140/obs.2013.1.213
9. Official Sage quadratic forms documentation and OSCAR quadratic-lattice tutorial listings were inspected to establish the existing exact-computation ecosystem. No runtime performance comparison against either system was performed.

No search can certify universal absence of prior art. The manuscript does not assert that its elementary ingredients are undiscovered. The exact chart formula, explicit transport, saturation certificate, full-lattice comparison, and sharpness examples are proved directly. Whether their combination clears the novelty threshold of a research journal remains a matter for expert review.

## Claim boundaries

| Claim | Evidence | Limit |
|---|---|---|
| Exact chart height | Theorem 3.1; 1,025 independent direct minima | One hyperbolic coordinate is fixed to m |
| Correct marked representative | Explicit norm/divisibility calculation and stable isometry | Supplied label in fixed split lattice |
| Correct integral quotient | Bezout kernel proof; signed maximal minors; Gram check | Quotient type itself is classical |
| Full-lattice comparison | Theorem 5.1; negative-definiteness argument | Additive m/2 term is necessary for stated leading factor |
| Sharp leading constant | Explicit family with independently proved global minimum | Does not solve global optimization for every label |
| Five-coordinate versus full-lattice distinction | d=63 E8 example, explicit rank-21 check | Fixed simple-root coordinate bases |
| Reduced coefficient sizes | Complete d≤4096 atlas | Baseline is the direct lift, not the best existing software |
| Runtime | Recorded process-local measurements | No downstream speedup claim |
| Commercial application | Exact-computation and validation infrastructure is plausible | No market validation, revenue evidence, or patent assessment |

## Publication readiness assessment

The result is a focused computational mathematics note with proofs and reproducible certificates. Its elementary nature is a material novelty risk at a major algebraic-geometry journal. It should not be described as industry-defining, a new K3 compactification, or a high-probability acceptance. The requested ICERM submission is a participation application, not acceptance or publication of this paper. A poster or discussion contribution is more appropriate to request than an invited lecture.
