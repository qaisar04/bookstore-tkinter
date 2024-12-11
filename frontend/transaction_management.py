import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from config.db_connection import SessionLocal
from repository.transaction import TransactionRepository


class TransactionManagement:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.db = SessionLocal()
        self.transaction_crud = TransactionRepository(self.db)

        self.button_frame = tk.Frame(parent)
        self.button_frame.pack(pady=10)

        self.label = tk.Label(parent, text="Управление транзакциями", font=("Arial", 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(parent, columns=("ID", "Пользователь", "Книга", "Дата покупки", "Цена"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.refresh_button = tk.Button(self.button_frame, text="Обновить список", command=self.load_transactions)
        self.refresh_button.pack(side="left", padx=5)

        self.export_diagram_button = tk.Button(self.button_frame, text="Скачать диаграмму", command=self.save_expenses_chart)
        self.export_diagram_button.pack(side="left", padx=5)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Пользователь", text="Пользователь")
        self.tree.heading("Книга", text="Книга")
        self.tree.heading("Дата покупки", text="Дата покупки")
        self.tree.heading("Цена", text="Цена")

        self.load_transactions()

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.user.role_id == 1:
            transactions = self.transaction_crud.read_all()
        else:
            transactions = self.transaction_crud.read_by_user(self.user.id)

        for transaction in transactions:
            self.tree.insert(
                "",
                "end",
                values=(
                    transaction.id,
                    transaction.user.name,
                    transaction.book.title,
                    transaction.purchase_date.strftime("%Y-%m-%d %H:%M"),
                    f"{transaction.price:.2f}",
                ),
            )

    def save_expenses_chart(self):
        if self.user.role_id == 1:
            transactions = self.transaction_crud.read_all()
        else:
            transactions = self.transaction_crud.read_by_user(self.user.id)

        if not transactions:
            messagebox.showinfo("Информация", "Нет данных для построения диаграммы.")
            return

        expenses_per_day = Counter(
            transaction.purchase_date.strftime("%Y-%m-%d")
            for transaction in transactions
        )

        dates = sorted(expenses_per_day.keys())
        totals = [expenses_per_day[date] for date in dates]

        if len(dates) == 1:
            plt.figure(figsize=(6, 4))
            plt.bar(dates, totals)
            plt.title("Количество покупок по дням (Одна дата)", fontsize=14)
        else:
            plt.figure(figsize=(10, 6))
            plt.bar(dates, totals)
            plt.title("Количество покупок по дням", fontsize=16)

        plt.xlabel("Дата", fontsize=12)
        plt.ylabel("Количество покупок", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        file_path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Сохранить диаграмму как"
        )

        if not file_path:
            return

        try:
            plt.savefig(file_path)
            plt.close()
            messagebox.showinfo("Успех", f"Диаграмма сохранена в файл:\n{file_path}")
        except Exception as e:
            plt.close()
            messagebox.showerror("Ошибка", f"Не удалось сохранить диаграмму: {e}")
