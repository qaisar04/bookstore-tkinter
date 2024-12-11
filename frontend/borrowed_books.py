import tkinter as tk
from tkinter import ttk, messagebox
from repository.borrowed_book import BorrowedBookRepository
from config.db_connection import SessionLocal


class BorrowedBooksManagement:
    def __init__(self, parent):
        self.parent = parent
        self.db = SessionLocal()
        self.borrowed_book_crud = BorrowedBookRepository(self.db)

        self.label = tk.Label(parent, text="Управление выданными книгами", font=("Arial", 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(parent, columns=("ID", "Книга ID", "Пользователь ID", "Дата выдачи", "Дата возврата"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Книга ID", text="Книга ID")
        self.tree.heading("Пользователь ID", text="Пользователь ID")
        self.tree.heading("Дата выдачи", text="Дата выдачи")
        self.tree.heading("Дата возврата", text="Дата возврата")

        self.button_frame = tk.Frame(parent)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Добавить", command=self.add_borrowed_book)
        self.add_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Удалить", command=self.delete_borrowed_book)
        self.delete_button.pack(side="left", padx=5)

        self.load_borrowed_books()


    def load_borrowed_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        borrowed_books = self.borrowed_book_crud.read_all()
        for record in borrowed_books:
            self.tree.insert("", "end", values=(record.id, record.book_id, record.user_id, record.borrowed_date, record.return_date))

    def add_borrowed_book(self):
        def save_borrowed_book():
            book_id = book_id_entry.get()
            user_id = user_id_entry.get()
            borrowed_date = borrowed_date_entry.get()
            return_date = return_date_entry.get()

            if book_id and user_id:
                self.borrowed_book_crud.create(book_id=int(book_id), user_id=int(user_id), borrowed_date=borrowed_date, return_date=return_date)
                self.load_borrowed_books()
                add_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить запись о выдаче книги")

        tk.Label(add_window, text="Книга ID:").pack()
        book_id_entry = tk.Entry(add_window)
        book_id_entry.pack()

        tk.Label(add_window, text="Пользователь ID:").pack()
        user_id_entry = tk.Entry(add_window)
        user_id_entry.pack()

        tk.Label(add_window, text="Дата выдачи:").pack()
        borrowed_date_entry = tk.Entry(add_window)
        borrowed_date_entry.pack()

        tk.Label(add_window, text="Дата возврата:").pack()
        return_date_entry = tk.Entry(add_window)
        return_date_entry.pack()

        tk.Button(add_window, text="Сохранить", command=save_borrowed_book).pack()

    def delete_borrowed_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return

        record_id = self.tree.item(selected_item[0], "values")[0]
        self.borrowed_book_crud.delete(int(record_id))
        self.load_borrowed_books()
