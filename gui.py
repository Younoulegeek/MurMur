"""Interface graphique Tkinter pour MurMur.

Cette interface offre un tableau de bord minimaliste permettant
de surveiller l'agent et de déclencher un scan manuel.
Style sombre, texte blanc et boutons verts.
"""

import tkinter as tk
from tkinter import ttk


class MurMurGUI:
    """Fenêtre principale de l'application."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("MurMur — Agent Silencieux de Surveillance")

        # Palette de couleurs
        self.bg_color = "#1e1e2f"
        self.fg_color = "white"
        self.btn_color = "#2ecc71"

        self.master.configure(bg=self.bg_color)

        # Liste des événements simulés
        self.events: list[str] = []

        # Configuration du style ttk pour fond sombre
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.bg_color, foreground=self.fg_color)
        style.map("TNotebook.Tab", background=[("selected", self.bg_color)])

        # Création du Notebook (onglets)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)

        # Onglets
        self.state_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.history_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.settings_frame = tk.Frame(self.notebook, bg=self.bg_color)

        self.notebook.add(self.state_frame, text="État")
        self.notebook.add(self.history_frame, text="Historique")
        self.notebook.add(self.settings_frame, text="Paramètres")

        # ----- Onglet État -----
        self.status_var = tk.StringVar(value="🟢 Tout est calme.")
        status_label = tk.Label(
            self.state_frame,
            textvariable=self.status_var,
            fg=self.fg_color,
            bg=self.bg_color,
            font=("Arial", 14),
        )
        status_label.pack(pady=10)

        # Boutons de l'onglet État
        button_frame = tk.Frame(self.state_frame, bg=self.bg_color)
        button_frame.pack(pady=5)

        details_btn = tk.Button(
            button_frame,
            text="Voir les détails",
            command=self.show_details,
            bg=self.btn_color,
            fg="white",
            width=15,
            relief=tk.FLAT,
        )
        details_btn.grid(row=0, column=0, padx=5)

        scan_btn = tk.Button(
            button_frame,
            text="Forcer un scan",
            command=self.force_scan,
            bg=self.btn_color,
            fg="white",
            width=15,
            relief=tk.FLAT,
        )
        scan_btn.grid(row=0, column=1, padx=5)

        # Canvas pour une petite animation circulaire
        self.canvas = tk.Canvas(self.state_frame, width=40, height=40, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.circle = self.canvas.create_oval(10, 10, 30, 30, fill=self.btn_color, outline=self.btn_color)
        self.pulse_direction = 1
        self.animate()

        # ----- Onglet Historique -----
        self.history_listbox = tk.Listbox(
            self.history_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            highlightthickness=0,
            selectbackground="#444",
            width=50,
        )
        self.history_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        # ----- Onglet Paramètres -----
        tk.Label(
            self.settings_frame,
            text="(Paramètres à venir)",
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(pady=20)

    # ----- Méthodes de l'interface -----
    def show_details(self) -> None:
        """Ouvre une fenêtre affichant la liste des événements."""
        details = tk.Toplevel(self.master)
        details.title("Événements récents")
        details.configure(bg=self.bg_color)

        listbox = tk.Listbox(details, bg=self.bg_color, fg=self.fg_color, width=60)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)
        for evt in self.events[-50:]:
            listbox.insert(tk.END, evt)

    def force_scan(self) -> None:
        """Simule un scan de 3 secondes."""
        self.status_var.set("Scan en cours...")
        self.master.after(3000, self.scan_finished)

    def scan_finished(self) -> None:
        """Fin du scan : mise à jour de l'état et journalisation."""
        self.status_var.set("Scan terminé")
        self.events.append("Scan manuel exécuté")
        self.history_listbox.insert(tk.END, self.events[-1])

    def animate(self) -> None:
        """Fait pulser le cercle pour indiquer l'activité."""
        x0, y0, x1, y1 = self.canvas.coords(self.circle)
        if x0 <= 5:
            self.pulse_direction = 1
        elif x0 >= 15:
            self.pulse_direction = -1

        self.canvas.move(self.circle, -self.pulse_direction, -self.pulse_direction)
        self.canvas.after(200, self.animate)


def main() -> None:
    root = tk.Tk()
    MurMurGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

