from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from utils.FSM import Menu
from utils.database.requests_old import get_user_info, del_user, add_to_banlist
from utils.kb.inline_kb import confirm_fire
from utils.fucntions import menu_text

router = Router()


# подтверждение увольнения
@router.callback_query(F.data == "fire")
async def confirm_fire_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_text(text="<b>Подтвердите увольнение сотрудника</b>",
                                chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                reply_markup=confirm_fire)
    await call.answer()


# увольнение
@router.callback_query(F.data.startswith('f_'))
async def fire_user(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    # удаление пользователя
    if "yes" in call.data:
        user = await get_user_info(int(data['choose_user_id']))

        # отправка сообщения уволенному
        await bot.send_message(text="<b>ВЫ БЫЛИ УВОЛЕНЫ!</b>",
                               chat_id=user.chat_id)
        # добавление в банлист
        await add_to_banlist(user.tg_id)

        # удаление из бд
        await del_user(data['choose_user_id'])
        await call.message.edit_text(text="<b>Сотрудник уволен!</b>")
        sleep(0.5)
        await menu_text(data["category"], chat_id=call.from_user.id, message_id=data['msg_id'], bot=bot, state=state)

    # отмена удаления и вывод меню
    else:
        await menu_text(data["category"], chat_id=call.from_user.id, message_id=data['msg_id'], bot=bot, state=state)

