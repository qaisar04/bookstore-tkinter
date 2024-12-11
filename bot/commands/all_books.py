from aiogram import Router, types
from aiogram.filters import Command
from config.db_connection import SessionLocal
from repository.book import BookRepository

books_router = Router()


@books_router.message(Command("all_books"))
async def all_books_command(message: types.Message):
    session = SessionLocal()
    book_repo = BookRepository(session)
    books = book_repo.read_all()

    if not books:
        await message.answer("Нет доступных книг.")
        return

    response_lines = []
    for book in books:
        line = (
            "📖 *Название:* {title}\n"
            "👤 *Автор:* {author}\n"
            "📕 *Категория:* {category}\n"
            "🔖 *ISBN:* {isbn}\n"
            "💰 *Цена:* {price} тенге\n"
            "✅ *Доступна:* {available}"
        ).format(
            title=book.title,
            author=book.author,
            category=book.category,
            isbn=book.isbn,
            price=book.price,
            available="Да" if book.is_available else "Нет"
        )
        response_lines.append(line)

    response_text = "📚 *Список доступных книг:*\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(response_lines)

    await message.answer(response_text, parse_mode="Markdown")
