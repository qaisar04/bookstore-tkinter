from tkinter import Tk
from frontend.auth_menu import AuthMenu
from config.db_connection import engine, Base
import models
import threading
from bot.main import run_bot


def initialize_database():
    print("Инициализация базы данных...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


def main():
    # initialize_database()
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    root = Tk()
    app = AuthMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
