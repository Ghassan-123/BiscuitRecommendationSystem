import tkinter as tk
from tkinter import messagebox
from RecommendationEngine import RecommendationEngine
from MyFacts import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quality Control Recommendation System")
        self.geometry("800x600")
        self.configure(bg="#2E2E2E")

        self.engine = RecommendationEngine()
        self.questions = [
            {"id": "total", "text": "What is the batch size?", "type": "int"},
            {
                "id": "deffected",
                "text": "how many biscuits are deffected?",
                "type": "int",
            },
            {"id": "cracked", "text": "how many biscuits are cracked?", "type": "int"},
            {"id": "burned", "text": "how many biscuits are burned?", "type": "int"},
            {
                "id": "under_cooked",
                "text": "how many biscuits are under_cooked?",
                "type": "int",
            },
            {
                "id": "over_sized",
                "text": "how many biscuits are over_sized?",
                "type": "int",
            },
            {
                "id": "under_sized",
                "text": "how many biscuits are under_sized?",
                "type": "int",
            },
            {
                "id": "contaminated",
                "text": "how many biscuits are contaminated?",
                "type": "int",
            },
            {
                "id": "severly_cracked_count",
                "text": "How many severly cracked biscuits (>50%)?",
                "type": "int",
            },
            {
                "id": "moderate_cracked_count",
                "text": "How many moderate cracked biscuits (20%~50%)?",
                "type": "int",
            },
            {
                "id": "low_cracked_count",
                "text": "How many low cracked biscuits (<20%)?",
                "type": "int",
            },
            {
                "id": "severly_burned_count",
                "text": "How many severly burned biscuits (>40%)?",
                "type": "int",
            },
            {
                "id": "moderate_burned_count",
                "text": "How many moderate burned biscuits(10%~40%)?",
                "type": "int",
            },
            {
                "id": "low_burned_count",
                "text": "How many low burned biscuits(<10%)?",
                "type": "int",
            },
            {
                "id": "severly_under_cooked_count",
                "text": "How many severly under_cooked biscuits (>40%)?",
                "type": "int",
            },
            {
                "id": "moderate_under_cooked_count",
                "text": "How many moderate under_cooked biscuits(10%~40%)?",
                "type": "int",
            },
            {
                "id": "low_under_cooked_count",
                "text": "How many low under_cooked biscuits(<10%)?",
                "type": "int",
            },
            {
                "id": "severely_over_sized_count",
                "text": "How many biscuits have raduis greater than 4cm",
                "type": "int",
            },
            {
                "id": "moderate_over_sized_count",
                "text": "How many biscuits have raduis between 3.5cm and 4cm?",
                "type": "int",
            },
            {
                "id": "moderate_under_sized_count",
                "text": "How many biscuits have raduis between 2.5cm and 3cm?",
                "type": "int",
            },
            {
                "id": "severly_under_sized_count",
                "text": "How many biscuits have raduis lower than 2.5cm?",
                "type": "int",
            },
        ]
        self.answer_entries = {}
        self.answers = {}

        # Main frame
        main_frame = tk.Frame(self, bg="#2E2E2E")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for questions and input
        # Container with canvas and scrollbar
        scroll_container = tk.Frame(main_frame, bg="#2E2E2E")
        scroll_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas that will scroll
        canvas = tk.Canvas(scroll_container, bg="#2E2E2E", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar linked to canvas
        scrollbar = tk.Scrollbar(
            scroll_container, orient="vertical", command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg="#2E2E2E")
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for q in self.questions:
            label = tk.Label(
                scrollable_frame,
                text=q["text"],
                wraplength=480,
                font=("Segoe UI", 12),
                bg="#2E2E2E",
                fg="#FFFFFF",
            )
            label.pack(pady=(10, 2), anchor="w")

            entry = tk.Entry(
                scrollable_frame,
                font=("Segoe UI", 12),
                bg="#3C3C3C",
                fg="#FFFFFF",
                insertbackground="#FFFFFF",
                borderwidth=0,
            )
            entry.pack(pady=(0, 10), fill=tk.X)

            self.answer_entries[q["id"]] = entry

        self.submit_button = tk.Button(
            scrollable_frame,
            text="Submit All",
            command=self.submit_all_answers,
            font=("Segoe UI", 12, "bold"),
            bg="#4A90E2",
            fg="#FFFFFF",
            borderwidth=0,
            relief="flat",
            activebackground="#357ABD",
            activeforeground="#FFFFFF",
        )
        self.submit_button.pack(pady=20)

        # Right frame for graph and recommendations
        right_frame = tk.Frame(main_frame, bg="#2E2E2E")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Graph
        self.fig = Figure(figsize=(6, 5), dpi=100, facecolor="#2E2E2E")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#3C3C3C")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Recommendations with Scrollbar ---
        recommendation_frame = tk.Frame(right_frame, bg="#2E2E2E")
        recommendation_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create the Text widget
        self.recommendation_text = tk.Text(
            recommendation_frame,
            wrap="word",
            height=10,
            width=80,
            font=("Segoe UI", 12),
            bg="#3C3C3C",
            fg="#FFFFFF",
            borderwidth=0,
        )

        # Add vertical scrollbar
        scrollbar = tk.Scrollbar(
            recommendation_frame,
            orient="vertical",
            command=self.recommendation_text.yview,
        )
        self.recommendation_text.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        self.recommendation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert placeholder text
        self.recommendation_text.insert(tk.END, "Recommendations will appear here.")
        self.recommendation_text.config(state="disabled")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind only when mouse is over the canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        self.update_graph()

    def submit_all_answers(self):
        self.answers.clear()

        for q in self.questions:
            qid = q["id"]
            qtype = q["type"]
            value = self.answer_entries[qid].get()

            if not self.validate_answer(value, qtype):
                messagebox.showerror(
                    "Invalid Input", f"Please provide a valid input for: {q['text']}"
                )
                return

            self.answers[qid] = value

        self.run_engine_and_show_recommendations()
        self.submit_button.config(state="disabled")  # Disable after submission
        self.update_graph()

    def validate_answer(self, answer, answer_type):
        if answer_type == "int":
            return answer.isdigit()
        return True

    def run_engine_and_show_recommendations(self):
        self.engine.reset()
        for fact_id, fact_value in self.answers.items():
            self.engine.declare(Answer(id=fact_id, text=fact_value))
        self.engine.run()

        predictions = []
        recommendations = set()  # Use set to avoid duplicates
        final_recommendation = ""

        for fact in self.engine.facts.values():
            if isinstance(fact, Prediction):
                predictions.append(fact)
            elif fact.get("recommendation"):
                recommendations.add(fact["recommendation"])

        # Sort predictions by CF descending for prioritization
        predictions.sort(key=lambda p: p["cf"], reverse=True)

        # Format and print the output
        final_recommendation += "### Biscuit Production Line Recommendations\n\n"

        total = next(
            (
                f["text"]
                for f in self.engine.facts.values()
                if isinstance(f, Answer) and f["id"] == "total"
            ),
            0,
        )
        defected = next(
            (
                f["text"]
                for f in self.engine.facts.values()
                if isinstance(f, Answer) and f["id"] == "deffected"
            ),
            0,
        )
        overall_rate = (int(defected) / int(total) * 100) if int(total) > 0 else 0

        final_recommendation += f"Based on the provided batch data (total: {total} biscuits, defective: {defected}), the system identified the following issues and corresponding actions. Recommendations are prioritized by severity (e.g., contamination is critical). Only triggered defects are listed.\n\n"

        if predictions:
            for idx, pred in enumerate(predictions, 1):
                text_parts = pred["text"].split(" - ")
                if len(text_parts) >= 2:
                    defect_type = text_parts[0]
                    remaining = " - ".join(text_parts[1:])
                    level_parts = remaining.split(" (")
                    if len(level_parts) >= 2:
                        level = level_parts[0]
                        percentage_str = "(" + " (".join(level_parts[1:]).rstrip(")")
                    else:
                        level = remaining
                        percentage_str = ""
                else:
                    defect_type = pred["text"]
                    level = ""
                    percentage_str = ""

                cf = pred["cf"]

                header = f"#### {idx}. **{defect_type.strip()}"
                if level:
                    header += f" ({level.capitalize()}"
                    if percentage_str:
                        header += f" - {percentage_str}"
                    header += ")**"
                else:
                    header += "**"

                final_recommendation += header + "\n"
                final_recommendation +=  f"   - **Certainty Factor (CF)**: {cf:.3f} (adjusted for severity and proportion)\n"

                final_recommendation += "   - **Actions**:\n"
                # Find matching recommendation
                matching_rec = next(
                    (
                        rec
                        for rec in recommendations
                        if any(
                            key in rec.lower() for key in defect_type.lower().split()
                        )
                    ),
                    "No specific actions defined.",
                )
                for line in matching_rec.split("\n"):
                    final_recommendation += f"     {line}\n"
                final_recommendation += "\n"

                # Remove used recommendation to avoid duplication
                recommendations.discard(matching_rec)

        # Any remaining recommendations (e.g., overall)
        if recommendations:
            final_recommendation += "#### Additional Recommendations\n"
            for rec in recommendations:
                for line in rec.split("\n"):
                    final_recommendation += f"   {line}\n"

        final_recommendation += "### Summary\n"
        final_recommendation += f"- **Overall Defect Rate**: {overall_rate:.1f}% ({'critical' if overall_rate > 33 else 'moderate' if overall_rate > 10 else 'low'}).\n"

        if not recommendations:
            self.recommendation_text.config(state="normal")
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, "No recommendations.")
            self.recommendation_text.config(state="disabled")
        else:
            self.recommendation_text.config(state="normal")
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, f"{final_recommendation}\n\n")
            self.recommendation_text.config(state="disabled")

        self.submit_button.pack_forget()

    def update_graph(self):
        self.fig.clear()

        gs = self.fig.add_gridspec(2, 2)

        # Donut chart
        ax_donut = self.fig.add_subplot(gs[0, 0])
        self.plot_donut(ax_donut)

        # Bar chart
        ax_bar = self.fig.add_subplot(gs[0, 1])
        self.plot_bar(ax_bar)

        # Sub-plots for defect severity
        ax_cracked = self.fig.add_subplot(gs[1, 0])
        self.plot_severity("cracked", ax_cracked)
        ax_burned = self.fig.add_subplot(gs[1, 1])
        self.plot_severity("burned", ax_burned)

        self.fig.tight_layout()
        self.canvas.draw()

    def plot_donut(self, ax):
        ax.set_title("Defect Proportions", color="white")
        ax.set_facecolor("#2E2E2E")

        defect_counts = {
            "cracked": 0,
            "burned": 0,
            "under_cooked": 0,
            "over_sized": 0,
            "under_sized": 0,
            "contaminated": 0,
        }
        for key, value in self.answers.items():
            if key in defect_counts:
                defect_counts[key] = int(value)

        labels = defect_counts.keys()
        sizes = list(defect_counts.values())

        if sum(sizes) > 0:
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=[
                    "#FF6384", "#36A2EB", "#FFCE56",
                    "#4BC0C0", "#9966FF", "#FF9F40",
                ],
                textprops={"color": "w"},
            )
            centre_circle = plt.Circle((0, 0), 0.70, fc="#2E2E2E")
            ax.add_artist(centre_circle)
            ax.axis("equal")  # 💡 Ensures the donut is circular and fills space


    def plot_bar(self, ax):
        defect_counts = {
            "cracked": 0,
            "burned": 0,
            "under_cooked": 0,
            "over_sized": 0,
            "under_sized": 0,
            "contaminated": 0,
        }
        for key, value in self.answers.items():
            if key in defect_counts:
                defect_counts[key] = int(value)

        ax.bar(
            list(defect_counts.keys()), list(defect_counts.values()), color="#4A90E2"
        )
        ax.set_ylabel("Count", color="white")
        ax.set_title("Defective Biscuits", color="white")
        ax.tick_params(axis="x", colors="white", rotation=45)
        ax.tick_params(axis="y", colors="white")
        ax.set_facecolor("#3C3C3C")

    def plot_severity(self, defect_type, ax):
        severities = {
            "severly": 0,
            "moderate": 0,
            "low": 0,
        }
        for key, value in self.answers.items():
            if defect_type in key:
                if "severly" in key:
                    severities["severly"] = int(value)
                elif "moderate" in key:
                    severities["moderate"] = int(value)
                elif "low" in key:
                    severities["low"] = int(value)

        ax.bar(
            severities.keys(),
            severities.values(),
            color=["#FF6384", "#FFCE56", "#36A2EB"],
        )
        ax.set_title(f"{defect_type.capitalize()} Severity", color="white")
        ax.set_ylabel("Count", color="white")
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.set_facecolor("#3C3C3C")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
