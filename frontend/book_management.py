import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename

from repository.book import BookRepository
from repository.subscribers import SubscriberRepository
from repository.transaction import TransactionRepository
from config.db_connection import SessionLocal
from openpyxl import Workbook


class BookManagement:
    def __init__(self, parent, user):
        self.parent = parent
        self.db = SessionLocal()
        self.book_crud = BookRepository(self.db)
        self.subscriber_crud = SubscriberRepository(self.db)
        self.transaction_crud = TransactionRepository(self.db)
        self.user = user

        self.label = tk.Label(parent, text="Управление книгами", font=("Arial", 16))
        self.label.pack(pady=10)

        # Поисковая строка
        self.search_frame = tk.Frame(parent)
        self.search_frame.pack(pady=5)

        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_books())  # Поиск по Enter

        self.search_button = tk.Button(self.search_frame, text="Поиск", command=self.search_books)
        self.search_button.pack(side="left", padx=5)

        # Таблица с книгами
        self.tree = ttk.Treeview(parent, columns=("ID", "Название", "Автор", "Категория", "ISBN", "Цена", "Доступно"), show="headings")
        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Цена", text="Цена")
        self.tree.heading("Доступно", text="Доступно")

        self.button_frame = tk.Frame(parent)
        self.button_frame.pack(pady=10)

        if self.user.role_id == 1:
            self.add_button = tk.Button(self.button_frame, text="Добавить", command=self.add_book)
            self.add_button.pack(side="left", padx=5)

            self.edit_button = tk.Button(self.button_frame, text="Редактировать", command=self.edit_book)
            self.edit_button.pack(side="left", padx=5)

            self.delete_button = tk.Button(self.button_frame, text="Удалить", command=self.delete_book)
            self.delete_button.pack(side="left", padx=5)

        if self.user.role_id != 1:
            self.buy_button = tk.Button(self.button_frame, text="Купить", command=self.buy_book)
            self.buy_button.pack(side="left", padx=5)

        self.refresh_button = tk.Button(self.button_frame, text="Обновить список", command=self.load_books)
        self.refresh_button.pack(side="left", padx=5)

        self.export_button = tk.Button(self.button_frame, text="Экспорт в Excel", command=self.export_to_excel)
        self.export_button.pack(side="left", padx=5)

        self.subscribe_button = tk.Button(self.button_frame, text="Подписаться на рассылку", command=self.save_subscription)
        self.subscribe_button.pack(side="left", padx=5)

        self.load_books()

    def load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        books = self.book_crud.read_all()
        for book in books:
            self.tree.insert("", "end", values=(book.id, book.title, book.author, book.category, book.isbn, f"{book.price:.2f}", book.is_available))

    def search_books(self):
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showerror("Ошибка", "Введите ключевое слово для поиска!")
            return

        results = self.book_crud.search(query)
        self.tree.delete(*self.tree.get_children())  # Очистить таблицу

        if results:
            for book in results:
                self.tree.insert("", "end", values=(book.id, book.title, book.author, book.category, book.isbn, f"{book.price:.2f}", book.is_available))
        else:
            messagebox.showinfo("Результаты поиска", "Книги не найдены!")

    def add_book(self):
        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            category = category_entry.get()
            isbn = isbn_entry.get()
            price = price_entry.get()

            if not title or not author or not isbn or not price:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом!")
                return

            self.book_crud.create(title=title, author=author, category=category, isbn=isbn, price=price)
            self.load_books()
            add_window.destroy()

        add_window = tk.Toplevel(self.parent)
        add_window.title("Добавить книгу")

        tk.Label(add_window, text="Название:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Автор:").pack()
        author_entry = tk.Entry(add_window)
        author_entry.pack()

        tk.Label(add_window, text="Категория:").pack()
        category_entry = tk.Entry(add_window)
        category_entry.pack()

        tk.Label(add_window, text="ISBN:").pack()
        isbn_entry = tk.Entry(add_window)
        isbn_entry.pack()

        tk.Label(add_window, text="Цена:").pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()

        tk.Button(add_window, text="Сохранить", command=save_book).pack()

    def edit_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для редактирования!")
            return

        book_id = int(self.tree.item(selected_item[0], "values")[0])
        book = self.book_crud.read_by_id(book_id)

        def save_changes():
            title = title_entry.get()
            author = author_entry.get()
            category = category_entry.get()
            isbn = isbn_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()

            if not title or not author or not isbn or not price or not quantity:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            try:
                price = float(price)
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом, а количество - целым числом!")
                return

            try:
                self.book_crud.update(book_id=book.id,
                                      title=title,
                                      author=author,
                                      category=category,
                                      isbn=isbn,
                                      price=price,
                                      quantity=quantity,
                                      is_available=quantity > 0)
                self.db.commit()
                self.load_books()
                edit_window.destroy()
                messagebox.showinfo("Успех", "Данные книги успешно обновлены!")
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Ошибка", f"Не удалось обновить книгу: {e}")

        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Редактировать книгу")

        tk.Label(edit_window, text="Название:").pack()
        title_entry = tk.Entry(edit_window)
        title_entry.insert(0, book.title)
        title_entry.pack()

        tk.Label(edit_window, text="Автор:").pack()
        author_entry = tk.Entry(edit_window)
        author_entry.insert(0, book.author)
        author_entry.pack()

        tk.Label(edit_window, text="Категория:").pack()
        category_entry = tk.Entry(edit_window)
        category_entry.insert(0, book.category)
        category_entry.pack()

        tk.Label(edit_window, text="ISBN:").pack()
        isbn_entry = tk.Entry(edit_window)
        isbn_entry.insert(0, book.isbn)
        isbn_entry.pack()

        tk.Label(edit_window, text="Цена:").pack()
        price_entry = tk.Entry(edit_window)
        price_entry.insert(0, f"{book.price:.2f}")
        price_entry.pack()

        tk.Label(edit_window, text="Количество:").pack()
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.insert(0, str(book.quantity))
        quantity_entry.pack()

        tk.Button(edit_window, text="Сохранить изменения", command=save_changes).pack()

    def delete_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для удаления!")
            return

        book_id = self.tree.item(selected_item[0], "values")[0]
        try:
            self.book_crud.delete(int(book_id))
            self.db.commit()
            self.load_books()
            messagebox.showinfo("Успех", "Книга успешно удалена!")
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить книгу: {e}")

    def buy_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите книгу для покупки!")
            return

        book_id = int(self.tree.item(selected_item[0], "values")[0])
        selected_book = self.book_crud.read_by_id(book_id)

        if selected_book and selected_book.is_available:
            try:
                self.transaction_crud.create(user_id=self.user.id, book_id=book_id, price=selected_book.price)

                selected_book.quantity -= 1
                if selected_book.quantity <= 0:
                    selected_book.is_available = False

                self.db.commit()

                self.load_books()

                messagebox.showinfo("Успех", f"Вы купили книгу '{selected_book.title}' за {selected_book.price:.2f}!")
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Ошибка", f"Не удалось завершить покупку: {e}")
        else:
            messagebox.showerror("Ошибка", "Книга недоступна для покупки!")

    def save_subscription(self):
        def subscribe():
            chat_id = chat_id_entry.get().strip()

            if not chat_id:
                messagebox.showerror("Ошибка", "Введите ваш Telegram ID!")
                return

            existing_subscription = self.subscriber_crud.get_subscription_by_user_id(self.user.id)
            if existing_subscription:
                messagebox.showinfo("Информация", "Вы уже подписаны на рассылку.")
                subscribe_window.destroy()
                return

            try:
                self.subscriber_crud.add_subscription(chat_id=chat_id, user_id=self.user.id)
                messagebox.showinfo("Успех", "Вы успешно подписались на рассылку!")
                subscribe_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось подписаться: {e}")
                subscribe_window.destroy()

        subscribe_window = tk.Toplevel(self.parent)
        subscribe_window.title("Подписка на рассылку")

        tk.Label(subscribe_window, text="Введите ваш Telegram ID:").pack(pady=5)
        chat_id_entry = tk.Entry(subscribe_window)
        chat_id_entry.pack(pady=5)

        tk.Button(subscribe_window, text="Подписаться", command=subscribe).pack(pady=10)

    def export_to_excel(self):
        books = self.book_crud.read_all()
        if not books:
            messagebox.showinfo("Информация", "Нет данных для экспорта.")
            return

        file_path = asksaveasfilename(defaultextension=".xlsx",
                                      filetypes=[("Excel files", "*.xlsx")],
                                      title="Сохранить файл как")
        if not file_path:
            return

        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Books"

            headers = ["ID", "Название", "Автор", "Категория", "ISBN", "Цена", "Доступно"]
            sheet.append(headers)

            for book in books:
                sheet.append([book.id, book.title, book.author, book.category, book.isbn, f"{book.price:.2f}", "Да" if book.is_available else "Нет"])

            workbook.save(file_path)
            messagebox.showinfo("Успех", f"Данные успешно экспортированы в файл: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные: {e}")
