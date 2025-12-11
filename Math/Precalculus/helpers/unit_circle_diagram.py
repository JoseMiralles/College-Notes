import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import ipywidgets as widgets

def show(angle, unit):
    # convert to radians and degrees
    if unit == 'rad':
        angle_rad = float(angle)
        angle_deg = np.degrees(angle_rad)
    else:
        angle_deg = float(angle)
        angle_rad = np.radians(angle_deg)

    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    # handle tan undefined when cos ~ 0
    if abs(c) < 1e-12:
        t = np.nan
        tan_str = "undefined"
    else:
        t = np.tan(angle_rad)
        tan_str = f"{t:.6g}"

    display(Markdown(f"**Angle:** {angle_deg:.6g}° ({angle_rad:.6g} rad)  \n"
                     f"**sin:** {s:.6g}  **cos:** {c:.6g}  **tan:** {tan_str}"))

    fig, ax = plt.subplots(figsize=(5,5))
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color='black')            # unit circle
    ax.axhline(0, color='gray', linewidth=0.6)
    ax.axvline(0, color='gray', linewidth=0.6)

    # radius vector to the point (cos, sin)
    ax.plot([0, c], [0, s], color='red', linewidth=2)
    ax.scatter([c], [s], color='red', zorder=5)

    # projections to axes
    ax.plot([c, c], [0, s], linestyle='--', color='blue')
    ax.plot([0, c], [s, s], linestyle='--', color='blue')

    # tangent visualization at x=1 (length = tan)
    if np.isfinite(t):
        ax.plot([0, 1], [0, t], color='green', linestyle='--', linewidth=1, zorder=1)
        ax.plot([1, 1], [0, t], color='green', linewidth=2)
        ax.scatter([1], [t], color='green', zorder=5)
        ax.text(1.05, t, f"tan={t:.3g}", color='green', va='center')
    else:
        ax.text(0.1, 1.15, "tan undefined (cos ≈ 0)", color='green')

    ax.set_aspect('equal', 'box')
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel('cos(θ)')
    ax.set_ylabel('sin(θ)')
    ax.set_title(f"Unit circle — θ = {angle_deg:.2f}°")
    plt.show()

def render():
    # Widgets
    angle_widget = widgets.FloatText(value=45, min=-360, max=360, step=1, description='Angle')
    unit_widget = widgets.Dropdown(options=[('Degrees','deg'), ('Radians','rad')], value='deg', description='Unit')

    # adjust slider range/step when unit changes
    def on_unit_change(change):
        if change['new'] == 'rad':
            angle_widget.min = -2*np.pi
            angle_widget.max = 2*np.pi
            angle_widget.step = 0.01
            angle_widget.value = np.pi/4
            angle_widget.description = 'Angle (rad)'
        else:
            angle_widget.min = -360
            angle_widget.max = 360
            angle_widget.step = 1
            angle_widget.value = 45
            angle_widget.description = 'Angle (°)'

    unit_widget.observe(on_unit_change, names='value')

    out = widgets.interactive_output(show, {'angle': angle_widget, 'unit': unit_widget})

    ui = widgets.VBox([widgets.HBox([angle_widget, unit_widget]), out])
    display(ui)