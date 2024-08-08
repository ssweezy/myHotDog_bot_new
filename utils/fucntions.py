from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.database.requests_old import get_user_info
from utils.kb.inline_kb import emp_menu_kb, adm_menu_kb, boss_menu_kb
from .config import EMP_MENU_TEXT, ADM_MENU_TEXT, BOSS_MENU_TEXT


# данный файл хранит в себе функции для общего использования


router = Router()


# функция для обновления данных в data, это сделано для того чтобы можно в любой момент обновить данные в любой функции
# берет данные из бд и заменяет текущие данные на данные из бд
async def update_data(user_id, state):
    user = await get_user_info(user_id)  # получение данных с бд
    # замена данных в state
    await state.update_data(tg_id=user.tg_id)
    await state.update_data(tg_username=user.tg_username)
    await state.update_data(role=user.role)
    await state.update_data(category=user.category)
    await state.update_data(name=user.name)
    await state.update_data(surname=user.surname)
    await state.update_data(birthday=user.birthday)
    await state.update_data(phone=user.phone)
    await state.update_data(msg_id=user.msg_id)
    await state.update_data(chat_id=user_id)


# функция для обработки нажатия на кнопку "назад"
@router.callback_query(F.data == "back")
async def func_back(call: CallbackQuery, state: FSMContext, bot: Bot):
    await update_data(call.from_user.id, state)  # обновление данных в data
    await call.answer()
    data = await state.get_data()
    # вывод нужной клавиатуры
    if data["category"] == "emp":
        await call.message.edit_text(EMP_MENU_TEXT, reply_markup=emp_menu_kb)
    elif data["category"] == "adm":
        await call.message.edit_text(ADM_MENU_TEXT, reply_markup=adm_menu_kb)

    # меню для владельца
    else:
        # удаление видео при замене видео, learning_settings line ~24, используется данная конструкция потому что видео
        # не всегда существует в чате и попытка его удаления вызовет ошибку
        try:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=data["video_id"])
        except:
            pass
        await call.message.edit_text(BOSS_MENU_TEXT, reply_markup=boss_menu_kb)
    await state.set_state(None)


# функция для вывода правильного меню
async def menu_text(category: str, chat_id, message_id, bot: Bot, state: FSMContext):
    # меню для сотрудников
    if category == "emp":
        await bot.edit_message_text(text=EMP_MENU_TEXT,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=emp_menu_kb)
    # админская панель
    elif category == "adm":
        await bot.edit_message_text(text=ADM_MENU_TEXT,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=adm_menu_kb)

    # панель для boss
    elif category == "boss":
        await bot.edit_message_text(text=BOSS_MENU_TEXT,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=boss_menu_kb)

    await state.set_state(None)


# удаляет не значащие сообщения
@router.message()
async def del_trash(message: Message):
    await message.delete()