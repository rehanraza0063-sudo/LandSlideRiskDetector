
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime

DB_NAME = "landslide_history.db"


def initialize_database():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                location TEXT,
                rainfall REAL,
                slope REAL,
                moisture REAL,
                movement TEXT,
                earthquake TEXT,
                score INTEGER,
                risk TEXT,
                recommendation TEXT
            )
        """)


def assess_risk(rainfall, slope, moisture, movement, earthquake):
    """Illustrative screening score, not a validated prediction model."""
    score = 0

    # Rainfall: mm entered for the preceding 24 hours
    if rainfall >= 200:
        score += 35
    elif rainfall >= 100:
        score += 25
    elif rainfall >= 50:
        score += 15
    elif rainfall >= 25:
        score += 5

    # Slope angle in degrees
    if slope >= 45:
        score += 20
    elif slope >= 35:
        score += 15
    elif slope >= 25:
        score += 10
    elif slope >= 15:
        score += 5

    # Soil moisture entered as a percentage
    if moisture >= 90:
        score += 25
    elif moisture >= 75:
        score += 20
    elif moisture >= 60:
        score += 10
    elif moisture >= 40:
        score += 5

    movement_points = {
        "None observed": 0,
        "Slow movement": 15,
        "Abrupt movement": 30
    }
    score += movement_points[movement]

    if earthquake == "Recent earthquake":
        score += 15

    score = min(score, 100)

    # Movement can be an immediate warning sign regardless of score.
    if movement == "Abrupt movement":
        risk = "CRITICAL"
        advice = (
            "Potential immediate danger. Keep people away from the slope, "
            "follow local emergency instructions, and contact authorities."
        )
    elif score >= 65:
        risk = "HIGH"
        advice = (
            "Restrict access to the slope, inspect for warning signs, "
            "and notify the responsible monitoring team."
        )
    elif score >= 40:
        risk = "MODERATE"
        advice = (
            "Increase observation frequency and check rainfall, cracks, "
            "drainage, and changes in ground movement."
        )
    else:
        risk = "LOW"
        advice = (
            "Continue routine monitoring. A low score does not guarantee "
            "slope stability."
        )

    return score, risk, advice


class LandslideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Landslide Risk Assessment System")
        self.root.geometry("1100x760")
        self.root.minsize(850, 650)
        self.root.configure(bg="#eef2f7")

        self.last_assessment = None
        self.setup_style()
        self.build_ui()
        self.load_history()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold")
        )
        style.configure(
            "TCombobox",
            padding=5
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg="#183153", padx=20, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="LANDSLIDE MONITORING SYSTEM",
            font=("Segoe UI", 19, "bold"),
            fg="white",
            bg="#183153"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Rainfall • Slope • Soil Moisture • Ground Movement",
            font=("Segoe UI", 10),
            fg="#d8e6f5",
            bg="#183153"
        ).pack(anchor="w", pady=(5, 0))

        container = tk.Frame(self.root, bg="#eef2f7", padx=18, pady=14)
        container.pack(fill="both", expand=True)

        form = ttk.LabelFrame(
            container, text="Assessment Inputs", padding=12
        )
        form.pack(fill="x")

        self.location = tk.StringVar(value="Monitoring Site 01")
        self.rainfall = tk.StringVar(value="50")
        self.slope = tk.StringVar(value="30")
        self.moisture = tk.StringVar(value="60")
        self.movement = tk.StringVar(value="None observed")
        self.earthquake = tk.StringVar(value="No known recent earthquake")

        fields = [
            ("Location / Site ID", self.location, 0, 0),
            ("Rainfall in last 24 hours (mm)", self.rainfall, 0, 2),
            ("Slope angle (degrees)", self.slope, 1, 0),
            ("Soil moisture (%)", self.moisture, 1, 2)
        ]

        for label, variable, row, col in fields:
            ttk.Label(form, text=label).grid(
                row=row, column=col, sticky="w", padx=5, pady=7
            )
            ttk.Entry(
                form, textvariable=variable, width=27
            ).grid(
                row=row, column=col + 1, sticky="ew", padx=5, pady=7
            )

        ttk.Label(form, text="Ground movement").grid(
            row=2, column=0, sticky="w", padx=5, pady=7
        )
        ttk.Combobox(
            form, textvariable=self.movement,
            values=["None observed", "Slow movement", "Abrupt movement"],
            state="readonly", width=24
        ).grid(row=2, column=1, sticky="ew", padx=5, pady=7)

        ttk.Label(form, text="Earthquake observation").grid(
            row=2, column=2, sticky="w", padx=5, pady=7
        )
        ttk.Combobox(
            form, textvariable=self.earthquake,
            values=["No known recent earthquake", "Recent earthquake"],
            state="readonly", width=24
        ).grid(row=2, column=3, sticky="ew", padx=5, pady=7)

        for col in range(4):
            form.columnconfigure(col, weight=1)

        actions = tk.Frame(container, bg="#eef2f7")
        actions.pack(fill="x", pady=10)

        tk.Button(
            actions, text="ASSESS RISK",
            command=self.run_assessment,
            bg="#176b50", fg="white",
            activebackground="#12543e",
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=16, pady=9
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            actions, text="Export CSV",
            command=self.export_csv
        ).pack(side="left", padx=5)

        ttk.Button(
            actions, text="Refresh History",
            command=self.load_history
        ).pack(side="left", padx=5)

        ttk.Button(
            actions, text="Clear Inputs",
            command=self.clear_inputs
        ).pack(side="left", padx=5)

        result = ttk.LabelFrame(
            container, text="Assessment Result", padding=12
        )
        result.pack(fill="x", pady=(0, 10))

        self.risk_label = tk.Label(
            result, text="NO ASSESSMENT YET",
            font=("Segoe UI", 16, "bold"),
            bg="#e0e7ef", fg="#183153",
            padx=12, pady=10
        )
        self.risk_label.pack(fill="x")

        self.score_label = tk.Label(
            result, text="Screening score: -- / 100",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff", fg="#183153",
            pady=8
        )
        self.score_label.pack(fill="x")

        self.advice_label = tk.Label(
            result,
            text="Enter site observations and select Assess Risk.",
            font=("Segoe UI", 10),
            bg="#ffffff", fg="#263648",
            wraplength=950, justify="left",
            padx=10, pady=10
        )
        self.advice_label.pack(fill="x")

        history_frame = ttk.LabelFrame(
            container, text="Assessment History", padding=8
        )
        history_frame.pack(fill="both", expand=True)

        columns = (
            "time", "location", "rainfall", "slope",
            "moisture", "movement", "score", "risk"
        )

        self.table = ttk.Treeview(
            history_frame, columns=columns,
            show="headings", height=7
        )

        headings = {
            "time": "Date / Time",
            "location": "Location",
            "rainfall": "Rain (mm)",
            "slope": "Slope (°)",
            "moisture": "Moisture (%)",
            "movement": "Movement",
            "score": "Score",
            "risk": "Risk"
        }

        widths = {
            "time": 145, "location": 130,
            "rainfall": 75, "slope": 65,
            "moisture": 85, "movement": 120,
            "score": 60, "risk": 85
        }

        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(
                col, width=widths[col], anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            history_frame, orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = tk.Label(
            self.root,
            text="Educational prototype — not a validated early-warning system",
            bg="#eef2f7", fg="#526273",
            font=("Segoe UI", 9)
        )
        footer.pack(pady=(0, 8))

    def run_assessment(self):
        try:
            location = self.location.get().strip()
            rainfall = float(self.rainfall.get())
            slope = float(self.slope.get())
            moisture = float(self.moisture.get())

            if not location:
                raise ValueError("Enter a location or site ID.")
            if not 0 <= rainfall <= 2000:
                raise ValueError("Rainfall must be between 0 and 2000 mm.")
            if not 0 <= slope <= 90:
                raise ValueError("Slope angle must be between 0 and 90 degrees.")
            if not 0 <= moisture <= 100:
                raise ValueError("Soil moisture must be between 0 and 100%.")

        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        movement = self.movement.get()
        earthquake = self.earthquake.get()

        score, risk, advice = assess_risk(
            rainfall, slope, moisture, movement, earthquake
        )

        colors = {
            "LOW": ("#d9f2e6", "#176b50"),
            "MODERATE": ("#fff0c2", "#805b00"),
            "HIGH": ("#ffe0cc", "#a33c00"),
            "CRITICAL": ("#ffdada", "#a00000")
        }

        background, foreground = colors[risk]
        self.risk_label.configure(
            text=f"{risk} RISK",
            bg=background, fg=foreground
        )
        self.score_label.configure(
            text=f"Screening score: {score} / 100"
        )
        self.advice_label.configure(text=advice)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = (
            timestamp, location, rainfall, slope, moisture,
            movement, earthquake, score, risk, advice
        )

        try:
            with sqlite3.connect(DB_NAME) as con:
                con.execute("""
                    INSERT INTO assessments (
                        timestamp, location, rainfall, slope,
                        moisture, movement, earthquake,
                        score, risk, recommendation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, record)
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
            return

        self.last_assessment = record
        self.load_history()

        if risk == "CRITICAL":
            messagebox.showwarning(
                "Critical warning",
                "Abrupt movement was reported. Treat this as a "
                "potential emergency and follow local safety procedures."
            )

    def load_history(self):
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            with sqlite3.connect(DB_NAME) as con:
                rows = con.execute("""
                    SELECT timestamp, location, rainfall, slope,
                           moisture, movement, score, risk
                    FROM assessments
                    ORDER BY id DESC LIMIT 200
                """).fetchall()

            for row in rows:
                self.table.insert("", "end", values=row)

        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Export assessment history",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not path:
            return

        try:
            with sqlite3.connect(DB_NAME) as con:
                rows = con.execute("""
                    SELECT id, timestamp, location, rainfall, slope,
                           moisture, movement, earthquake, score,
                           risk, recommendation
                    FROM assessments ORDER BY id DESC
                """).fetchall()

            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "ID", "Timestamp", "Location", "Rainfall (mm)",
                    "Slope (degrees)", "Soil moisture (%)",
                    "Movement", "Earthquake", "Score", "Risk",
                    "Recommendation"
                ])
                writer.writerows(rows)

            messagebox.showinfo(
                "Export complete", f"Assessment history saved to:\n{path}"
            )

        except (OSError, sqlite3.Error) as error:
            messagebox.showerror("Export failed", str(error))

    def clear_inputs(self):
        self.location.set("")
        self.rainfall.set("")
        self.slope.set("")
        self.moisture.set("")
        self.movement.set("None observed")
        self.earthquake.set("No known recent earthquake")


if __name__ == "__main__":
    initialize_database()
    root = tk.Tk()
    app = LandslideApp(root)
    root.mainloop()