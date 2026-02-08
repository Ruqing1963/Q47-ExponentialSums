# Q47-ExponentialSums

**Exponential Sums of the Titan Polynomial: Numerical Evidence for Non-Generic Monodromy**

**Author:** Ruqing Chen, GUT Geoservice Inc., Montreal, Canada

---

## Overview

This repository contains the paper, data, and scripts for a numerical study of the exponential sums

$$S_p = \sum_{n=0}^{p-1} \exp\!\left(\frac{2\pi i\, Q(n)}{p}\right), \quad Q(n) = n^{47} - (n-1)^{47}$$

normalized by $\sqrt{p}$, for primes $p \equiv 1 \pmod{47}$ up to 50,000.

## Key Finding

| Model | Predicted Mean $\|S_p\|/\sqrt{p}$ |
|-------|:---------------------------------:|
| Gaussian Random Walk (45 vectors) | ≈ 5.97 |
| Generic Symplectic USp(44) | ≈ 3.74 |
| **Observed (Titan)** | **≈ 1.50** |

The observed mean is dramatically lower than all higher-dimensional predictions, suggesting the geometric monodromy group is a **proper subgroup** of USp(44), constrained by the cyclotomic structure of $Q(n) = \Phi_{47}(n/(n-1))$.

### Why symplectic?

The palindromic symmetry $Q(n) = Q(1-n)$ constrains the monodromy to a symplectic group rather than the full unitary group SU(45). By Katz's theorem, the cyclotomic origin (odd prime order 47) selects USp(44) over O(45).

### Conjecture (Jacobian Splitting)

The remarkably low mean suggests that the Jacobian variety associated with $Q(n)$ undergoes a significant algebraic decomposition, splitting into lower-dimensional CM abelian sub-varieties indexed by the characters of $(\mathbb{Z}/47\mathbb{Z})^\times$.

## Repository Structure

```
Q47-ExponentialSums/
├── README.md
├── LICENSE
├── .gitignore
├── paper/
│   ├── ExponentialSums_TitanPolynomial.tex     # LaTeX source (5 pages)
│   └── ExponentialSums_TitanPolynomial.pdf     # Compiled paper
├── figures/
│   └── expsum_figure.pdf                       # 4-panel publication figure (PDF vector)
├── data/
│   ├── exponential_sums.csv                    # All 111 data points (p, Re, Im, |x_p|)
│   └── statistics.csv                          # Summary statistics
└── scripts/
    ├── compute_exponential_sums.py             # Compute S_p for all effective primes
    ├── generate_figure.py                      # Reproduce Figure 1 (PDF output)
    └── sato_sqrt.sage                          # Original SageMath computation script
```

## Quick Start

### Compute Exponential Sums
```bash
python scripts/compute_exponential_sums.py
```
Takes ~5 minutes (iterates over all residues mod p for 111 primes up to 50,000).

### Generate Figure
```bash
python scripts/generate_figure.py
```
Requires `matplotlib` and `numpy`. Reads `data/exponential_sums.csv`.

## Companion Papers

1. **Titan paper** (local root structure, bounded gap conjecture):
   [Zenodo](https://zenodo.org/records/18521551)

2. **Bateman–Horn constant** ($C_Q \approx 8.68$):
   [GitHub](https://github.com/Ruqing1963/Q47-BatemanHorn-Constant)

3. **Admissible Shifts** (fixed divisor analysis):
   [GitHub](https://github.com/Ruqing1963/Q47-Admissible-Shifts)

4. **Null–Sparse Decomposition** (Bombieri–Vinogradov):
   [Zenodo](https://zenodo.org/records/18521778)

5. **Landau–Siegel paper** (15.4M primes, spectral gap):
   [Zenodo](https://zenodo.org/records/18315796)

## Citation

```bibtex
@article{chen2026exponentialsums,
  title   = {Exponential Sums of the Titan Polynomial:
             Numerical Evidence for Non-Generic Monodromy},
  author  = {Chen, Ruqing},
  year    = {2026},
  note    = {Preprint, \url{https://github.com/Ruqing1963/Q47-ExponentialSums}}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
