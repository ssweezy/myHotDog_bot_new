from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.database.requests_old import get_adm_empls, get_by_user_category, get_all_users
from utils.FSM import SendMsgToAll, Menu
from utils.fucntions import menu_text
from utils.kb.inline_kb import back_kb, acceptation_msg_all, all_emp_kb, mail_menu_kb

router = Router()


# запрос сообщения для отправления рассылки
@router.callback_query(F.data.startswith("mail"))
async def asking_msg_for_all(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # фильтровка кто отправляет сообщение
    if data["category"] == "boss":
        await call.message.edit_text("<b>Выберите, для кого сделать рассылку?</b>", reply_markup=mail_menu_kb)
    else:
        await call.message.edit_text("<b>Напишите сообщение для рассылки:</b>", reply_markup=back_kb)
        await state.set_state(SendMsgToAll.confirm_msg)
    await call.answer()


# определение для какой категории отправляется рассылка BOSS
@router.callback_query(F.data.startswith('to'))
async def category_to_send(call: CallbackQuery, state: FSMContext):
    # определение категории
    if call.data == 'to_all':
        await state.update_data(mail_category="all")
    elif call.data == 'to_adm':
        await state.update_data(mail_category="adm")
    else:
        await state.update_data(mail_category="emp")

    transcription = {"to_all": "всех", "to_adm": "управляющих", "to_emp": "сотрудников"}
    await call.message.edit_text(f"Вы выбрали для <b>{transcription[call.data]}</b>"
                                 "\n\n<b>Напишите сообщение для рассылки:</b>", reply_markup=back_kb)
    await state.set_state(SendMsgToAll.confirm_msg)


# подтверждение отправки сообщения рассылки
@router.message(SendMsgToAll.confirm_msg)
async def confirm_sending(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.update_data(msg_to_all=message.text)  # сохранение сообщения в data
    await bot.edit_message_text(text=f"<b>Ваше сообщение для рассылки:</b>"
                                     f"\n<blockquote>{message.text}</blockquote>",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"],
                                reply_markup=acceptation_msg_all)
    await message.delete()


# обработка callback "yes_a", отправка рассылки
@router.callback_query(F.data.startswith("yes"))
async def sending_msg_all(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    # указывает кем было отправлено сообщение
    if data["category"] == "adm":
        sender = "управляющего"
        # отправление сообщений для сотрудников управляющего
        for emp in (await get_adm_empls(data['role'])):
            await bot.edit_message_text(text=f"Сообщение от {sender}:"
                                             f"\n<blockquote>{data["msg_to_all"]}</blockquote>",
                                        chat_id=emp.chat_id,
                                        message_id=emp.msg_id,
                                        reply_markup=back_kb)
    # обработка запроса от boss
    elif data["category"] == "boss":
        sender = data['name']

        # условие для правильной рассылки
        # emp, adm
        if data["mail_category"] != 'all':
            # алгоритм отправки для нужной категории пользователей
            for user in (await get_by_user_category(data['mail_category'])):
                await bot.edit_message_text(text=f"Сообщение от {sender}:"
                                                 f"\n<blockquote>{data["msg_to_all"]}</blockquote>",
                                            chat_id=user.chat_id,
                                            message_id=user.msg_id,
                                            reply_markup=back_kb)
        # рассылка для всех
        else:
            for var in (await get_all_users()):
                for user in var:
                    await bot.edit_message_text(text=f"Сообщение от {sender}:"
                                                f"\n<blockquote>{data["msg_to_all"]}</blockquote>",
                                                chat_id=user.chat_id,
                                                message_id=user.msg_id,
                                                reply_markup=back_kb)

    await call.message.edit_text("<b>Рассылка завершена✔️</b>")
    sleep(2)
    await menu_text(data["category"], chat_id=call.from_user.id, message_id=data['msg_id'], bot=bot, state=state)
    await call.answer()


# реакция на callback no_a, отмена отправки рассылки
@router.callback_query(F.data == 'no_a')
async def cancel_sending_msg(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text("<b>Отмена отправки.</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки..</b>")
    sleep(0.5)
    await call.message.edit_text("<b>Отмена отправки...</b>")
    sleep(0.5)
    await menu_text(data["category"], chat_id=call.from_user.id, message_id=call.message.message_id, bot=bot, state=state)
    await state.set_state(Menu.show_emp)
    await call.answer()
