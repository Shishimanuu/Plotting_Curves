import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider, CheckButtons, Button
from matplotlib.animation import FuncAnimation
import math
i = 0
def bezier(t, control_points):
    n = len(control_points) - 1
    return sum(
        math.comb(n, i) * (1 - t)**(n - i) * t**i * np.array(control_points[i])
        for i in range(n + 1)
    )

control_points = []
point_labels = []

fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25, right=0.8)

curve, = plt.plot([], [], lw=2, label='Bézier Curve')
control_lines, = plt.plot([], [], 'ro-', markersize=8, label='Control Points')
point_t, = plt.plot([], [], 'go', markersize=10, label='Point at t')
dragging_point = None
mode = 'add'
slider_mode = True
animating = False

def update_plot(val=None):
    global point_labels
    if control_points:
        x, y = zip(*control_points)
        control_lines.set_data(x, y)
        
        t = t_slider.val
        if slider_mode or animating:
            t_values = np.linspace(0, t, 100)
        else:
            t_values = np.linspace(0, 1, 100)
        
        bezier_points = [bezier(t, control_points) for t in t_values]
        curve.set_data(*zip(*bezier_points))
        
        point = bezier(t, control_points)
        point_t.set_data(*point)
    else:
        control_lines.set_data([], [])
        curve.set_data([], [])
        point_t.set_data([], [])

    for label in point_labels:
        label.remove()
    
    point_labels = []
    for i, (x, y) in enumerate(control_points):
        label = ax.text(x, y, f'P{i}', fontsize=12, ha='right', va='bottom')
        point_labels.append(label)
    
    fig.canvas.draw()
    # fig.canvas.flush_events()

def on_press(event):
    global dragging_point, mode
    if event.inaxes != ax:
        return
    if mode == 'move':
        for i, (x, y) in enumerate(control_points):
            if np.hypot(x - event.xdata, y - event.ydata) < 0.05:
                dragging_point = i
                break
    elif mode == 'add':
        control_points.append((event.xdata, event.ydata))
        update_plot()
    elif mode == 'remove':
        for i, (x, y) in enumerate(control_points):
            if np.hypot(x - event.xdata, y - event.ydata) < 0.05:
                del control_points[i]
                update_plot()
                break

def on_motion(event):
    global dragging_point, mode
    if dragging_point is None:
        return
    if event.inaxes != ax:
        return
    if mode == 'move' and dragging_point is not None:
        control_points[dragging_point] = (event.xdata, event.ydata)
        update_plot()

def on_release(event):
    global dragging_point
    dragging_point = None

def update_mode(label):
    global mode
    mode = label.lower()
    print(f"Mode switched to: {mode}")

def toggle_slider_mode(label):
    global slider_mode
    slider_mode = not slider_mode
    update_plot()

def animate(frame):
    global animating
    animating = True
    t = frame / 100
    t_slider.set_val(t)
    update_plot()
    return curve, point_t, control_lines

def on_animation_complete():
    global animating
    animating = False
    print("Animation complete!")

def start_animation(event):
    global anim
    anim = FuncAnimation(fig, animate, frames=np.linspace(0, 101, 100),
                         interval=1, blit=False, repeat=False)
    anim._start()
    anim.event_source.add_callback(on_animation_complete)

rax = plt.axes([0.81, 0.5, 0.18, 0.15])
radio = RadioButtons(rax, ('Add', 'Move', 'Remove'))
radio.on_clicked(update_mode)

slider_ax = plt.axes([0.1, 0.05, 0.65, 0.03])
t_slider = Slider(slider_ax, 't', 0, 1, valinit=0, valstep=0.01)
t_slider.on_changed(update_plot)

check_ax = plt.axes([0.81, 0.4, 0.18, 0.1])
check = CheckButtons(check_ax, ['Slider Mode'], [True])
check.on_clicked(toggle_slider_mode)

animate_ax = plt.axes([0.81, 0.3, 0.18, 0.05])
animate_button = Button(animate_ax, 'Animate')
animate_button.on_clicked(start_animation)

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

update_plot()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend()
plt.show()