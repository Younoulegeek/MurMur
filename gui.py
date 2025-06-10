import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class MurMurGUI:
    def __init__(self, master):
        self.master = master
        master.title("MurMur GUI")
        self.process = None

        self.status_var = tk.StringVar(value="Stopped")
        tk.Label(master, text="MurMur status:").pack(pady=(10,0))
        self.status_label = tk.Label(master, textvariable=self.status_var, fg="green")
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Start", command=self.start_murmur)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_murmur, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def start_murmur(self):
        if self.process is None:
            self.process = subprocess.Popen([sys.executable, "main.py"])
            self.status_var.set("Running")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_murmur(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.status_var.set("Stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def on_close(self):
        if self.process is not None:
            self.process.terminate()
        self.master.destroy()


def main():
    root = tk.Tk()
    gui = MurMurGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
