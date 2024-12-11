import tkinter as tk
from tkinter import ttk, messagebox
from config.db_connection import SessionLocal
from repository.feedback import FeedbackRepository


class FeedbackManagement:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.db = SessionLocal()
        self.feedback_crud = FeedbackRepository(self.db)

        self.label = tk.Label(parent, text="Управление обратной связью", font=("Arial", 16))
        self.label.pack(pady=10)

        if self.user.role_id != 1:
            self.add_feedback_form()
        else:
            self.show_feedback_table()

    def add_feedback_form(self):
        tk.Label(self.parent, text="Ваш отзыв:").pack(pady=5)
        self.feedback_entry = tk.Text(self.parent, height=10, width=50)
        self.feedback_entry.pack(pady=5)

        tk.Button(self.parent, text="Отправить отзыв", command=self.submit_feedback).pack(pady=5)

    def submit_feedback(self):
        feedback_text = self.feedback_entry.get("1.0", tk.END).strip()
        if not feedback_text:
            messagebox.showerror("Ошибка", "Введите текст отзыва!")
            return

        try:
            self.feedback_crud.create(user_id=self.user.id, feedback=feedback_text)
            messagebox.showinfo("Успех", "Ваш отзыв отправлен!")
            self.feedback_entry.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отправить отзыв: {e}")

    def show_feedback_table(self):
        self.tree = ttk.Treeview(self.parent, columns=("ID", "Пользователь", "Отзыв", "Дата"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Пользователь", text="Пользователь")
        self.tree.heading("Отзыв", text="Отзыв")
        self.tree.heading("Дата", text="Дата")

        self.refresh_button = tk.Button(self.parent, text="Обновить список", command=self.load_feedbacks)
        self.refresh_button.pack(pady=5)

        self.load_feedbacks()

    def load_feedbacks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        feedbacks = self.feedback_crud.read_all()
        for feedback in feedbacks:
            self.tree.insert(
                "",
                "end",
                values=(
                    feedback.id,
                    feedback.user.name,
                    feedback.feedback_text,
                    feedback.date.strftime("%Y-%m-%d %H:%M"),
                ),
            )
