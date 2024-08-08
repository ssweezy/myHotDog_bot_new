from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from utils.database.requests.roles_req import get_role_by_password, del_role, change_role_password, add_role
from utils.fucntions import menu_text
from utils.kb.inline_kb import back_kb, all_roles_and_add_kb, role_settings_menu, confirm_del_role, confirm_add_role
from utils.FSM import Roles

router = Router()


# переход в настройки ролей
@router.callback_query(F.data == "change_role")
async def show_role_settings_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="<b>Имеются следующие роли</b>"
                                      "\n\n💡Для настройки выберите интересующую роль",
                                 reply_markup=await all_roles_and_add_kb())
    await state.set_state(Roles.Choose_role)
    await call.answer()


# обработка callback с настройкой роли
@router.callback_query(Roles.Choose_role, F.data != 'back', F.data != 'add_role')
async def change_role_settings(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f"<b>О РОЛИ</b>"
                                      f"\n\n🏷Название: {await get_role_by_password(call.data)}"
                                      f"\n🔑Пароль: {call.data}",
                                 reply_markup=role_settings_menu)
    await state.update_data(chosen_role=call.data)
    await state.set_state(None)
    await call.answer()


'''================================УДАЛЕНИЕ РОЛИ============================='''


# удаление роли
@router.callback_query(F.data == "del_role")
async def confirming_del_role(call: CallbackQuery):
    await call.message.edit_text("Подтвердите удаление", reply_markup=confirm_del_role)
    await call.answer()


# реакция на удаления
@router.callback_query(F.data.startswith('r_'))
async def deleting_role(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if call.data == 'r_yes':
        await del_role(data['chosen_role'])  # удаление роли из базы данных
        await call.message.edit_text("<b>Роль удалена!</b>")
        sleep(1)
        # вывод меню
        await menu_text(data["category"],
                        chat_id=call.from_user.id,
                        message_id=call.message.message_id,
                        bot=bot,
                        state=state)
    else:
        await call.message.edit_text("<b>Отмена удаления</b>")
        sleep(1)
        # вывод меню
        await menu_text(data["category"],
                        chat_id=call.from_user.id,
                        message_id=call.message.message_id,
                        bot=bot,
                        state=state)
        await call.answer()

'''================================КОНЕЦ УДАЛЕНИЕ РОЛИ============================================================'''


'''============================ИЗМЕНЕНИЕ ПАРОЛЯ========================='''


# запрос нового пароля
@router.callback_query(F.data == "change_role_password")
async def ask_new_role_password(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='<b>Введите новый пароль</b>',
                                 reply_markup=back_kb)
    await state.set_state(Roles.Change_password)
    await call.answer()


# изменение пароля
@router.message(Roles.Change_password)
async def changing_role_password(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    # изменение пароля в бд
    await change_role_password(data['chosen_role'], message.text)

    # изменение сообщения
    await bot.edit_message_text(text='<b>Пароль успешно изменен!</b>',
                                chat_id=message.chat.id,
                                message_id=data["msg_id"])

    sleep(1)
    # вывод меню
    await menu_text(data["category"],
                    chat_id=message.chat.id,
                    message_id=data['msg_id'],
                    bot=bot,
                    state=state)
'''================================КОНЕЦ ИЗМЕНЕНИЯ ПАРОЛЯ============================================================'''


'''===================================ДОБАВЛЕНИЕ РОЛИ============================='''


# установка правильного состояние, для того чтобы код правильно работал при нажатии "нет" при подтверждении
@router.callback_query(F.data == "add_role")
async def new_role(call: CallbackQuery, state: FSMContext):
    await call.answer()
    # начало заполнения новой роли
    await call.message.edit_text(text='<b>ДАННЫЕ РОЛИ</b>'
                                      '\n\n🏷Название: ???'
                                      '\n🔑Пароль: ???'
                                      '\n\n<b>Введите название роли:</b>',
                                 reply_markup=back_kb)
    await state.set_state(Roles.New_role_name)


# запрос новой роли
@router.message(Roles.New_role)
async def ask_new_roles_name(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    # начало заполнения новой роли
    await bot.edit_message_text(text='<b>ДАННЫЕ РОЛИ</b>'
                                     '\n\n🏷Название: ???'
                                     '\n🔑Пароль: ???'
                                     '\n\n<b>Введите название роли:</b>',
                                chat_id=message.chat.id,
                                message_id=data['msg_id'],
                                reply_markup=back_kb)
    await state.set_state(Roles.New_role_name)


# сохранение названия и запрос пароля
@router.message(Roles.New_role_name)
async def ask_new_roles_password(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    # сохранение названия в data
    await state.update_data(new_role_name=message.text)

    data = await state.get_data()
    # изменение сообщения
    await bot.edit_message_text(text='<b>ДАННЫЕ РОЛИ</b>'
                                     f'\n\n🏷Название: {data["new_role_name"]}'
                                     f'\n🔑Пароль: ???'
                                     f'\n\n<b>Введите пароль:</b>',
                                chat_id=message.chat.id,
                                message_id=data["msg_id"])

    await state.set_state(Roles.New_role_password)


# сохранение пароля и запрос подтверждения
@router.message(Roles.New_role_password)
async def confirm(message: Message, bot: Bot, state: FSMContext):

    # сохранение названия в data
    await state.update_data(new_role_password=message.text)

    data = await state.get_data()
    # изменение сообщения
    await bot.edit_message_text(text='<b>ДАННЫЕ РОЛИ</b>'
                                     f'\n\n🏷Название: {data["new_role_name"]}'
                                     f'\n🔑Пароль: {data['new_role_password']}'
                                     f'\n\n<b>Все верно?</b>',
                                chat_id=message.chat.id,
                                message_id=data["msg_id"],
                                reply_markup=confirm_add_role)
    await message.delete()

    await state.set_state(Roles.New_role_confirm)


# подтверждение роли
@router.callback_query(F.data.startswith("add"))
async def adding_role_to_db(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()

    # подтверждение
    if call.data == 'add_yes':
        await add_role(data['new_role_name'], data['new_role_password'])  # добавление в бд
        await call.message.edit_text(text="<b>Роль успешно добавлена!</b>")
        sleep(1)
        await menu_text(data["category"],
                        chat_id=call.message.chat.id,
                        message_id=data['msg_id'],
                        bot=bot,
                        state=state)
    else:
        await call.message.edit_text(text='Заполняем заново.')
        sleep(0.5)
        await call.message.edit_text(text='Заполняем заново..')
        sleep(0.5)
        await call.message.edit_text(text='Заполняем заново...')
        sleep(0.5)

        # начало заполнения новой роли
        await bot.edit_message_text(text='<b>ДАННЫЕ РОЛИ</b>'
                                         '\n\n🏷Название: ???'
                                         '\n🔑Пароль: ???'
                                         '\n\n<b>Введите название роли:</b>',
                                    chat_id=call.message.chat.id,
                                    message_id=data['msg_id'],
                                    reply_markup=back_kb)
        await state.set_state(Roles.New_role_name)
        await call.answer()


'''================================КОНЕЦ ДОБАВЛЕНИЯ РОЛИ============================================================'''
