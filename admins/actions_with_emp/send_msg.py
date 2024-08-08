from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.FSM import SendMsgToEmp, Menu
from utils.database.requests_old import get_user_info
from utils.fucntions import menu_text
from utils.kb.inline_kb import acceptation_msg, all_emp_kb, back_kb

router = Router()


# запрос сообщения для отправления
@router.callback_query(F.data == "send_msg")
async def asking_msg(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('<b>Напишите сообщение для отправки:</b>', reply_markup=back_kb)
    await state.set_state(SendMsgToEmp.msg_to_send)
    await call.answer()


# подтверждение отправки сообщения
@router.message(SendMsgToEmp.msg_to_send)
async def confirm_send_msg(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.edit_message_text(text=f"<b>Текст сообщения:</b>\n\n<blockquote>{message.text}</blockquote>",
                                chat_id=data["chat_id"],
                                message_id=data["msg_id"],
                                reply_markup=acceptation_msg)
    await state.update_data(msg_to_send=message.text)
    await message.delete()


# реакция на callback yes_m, отправка сообщения
@router.callback_query(F.data == 'yes_m')
async def sending_msg(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user = await get_user_info(data["choose_user_id"])

    # указывает кем было отправлено сообщение
    if data["category"] == "adm":
        sender = "управляющего"
    else:
        sender = data['name']

    await bot.edit_message_text(text=f"📩 Новое личное сообщение от {sender}:"
                                f"\n<blockquote>{data["msg_to_send"]}</blockquote>",
                                chat_id=user.chat_id,
                                message_id=user.msg_id,
                                reply_markup=back_kb)
    await call.message.edit_text("<b>Сообщение успешно отправлено!</b>")
    sleep(2)
    await menu_text(data["category"], chat_id=call.from_user.id, message_id=call.message.message_id, bot=bot, state=state)
    await call.answer()


# реакция на callback no_m, отмена отправка сообщения
@router.callback_query(F.data == 'no_m')
async def cancel_sending_msg(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text("<b>Отмена отправки.</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки..</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки...</b>")
    sleep(0.5)
    await menu_text(data["category"], chat_id=call.from_user.id, message_id=call.message.message_id, bot=bot,
                    state=state)
    await state.set_state(None)
    await call.answer()



