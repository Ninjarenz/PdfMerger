#!/usr/bin/env python3
"""
A single Python script: PDF Merger with a simple Tkinter UI.
Required packages:
  - pypdf (or PyPDF2 as fallback)
  - Pillow (optional, only for file icons if desired)

Installation (Example):
  pip install pypdf

Execution:
  python pdf_merger_tkinter.py
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

# PDF merger implementation: try pypdf, otherwise PyPDF2
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

        btn_add = ttk.Button(ctrl_frame, text="Add", command=self.add_files)
        btn_add.pack(fill=tk.X, pady=4)

        btn_remove = ttk.Button(ctrl_frame, text="Remove", command=self.remove_selected)
        btn_remove.pack(fill=tk.X, pady=4)

        btn_up = ttk.Button(ctrl_frame, text="Move Up", command=lambda: self.move_selected(-1))
        btn_up.pack(fill=tk.X, pady=4)

        btn_down = ttk.Button(ctrl_frame, text="Move Down", command=lambda: self.move_selected(1))
        btn_down.pack(fill=tk.X, pady=4)

        ttk.Separator(ctrl_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        btn_merge = ttk.Button(ctrl_frame, text="Merge", command=self.start_merge)
        btn_merge.pack(fill=tk.X, pady=4)

        btn_saveas = ttk.Button(ctrl_frame, text="Save As... (Choose Destination)", command=self.save_as)
        btn_saveas.pack(fill=tk.X, pady=4)

        btn_clear = ttk.Button(ctrl_frame, text="Clear List", command=self.clear_list)
        btn_clear.pack(fill=tk.X, pady=4)

        # Progress and status
        bottom = ttk.Frame(self, padding=(10,6))
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress = ttk.Progressbar(bottom, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0,8))

        self.status = ttk.Label(bottom, text="Ready")

    def add_files(self):
        paths = filedialog.askopenfilenames(title="Select PDFs", filetypes=[("PDF files", "*.pdf")])
        if not paths:
            return
        added = 0
        for p in paths:
            if p not in self.file_list:
                self.file_list.append(p)
                self.lb.insert(tk.END, os.path.basename(p))
                added += 1
        self.status.config(text=f"{added} files added")

    def remove_selected(self):
        sel = list(self.lb.curselection())
        if not sel:
            return
        for i in reversed(sel):
            self.lb.delete(i)
            del self.file_list[i]
        self.status.config(text=f"{len(sel)} files removed")

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
                self.lb.selection_set(new_index)
        self.status.config(text="Order adjusted")

    def clear_list(self):
        self.lb.delete(0, tk.END)
        self.file_list.clear()
        self.status.config(text="List cleared")

    def save_as(self):
        path = filedialog.asksaveasfilename(title="Save Destination File As", defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if not path:
            return
        self._last_output = path
        self.status.config(text=f"Destination: {os.path.basename(path)}")

    def start_merge(self):
        if PdfMerger is None:
            messagebox.showerror("Error", "No PDF merger available. Please install 'pypdf' or 'PyPDF2'.")
            return
        if not self.file_list:
            messagebox.showwarning("No Files", "Please add PDF files first.")
            return
        output = getattr(self, '_last_output', None)
        if not output:
            output = filedialog.asksaveasfilename(title="Save Destination File As", defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
            if not output:
                return
            self._last_output = output

        # Start Merge in background thread, UI remains responsive
        t = threading.Thread(target=self._merge_files, args=(self.file_list[:], output), daemon=True)
        t.start()

    def _merge_files(self, files, output_path):
        try:
            self.progress['value'] = 0
            total = len(files)
            step = 100.0 / max(total, 1)
            self.status.config(text="Merging...")

            merger = PdfMerger()
            for i, f in enumerate(files, start=1):
                # pypdf/PyPDF2 accepts file path
                merger.append(f)
                self.progress['value'] += step
                # force UI update
                self.update_idletasks()
            # Write out
            with open(output_path, 'wb') as out_f:
                merger.write(out_f)
            merger.close()
            self.progress['value'] = 100
            self.status.config(text=f"Done: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", f"Merged as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Merge Error", str(e))
            self.status.config(text="Error")
            self.progress['value'] = 0

if __name__ == '__main__':
    app = PDFMergerApp()
    app.mainloop()
