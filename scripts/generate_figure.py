#!/usr/bin/env python3
"""
Generate publication-quality 4-panel figure for the exponential sums paper.

Reads data/exponential_sums.csv and produces figures/expsum_figure.pdf.
Line styles in panel (d) are chosen for B&W distinguishability:
  Observed = solid, USp(44) = dashed, Gaussian RW = dot-dash.

Author: Ruqing Chen
Repository: https://github.com/Ruqing1963/Q47-ExponentialSums
"""

import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def load_data(path="data/exponential_sums.csv"):
    """Load exponential sum data from CSV."""
    re_vals, im_vals, mag_vals, p_vals = [], [], [], []
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].startswith('#') or row[0] == 'prime_p':
                continue
            p_vals.append(int(row[0]))
            re_vals.append(float(row[1]))
            im_vals.append(float(row[2]))
            mag_vals.append(float(row[3]))
    return (np.array(re_vals), np.array(im_vals),
            np.array(mag_vals), np.array(p_vals))


def main():
    re_vals, im_vals, mag_vals, p_vals = load_data()

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # ── Panel (a): Real Part ──
    ax = axes[0, 0]
    ax.hist(re_vals, bins=25, density=True, color='#5B9BD5',
            edgecolor='white', alpha=0.85,
            label=r'$\mathrm{Re}(S_p)/\sqrt{p}$')
    x = np.linspace(-10, 10, 300)
    ax.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-x**2/2), 'r--', lw=1.5,
            label=r'$\mathcal{N}(0,1)$')
    ax.set_xlim(-10, 10)
    ax.set_xlabel(r'$\mathrm{Re}(S_p)/\sqrt{p}$', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.set_title(r'(a) Real Part Distribution', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.2)

    # ── Panel (b): Imaginary Part ──
    ax = axes[0, 1]
    ax.hist(im_vals, bins=25, density=True, color='#70AD47',
            edgecolor='white', alpha=0.85,
            label=r'$\mathrm{Im}(S_p)/\sqrt{p}$')
    ax.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-x**2/2), 'r--', lw=1.5,
            label=r'$\mathcal{N}(0,1)$')
    ax.set_xlim(-5, 5)
    ax.set_xlabel(r'$\mathrm{Im}(S_p)/\sqrt{p}$', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.set_title(r'(b) Imaginary Part Distribution', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.2)

    # ── Panel (c): Complex Plane Scatter ──
    ax = axes[1, 0]
    mask = p_vals != 283
    sc = ax.scatter(re_vals[mask], im_vals[mask], c=p_vals[mask],
                    cmap='viridis', s=25, alpha=0.8,
                    edgecolors='k', linewidths=0.3)
    plt.colorbar(sc, ax=ax, label='Prime $p$')
    for r in [2, 4, 6, 8]:
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(r*np.cos(theta), r*np.sin(theta),
                'k--', alpha=0.2, lw=0.8)
    # p=283 outlier: red star with white-bg label
    idx283 = np.where(p_vals == 283)[0]
    if len(idx283) > 0:
        i = idx283[0]
        ax.scatter([re_vals[i]], [im_vals[i]], c='red', s=80,
                   marker='*', zorder=10, edgecolors='darkred',
                   linewidths=0.5)
        ax.annotate(r'$p\!=\!283$', (re_vals[i], im_vals[i]),
                    textcoords='offset points', xytext=(-10, 14),
                    fontsize=10, fontweight='bold', color='red',
                    arrowprops=dict(arrowstyle='->', color='red',
                                    lw=1.2),
                    bbox=dict(boxstyle='round,pad=0.2', fc='white',
                              ec='red', alpha=0.9))
    ax.set_xlabel(r'$\mathrm{Re}(S_p)/\sqrt{p}$', fontsize=11)
    ax.set_ylabel(r'$\mathrm{Im}(S_p)/\sqrt{p}$', fontsize=11)
    ax.set_title(r'(c) Complex Plane', fontsize=12)
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-6, 6)
    ax.grid(True, alpha=0.2)

    # ── Panel (d): Magnitude Distribution (B&W-safe) ──
    ax = axes[1, 1]
    ax.hist(mag_vals, bins=20, density=True, color='#ED7D31',
            edgecolor='white', alpha=0.85,
            label=r'$|S_p|/\sqrt{p}$')
    ax.axvline(np.mean(mag_vals), color='red', ls='-', lw=2.0,
               label=rf'Observed: $\mu \approx {np.mean(mag_vals):.2f}$'
                     ' (solid)')
    ax.axvline(3.74, color='purple', ls='--', lw=2.0,
               label=r'$USp(44)$: $\mu \approx 3.74$ (dashed)')
    ax.axvline(5.97, color='dimgray', ls='-.', lw=2.0,
               label=r'Gaussian RW: $\mu \approx 5.97$ (dot-dash)')
    ax.set_xlabel(r'$|S_p|/\sqrt{p}$', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.set_title(r'(d) Magnitude Distribution', fontsize=12)
    ax.legend(fontsize=8.5, loc='upper right')
    ax.set_xlim(0, 10)
    ax.grid(True, alpha=0.2)

    plt.tight_layout(pad=1.5)
    os.makedirs("figures", exist_ok=True)
    plt.savefig("figures/expsum_figure.pdf", dpi=300,
                bbox_inches='tight')
    print("Figure saved to figures/expsum_figure.pdf")


if __name__ == "__main__":
    main()
