from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from utils.FSM import Menu
from utils.database.requests_old import get_user_info
from utils.fucntions import update_data
from utils.kb.inline_kb import control_emp_a, all_emp_kb


router = Router()


# вывод всех сотрудников для владельца
@router.callback_query(F.data == "empls_a")
async def catalog(call: CallbackQuery, state: FSMContext):
    await update_data(call.from_user.id, state)

    await call.message.edit_text("<b>Выберите сотрудника:</b>", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp_b)
    await call.answer()


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Menu.show_emp_b, F.data != "back")
async def show_user_info(call: CallbackQuery, state: FSMContext):
    user = await get_user_info(int(call.data))
    # присваивание айди юзера в data чтобы можно было дальше с ним работать
    await state.update_data(choose_user_id=call.data)
    await call.message.edit_text("<b>Информация по сотруднику:</b>"
                                 f"\n\nИмя - {user.name} {user.surname}"
                                 f"\nСсылка - {user.tg_url}"
                                 f"\nРоль - {user.role}"
                                 f"\nДата регистрации в бот - {user.reg_date}"
                                 f"\nБаллы - <b>{user.points}</b>", reply_markup=control_emp_a)
    await call.answer()
    await state.set_state(None)

