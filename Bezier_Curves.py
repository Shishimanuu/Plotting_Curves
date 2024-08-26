import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import math

# Bézier function
def bezier(t, control_points):
    n = len(control_points) - 1
    return sum(
        math.comb(n, i) * (1 - t)**(n - i) * t**i * np.array(control_points[i])
        for i in range(n + 1)
    )

# Initial control points
control_points = [(0.1, 0.2), (0.4, 0.8), (0.6, 0.4), (0.9, 0.9)]

# Plot setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)  # Adjust bottom to give more space for sliders

t_values = np.linspace(0, 1, 100)
curve, = plt.plot([], [], lw=2, label='Bézier Curve')
control_lines, = plt.plot([], [], 'ro-', markersize=8, label='Control Points')

# Initialize the plot with initial control points
def init_plot():
    x, y = zip(*control_points)
    bezier_points = [bezier(t, control_points) for t in t_values]
    curve.set_data(*zip(*bezier_points))
    control_lines.set_data(x, y)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    return curve, control_lines

# Update the plot with new control points
def update_plot(val):
    x, y = zip(*control_points)
    control_lines.set_data(x, y)

    bezier_points = [bezier(t, control_points) for t in t_values]
    curve.set_data(*zip(*bezier_points))
    
    fig.canvas.draw_idle()

# Create sliders for each control point
ax_sliders = []
sliders = []
for i, (x, y) in enumerate(control_points):
    ax_slider_x = plt.axes([0.1, 0.25 - i * 0.07, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_slider_y = plt.axes([0.1, 0.25 - i * 0.07 - 0.04, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    
    slider_x = Slider(ax_slider_x, f'P{i} X', 0.0, 1.0, valinit=x)
    slider_y = Slider(ax_slider_y, f'P{i} Y', 0.0, 1.0, valinit=y)
    
    ax_sliders.extend([ax_slider_x, ax_slider_y])
    sliders.extend([slider_x, slider_y])
    
    def update_control_point_x(val, idx=i):
        control_points[idx] = (sliders[2 * idx].val, control_points[idx][1])
        update_plot(val)
    
    def update_control_point_y(val, idx=i):
        control_points[idx] = (control_points[idx][0], sliders[2 * idx + 1].val)
        update_plot(val)
    
    slider_x.on_changed(update_control_point_x)
    slider_y.on_changed(update_control_point_y)

# Reset button
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_ax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

def reset(event):
    for i, (x, y) in enumerate([(0.1, 0.2), (0.4, 0.8), (0.6, 0.4), (0.9, 0.9)]):
        sliders[2 * i].set_val(x)
        sliders[2 * i + 1].set_val(y)

button.on_clicked(reset)

# Initial plot
init_plot()
plt.show()
