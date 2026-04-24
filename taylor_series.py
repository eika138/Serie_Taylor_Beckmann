"""
Taylor Series Interactive Visualizer
=====================================
Controles:
  - Slider "Grado n": número de términos de la serie
  - Slider "Centro a": punto alrededor del cual se expande la serie
  - Menú "Función": elige entre sin, cos, exp, ln(1+x), 1/(1-x), arctan(x)

Dependencias: numpy, matplotlib
  pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.patches import FancyArrowPatch
from math import factorial, comb
import matplotlib

matplotlib.use('TkAgg')   # reemplazá 'TkAgg' con esto

def deriv_at(f, a, k, h=1e-4):
    """Derivada k-ésima de f en el punto a via diferencias finitas."""
    if k == 0:
        return f(a)
    return sum(
        ((-1) ** (k - j)) * comb(k, j) * f(a + j * h)
        for j in range(k + 1)
    ) / h ** k

def num_taylor(f, x, a, n):
    """Serie de Taylor numérica de grado n alrededor de a, evaluada en x."""
    return sum(deriv_at(f, a, k) / factorial(k) * (x - a) ** k for k in range(n + 1))

# ── Paleta ──────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
ACCENT    = "#58a6ff"
APPROX    = "#f78166"
CENTER    = "#3fb950"
GRID      = "#21262d"
TEXT      = "#c9d1d9"
MUTED     = "#8b949e"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   TEXT,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        TEXT,
    "grid.color":        GRID,
    "grid.linestyle":    "--",
    "grid.alpha":        0.6,
    "font.family":       "monospace",
})

# ── Funciones y sus series de Taylor ────────────────────────────────────────
FUNCTIONS = {
    "sin(x)": {
        "f":      np.sin,
        "taylor": lambda x, a, n: sum(
            ((-1)**k / factorial(2*k+1)) * (x - a)**(2*k+1)
            for k in range(n+1)
        ),
        "domain": (-3*np.pi, 3*np.pi),
        "ylim":   (-2.5, 2.5),
    },
    "cos(x)": {
        "f":      np.cos,
        "taylor": lambda x, a, n: sum(
            ((-1)**k / factorial(2*k)) * (x - a)**(2*k)
            for k in range(n+1)
        ),
        "domain": (-3*np.pi, 3*np.pi),
        "ylim":   (-2.5, 2.5),
    },
    "exp(x)": {
        "f":      np.exp,
        "taylor": lambda x, a, n: sum(
            (np.exp(a) / factorial(k)) * (x - a)**k
            for k in range(n+1)
        ),
        "domain": (-4, 4),
        "ylim":   (-1, 30),
    },
    "ln(1+x)": {
        "f":      lambda x: np.log(1 + x),
        "taylor": lambda x, a, n: (
            np.log(1 + a) + sum(
                ((-1)**(k+1) / (k * (1+a)**k)) * (x - a)**k
                for k in range(1, n+1)
            )
        ),
        "domain": (-0.95, 4),
        "ylim":   (-4, 4),
    },
    "1/(1-x)": {
        "f":      lambda x: 1 / (1 - x),
        "taylor": lambda x, a, n: sum(
            ((x - a)**k / (1 - a)**(k+1))
            for k in range(n+1)
        ),
        "domain": (-2.5, 0.9),
        "ylim":   (-6, 15),
    },
    "arctan(x)": {
        "f":      np.arctan,
        "taylor": lambda x, a, n: num_taylor(np.arctan, x, a, n),
        "domain": (-4, 4),
        "ylim":   (-2.5, 2.5),
    },
}

# ── Layout ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13, 8))
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(
    3, 2,
    figure=fig,
    left=0.08, right=0.72,
    top=0.92,  bottom=0.08,
    hspace=0.08,
)

ax_main  = fig.add_subplot(gs[:2, :])
ax_error = fig.add_subplot(gs[2, :], sharex=ax_main)

for ax in (ax_main, ax_error):
    ax.set_facecolor(PANEL)
    ax.grid(True)
    ax.tick_params(colors=MUTED)

ax_main.tick_params(labelbottom=False)

# Widgets area (derecha)
ax_radio  = fig.add_axes([0.76, 0.52, 0.22, 0.38], facecolor=PANEL)
ax_sn     = fig.add_axes([0.76, 0.35, 0.20, 0.04], facecolor=PANEL)
ax_sa     = fig.add_axes([0.76, 0.25, 0.20, 0.04], facecolor=PANEL)

s_n = Slider(ax_sn, "Grado n", 0, 15, valinit=2, valstep=1,
             color=ACCENT, handle_style={"facecolor": ACCENT, "edgecolor": BG})
s_a = Slider(ax_sa, "Centro a", -3, 3, valinit=0, valstep=0.1,
             color=CENTER, handle_style={"facecolor": CENTER, "edgecolor": BG})

for sl in (s_n, s_a):
    sl.label.set_color(TEXT)
    sl.valtext.set_color(ACCENT)

radio = RadioButtons(
    ax_radio,
    list(FUNCTIONS.keys()),
    activecolor=ACCENT,
)
for lbl in radio.labels:
    lbl.set_color(TEXT)
    lbl.set_fontsize(9)

# ── Estado ───────────────────────────────────────────────────────────────────
state = {"func": "sin(x)"}

# ── Líneas y texto ───────────────────────────────────────────────────────────
N_PTS = 800

fn_info = FUNCTIONS[state["func"]]
x_min, x_max = fn_info["domain"]
x = np.linspace(x_min, x_max, N_PTS)

line_f,  = ax_main.plot([], [], color=ACCENT,  lw=2.2, label="f(x) exacta")
line_t,  = ax_main.plot([], [], color=APPROX,  lw=2.2, ls="--", label="Taylor Tₙ(x)")
line_c   = ax_main.axvline(0, color=CENTER, lw=1.2, ls=":", alpha=0.8, label="Centro a")
line_err,= ax_error.plot([], [], color=APPROX, lw=1.5)
ax_error.axhline(0, color=MUTED, lw=0.8)

ax_main.legend(loc="upper left", fontsize=9,
               facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT)

ax_main.set_ylabel("y", fontsize=10)
ax_error.set_ylabel("|error|", fontsize=9)
ax_error.set_xlabel("x", fontsize=10)

formula_text = ax_main.text(
    0.02, 0.97, "", transform=ax_main.transAxes,
    fontsize=8, va="top", color=MUTED,
    bbox=dict(facecolor=BG, edgecolor=GRID, boxstyle="round,pad=0.4"),
)

fig.suptitle("Series de Taylor — Visualizador Interactivo",
             fontsize=13, color=TEXT, y=0.97)

# ── Fórmulas de display ──────────────────────────────────────────────────────
FORMULAS = {
    "sin(x)":  "sin(x) ≈ Σ (-1)ᵏ x^(2k+1) / (2k+1)!",
    "cos(x)":  "cos(x) ≈ Σ (-1)ᵏ x^(2k) / (2k)!",
    "exp(x)":  "eˣ ≈ Σ xᵏ / k!",
    "ln(1+x)": "ln(1+x) ≈ Σ (-1)^(k+1) xᵏ / k",
    "1/(1-x)": "1/(1-x) ≈ Σ xᵏ",
    "arctan(x)": "arctan(x) ≈ Σ (-1)ᵏ x^(2k+1) / (2k+1)",
}

# ── Actualización ─────────────────────────────────────────────────────────────
def update(_=None):
    fname  = state["func"]
    fn     = FUNCTIONS[fname]
    n      = int(s_n.val)
    a      = float(s_a.val)

    x_min, x_max = fn["domain"]
    x = np.linspace(x_min, x_max, N_PTS)

    # Función exacta (con manejo de singularidades)
    with np.errstate(all="ignore"):
        y_exact = fn["f"](x)

    # Serie de Taylor (vectorizada por comprensión)
    y_taylor = np.array([fn["taylor"](xi, a, n) for xi in x], dtype=float)

    # Clamp para visualización limpia
    y_lim = fn["ylim"]
    y_exact  = np.clip(y_exact,  y_lim[0], y_lim[1])
    y_taylor = np.clip(y_taylor, y_lim[0]*3, y_lim[1]*3)

    line_f.set_data(x, y_exact)
    line_t.set_data(x, y_taylor)
    line_c.set_xdata([a, a])

    # Error
    with np.errstate(all="ignore"):
        error = np.abs(y_exact - y_taylor)
    error = np.clip(error, 0, abs(y_lim[1] - y_lim[0]))
    line_err.set_data(x, error)

    ax_main.set_xlim(x_min, x_max)
    ax_main.set_ylim(*y_lim)
    ax_error.set_xlim(x_min, x_max)
    ax_error.set_ylim(0, np.nanpercentile(error, 98) * 1.3 + 1e-9)

    s_a.valmin = x_min + 0.1
    s_a.valmax = x_max - 0.1

    formula_text.set_text(f"n={n}, a={a:.1f}  │  {FORMULAS[fname]}")
    fig.canvas.draw_idle()

def on_radio(label):
    state["func"] = label
    update()

s_n.on_changed(update)
s_a.on_changed(update)
radio.on_clicked(on_radio)

update()
plt.show()