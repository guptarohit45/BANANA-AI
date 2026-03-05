import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Quiz Data ---------------- #
quiz_data = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Newton", "Einstein", "Tesla", "Edison"],
        "answer": "Einstein"
    },
    {
        "question": "Which is the largest ocean on Earth?",
        "options": ["Atlantic", "Pacific", "Indian", "Arctic"],
        "answer": "Pacific"
    },
    {
        "question": "What is the national animal of India?",
        "options": ["Lion", "Tiger", "Elephant", "Peacock"],
        "answer": "Tiger"
    }
]

# ---------------- Quiz Application ---------------- #
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Game")
        self.geometry("700x500")
        self.configure(bg="#0f172a")

        # Game variables
        self.score = 0
        self.q_index = 0
        self.selected_option = tk.StringVar()

        # Setup UI
        self.setup_styles()
        self.create_start_screen()

    # ---------- Styling ---------- #
    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure("Title.TLabel", background="#0f172a", foreground="#22d3ee", font=("Segoe UI", 24, "bold"))
        style.configure("Ques.TLabel", background="#1f2937", foreground="white", font=("Segoe UI", 16), padding=20)
        style.configure("TButton", font=("Segoe UI", 12), padding=10)
        style.map("TButton", background=[("active", "#22d3ee")])
        style.configure("Opt.TRadiobutton", background="#1f2937", foreground="white", font=("Segoe UI", 13))
        style.map("Opt.TRadiobutton", background=[("active", "#22d3ee")])

    # ---------- Start Screen ---------- #
    def create_start_screen(self):
        self.clear_screen()
        frame = ttk.Frame(self)
        frame.pack(expand=True)

        title = ttk.Label(frame, text="🎯 Quiz Game", style="Title.TLabel")
        title.pack(pady=40)

        start_btn = ttk.Button(frame, text="Start Quiz ▶", command=self.start_quiz)
        start_btn.pack(pady=20)

    # ---------- Quiz Screen ---------- #
    def start_quiz(self):
        self.score = 0
        self.q_index = 0
        self.load_question()

    def load_question(self):
        self.clear_screen()
        if self.q_index < len(quiz_data):
            q_data = quiz_data[self.q_index]

            q_frame = ttk.Frame(self)
            q_frame.pack(expand=True, fill="both", padx=20, pady=20)

            question_lbl = ttk.Label(q_frame, text=f"Q{self.q_index+1}. {q_data['question']}", style="Ques.TLabel")
            question_lbl.pack(pady=20, fill="x")

            self.selected_option.set(None)
            for option in q_data["options"]:
                ttk.Radiobutton(
                    q_frame, text=option, value=option,
                    variable=self.selected_option, style="Opt.TRadiobutton"
                ).pack(anchor="w", pady=5, padx=20)

            submit_btn = ttk.Button(q_frame, text="Submit", command=self.check_answer)
            submit_btn.pack(pady=20)
        else:
            self.show_result()

    def check_answer(self):
        chosen = self.selected_option.get()
        correct = quiz_data[self.q_index]["answer"]
        if chosen == correct:
            self.score += 1
        self.q_index += 1
        self.load_question()

    # ---------- Result Screen ---------- #
    def show_result(self):
        self.clear_screen()
        frame = ttk.Frame(self)
        frame.pack(expand=True)

        result_text = f"🏆 Quiz Finished!\n\nYour Score: {self.score}/{len(quiz_data)}"
        result_lbl = ttk.Label(frame, text=result_text, style="Title.TLabel")
        result_lbl.pack(pady=40)

        restart_btn = ttk.Button(frame, text="🔄 Restart Quiz", command=self.start_quiz)
        restart_btn.pack(pady=20)

        exit_btn = ttk.Button(frame, text="❌ Exit", command=self.destroy)
        exit_btn.pack()

    # ---------- Utility ---------- #
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

# ---------------- Run ---------------- #
if __name__== "__main__":
    app = QuizApp()
    app.mainloop()