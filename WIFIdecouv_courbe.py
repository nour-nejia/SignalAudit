from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from WIFIdecouv import GetDSignal

# runtime state
_fig = None
_ax = None
_anim = None
_times = []
_series = {}   # ssid -> list
_lines = {}

def _on_close(event):
    global _fig, _ax, _anim, _times, _series, _lines
    _anim = None
    _fig = None
    _ax = None
    _times = []
    _series = {}
    _lines = {}

def _update_all(frame):
    now = datetime.now()
    _times.append(now)
    data = GetDSignal() or []
    seen = set()
    for item in data:
        try:
            ssid, sig = item[0], item[1]
        except Exception:
            continue
        if not ssid or 'BSSID' in str(ssid).upper():
            continue
        ssid = str(ssid).strip()
        seen.add(ssid)
        _series.setdefault(ssid, [])
        try:
            _series[ssid].append(int(sig))
        except Exception:
            _series[ssid].append(float('nan'))
        if ssid not in _lines:
            ln, = _ax.plot([], [], '-', label=ssid)
            _lines[ssid] = ln
            _ax.legend(loc='upper right', fontsize='small')
        _lines[ssid].set_data(_times[-len(_series[ssid]):], _series[ssid])

    # append gap for missing SSIDs
    for ssid in list(_series.keys()):
        if ssid not in seen:
            _series[ssid].append(float('nan'))
            _lines[ssid].set_data(_times[-len(_series[ssid]):], _series[ssid])

    _ax.relim(); _ax.autoscale_view()
    return list(_lines.values())

def start_updateALL(interval_ms=1000):
    """Create multi-SSID figure+animation on demand."""
    global _fig, _ax, _anim
    if _anim is not None:
        return
    _fig = pyplot.figure(figsize=(12, 6), dpi=100)
    _ax = _fig.gca()
    _ax.grid(True)
    _ax.set_xlabel('Temps'); _ax.set_ylabel('Puissance Signal (%)')
    _ax.set_title('Puissance du signal Wi‑Fi')
    _fig.canvas.mpl_connect('close_event', _on_close)
    _anim = FuncAnimation(_fig, _update_all, interval=interval_ms, blit=False)
    pyplot.show(block=False)

def stop_updateALL():
    global _fig, _anim
    if _anim is not None:
        try: _anim.event_source.stop()
        except Exception: pass
    if _fig is not None:
        try: pyplot.close(_fig)
        except Exception: pass
    _fig = None
    _anim = None