# DEIVS - Digital Evidence Integrity & Verification System
# GUI connected to the existing SQLite, SHA-256 and PDF modules.

import os
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

from database import (
    initialize_database, add_evidence, get_all_evidence,
    get_evidence_by_id, get_verification_history,
    get_deleted_evidence, delete_evidence_record, save_verification,
    restore_evidence_record, permanently_delete_evidence_record
)
from hashing import calculate_sha256
from report import generate_report
from app_paths import get_database_path, get_reports_dir


class DEIVSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEIVS | Digital Evidence Integrity System")
        self.root.geometry("1240x780")
        self.root.minsize(1050, 680)
        self.c = {
            "bg": "#0B1220", "sidebar": "#111C2E", "panel": "#17243A",
            "panel2": "#1D2D46", "blue": "#3478F6", "blue_hover": "#2563D9",
            "text": "#F3F6FC", "muted": "#9AAAC1", "green": "#19B985",
            "red": "#F05B63", "amber": "#E9AD4B", "line": "#2A3B55"
        }
        self.root.configure(bg=self.c["bg"])
        initialize_database()
        self.configure_styles()
        self.build_shell()
        self.show_dashboard()

    def configure_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("DEIVS.Treeview", background=self.c["panel"],
                    foreground=self.c["text"], fieldbackground=self.c["panel"],
                    rowheight=34, borderwidth=0, font=("Arial", 10))
        s.configure("DEIVS.Treeview.Heading", background=self.c["panel2"],
                    foreground=self.c["text"], font=("Arial", 10, "bold"),
                    relief="flat", padding=9)
        s.map("DEIVS.Treeview", background=[("selected", "#244C88")],
              foreground=[("selected", "#FFFFFF")])

    def build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=self.c["sidebar"], width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="DEIVS", bg=self.c["sidebar"],
                 fg="#43C6F5", font=("Arial", 29, "bold")).pack(anchor="w", padx=25, pady=(30, 0))
        tk.Label(self.sidebar, text="DIGITAL FORENSICS", bg=self.c["sidebar"],
                 fg=self.c["muted"], font=("Arial", 9, "bold")).pack(anchor="w", padx=27, pady=(2, 30))

        items = [
            ("Dashboard", self.show_dashboard),
            ("Register Evidence", self.register_evidence),
            ("View Evidence", self.show_evidence),
            ("Verify Integrity", self.verify_prompt),
            ("Verification History", self.history_prompt),
            ("Deleted Evidence", self.show_deleted),
            ("Generate Report", self.report_prompt),
            ("Reset Database", self.reset_database),
            ("About / Credits", self.show_about),
            ("Exit", self.exit_app),
        ]
        for label, action in items:
            b = tk.Label(self.sidebar, text=label, anchor="w",
                         padx=18, pady=12, bg=self.c["panel2"], fg=self.c["text"],
                         cursor="hand2", font=("Arial", 10, "bold"))
            b.pack(fill="x", padx=12, pady=3)
            b.bind("<Button-1>", lambda event, fn=action: fn())
            b.bind("<Enter>", lambda e, w=b: w.configure(bg=self.c["blue"], fg="#FFFFFF"))
            b.bind("<Leave>", lambda e, w=b: w.configure(bg=self.c["panel2"], fg=self.c["text"]))

        tk.Label(self.sidebar, text="DEIVS v1.0  •  Group Academic Project",
                 bg=self.c["sidebar"], fg=self.c["muted"],
                 font=("Arial", 8)).pack(side="bottom", pady=18)
        self.main = tk.Frame(self.root, bg=self.c["bg"])
        self.main.pack(side="left", fill="both", expand=True)

    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    def header(self, title, subtitle):
        tk.Label(self.main, text=title, bg=self.c["bg"], fg=self.c["text"],
                 font=("Arial", 25, "bold")).pack(anchor="w", padx=34, pady=(28, 3))
        tk.Label(self.main, text=subtitle, bg=self.c["bg"], fg=self.c["muted"],
                 font=("Arial", 10)).pack(anchor="w", padx=36, pady=(0, 22))

    def panel(self, parent, padx=18, pady=16):
        return tk.Frame(parent, bg=self.c["panel"], padx=padx, pady=pady)

    def button(self, parent, text, action, color=None):
        # Labels are used as custom-drawn buttons because macOS Aqua can
        # override the background colours of native Tk buttons.
        base = color or self.c["blue"]
        b = tk.Label(parent, text=text, bg=base, fg="#FFFFFF",
                     padx=16, pady=11, cursor="hand2",
                     font=("Arial", 10, "bold"), relief="flat", bd=0)
        b.bind("<Button-1>", lambda event: action())
        b.bind("<Enter>", lambda event: b.configure(bg=self.c["blue_hover"]))
        b.bind("<Leave>", lambda event: b.configure(bg=base))
        return b

    def stats(self):
        rows = get_all_evidence()
        unchanged = modified = missing = 0
        for row in rows:
            history = get_verification_history(row[0])
            if history:
                status = history[0][3]
                unchanged += status == "UNCHANGED"
                modified += status == "MODIFIED"
                missing += status == "MISSING"
        return len(rows), unchanged, modified, missing

    def show_dashboard(self):
        self.clear()
        self.header("Dashboard", "Digital Evidence Integrity & Verification System")
        total, unchanged, modified, missing = self.stats()
        cards = tk.Frame(self.main, bg=self.c["bg"])
        cards.pack(fill="x", padx=34)
        for title, value, color in [
            ("ACTIVE EVIDENCE", total, "#4B8BFF"),
            ("UNCHANGED", unchanged, self.c["green"]),
            ("MODIFIED", modified, self.c["red"]),
            ("MISSING", missing, self.c["amber"])
        ]:
            card = self.panel(cards, 18, 17)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            tk.Label(card, text=title, bg=self.c["panel"], fg=self.c["muted"],
                     font=("Arial", 9, "bold")).pack(anchor="w")
            tk.Label(card, text=str(value), bg=self.c["panel"], fg=color,
                     font=("Arial", 28, "bold")).pack(anchor="w", pady=(9, 0))

        welcome = self.panel(self.main, 26, 24)
        welcome.pack(fill="x", padx=34, pady=(28, 20))
        tk.Label(welcome, text="Welcome to DEIVS", bg=self.c["panel"],
                 fg=self.c["text"], font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(welcome, text="Register digital evidence, preserve its SHA-256 reference hash,\n"
                               "and verify whether the original file has changed.",
                 bg=self.c["panel"], fg=self.c["muted"], justify="left",
                 font=("Arial", 10)).pack(anchor="w", pady=(10, 0))

        tk.Label(self.main, text="Quick Actions", bg=self.c["bg"], fg=self.c["text"],
                 font=("Arial", 15, "bold")).pack(anchor="w", padx=34, pady=(3, 12))
        actions = tk.Frame(self.main, bg=self.c["bg"])
        actions.pack(anchor="w", padx=34)
        self.button(actions, "Register Evidence", self.register_evidence).pack(side="left", padx=(0, 10))
        self.button(actions, "Verify by ID", self.verify_prompt, self.c["green"]).pack(side="left", padx=10)
        self.button(actions, "Generate Report", self.report_prompt, "#475F80").pack(side="left", padx=10)

        recent = self.panel(self.main, 18, 14)
        recent.pack(fill="both", expand=True, padx=34, pady=(22, 24))
        tk.Label(recent, text="Recently Registered Evidence", bg=self.c["panel"],
                 fg=self.c["text"], font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        rows = get_all_evidence()[:5]
        if not rows:
            tk.Label(recent, text="No evidence registered yet.", bg=self.c["panel"],
                     fg=self.c["muted"]).pack(anchor="w")
        for row in rows:
            tk.Label(recent, text=f"#{row[0]}   {row[1]}   •   {row[5]}",
                     bg=self.c["panel"], fg=self.c["muted"], font=("Arial", 9)).pack(anchor="w", pady=3)

    def register_evidence(self):
        path = filedialog.askopenfilename(title="Select Digital Evidence",
                                          filetypes=[("All files", "*.*")])
        if not path:
            return
        try:
            path = os.path.abspath(path)
            name = os.path.basename(path)
            size = os.path.getsize(path)
            digest = calculate_sha256(path)
            if not digest:
                messagebox.showerror("DEIVS", "Could not read the selected file.")
                return
            eid = add_evidence(name, path, size, digest)
            messagebox.showinfo("Evidence Registered",
                                f"Evidence ID: {eid}\nFile: {name}\nSize: {size:,} bytes\n\nSHA-256:\n{digest}")
            self.show_dashboard()
        except Exception as exc:
            messagebox.showerror("Registration Error", str(exc))

    def make_tree(self, parent, columns, headings, widths):
        frame = tk.Frame(parent, bg=self.c["panel"])
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=columns, show="headings", style="DEIVS.Treeview")
        for col, heading, width in zip(columns, headings, widths):
            # Keep every table visually consistent: centered headings and cell values.
            tree.heading(col, text=heading, anchor="center")
            tree.column(col, width=width, minwidth=65, anchor="center", stretch=True)

        # Scrollbars appear only when the table content exceeds the visible area.
        vertical_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        horizontal_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky="nsew")

        def update_vertical_scroll(first, last):
            vertical_scroll.set(first, last)
            if float(first) <= 0.0 and float(last) >= 1.0:
                vertical_scroll.grid_remove()
            else:
                vertical_scroll.grid(row=0, column=1, sticky="ns")

        def update_horizontal_scroll(first, last):
            horizontal_scroll.set(first, last)
            if float(first) <= 0.0 and float(last) >= 1.0:
                horizontal_scroll.grid_remove()
            else:
                horizontal_scroll.grid(row=1, column=0, sticky="ew")

        tree.configure(
            yscrollcommand=update_vertical_scroll,
            xscrollcommand=update_horizontal_scroll
        )

        return tree

    def show_evidence(self):
        self.clear()
        self.header("Evidence Repository", "Browse, search and manage active evidence records")
        bar = tk.Frame(self.main, bg=self.c["bg"])
        bar.pack(fill="x", padx=34, pady=(0, 12))
        query = tk.StringVar()
        tk.Entry(bar, textvariable=query, width=30, bg=self.c["panel"], fg=self.c["text"],
                 insertbackground="white", relief="flat").pack(side="left", ipady=8)
        box = self.panel(self.main, 12, 12)
        box.pack(fill="both", expand=True, padx=34, pady=(0, 22))
        tree = self.make_tree(box, ("id", "name", "size", "date", "status"),
                              ("ID", "FILE NAME", "SIZE (BYTES)", "REGISTERED", "STATUS"),
                              (65, 300, 130, 180, 110))

        def load():
            tree.delete(*tree.get_children())
            q = query.get().strip().lower()
            for r in get_all_evidence():
                if not q or q in str(r[0]).lower() or q in r[1].lower():
                    tree.insert("", "end", iid=str(r[0]), values=(r[0], r[1], r[3], r[5], r[6]))

        def selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select Evidence", "Select a record in the table first.")
                return None
            return int(sel[0])

        def details():
            eid = selected()
            if eid is None:
                return
            r = get_evidence_by_id(eid)
            if r:
                messagebox.showinfo(f"Evidence #{eid}",
                    f"File: {r[1]}\nPath: {r[2]}\nSize: {r[3]} bytes\n"
                    f"Original SHA-256:\n{r[4]}\nRegistered: {r[5]}\nStatus: {r[6]}")

        def verify():
            eid = selected()
            if eid is not None:
                self.verify_id(eid)

        def archive():
            eid = selected()
            if eid is None:
                return
            r = get_evidence_by_id(eid)
            if messagebox.askyesno("Archive Evidence",
                    f"Archive #{eid} ({r[1]})?\nThe original file will NOT be deleted."):
                result = delete_evidence_record(eid)
                if result == "DELETED":
                    messagebox.showinfo("DEIVS", "Evidence record archived.")
                    load()
                else:
                    messagebox.showwarning("DEIVS", f"Action result: {result}")

        self.button(bar, "Search", load).pack(side="left", padx=8)
        self.button(bar, "Refresh", load, "#475F80").pack(side="left", padx=4)
        self.button(bar, "Details", details, "#475F80").pack(side="right", padx=4)
        self.button(bar, "Verify", verify, self.c["green"]).pack(side="right", padx=4)
        self.button(bar, "Archive", archive, self.c["red"]).pack(side="right", padx=4)
        tree.bind("<Double-1>", lambda event: details())
        load()

    def ask_id(self, title):
        return simpledialog.askinteger(title, "Enter Evidence ID:", parent=self.root, minvalue=1)

    def verify_prompt(self):
        eid = self.ask_id("Verify Evidence")
        if eid is not None:
            self.verify_id(eid)

    def verify_id(self, eid):
        r = get_evidence_by_id(eid)
        if not r:
            messagebox.showerror("Not Found", f"Evidence ID {eid} was not found.")
            return
        if r[6] == "DELETED":
            messagebox.showwarning("Archived Evidence", "Verification is not allowed for archived records.")
            return
        if not os.path.isfile(r[2]):
            current, status = None, "MISSING"
        else:
            current = calculate_sha256(r[2])
            if current is None:
                status = "ERROR"
            elif current == r[4]:
                status = "UNCHANGED"
            else:
                status = "MODIFIED"
        save_verification(eid, current, status)
        messagebox.showinfo("Integrity Verification",
            f"Evidence ID: {eid}\nFile: {r[1]}\n\nResult: {status}\n\n"
            f"Original SHA-256:\n{r[4]}\n\nCurrent SHA-256:\n{current or 'Not available'}")
        self.show_dashboard()

    def history_prompt(self):
        eid = self.ask_id("Verification History")
        if eid is not None:
            self.show_history(eid)

    def show_history(self, eid):
        r = get_evidence_by_id(eid)
        if not r:
            messagebox.showerror("Not Found", f"Evidence ID {eid} was not found.")
            return
        self.clear()
        self.header(f"Verification History — Evidence #{eid}", r[1])
        box = self.panel(self.main, 12, 12)
        box.pack(fill="both", expand=True, padx=34, pady=(0, 20))
        tree = self.make_tree(box, ("vid", "status", "date", "hash"),
                              ("VERIFICATION ID", "RESULT", "DATE", "CURRENT SHA-256"),
                              (130, 130, 190, 470))
        for item in get_verification_history(eid):
            tree.insert("", "end", values=(item[0], item[3], item[4], item[2] or "Not available"))
        self.button(self.main, "Back to Dashboard", self.show_dashboard, "#475F80").pack(
            anchor="w", padx=34, pady=(0, 20))

    def show_deleted(self):
        self.clear()
        self.header("Deleted Evidence", "Restore archived records or permanently remove them from the DEIVS database")
        bar = tk.Frame(self.main, bg=self.c["bg"])
        bar.pack(fill="x", padx=34, pady=(0, 12))

        box = self.panel(self.main, 12, 12)
        box.pack(fill="both", expand=True, padx=34, pady=(0, 20))
        tree = self.make_tree(box, ("id", "name", "date", "deleted"),
                              ("ID", "FILE NAME", "REGISTERED", "ARCHIVED AT"),
                              (70, 330, 200, 200))

        def load():
            tree.delete(*tree.get_children())
            for r in get_deleted_evidence():
                tree.insert("", "end", iid=str(r[0]),
                            values=(r[0], r[1], r[5], r[7] or "—"))

        def selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select Evidence", "Select an archived record first.")
                return None
            return int(sel[0])

        def restore():
            eid = selected()
            if eid is None:
                return
            record = get_evidence_by_id(eid)
            if not record:
                messagebox.showerror("Not Found", "The selected evidence record no longer exists.")
                load()
                return
            if not messagebox.askyesno(
                "Restore Evidence",
                f"Restore Evidence #{eid} — {record[1]}?\n\n"
                "The record will return to the active Evidence Repository."
            ):
                return
            result = restore_evidence_record(eid)
            if result == "RESTORED":
                messagebox.showinfo("DEIVS", "Evidence record restored successfully.")
                load()
                self.show_dashboard()
            else:
                messagebox.showwarning("DEIVS", f"Action result: {result}")

        def permanently_delete():
            eid = selected()
            if eid is None:
                return
            record = get_evidence_by_id(eid)
            if not record:
                messagebox.showerror("Not Found", "The selected evidence record no longer exists.")
                load()
                return
            confirmed = messagebox.askyesno(
                "Permanent Deletion — Step 1",
                f"PERMANENTLY DELETE Evidence #{eid} — {record[1]}?\n\n"
                "This removes the evidence record and its verification history from DEIVS.\n"
                "The original file on your computer will NOT be deleted.\n\n"
                "This action cannot be undone."
            )
            if not confirmed:
                return
            typed = simpledialog.askstring(
                "Confirm Permanent Deletion",
                "Type DELETE to permanently remove this record:",
                parent=self.root
            )
            if typed != "DELETE":
                messagebox.showinfo("DEIVS", "Permanent deletion cancelled.")
                return
            result = permanently_delete_evidence_record(eid)
            if result == "PERMANENTLY_DELETED":
                messagebox.showinfo("DEIVS", "Evidence record and its verification history permanently deleted.")
                load()
                self.show_dashboard()
            else:
                messagebox.showwarning("DEIVS", f"Action result: {result}")

        self.button(bar, "Restore Evidence", restore, self.c["green"]).pack(side="left", padx=(0, 8))
        self.button(bar, "Delete Permanently", permanently_delete, self.c["red"]).pack(side="left", padx=8)
        self.button(bar, "Refresh", load, "#475F80").pack(side="right", padx=4)
        self.button(self.main, "Back to Dashboard", self.show_dashboard, "#475F80").pack(
            anchor="w", padx=34, pady=(0, 20))
        tree.bind("<Double-1>", lambda event: restore())
        load()

    def report_prompt(self):
        eid = self.ask_id("Generate Investigation Report")

        if eid is None:
            return

        record = get_evidence_by_id(eid)
        if not record:
            messagebox.showerror(
                "Not Found",
                f"Evidence ID {eid} was not found."
            )
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggested_name = f"DEIVS_Report_{eid}_{timestamp}.pdf"

        # Let the user choose the exact PDF destination before generation.
        selected_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save DEIVS Investigation Report",
            initialdir=str(get_reports_dir()),
            initialfile=suggested_name,
            defaultextension=".pdf",
            filetypes=[("PDF document", "*.pdf")],
            confirmoverwrite=True
        )

        # Cancel means no report is generated.
        if not selected_path:
            return

        try:
            report_path = generate_report(eid, output_path=selected_path)

            if not report_path:
                messagebox.showerror(
                    "Report Error",
                    "Could not generate the PDF report."
                )
                return

            self.show_report_success_dialog(report_path)

        except Exception as exc:
            messagebox.showerror("Report Error", str(exc))

    def show_report_success_dialog(self, report_path):
        """Show a custom success window with quick PDF and folder actions."""
        report_path = str(Path(report_path).resolve())
        report_name = os.path.basename(report_path)

        window = tk.Toplevel(self.root)
        window.title("Report Generated | DEIVS")
        window.configure(bg=self.c["bg"])
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        card = tk.Frame(window, bg=self.c["panel"], padx=26, pady=22)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(
            card, text="✓", bg=self.c["panel"], fg=self.c["green"],
            font=("Arial", 30, "bold")
        ).pack(anchor="w")

        tk.Label(
            card, text="Report Generated Successfully!", bg=self.c["panel"],
            fg=self.c["text"], font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(4, 6))

        tk.Label(
            card, text="Your investigation report has been saved.",
            bg=self.c["panel"], fg=self.c["muted"],
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 14))

        tk.Label(
            card, text=report_name, bg=self.c["panel2"],
            fg=self.c["text"], font=("Arial", 10, "bold"),
            anchor="w", padx=10, pady=9, wraplength=440, justify="left"
        ).pack(fill="x")

        tk.Label(
            card, text=report_path, bg=self.c["panel"],
            fg=self.c["muted"], font=("Arial", 8),
            anchor="w", justify="left", wraplength=440
        ).pack(fill="x", pady=(8, 16))

        actions = tk.Frame(card, bg=self.c["panel"])
        actions.pack(fill="x")

        self.button(
            actions, "Open File",
            lambda: self.open_report_file(report_path), self.c["blue"]
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.button(
            actions, "Open File Location",
            lambda: self.open_report_location(report_path), "#475F80"
        ).pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.button(
            card, "OK", window.destroy, self.c["green"]
        ).pack(anchor="e", pady=(18, 0))

        window.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - window.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - window.winfo_height()) // 2
        window.geometry(f"+{max(0, x)}+{max(0, y)}")

    def open_report_file(self, report_path):
        """Open the generated PDF with the operating system's default viewer."""
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", report_path])
            elif sys.platform == "win32":
                os.startfile(report_path)
            else:
                subprocess.Popen(["xdg-open", report_path])
        except Exception as exc:
            messagebox.showerror("Open File Error", str(exc), parent=self.root)

    def open_report_location(self, report_path):
        """Reveal the PDF in Finder/Explorer or open its containing folder."""
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", "-R", report_path])
            elif sys.platform == "win32":
                subprocess.Popen(["explorer", "/select,", os.path.normpath(report_path)])
            else:
                subprocess.Popen(["xdg-open", str(Path(report_path).parent)])
        except Exception as exc:
            messagebox.showerror("Open Location Error", str(exc), parent=self.root)

    def show_about(self):
        window = tk.Toplevel(self.root)
        window.title("About DEIVS | Project Team")
        window.configure(bg=self.c["bg"])
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        outer = tk.Frame(window, bg=self.c["panel"], padx=28, pady=24)
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        tk.Label(outer, text="DEIVS", bg=self.c["panel"], fg="#43C6F5",
                 font=("Arial", 25, "bold")).pack(anchor="w")
        tk.Label(outer, text="Digital Evidence Integrity & Verification System",
                 bg=self.c["panel"], fg=self.c["muted"],
                 font=("Arial", 10)).pack(anchor="w", pady=(2, 18))

        tk.Label(outer, text="PROJECT TEAM", bg=self.c["panel"],
                 fg=self.c["text"], font=("Arial", 10, "bold")).pack(anchor="w")
        team = [
            "Pranav Mohan Agrawal  •  1272260373",
            "Rujula Jadhav  •  1272261758",
            "Swayam Dakare  •  1272261583",
            "Samruddhi Salunke  •  1272261145",
        ]
        for member in team:
            tk.Label(outer, text=member, bg=self.c["panel"],
                     fg=self.c["muted"], font=("Arial", 9)).pack(anchor="w", pady=3)

        tk.Frame(outer, bg=self.c["line"], height=1).pack(fill="x", pady=15)
        tk.Label(outer, text="TEAM CONTRIBUTIONS", bg=self.c["panel"],
                 fg=self.c["text"], font=("Arial", 10, "bold")).pack(anchor="w")
        contributions = [
            ("Pranav Mohan Agrawal", "Software Development & Code Implementation"),
            ("Rujula Jadhav", "Presentation (PPT) Preparation"),
            ("Swayam Dakare", "Project Poster Design"),
            ("Samruddhi Salunke", "Project Presentation"),
        ]
        for name, role in contributions:
            tk.Label(outer, text=name, bg=self.c["panel"], fg=self.c["text"],
                     font=("Arial", 9, "bold")).pack(anchor="w", pady=(8, 1))
            tk.Label(outer, text=role, bg=self.c["panel"], fg=self.c["muted"],
                     font=("Arial", 9)).pack(anchor="w")
        tk.Label(outer, text="Group Academic Project  •  DEIVS v1.0",
                 bg=self.c["panel"], fg=self.c["muted"],
                 font=("Arial", 8)).pack(anchor="w", pady=(15, 0))

        self.button(outer, "Close", window.destroy, "#475F80").pack(anchor="e", pady=(18, 0))
        window.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - window.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - window.winfo_height()) // 2
        window.geometry(f"+{max(0, x)}+{max(0, y)}")

    def exit_app(self):
        if messagebox.askyesno(
            "Exit DEIVS",
            "Are you sure you want to close DEIVS?"
        ):
            self.root.destroy()

    def reset_database(self):
        ok = messagebox.askyesno(
            "Reset Database",
            "Permanently clear ALL evidence records and verification history?\n\n"
            "Original evidence files and generated PDF reports will be preserved."
        )
        if not ok:
            return
        try:
            conn = sqlite3.connect(str(get_database_path()))
            try:
                conn.execute("PRAGMA foreign_keys = ON")
                conn.execute("DELETE FROM verification_history")
                conn.execute("DELETE FROM evidence")
                conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('evidence', 'verification_history')")
                conn.commit()
            finally:
                conn.close()
            messagebox.showinfo("DEIVS", "Database reset successfully.")
            self.show_dashboard()
        except sqlite3.Error as exc:
            messagebox.showerror("Reset Error", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = DEIVSApp(root)
    root.mainloop()
