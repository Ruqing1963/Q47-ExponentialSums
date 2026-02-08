#!/usr/bin/env python3
"""
Compute exponential sums S_p for Q(n) = n^47 - (n-1)^47.

For each prime p ≡ 1 (mod 47) up to MAX_PRIME, computes:
    S_p = sum_{n=0}^{p-1} exp(2*pi*i*Q(n)/p)
and the normalized quantity x_p = S_p / sqrt(p).

The Weil bound gives |x_p| ≤ 45.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-ExponentialSums
"""

import cmath
import csv
import math
import os


MAX_PRIME = 50000


def sieve_primes(n: int) -> list:
    """Sieve of Eratosthenes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def compute_expsum(p: int) -> complex:
    """Compute S_p = sum_{n=0}^{p-1} exp(2*pi*i*Q(n)/p)."""
    S = 0j
    for n in range(p):
        val = (pow(n, 47, p) - pow((n - 1) % p, 47, p)) % p
        theta = 2 * math.pi * val / p
        S += cmath.exp(1j * theta)
    return S


def main():
    print("=" * 65)
    print("  Exponential Sums for Q(n) = n^47 - (n-1)^47")
    print("  Primes p ≡ 1 (mod 47), p ≤", MAX_PRIME)
    print("=" * 65)
    print()

    primes = sieve_primes(MAX_PRIME)
    eff_primes = [p for p in primes if (p - 1) % 47 == 0]
    print(f"Effective primes: N = {len(eff_primes)}")
    print(f"Range: {eff_primes[0]} to {eff_primes[-1]}")
    print()

    results = []
    for idx, p in enumerate(eff_primes):
        S = compute_expsum(p)
        sqrtp = math.sqrt(p)
        normed = S / sqrtp
        results.append({
            'p': p,
            're': normed.real,
            'im': normed.imag,
            'mag': abs(normed)
        })
        if (idx + 1) % 20 == 0 or idx == 0:
            print(f"  [{idx+1:>3}/{len(eff_primes)}] p={p:>5}, "
                  f"|S_p|/sqrt(p) = {abs(normed):.4f}")

    mags = [r['mag'] for r in results]
    max_idx = mags.index(max(mags))

    print()
    print(f"{'Statistic':<30} {'Value':>10}")
    print("-" * 42)
    print(f"{'N':.<30} {len(results):>10}")
    print(f"{'Mean |S_p|/sqrt(p)':.<30} {sum(mags)/len(mags):>10.4f}")
    print(f"{'Max  |S_p|/sqrt(p)':.<30} {max(mags):>10.4f}")
    print(f"{'Max at p =':.<30} {results[max_idx]['p']:>10}")

    mags_ex = [r['mag'] for r in results if r['p'] != 283]
    print(f"{'Mean (excl. p=283)':.<30} {sum(mags_ex)/len(mags_ex):>10.4f}")
    print(f"{'Max  (excl. p=283)':.<30} {max(mags_ex):>10.4f}")

    print()
    print("Reference predictions:")
    print(f"  Gaussian RW (45 vectors):  ≈ 5.97")
    print(f"  USp(44):                   ≈ 3.74")
    print(f"  Observed:                  ≈ {sum(mags)/len(mags):.2f}")

    # Save CSV
    os.makedirs("data", exist_ok=True)
    with open("data/exponential_sums.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prime_p", "Re_Sp_over_sqrtp",
                     "Im_Sp_over_sqrtp", "magnitude"])
        for r in results:
            w.writerow([r['p'], f"{r['re']:.6f}",
                        f"{r['im']:.6f}", f"{r['mag']:.6f}"])
    print("\n  Saved to data/exponential_sums.csv")
    print("  [DONE]")


if __name__ == "__main__":
    main()
