import tkinter as tk
from tkinter import ttk

from config.db_connection import SessionLocal
from repository.transaction import TransactionRepository


class TransactionManagement:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.db = SessionLocal()
        self.transaction_crud = TransactionRepository(self.db)

        self.label = tk.Label(parent, text="Управление транзакциями", font=("Arial", 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(parent, columns=("ID", "Пользователь", "Книга", "Дата покупки", "Цена"), show="headings")
        self.tree.pack(fill="both", expand=True)

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
