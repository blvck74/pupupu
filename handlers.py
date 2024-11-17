from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import Command
import asyncio
import database
from buttons import add_menu_keyboard, delete_menu_keyboard, main_menu_keyboard, view_menu_keyboard, compare_menu_keyboard

# Определяем состояния для FSM
class Form(StatesGroup):
    waiting_for_save_changes = State()
    waiting_for_section = State()
    waiting_for_text = State()
    waiting_for_delete_section = State()
    waiting_for_delete_text = State()
    waiting_for_view_section = State()
    waiting_for_compare_section = State()
    waiting_for_compare_text = State()

router = Router()

# Обработчик команды "Добавить текст"
@router.message(lambda message: message.text == "Добавить текст")
async def add_text(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    sent_message = await message.answer("Выберите раздел для добавления текста:", reply_markup=add_menu_keyboard)
    await state.set_state(Form.waiting_for_section)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик выбора раздела для добавления текста
@router.message(Form.waiting_for_section)
async def process_section_add(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    if message.text in ["Раздел 1", "Раздел 2", "Раздел 3", "Раздел 4"]:
        await state.update_data(section=message.text)
        sent_message = await message.answer("Введите текст, который хотите добавить:")
        await state.set_state(Form.waiting_for_text)
    elif message.text == "Назад":
        await state.clear()
        sent_message = await message.answer("Возвращение на главный экран:", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, выберите один из доступных разделов или нажмите 'Назад'.")
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик добавления текста
@router.message(Form.waiting_for_text)
async def process_text_add(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    user_data = await state.get_data()
    section = user_data['section']
    content = message.text
    database.insert_text(section, content)
    await state.clear()
    sent_message = await message.answer("Текст успешно добавлен!", reply_markup=main_menu_keyboard)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик команды "Удалить текст"
@router.message(lambda message: message.text == "Удалить текст")
async def delete_text(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    sent_message = await message.answer("Выберите раздел для удаления текста:", reply_markup=delete_menu_keyboard)
    await state.set_state(Form.waiting_for_delete_section)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик выбора раздела для удаления текста
@router.message(Form.waiting_for_delete_section)
async def process_section_delete(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    if message.text in ["Раздел 1", "Раздел 2", "Раздел 3", "Раздел 4"]:
        await state.update_data(section=message.text)
        section = message.text
        rows = database.get_texts_by_section(section)
        if rows:
            response = "Выберите текст для удаления:\n"
            for row in rows:
                response += f"{row[0]}. {row[1]}\n"
            sent_message = await message.answer(response)
            await state.set_state(Form.waiting_for_delete_text)
        else:
            sent_message = await message.answer("В этом разделе нет текстов.", reply_markup=main_menu_keyboard)
            await state.clear()
    elif message.text == "Назад":
        await state.clear()
        sent_message = await message.answer("Возвращение на главный экран:", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, выберите один из доступных разделов или нажмите 'Назад'.")
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик удаления текста
@router.message(Form.waiting_for_delete_text)
async def process_text_delete(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    if message.text.isdigit():
        text_id = int(message.text)
        database.delete_text_by_id(text_id)
        await state.clear()
        sent_message = await message.answer("Текст успешно удален!", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, введите корректный номер текста для удаления.")
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик команды "Посмотреть текст"
@router.message(lambda message: message.text == "Посмотреть текст")
async def view_text(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    sent_message = await message.answer("Выберите раздел для просмотра текста:", reply_markup=view_menu_keyboard)
    await state.set_state(Form.waiting_for_view_section)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик выбора раздела для просмотра текста
@router.message(Form.waiting_for_view_section)
async def process_section_view(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    if message.text in ["Раздел 1", "Раздел 2", "Раздел 3", "Раздел 4"]:
        section = message.text
        rows = database.get_texts_by_section(section)
        if rows:
            response = f"Тексты в разделе '{section}':\n"
            for row in rows:
                response += f"- {row[1]}\n"
            sent_message = await message.answer(response, reply_markup=main_menu_keyboard)
        else:
            sent_message = await message.answer("В этом разделе нет текстов.", reply_markup=main_menu_keyboard)
        await state.clear()
    elif message.text == "Назад":
        await state.clear()
        sent_message = await message.answer("Возвращение на главный экран:", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, выберите один из доступных разделов или нажмите 'Назад'.")
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик команды "Сравнить текст"
@router.message(lambda message: message.text == "Сравнить текст")
async def compare_text(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    sent_message = await message.answer("Выберите раздел для сравнения текста:", reply_markup=compare_menu_keyboard)
    await state.set_state(Form.waiting_for_compare_section)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик выбора раздела для сравнения текста
@router.message(Form.waiting_for_compare_section)
async def process_section_compare(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    if message.text in ["Раздел 1", "Раздел 2", "Раздел 3", "Раздел 4"]:
        await state.update_data(section=message.text)
        sent_message = await message.answer("Введите текст, который хотите сравнить:")
        await state.set_state(Form.waiting_for_compare_text)
    elif message.text == "Назад":
        await state.clear()
        sent_message = await message.answer("Возвращение на главный экран:", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, выберите один из доступных разделов или нажмите 'Назад'.")
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик ввода текста для сравнения
@router.message(Form.waiting_for_compare_text)
async def process_text_compare(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    user_data = await state.get_data()
    section = user_data['section']
    new_text = message.text.splitlines()
    existing_text_rows = database.get_texts_by_section(section)
    existing_text = [row[1] for row in existing_text_rows]

    removed_lines = [line for line in existing_text if line not in new_text]
    added_lines = [line for line in new_text if line not in existing_text]

    response = "Сравнение завершено:\n"
    if removed_lines:
        response += "\nУшедшие строки:\n" + "\n".join(removed_lines)
    if added_lines:
        response += "\nНовые строки:\n" + "\n".join(added_lines)

    sent_message = await message.answer(response + "\n\nВнести изменения?", reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton("Сохранить изменения"), types.KeyboardButton("Отменить изменения")]],
        resize_keyboard=True
    ))
    await state.update_data(new_text=message.text)
    await state.set_state(Form.waiting_for_save_changes)
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass

# Обработчик для сохранения изменений после сравнения текста
@router.message(Form.waiting_for_save_changes)
async def save_changes(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    user_data = await state.get_data()
    section = user_data['section']
    new_text = user_data.get('new_text').splitlines()

    if message.text == "Сохранить изменения":
        # Удаляем ушедшие строки из базы данных
        existing_text_rows = database.get_texts_by_section(section)
        existing_text = [row[1] for row in existing_text_rows]

        removed_lines = [line for line in existing_text if line not in new_text]
        added_lines = [line for line in new_text if line not in existing_text]

        for line in removed_lines:
            database.delete_text_by_content(section, line)
        for line in added_lines:
            database.insert_text(section, line)

        sent_message = await message.answer("Изменения успешно сохранены!", reply_markup=main_menu_keyboard)
    elif message.text == "Отменить изменения":
        sent_message = await message.answer("Изменения отменены.", reply_markup=main_menu_keyboard)
    else:
        sent_message = await message.answer("Пожалуйста, выберите 'Сохранить изменения' или 'Отменить изменения'.")
        return
    await state.clear()
    await asyncio.sleep(600)
    try:
        await message.bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception:
        pass
