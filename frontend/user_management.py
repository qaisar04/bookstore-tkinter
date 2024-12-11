import tkinter as tk
from tkinter import ttk, messagebox
from repository.user import UserRepository
from config.db_connection import SessionLocal


class UserManagement:
    def __init__(self, parent):
        self.parent = parent
        self.db = SessionLocal()
        self.user_crud = UserRepository(self.db)

        self.label = tk.Label(parent, text="Управление пользователями", font=("Arial", 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(parent, columns=("ID", "Имя", "Email", "Телефон", "Роль"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Имя", text="Имя")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Телефон", text="Телефон")
        self.tree.heading("Роль", text="Роль")

        self.button_frame = tk.Frame(parent)
        self.button_frame.pack(pady=10)

        self.refresh_button = tk.Button(self.button_frame, text="Обновить список", command=self.load_users)
        self.refresh_button.pack(side="left", padx=5)

        self.add_button = tk.Button(self.button_frame, text="Добавить", command=self.add_user)
        self.add_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Удалить", command=self.delete_user)
        self.delete_button.pack(side="left", padx=5)

        self.load_users()

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.user_crud.read_all()
        for user in users:
            self.tree.insert("", "end", values=(user.id, user.name, user.email, user.password, user.role_id))

    def add_user(self):
        def save_user():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role_id = role_id_entry.get()

            if name and email and password:
                self.user_crud.create(name=name, email=email, password=password, role_id=int(role_id))
                self.load_users()
                add_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить пользователя")

        tk.Label(add_window, text="Имя:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Email:").pack()
        email_entry = tk.Entry(add_window)
        email_entry.pack()

        tk.Label(add_window, text="Пароль:").pack()
        password_entry = tk.Entry(add_window)
        password_entry.pack()

        tk.Label(add_window, text="Роль ID:").pack()
        role_id_entry = tk.Entry(add_window)
        role_id_entry.pack()

        tk.Button(add_window, text="Сохранить", command=save_user).pack()

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите пользователя для удаления!")
            return

        user_id = self.tree.item(selected_item[0], "values")[0]
        self.user_crud.delete(int(user_id))
        self.load_users()
