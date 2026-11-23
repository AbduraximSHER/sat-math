"""Print-clean figures for the lessons that need a picture."""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge

NAVY = "#1B3A4B"
TEAL = "#0F6E6B"
GOLD = "#B0893E"
INK = "#243038"
CREAM = "#F4EFE4"
LIGHT = "#E7F2F1"

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "guide" / "assets"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "text.color": INK,
            "axes.edgecolor": NAVY,
            "axes.labelcolor": NAVY,
            "xtick.color": NAVY,
            "ytick.color": NAVY,
            "axes.titlecolor": NAVY,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.linewidth": 1.1,
            # Text becomes outlines from the font matplotlib ships, and ids come
            # from a fixed salt, so the SVG is byte-identical on every machine.
            "svg.fonttype": "path",
            "svg.hashsalt": "sat-math",
        }
    )


def _short(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def _tidy_svg(text: str) -> str:
    """Round coordinates to 0.01 so float noise from one CPU to the next disappears.

    Glyph scale factors such as scale(0.015625) stay exact.
    """
    parts = re.split(r"(scale\([^)]*\))", text)
    for index in range(0, len(parts), 2):
        parts[index] = re.sub(
            r"(?<![\w#.])-?\d+\.\d{3,}",
            lambda match: _short(float(match.group(0))),
            parts[index],
        )
    return "".join(parts)


def _save(fig: plt.Figure, name: str) -> Path:
    """Write a print PNG for the Word book and a vector SVG for the website."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / f"{name}.png"
    options = dict(bbox_inches="tight", pad_inches=0.18)
    fig.savefig(path, dpi=300, **options)
    svg = io.StringIO()
    fig.savefig(svg, format="svg", metadata={"Date": None}, **options)
    (ASSET_DIR / f"{name}.svg").write_text(_tidy_svg(svg.getvalue()), encoding="utf-8")
    plt.close(fig)
    return path


def _number_line() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 2.8))
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-1.15, 1.55)
    ax.axis("off")
    ax.annotate(
        "",
        xy=(5.35, 0),
        xytext=(-5.35, 0),
        arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.6),
    )
    for tick in range(-5, 6):
        ax.plot([tick, tick], [-0.08, 0.08], color=NAVY, lw=1.1)
        ax.text(tick, -0.28, str(tick), ha="center", va="top", fontsize=11, color=NAVY)
    ax.plot([-4, 3], [0, 0], color=TEAL, lw=4, solid_capstyle="butt", zorder=2)
    for point, name in ((-4, "A"), (3, "B")):
        ax.scatter([point], [0], s=46, color=TEAL, zorder=3)
        ax.text(point, 0.22, name, ha="center", va="bottom", fontsize=13, color=TEAL)
    ax.annotate(
        "",
        xy=(3, 0.72),
        xytext=(-4, 0.72),
        arrowprops=dict(arrowstyle="<->", color=GOLD, lw=1.3),
    )
    ax.text( -0.5, 0.86, "|3 − (−4)| = 7", ha="center", va="bottom", fontsize=12, color=INK)
    ax.text(0, -0.95, "0", ha="center", color=NAVY, fontsize=11)
    _save(fig, "number_line")


def _line_slope() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.axhline(0, color="#9AABA3", lw=1)
    ax.axvline(0, color="#9AABA3", lw=1)
    xs = [-1, 4]
    ax.plot(xs, [2 * x + 1 for x in xs], color=NAVY, lw=2.2, zorder=2)
    ax.plot([0, 2, 2], [1, 1, 5], color=GOLD, lw=1.5, zorder=3)
    ax.scatter([0, 2], [1, 5], s=42, color=TEAL, zorder=4)
    ax.annotate("(0, 1)", (0, 1), textcoords="offset points", xytext=(-28, -18), color=INK, fontsize=11)
    ax.annotate("(2, 5)", (2, 5), textcoords="offset points", xytext=(8, 6), color=INK, fontsize=11)
    ax.text(1, 0.72, "run 2", ha="center", va="top", color=GOLD, fontsize=11)
    ax.text(2.12, 3, "rise 4", ha="left", va="center", color=GOLD, fontsize=11)
    ax.text(2.55, 2 * 2.55 + 1.15, "y = 2x + 1", color=NAVY, fontsize=13)
    ax.set_xlim(-1.4, 4.4)
    ax.set_ylim(-1.2, 8.2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "line_slope")


def _parabola() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.8))
    left, right = axes
    import numpy as np

    x_left = np.linspace(-0.2, 4.2, 200)
    left.plot(x_left, x_left**2 - 4 * x_left + 3, color=NAVY, lw=2.2)
    left.scatter([1, 3, 2], [0, 0, -1], color=TEAL, s=36, zorder=3)
    left.annotate("root", (1, 0), textcoords="offset points", xytext=(-18, 8), fontsize=10, color=TEAL)
    left.annotate("root", (3, 0), textcoords="offset points", xytext=(4, 8), fontsize=10, color=TEAL)
    left.annotate("vertex (2, −1)", (2, -1), textcoords="offset points", xytext=(-20, -16), fontsize=10, color=INK)
    left.axhline(0, color="#9AABA3", lw=1)
    left.axvline(0, color="#9AABA3", lw=1)
    left.set_title("y = x² − 4x + 3", fontsize=12, color=NAVY, pad=8)
    left.set_xlim(-0.6, 4.6)
    left.set_ylim(-2.2, 4.2)

    x_right = np.linspace(-1.2, 3.2, 200)
    y_right = -((x_right - 1) ** 2) + 4
    right.plot(x_right, y_right, color=NAVY, lw=2.2)
    right.scatter([1], [4], color=TEAL, s=36, zorder=3)
    right.annotate("maximum (1, 4)", (1, 4), textcoords="offset points", xytext=(-18, 8), fontsize=10, color=INK)
    right.axhline(0, color="#9AABA3", lw=1)
    right.axvline(0, color="#9AABA3", lw=1)
    right.set_title("y = −(x − 1)² + 4", fontsize=12, color=NAVY, pad=8)
    right.set_xlim(-1.5, 3.5)
    right.set_ylim(-1.5, 5.3)

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.tight_layout()
    _save(fig, "parabola")


def _triangle() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.set_aspect("equal")
    ax.axis("off")
    points = [(0, 0), (4, 0), (0, 3)]
    poly = Polygon(points, closed=True, fill=True, facecolor=LIGHT, edgecolor=NAVY, lw=2.2)
    ax.add_patch(poly)
    square = Polygon([(0, 0.28), (0.28, 0.28), (0.28, 0)], closed=True, fill=False, edgecolor=GOLD, lw=1.3)
    ax.add_patch(square)
    ax.text(2, -0.28, "4", ha="center", va="top", fontsize=14, color=NAVY)
    ax.text(-0.22, 1.5, "3", ha="right", va="center", fontsize=14, color=NAVY)
    ax.text(2.15, 1.7, "5", ha="left", va="center", fontsize=14, color=TEAL)
    ax.text(0.45, 0.08, "right angle", fontsize=10, color=GOLD)
    ax.set_xlim(-0.9, 4.8)
    ax.set_ylim(-0.7, 3.55)
    _save(fig, "triangle")


def _circle() -> None:
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    ax.set_aspect("equal")
    ax.axis("off")
    wedge = Wedge((0, 0), 1, 0, 72, facecolor=CREAM, edgecolor=GOLD, lw=1.4)
    ax.add_patch(wedge)
    circle = plt.Circle((0, 0), 1, fill=False, edgecolor=NAVY, lw=2.1)
    ax.add_patch(circle)
    ax.plot([0, 1], [0, 0], color=TEAL, lw=1.6)
    import math

    ax.plot([0, math.cos(math.radians(72))], [0, math.sin(math.radians(72))], color=TEAL, lw=1.6)
    ax.scatter([0], [0], s=28, color=NAVY, zorder=3)
    ax.text(-0.08, -0.1, "O", ha="right", va="top", fontsize=12, color=NAVY)
    ax.text(0.48, -0.12, "r", color=TEAL, fontsize=13)
    ax.text(0.72, 0.38, "72°", color=GOLD, fontsize=13)
    ax.annotate(
        "arc",
        xy=(math.cos(math.radians(36)) * 1.02, math.sin(math.radians(36)) * 1.02),
        xytext=(1.25, 0.85),
        fontsize=12,
        color=NAVY,
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8),
    )
    ax.set_xlim(-1.35, 1.7)
    ax.set_ylim(-1.35, 1.45)
    _save(fig, "circle")


def _scatter() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    points = [(1, 2), (2, 3.2), (3, 5), (4, 5.8), (5, 8)]
    xs, ys = zip(*points)
    ax.scatter(xs, ys, s=48, color=TEAL, zorder=3, label="measured points")
    line_x = [0.4, 6]
    ax.plot(line_x, [1.5 * x + 0.5 for x in line_x], color=NAVY, lw=2, label="y = 1.5x + 0.5")
    ax.set_xlim(0, 6.4)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    _save(fig, "scatter")


def make_figures() -> dict[str, Path]:
    _style()
    _number_line()
    _line_slope()
    _parabola()
    _triangle()
    _circle()
    _scatter()
    names = ("number_line", "line_slope", "parabola", "triangle", "circle", "scatter")
    return {name: ASSET_DIR / f"{name}.png" for name in names}


if __name__ == "__main__":
    paths = make_figures()
    for name, path in paths.items():
        print(f"{name}: {path} ({path.stat().st_size} bytes)")
