from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.database.requests_old import get_by_user_category
from utils.database.requests.roles_req import get_roles

# клавиатура для подтверждения корректности информации при регистрации
acceptation_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes_r"),
     InlineKeyboardButton(text='Нет', callback_data='no_r')]
    ])


# клавиатура для подтверждения информации при начислении баллов
acceptation_points = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes_p"),
     InlineKeyboardButton(text='Нет', callback_data='no_p')]
    ])


# клавиатура для подтверждения информации при отправлении сообщения
acceptation_msg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes_m"),
     InlineKeyboardButton(text='Нет', callback_data='no_m')]
    ])


# клавиатура для подтверждения информации при рассылке
acceptation_msg_all = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes_a"),
     InlineKeyboardButton(text='Нет', callback_data='no_a')]
    ])

# ==================== СОТРУДНИКИ ======================

# клавиатура для меню сотрудников
emp_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мой кабинет", callback_data="cabinet")],
    [InlineKeyboardButton(text="За что начисляем баллы?", url="https://telegra.ph/MYHOTDOG-Bally-06-13")],
    # [InlineKeyboardButton(text="Пройти обучение", callback_data="learn")]
    ])


# кнопка для возвращения в предыдущее положение
back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# кнопка для возвращения в предыдущее положение
back_points_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")],
    [InlineKeyboardButton(text="Проверить свои баллы", callback_data="check_points")]
    ])


# ==================== УПРАВЛЯЮЩИЕ ======================
# админская клавиатура
adm_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сотрудники", callback_data="empls_a")],
    [InlineKeyboardButton(text="Рейтинг", callback_data="rating_a")],
    [InlineKeyboardButton(text="Сделать Рассылку", callback_data="mail_a")],
])


# панель управления сотрудником для управляющих
control_emp_a = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начислить бонусы', callback_data='send_points')],
    [InlineKeyboardButton(text='Списать бонусы', callback_data='take_back_points')],
    [InlineKeyboardButton(text="Отправить сообщение сотруднику", callback_data="send_msg")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# вывод всех сотрудников, callback = айди юзера, это сделано чтобы можно было удобно доставать всю информацию о нем
async def all_emp_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data="back"))
    for emp in (await get_by_user_category("emp")):
        kb.add(InlineKeyboardButton(text=f'{emp.name} {emp.surname}', callback_data=f"{emp.tg_id}"))
    return kb.adjust(1).as_markup()


# ==================== BOSS ======================
# клавиатура владельца
boss_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сотрудники", callback_data="empls_b")],
    [InlineKeyboardButton(text="Управляющие", callback_data="admns_b")],
    [InlineKeyboardButton(text="Рейтинг", callback_data="rating_b")],
    [InlineKeyboardButton(text="Сделать Рассылку", callback_data="mail_b")],
    [InlineKeyboardButton(text="Настройки", callback_data="settings_b")]
])


# вывод всех управляющих, callback = айди юзера, это сделано чтобы можно было удобно доставать всю информацию о нем
async def all_adm_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data="back"))
    for adm in (await get_by_user_category("adm")):
        kb.add(InlineKeyboardButton(text=f'{adm.name} {adm.surname}', callback_data=f"{adm.tg_id}"))
    return kb.adjust(1).as_markup()


# панель управления управляющим(сори за тавтологию)
control_adm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Уволить", callback_data="fire")],
    [InlineKeyboardButton(text="Отправить сообщение управляющему", callback_data="send_msg")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# панель управления сотрудником для владельца
control_emp_b = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Уволить", callback_data="fire")],
    [InlineKeyboardButton(text='Начислить бонусы', callback_data='send_points')],
    [InlineKeyboardButton(text='Списать бонусы', callback_data='take_back_points')],
    [InlineKeyboardButton(text="Отправить сообщение сотруднику", callback_data="send_msg")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# подтверждение увольнения
confirm_fire = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить", callback_data='f_yes')],
    [InlineKeyboardButton(text="Отмена", callback_data='f_no')],

])

# меню доступных настроек
settings_kb = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text="Настроить обучение", callback_data="change_learn")],
    [InlineKeyboardButton(text="Настроить роли", callback_data="change_role")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])


# настройка обучения
learn_settings_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="заменить видео 1", callback_data="replace_1")],
    [InlineKeyboardButton(text="заменить видео 2", callback_data="replace_2")],
    [InlineKeyboardButton(text="заменить видео 3", callback_data="replace_3")],
    [InlineKeyboardButton(text="назад", callback_data="back")]
    ])


# кнопки для выбора категории рассылки
mail_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Всем", callback_data="to_all")],
    [InlineKeyboardButton(text="Управляющим", callback_data="to_adm")],
    [InlineKeyboardButton(text="Сотрудникам", callback_data="to_emp")],
    [InlineKeyboardButton(text="назад", callback_data="back")]
    ])


# клавиатура для вывода доступных ролей
async def all_roles_kb():
    kb = InlineKeyboardBuilder()
    for role in (await get_roles()):
        kb.add(InlineKeyboardButton(text=f"{role.role_name}", callback_data=f"{role.role_password}"))
    return kb.adjust(2).as_markup()  # вывод по две роли в строчку


# клавиатура для вывода доступных ролей и добавления новых
async def all_roles_and_add_kb():
    kb = InlineKeyboardBuilder()
    for role in (await get_roles()):
        kb.add(InlineKeyboardButton(text=f"{role.role_name}", callback_data=f"{role.role_password}"))
    kb.add(InlineKeyboardButton(text=f"➕Добавить роль", callback_data=f"add_role"))
    kb.add(InlineKeyboardButton(text=f"Назад", callback_data=f"back"))
    return kb.adjust(1).as_markup()


# настройки выбранной роли
role_settings_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить", callback_data="del_role")],
    [InlineKeyboardButton(text="Изменить пароль", callback_data="change_role_password")],
    [InlineKeyboardButton(text="назад", callback_data="back")]
    ])


# подтверждение удаления роли
confirm_del_role = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить", callback_data='r_yes')],
    [InlineKeyboardButton(text="Отмена", callback_data='r_no')],

])

# подтверждение добавления роли
confirm_add_role = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить", callback_data='add_yes')],
    [InlineKeyboardButton(text="Отмена", callback_data='add_no')],

])




