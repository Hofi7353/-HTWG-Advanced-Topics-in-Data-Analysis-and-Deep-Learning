import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import comb


def bernstein_polynomial(n, k, x):
    return comb(n, k) * x**k * (1 - x) ** (n - k)


def main():
    # Grad des Polynoms
    n = 5
    x = np.linspace(0, 1, 500)

    # Plot vorbereiten
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, bottom=0.35)  # Platz für Slider lassen

    lines = []
    sliders = []

    colors = plt.cm.viridis(np.linspace(0, 1, n + 1))

    # Anfangswert und Plot jedes Polynoms
    for k in range(n + 1):
        y = bernstein_polynomial(n, k, x)
        (line,) = ax.plot(x, y, label=f"$a_{k} B_{{{k},{n}}}(x)$", color=colors[k])
        lines.append(line)

    # Summe der Polynome
    (sum_line,) = ax.plot(
        x, sum([l.get_ydata() for l in lines]), "k--", lw=2, label="Summe"
    )
    ax.set_title(f"Bernstein-Polynome mit interaktiven Vorfaktoren (Grad {n})")
    ax.set_xlabel("x")
    ax.set_ylabel("$a_k B_{k,n}(x)$")
    ax.legend()
    ax.grid(True)
    ax.set_ybound(-1.0, 1.0)

    # Sliders hinzufügen
    slider_height = 0.03
    start_y = 0.25
    spacing = 0.05

    for k in range(n + 1):
        ax_slider = plt.axes([0.1, start_y - k * spacing, 0.8, slider_height])
        slider = Slider(ax_slider, f"a{k}", -1.0, 1.0, valinit=0.0)
        sliders.append(slider)

    # Update-Funktion
    def update(val):
        y_sum = np.zeros_like(x)
        for k, slider in enumerate(sliders):
            factor = slider.val
            y = factor * bernstein_polynomial(n, k, x)
            lines[k].set_ydata(y)
            y_sum += y
        sum_line.set_ydata(y_sum)
        fig.canvas.draw_idle()

    # Slider verbinden
    for slider in sliders:
        slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main()
