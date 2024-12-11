import tkinter as tk
from tkinter import ttk

from frontend.auth_menu import AuthMenu
from frontend.transaction_management import TransactionManagement
from frontend.user_management import UserManagement
from frontend.book_management import BookManagement


class MainWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Bookstore Management")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.user_tab = ttk.Frame(self.notebook)
        self.book_tab = ttk.Frame(self.notebook)

        if self.user.role_id == 1:
            self.notebook.add(self.user_tab, text="Управление пользователями")
            self.user_management = UserManagement(self.user_tab)

        self.notebook.add(self.book_tab, text="Управление книгами")
        self.book_management = BookManagement(self.book_tab, self.user)

        self.transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.transaction_tab, text="Управление транзакциями")
        self.transaction_management = TransactionManagement(self.transaction_tab, user)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.logout_button = tk.Button(self.button_frame, text="Выйти", command=self.logout)
        self.logout_button.pack(side="left", padx=5)

    def logout(self):
        self.root.destroy()
        self.open_auth_window()

    def open_auth_window(self):
        root = tk.Tk()
        app = AuthMenu(root)
        root.mainloop()
