import tempfile
from pathlib import Path

from aiogram import Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.state import Mode, get_state, set_mode
from app.reprice import reprice_process_file


def main_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="🧮 Пересчитать Новая цена")
    kb.button(text="❌ Сброс")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    set_mode(user_id, Mode.REPRICE)
    await message.answer(
        "Режим: 🧮 Пересчитать «Новая цена».\n"
        "Пришли файл .xlsx/.xls как документ — я заполню колонку «Новая цена».\n"
        "Учитываю колонку «цена_мин»: если расчёт ниже — ставлю минимальную.\n",
        reply_markup=main_menu_kb(),
    )


async def cmd_reset(message: Message) -> None:
    user_id = message.from_user.id
    set_mode(user_id, Mode.REPRICE)
    await message.answer(
        "Сбросил состояние. Пришли файл .xlsx/.xls как документ.",
        reply_markup=main_menu_kb(),
    )


async def set_mode_reprice(message: Message) -> None:
    user_id = message.from_user.id
    set_mode(user_id, Mode.REPRICE)
    await message.answer("Режим: 🧮 Пересчитать «Новая цена». Пришли файл .xlsx/.xls как документ.")


async def handle_document(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    st = get_state(user_id)
    mode: Mode = st["mode"]

    doc = message.document
    if not doc:
        return

    filename = doc.file_name or "file"
    ext = Path(filename).suffix.lower()
    if ext not in (".xlsx", ".xls"):
        await message.answer("Нужен файл .xlsx или .xls (как документ).")
        return

    if mode != Mode.REPRICE:
        set_mode(user_id, Mode.REPRICE)

    with tempfile.TemporaryDirectory(prefix="wb_bot_") as tmpdir:
        tmpdir_path = Path(tmpdir)
        in_path = tmpdir_path / filename

        file = await bot.get_file(doc.file_id)
        await bot.download_file(file.file_path, destination=in_path)

        out_path = tmpdir_path / (Path(filename).stem + "_FILLED.xlsx")
        await message.answer("Считаю и заполняю «Новая цена»…")
        try:
            filled = reprice_process_file(str(in_path), str(out_path))
        except Exception as e:
            await message.answer(f"Ошибка обработки: {e}")
            return

        await message.answer_document(
            document=FSInputFile(path=str(out_path), filename=out_path.name),
            caption=f"Готово: {out_path.name} (заполнено строк: {filled})",
        )


def register_handlers(dp) -> None:
    """Регистрирует все хендлеры в Dispatcher."""
    dp.message.register(cmd_start,        CommandStart())
    dp.message.register(cmd_reset,        Command("reset"))
    dp.message.register(cmd_reset,        F.text == "❌ Сброс")
    dp.message.register(set_mode_reprice, F.text == "🧮 Пересчитать Новая цена")
    dp.message.register(handle_document,  F.document)
