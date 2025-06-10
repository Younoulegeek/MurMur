# 🐚 MurMur – Silent Bug Fixer for Everyday Glitches

**MurMur** is a lightweight local agent that detects and automatically fixes small recurring bugs on your system — quietly and in real time.

> _"Because the most useful assistant is often the quietest one."_

---

## 🔧 Features

- 🔍 Real-time detection of system events
- 🔄 Auto-fix for common issues (Wi-Fi, frozen Explorer, temp files)
- 🚀 Wi-Fi reconnect uses `netsh` to auto-select your saved profile
- 🧠 Pattern-based logic engine
- ⚙️ Modular design — plug in your own monitors and fixes
- 🤫 Runs silently in the background

---

## 🖥️ Use Cases

- Wi-Fi drops? MurMur reconnects.
- Explorer.exe frozen? MurMur restarts it.
- Temp files bloating your disk? MurMur cleans them up.

---

## 🚀 Getting Started

```bash
git clone https://github.com/younoulegeek/murmur-agent.git
cd murmur-agent
python main.py
```

codex/expliquer-la-base-de-code-aux-débutants
## 🖱️ Dashboard GUI

Launch the graphical interface with `python gui.py`.
It offers tabs for status, history and settings as well as
buttons to force a scan or display recent events.

