from time import sleep
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.database.requests_old import set_user, user_exists, get_user_info, update_msg_id, get_banlist
from utils.database.requests.roles_req import get_role_by_password
from utils.FSM import Reg
from utils.config import PASSWORD_EMP, PASSWORD_ADMIN, ADM_MENU_TEXT, EMP_MENU_TEXT, BOSS_MENU_TEXT, PASSWORD_BOSS
from utils.kb.inline_kb import acceptation_reg, emp_menu_kb, adm_menu_kb, boss_menu_kb, all_roles_kb
from utils.fucntions import update_data, menu_text




router = Router()


# приветствие и запрос пароля
@router.message(Command('start'))
async def hello(message: Message, bot: Bot, state: FSMContext):
    # проверка если есть юзер то команда старт не будет работать
    if (not (await user_exists(message.from_user.id))) and (message.from_user.id not in (await get_banlist())):
        await message.answer(f"👋 Приветствуем!")
        msg = await message.answer("🔐 Для регистрации вам необходимо ввести код-пароль.\nВведите пароль:")
        await state.update_data(msg_id=msg.message_id)  # сохранение айди сообщения для дальнейшей работы
        await message.delete()  # удаление сообщения /start
        await state.set_state(Reg.password)
    # если юзер уже зареган
    elif message.from_user.id not in (await get_banlist()):
        # переприсваивание данных в statedata для того чтобы не возникали ошибки при перезапуске
        await update_data(message.from_user.id, state)

        # отправка юзеру соответсвующее ему меню
        user_data = await get_user_info(message.from_user.id)
        data = await state.get_data()

            # меню сотрудника
        if user_data.category == 'emp':
            msg = await message.answer(EMP_MENU_TEXT, reply_markup=emp_menu_kb)
            try:
                await bot.delete_message(chat_id=data["chat_id"], message_id=data["msg_id"])
            except:
                pass
            await message.delete()
            await state.update_data(msg_id=msg.message_id)
            await update_msg_id(message.from_user.id, msg.message_id)

            # меню админа
        elif user_data.category == 'adm':
            msg = await message.answer(ADM_MENU_TEXT, reply_markup=adm_menu_kb)
            try:
                await bot.delete_message(chat_id=data["chat_id"], message_id=data["msg_id"])
            except:
                pass
            await message.delete()
            await state.update_data(msg_id=msg.message_id)
            await update_msg_id(message.from_user.id, msg.message_id)

            # меню владельца
        else:
            msg = await message.answer(BOSS_MENU_TEXT, reply_markup=boss_menu_kb)
            try:
                await bot.delete_message(chat_id=data["chat_id"], message_id=data["msg_id"])
            except:
                pass
            await message.delete()
            await state.update_data(msg_id=msg.message_id)
            await update_msg_id(message.from_user.id, msg.message_id)

        await state.set_state(None)
    else:
        await message.delete()
        await state.set_state(None)


# проверка пароля или старт если человек зареган
@router.message(Reg.password)
async def pass_check(message: Message, bot: Bot, state: FSMContext):

    # регистрация для сотрудников
    if message.text == PASSWORD_EMP:
        data = await state.get_data()  # на данном этапе тут хранится только msg_id, и данная строка сделано чтобы
        # корректно менялось/удалялось основное сообщение
        await message.delete()
        await bot.edit_message_text(text="🔓 Вы успешно вошли в систему!\nВведите <b>имя:</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(tg_username=message.from_user.username)
        await state.update_data(role="")
        await state.update_data(category="emp")
        await state.set_state(Reg.name)

    # регистрация для админов
    elif message.text == PASSWORD_ADMIN:
        data = await state.get_data()
        await message.delete()
        await bot.edit_message_text(text="🔓 Вы успешно вошли в систему как <b>УПРАВЛЯЮЩИЙ</b>!\nВведите <b>имя:</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(tg_username=message.from_user.username)
        await state.update_data(role="")
        await state.update_data(category="adm")
        await state.set_state(Reg.name)

    # регистрация для владельца
    elif message.text == PASSWORD_BOSS:
        data = await state.get_data()
        await message.delete()
        await bot.edit_message_text(text="🔓 Вы успешно вошли в систему как <b>ВЛАДЕЛЕЦ</b>!\nВведите <b>имя:</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"])
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(tg_username=message.from_user.username)
        await state.update_data(role="boss")
        await state.update_data(category="boss")
        await state.set_state(Reg.name)

    # неправильный пароль
    else:
        await message.delete()
        data = await state.get_data()
        try:
            await bot.edit_message_text(text="🔒 <b>Неверный пароль</b>\nПопробуйте еще раз:",
                                        chat_id=message.chat.id,
                                        message_id=data["msg_id"])
        except:
            pass


# фамилия
@router.message(Reg.name)
async def get_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nВведите <b>фамилию:</b>",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.surname)


# день рождения
@router.message(Reg.surname)
async def get_surname(message: Message, bot: Bot ,state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nВведите <b>дату рождения:</b>",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.birthday)


# номер телефона
@router.message(Reg.birthday)
async def get_birthday(message: Message, bot: Bot ,state: FSMContext):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    await message.delete()
    await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nДата рождения - {data["birthday"]}"
                                     f"\nВведите <b>номер телефона:</b>",
                                chat_id=message.chat.id,
                                message_id=data["msg_id"])
    await state.set_state(Reg.phoneNum)


# роль
@router.message(Reg.phoneNum)
async def get_phone(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    # если пользователь, то ему нужно вводить свою роль
    if data["category"] in ['emp', 'adm']:
        await message.delete()
        await state.update_data(phone=message.text)
        data = await state.get_data()
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\nВыберите <b>свою роль</b>",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"],
                                    reply_markup=await all_roles_kb())  # отправление кб с ролями

        await state.set_state(Reg.role)

    # если пользователь boss, то ему не нужно указывать свою роль, смотрите pass_check line ~89, поэтому переходим
    # к номеру телефона
    else:
        # если boss ввел уже свой номер телефона, то при повторном вводе он не будет меняться
        if "phone" not in data:
            await message.delete()
            await state.update_data(phone=message.text)
            data = await state.get_data()
            await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                             f"\nИмя - {data["name"]}"
                                             f"\nФамилия - {data["surname"]}"
                                             f"\nДата рождения - {data["birthday"]}"
                                             f"\nТелефон - {data["phone"]}"
                                             f"\n\n<b>Все верно?</b>",
                                        chat_id=message.chat.id,
                                        message_id=data["msg_id"],
                                        reply_markup=acceptation_reg)
            await state.set_state(Reg.acceptation)  # сразу перескакиваем на подтверждение
        else:
            await message.delete()


# роль пользователя
@router.callback_query(Reg.role)
async def get_role(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    # проверка по категории
    if data["category"] == 'emp':
        await state.update_data(role=(await get_role_by_password(call.data)))
        data = await state.get_data()
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\nРоль - {data["role"]}"
                                         f"\n\n<b>Все верно?</b>",
                                    chat_id=call.from_user.id,
                                    message_id=data["msg_id"],
                                    reply_markup=acceptation_reg)  # подтверждение
        await state.set_state(Reg.acceptation)

        # для админов нужно ввести пароль роли
    else:
        await state.update_data(role=(await get_role_by_password(call.data)))
        await state.update_data(role_password=call.data)  # пароль в data через callback
        data = await state.get_data()
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                     f"\nИмя - {data["name"]}"
                                     f"\nФамилия - {data["surname"]}"
                                     f"\nДата рождения - {data["birthday"]}"
                                     f"\nТелефон - {data["phone"]}"
                                     f"\nРоль - {data["role"]}"
                                     f"\n\nВведите пароль роли:",
                                    chat_id=call.from_user.id,
                                    message_id=data["msg_id"],
                                    reply_markup=None)  # подтверждение
        await state.set_state(Reg.role_check_pass)


@router.message(Reg.role_check_pass)
async def role_check_pass(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()

    # если пароль правильный, то идет завершение
    if str(message.text) == data["role_password"]:
        await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\nРоль - {data["role"]}"
                                         f"\n\n<b>Успешно!</b>"
                                         f"\nПроверьте, все данные верны?",
                                    chat_id=message.chat.id,
                                    message_id=data["msg_id"],
                                    reply_markup=acceptation_reg)
        await state.set_state(Reg.acceptation)
        await message.delete()

    # если пароль неверный его нужно ввести еще раз
    else:
        try:
            await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                         f"\nИмя - {data["name"]}"
                                         f"\nФамилия - {data["surname"]}"
                                         f"\nДата рождения - {data["birthday"]}"
                                         f"\nТелефон - {data["phone"]}"
                                         f"\nРоль - {data["role"]}"
                                         f"\n\n🙅‍♂️Неверно🙅‍♀️"
                                         f"\nВведите пароль роли еще раз:",
                                        chat_id=message.chat.id,
                                        message_id=data["msg_id"],
                                        reply_markup=None)  # подтверждение
        except:
            await bot.edit_message_text(text=f"<b>Ваши данные</b>"
                                             f"\nИмя - {data["name"]}"
                                             f"\nФамилия - {data["surname"]}"
                                             f"\nДата рождения - {data["birthday"]}"
                                             f"\nТелефон - {data["phone"]}"
                                             f"\nРоль - {data["role"]}"
                                             f"\n\n❌Неверно❌"
                                             f"\nВведите пароль роли еще раз:",
                                        chat_id=message.chat.id,
                                        message_id=data["msg_id"],
                                        reply_markup=None)
        await message.delete()


# кнопка "Да" и добавление в бд
@router.callback_query(F.data == "yes_r", Reg.acceptation)
async def reg_db(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    info = [call.from_user.id,
            f"tg://user?id={call.from_user.id}",
            call.from_user.username,
            data["role"],
            data["category"],
            data["name"],
            data["surname"],
            data["birthday"],
            data["phone"],
            str(datetime.now())[:19],
            (data["msg_id"]),
            call.message.chat.id]
    # проверка на ошибку при регистрации, если она возникает, то регистрацию нужно пройти заново
    try:
        await set_user(info)  # функция добавления в бд нового юзера
        # отправление сообщение о регистрации создателю
        await bot.send_message(text=f"НОВЫЙ ЮЗЕР"
                                    f"\nИмя - {data["name"]}"
                                    f"\nФамилия - {data["surname"]}"
                                    f"\nСсылка - tg://user?id={call.from_user.id}"
                                    f"\nТелефон - {data["phone"]}"
                                    f"\nРоль - {data["role"]}"
                                    f"\nКатегория - {data["category"]}",
                               chat_id=892980299
                               )
    except:
        category = (await state.get_data())["category"]
        await state.clear()
        if category == 'adm':
            await state.update_data(category=category)
            await state.update_data(role=category)
        else:
            await state.update_data(category=category)
        await call.message.edit_text(text="Возникла ошибка...\nПройдите регистрацию заново\n<b>Введите имя</b>")
        await state.set_state(Reg.name)
        return

    await call.message.delete()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1) # тут баг
    msg = await bot.send_message(text="Поздравляем! Вы теперь зарегистрированы!", chat_id=call.message.chat.id,
                                 message_effect_id="5046509860389126442")
    await state.update_data(msg_id=msg.message_id)  # перепривязка айди сообщения чтобы им было удобно управлять
    await update_msg_id(call.from_user.id, msg.message_id)  # перепривязка айди сообщения в бд потому что изначально он там неправильное
    await call.answer()
    # фриз на 3 секунды, затем появляется меню, вид меню определяется в зависимости от категории пользователя
    sleep(3)

    # вывод подходящего меню через специальную фунцию
    await menu_text(data["category"], chat_id=call.from_user.id, message_id=msg.message_id, bot=bot, state=state)


# кнопка "Нет"
@router.callback_query(F.data == 'no_r')  # добавил проверку на стейт
# роль потому что клавиатура acceptation используется в других файлах кода (admins/main функция send_or_not
async def reg_repeat(call: CallbackQuery, bot: Bot, state: FSMContext):
    category = (await state.get_data())["category"]
    await state.clear()
    # проверка админ или нет для правильного заполнения роли, иначе без этого выдает ошибку
    if category == 'adm':
        await state.update_data(category=category)
        await state.update_data(role=category)
    else:
        await state.update_data(category=category)
        await state.update_data(role='')
    await state.update_data(msg_id=call.message.message_id)
    await call.message.edit_text(text="Заполняем заново...\n<b>Введите имя</b>")
    await state.set_state(Reg.name)
    await call.answer()



