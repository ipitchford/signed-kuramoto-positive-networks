"""Draw the construction figure for signed_kuramoto_networks_inside_positive_ones.tex.

Usage:  python -I code/make_figures.py --out OUTPUT_DIRECTORY
Writes kuramoto_construction.pdf and .png inside OUTPUT_DIRECTORY only.
"""
from pathlib import Path
import argparse
import math
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "kuramoto_mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

INK, TEAL, PLUM, GREY = "#45315D", "#137c79", "#9b4e9f", "#9a9a9a"


def ring(ax, cx, cy, R, phi, label):
    pos = []
    for a in range(6):
        ang = math.pi / 2 - a * math.pi / 3
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        pos.append((x, y))
    for a in range(6):
        (x0, y0), (x1, y1) = pos[a], pos[(a + 1) % 6]
        ax.plot([x0, x1], [y0, y1], color=GREY, lw=3.2, zorder=1, solid_capstyle="round")
    for a, (x, y) in enumerate(pos):
        ax.add_patch(Circle((x, y), 0.30, facecolor="white", edgecolor=INK, lw=1.2, zorder=2))
        th = phi + a * math.pi / 3
        ax.add_patch(FancyArrowPatch((x - 0.21 * math.cos(th), y - 0.21 * math.sin(th)),
                                     (x + 0.21 * math.cos(th), y + 0.21 * math.sin(th)),
                                     arrowstyle="-|>", mutation_scale=8, color=INK, lw=1.1, zorder=3))
        ax.text(x + 0.42 * math.cos(math.pi / 2 - a * math.pi / 3) * (1 if cx < 3 else 1),
                y + 0.42 * math.sin(math.pi / 2 - a * math.pi / 3), f"{a}", fontsize=12,
                ha="center", va="center", color=GREY)
    ax.text(cx, cy, label, fontsize=14, ha="center", va="center", color=INK)
    return pos


def edge_panel(ax, shift, title, colour):
    left = ring(ax, 0, 0, 1.25, 0.25, r"$i$")
    right = ring(ax, 4.2, 0, 1.25, 1.35, r"$j$")
    for a in range(6):
        (x0, y0), (x1, y1) = left[a], right[(a + shift) % 6]
        ax.plot([x0, x1], [y0, y1], color=colour, lw=0.9, alpha=0.85, zorder=0)
    ax.set_title(title, fontsize=14, color=INK)
    ax.set_xlim(-1.9, 6.1); ax.set_ylim(-1.9, 1.9); ax.set_aspect("equal"); ax.axis("off")


def balanced_panel(ax):
    ax.set_title("(c) cone point; nearby balanced state", fontsize=14, color=INK)
    for k, th in enumerate([0, 0, 0, math.pi, math.pi, math.pi]):
        x = -1.2 + 0.0 * k
        ax.add_patch(FancyArrowPatch((x, 0), (x + 0.9 * math.cos(th + 0.06 * (k % 3 - 1)),
                                             0.9 * math.sin(th + 0.06 * (k % 3 - 1))),
                                     arrowstyle="-|>", mutation_scale=14, color=INK, lw=1.6))
    ax.text(-1.2, -1.45, "3 at 0,\n3 at $\\pi$", fontsize=15,
            ha="center", color=INK)
    # a nearby balanced configuration drawn head to tail (a closed hexagon)
    t = 0.5
    angs = [t, 0.0, -t, math.pi + t, math.pi, math.pi - t]  # exactly balanced
    x, y = 1.1, 0.25
    for a in angs:
        s = 0.55
        ax.add_patch(FancyArrowPatch((x, y), (x + s * math.cos(a), y + s * math.sin(a)),
                                     arrowstyle="-|>", mutation_scale=13, color=TEAL, lw=1.6))
        x, y = x + s * math.cos(a), y + s * math.sin(a)
    ax.text(2.0, -1.45, "closes up\nhead to tail", fontsize=15,
            ha="center", color=TEAL)
    ax.set_xlim(-2.3, 3.6); ax.set_ylim(-2.05, 1.3); ax.set_aspect("equal"); ax.axis("off")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.4), constrained_layout=True)
    edge_panel(axes[0], 0, "(a) positive edge: group $a$ to $a$", TEAL)
    edge_panel(axes[1], 3, "(b) negative edge: group $a$ to $a+3$", PLUM)
    balanced_panel(axes[2])
    fig.savefig(args.out / "kuramoto_construction.pdf")
    fig.savefig(args.out / "kuramoto_construction.png", dpi=200)
    plt.close(fig)
    print("Wrote kuramoto_construction.pdf and .png")


if __name__ == "__main__":
    main()
