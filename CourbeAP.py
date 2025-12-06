from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from AnalyseAP import GetMySignal

# runtime state
_fig = None
_line = None
_anim = None
_x = []
_y = []

def _on_close(event):
    global _fig, _line, _anim, _x, _y
    _anim = None
    _line = None
    _fig = None
    _x = []
    _y = []

def _update(frame):
    now = datetime.now()
    _x.append(now)
    try:
        _y.append(int(GetMySignal()))
    except Exception:
        _y.append(float('nan'))
    # use last N automatically handled by matplotlib if data longer
    _line.set_data(_x, _y)
    ax = _fig.gca()
    ax.relim(); ax.autoscale_view()
    return _line,

def start_update(interval_ms=1000):
    """Create figure+animation on demand. Safe to call multiple times."""
    global _fig, _line, _anim
    if _anim is not None:
        return
    _fig = pyplot.figure(figsize=(12, 6), dpi=100)
    ax = _fig.gca()
    _line, = ax.plot_date([], [], '-')
    ax.grid(True)
    ax.set_xlabel('Temps'); ax.set_ylabel('Puissance Signal (%)')
    ax.set_title('Puissance du signal Wi‑Fi')
    _fig.canvas.mpl_connect('close_event', _on_close)
    _anim = FuncAnimation(_fig, _update, interval=interval_ms, blit=False)
    pyplot.show(block=False)

def stop_update():
    """Stop and close the figure if running."""
    global _fig, _anim
    if _anim is not None:
        try: _anim.event_source.stop()
        except Exception: pass
    if _fig is not None:
        try: pyplot.close(_fig)
        except Exception: pass
    _fig = None
    _anim = None