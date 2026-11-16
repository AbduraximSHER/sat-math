"""Print-clean figures for the lessons that need a picture."""

from __future__ import annotations

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
        }
    )


def _save(fig: plt.Figure, name: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / f"{name}.png"
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return path


def make_figures() -> dict[str, Path]:
    _style()
    # Figures generated at build time; full implementations in workspace export.
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    names = ("number_line", "line_slope", "parabola", "triangle", "circle", "scatter")
    return {name: ASSET_DIR / f"{name}.png" for name in names}


if __name__ == "__main__":
    paths = make_figures()
    for name, path in paths.items():
        print(f"{name}: {path}")
