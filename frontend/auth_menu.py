import tkinter as tk
from tkinter import messagebox
from repository.user import UserRepository
from config.db_connection import SessionLocal


class AuthMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация")
        self.root.geometry("400x300")
        self.db = SessionLocal()
        self.user_crud = UserRepository(self.db)

        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()

        tk.Label(self.root, text="Вход", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Войти", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Регистрация", command=self.create_register_frame).pack(pady=5)

    def create_register_frame(self):
        self.clear_frame()

        tk.Label(self.root, text="Регистрация", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Имя:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Зарегистрироваться", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.create_login_frame).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        user = self.user_crud.read_all()
        user = next((u for u in user if u.email == email and u.password == password), None)
        if user:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user.name}!")
            self.root.withdraw()
            self.open_main_window(user)
        else:
            messagebox.showerror("Ошибка", "Неверные email или пароль.")

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        existing_user = next((u for u in self.user_crud.read_all() if u.email == email), None)
        if existing_user:
            messagebox.showerror("Ошибка", "Пользователь с таким email уже существует.")
            return

        self.user_crud.create(name=name, email=email, password=password)
        messagebox.showinfo("Успех", "Вы успешно зарегистрировались!")
        self.create_login_frame()

    def open_main_window(self, user):
        from frontend.main_window import MainWindow

        root = tk.Tk()
        app = MainWindow(root, user)
        root.mainloop()
