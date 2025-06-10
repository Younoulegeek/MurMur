# MurMur
MurMur is a silent local agent that detects and auto-fixes common technical issues like Wi-Fi drops or frozen processes. Modular, real-time, and fully automated — it works quietly in the background to keep your system smooth without interruptions.

The Wi-Fi repair logic now uses `netsh` to detect your saved profile and reconnect automatically on Windows.

## GUI Front-end

An enhanced Tkinter dashboard is provided in `gui.py`.
Run it with:

```bash
python gui.py
```

The window shows MurMur's status, a quick history of events and
buttons to force a scan or view more details.
