from os import unlink

from utils import config, logger
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart
from search_engine.engine import ResultFetcher
from pathlib import Path

dp = Dispatcher()

class SearchDialog(StatesGroup):
    topic = State()

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Начать поиск", callback_data="start_search"))
    text = (
        "Привет! 👋 Это стартовое сообщение.\n"
        "Ты находишься в боте, который умеет искать на Википедии 📚 и Fandom 🎮 (для игр) "
        "любую статью, которую ты напишешь! Даже на русском 🇷🇺\n"
        "Поиск всегда осуществляется на английском для более точного нахождения и быстрого обновления 🔎\n"
        "Вот что я умею:\n"
        "/start — показывает это сообщение\n"
        "/search — запускает поиск"
    )
    await message.answer(text, reply_markup=kb.as_markup())

@dp.callback_query(F.data == "start_search")
async def start_search(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Окей, введи тему для поиска:")
    await state.set_state(SearchDialog.topic)
    await callback.answer()

@dp.message(F.text == "/search")
async def search(message: types.Message, state: FSMContext):
    await message.answer("Окей, введи тему для поиска:")
    await state.set_state(SearchDialog.topic)

@dp.message(SearchDialog.topic)
async def process_topic(message: types.Message, state: FSMContext):
    await message.answer("Подождите несколько минут, работаю...")
    topic = message.text
    fetcher = ResultFetcher(topic)
    fetcher.set_theme(topic)
    answer = None
    try:
        answer = fetcher.get()
    except Exception as e:
        await message.answer(f"Произошла непредвиденная ошибка ({e}) попробуйте снова.")
        await state.clear()
        return
    logger.log("DEBUG", f"Answer: {answer}")

    if isinstance(answer, list) and all(isinstance(p, Path) for p in answer):
        logger.log("DEBUG", f"Answer: {answer}")
        for file in answer:
            if file.exists():
                await message.answer_document(FSInputFile(file))
        fetcher.cleanup()
        await state.clear()

    elif isinstance(answer, list):
        for i in range(0, len(answer[0]), 4096):
            await message.answer(answer[0][i:i + 4096])
        with open(f"search_result_{message.from_user.id}.txt", "w", encoding="utf-8") as file:
            file.writelines(answer[1])

        await message.answer_document(FSInputFile(f"search_result_{message.from_user.id}.txt"))
        unlink(f"search_result_{message.from_user.id}.txt")
        await state.clear()
        return

    elif isinstance(answer, list) and all(isinstance(p, Path) for p in answer):
        for file in answer:
            if file.exists():
                await message.answer_document(FSInputFile(file))
        fetcher.cleanup()
        await state.clear()

    else:
        await message.answer("Что-то пошло не так 🤔")
        await state.clear()

@dp.update()
async def all_updates(update: types.Update):
    logger.log("DEBUG", update)


async def main():
    bot = Bot(config.TELEGRAM_API)
    await dp.start_polling(bot)

