# CuspLift: small integral lifts of K3 boundary labels

A reproducible computational research note by Shivam Gupta, Independent Researcher (2026).

The paper proves an exact coefficient-height minimum in a specified chart of the degree-2d K3 period lattice, gives an explicit stable integral isometry, constructs a saturated orthogonal-kernel basis, and proves a sharp-leading-constant comparison with the full-lattice optimum. The classical cusp classification and quotient isometry type are not claimed as new.

- [Paper PDF](paper/manuscript/main.pdf)
- [LaTeX source](paper/manuscript/main.tex)
- [Constructor](src/cusp_lifts.py)
- [Independent verifier](src/verify.py)
- [Literature and claim audit](docs/research_audit.md)
- [Recorded experimental summary](results/summary.json)

## Reproduce

Core mathematics: Python 3.9 or newer, standard library only. No API keys, external datasets, model calls, or human-subject data are needed. Run the study harness without Python's `-O` flag.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -O -m unittest discover -s tests -p 'test_*.py'
python3 tests/run_study.py
python3 tests/full_lattice_example.py
python3 src/verify.py results/certificates.jsonl
python3 src/verify.py results/stress_certificates.jsonl
```

The study regenerates descriptive timings, which vary by host. The mathematical CSV and JSONL datasets are deterministic. The committed summary records the original reference run.

For figures and PDF (Tectonic must be installed separately):

```sh
python3 -m pip install -r requirements-figures.txt
python3 paper/make_figures.py
tectonic paper/manuscript/main.tex
```

The reference figure environment used NumPy 1.26.4 and Matplotlib 3.9.4. Tectonic 0.17.0 compiled the manuscript in the reference environment (check your local version if reproducing layout).

## Minimal use

```python
import sys
sys.path.insert(0, 'src')
from cusp_lifts import certificate
from verify import verify
C = certificate(d=819, m=3, a=1)
assert verify(C)
print(C['c'])  # [30, 27, 3, 3, 1]
```

Coordinates in the five-coordinate sublattice are `(x1, y1, x2, y2, z)`, with norm `2*x1*y1 + 2*x2*y2 - 2*d*z*z`. The two negative E8 factors are fixed in the constructor and omitted from its certificate. `kernel_basis` is a list of **column vectors**. The verifier separately checks index-one saturation with maximal minors; correct rational span is insufficient.

## Recorded checks

- Complete isotropic-residue scans for all 4,096 values of d from 1 through 4,096.
- 12,710 oriented-label certificates; these are not counts of distinct cusps.
- 1,025 independent chart minima and 1,024 exact fixed-z, five-coordinate searches.
- 999 members of a family whose full-lattice optimum is proved analytically.
- 500 large-integer certificates and a separate full 21-coordinate E8 example.
- Targeted invalid-certificate rejection and eight unit tests, including execution under `-O`.

## Scope

Height depends on the specified lattice basis. The chart minimum, fixed-z five-coordinate minimum, and unrestricted full-lattice minimum are different problems. The E8 example gives heights 9, 9, and 6 respectively. Reduced representative height does not establish smaller quotient bases or faster downstream compactification computations. No new geometric compactification, universal novelty guarantee, publication acceptance, patentability, or commercial demand is asserted.

License: MIT for code; manuscript copyright 2026 Shivam Gupta, shared under CC BY 4.0.
