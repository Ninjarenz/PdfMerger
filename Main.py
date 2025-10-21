#!/usr/bin/env python3
"""
Ein einzelnes Python-Skript: PDF Merger mit einfacher Tkinter-UI.
Benötigte Pakete:
  - pypdf  (oder PyPDF2 als Fallback)
  - Pillow (optional, nur für Datei-Icons wenn gewünscht)

Installation (Beispiel):
  pip install pypdf

Ausführen:
  python pdf_merger_tkinter.py
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

# PDF merger implementation: versuche pypdf, sonst PyPDF2
try:
    from pypdf import PdfMerger
except Exception:
    try:
        from PyPDF2 import PdfMerger
    except Exception:
        PdfMerger = None

class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("640x360")
        self.minsize(520, 300)

        self.file_list = []  # Liste von (pfad)

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        # Listbox + scrollbar
        list_frame = ttk.Frame(frm)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lb = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lb.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb.config(yscrollcommand=sb.set)

        # Buttons rechts
        ctrl_frame = ttk.Frame(frm, width=180)
        ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10,0))

        btn_add = ttk.Button(ctrl_frame, text="Hinzufügen", command=self.add_files)
        btn_add.pack(fill=tk.X, pady=4)

        btn_remove = ttk.Button(ctrl_frame, text="Entfernen", command=self.remove_selected)
        btn_remove.pack(fill=tk.X, pady=4)

        btn_up = ttk.Button(ctrl_frame, text="Nach oben", command=lambda: self.move_selected(-1))
        btn_up.pack(fill=tk.X, pady=4)

        btn_down = ttk.Button(ctrl_frame, text="Nach unten", command=lambda: self.move_selected(1))
        btn_down.pack(fill=tk.X, pady=4)

        ttk.Separator(ctrl_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        btn_merge = ttk.Button(ctrl_frame, text="Zusammenführen (Merge)", command=self.start_merge)
        btn_merge.pack(fill=tk.X, pady=4)

        btn_saveas = ttk.Button(ctrl_frame, text="Als... (Ziel wählen)", command=self.save_as)
        btn_saveas.pack(fill=tk.X, pady=4)

        btn_clear = ttk.Button(ctrl_frame, text="Liste leeren", command=self.clear_list)
        btn_clear.pack(fill=tk.X, pady=4)

        # Progress und status
        bottom = ttk.Frame(self, padding=(10,6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress = ttk.Progressbar(bottom, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0,8))

        self.status = ttk.Label(bottom, text="Bereit")
        self.status.pack(side=tk.RIGHT)

    def add_files(self):
        paths = filedialog.askopenfilenames(title="PDFs wählen", filetypes=[("PDF files", "*.pdf")])
        if not paths:
            return
        added = 0
        for p in paths:
            if p not in self.file_list:
                self.file_list.append(p)
                self.lb.insert(tk.END, os.path.basename(p))
                added += 1
        self.status.config(text=f"{added} Dateien hinzugefügt")

    def remove_selected(self):
        sel = list(self.lb.curselection())
        if not sel:
            return
        for i in reversed(sel):
            self.lb.delete(i)
            del self.file_list[i]
        self.status.config(text=f"{len(sel)} Dateien entfernt")

    def move_selected(self, direction: int):
        sel = list(self.lb.curselection())
        if not sel:
            return
        for index in (sel if direction>0 else reversed(sel)):
            new_index = index + direction
            if 0 <= new_index < self.lb.size():
                text = self.lb.get(index)
                file = self.file_list.pop(index)
                self.file_list.insert(new_index, file)
                self.lb.delete(index)
                self.lb.insert(new_index, text)
                self.lb.selection_set(new_index)
        self.status.config(text="Reihenfolge angepasst")

    def clear_list(self):
        self.lb.delete(0, tk.END)
        self.file_list.clear()
        self.status.config(text="Liste geleert")

    def save_as(self):
        path = filedialog.asksaveasfilename(title="Zieldatei speichern als", defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if not path:
            return
        self._last_output = path
        self.status.config(text=f"Ziel: {os.path.basename(path)}")

    def start_merge(self):
        if PdfMerger is None:
            messagebox.showerror("Fehler", "Kein PDF-Merger verfügbar. Bitte installieren Sie 'pypdf' oder 'PyPDF2'.")
            return
        if not self.file_list:
            messagebox.showwarning("Keine Dateien", "Bitte fügen Sie zuerst PDF-Dateien hinzu.")
            return
        output = getattr(self, '_last_output', None)
        if not output:
            output = filedialog.asksaveasfilename(title="Zieldatei speichern als", defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
            if not output:
                return
            self._last_output = output

        # Start Merge in Hintergrund-Thread, UI bleibt responsiv
        t = threading.Thread(target=self._merge_files, args=(self.file_list[:], output), daemon=True)
        t.start()

    def _merge_files(self, files, output_path):
        try:
            self.progress['value'] = 0
            total = len(files)
            step = 100.0 / max(total, 1)
            self.status.config(text="Mergen...")

            merger = PdfMerger()
            for i, f in enumerate(files, start=1):
                # pypdf/PyPDF2 akzeptiert Dateipfad
                merger.append(f)
                self.progress['value'] += step
                # force UI update
                self.update_idletasks()
            # Write out
            with open(output_path, 'wb') as out_f:
                merger.write(out_f)
            merger.close()
            self.progress['value'] = 100
            self.status.config(text=f"Fertig: {os.path.basename(output_path)}")
            messagebox.showinfo("Erfolgreich", f"Zusammengeführt als:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Mergen", str(e))
            self.status.config(text="Fehler")
            self.progress['value'] = 0

if __name__ == '__main__':
    app = PDFMergerApp()
    app.mainloop()
