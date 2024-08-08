from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from utils.FSM import Menu
from utils.database.requests_old import get_user_info, get_by_user_category
from utils.fucntions import update_data
from utils.kb.inline_kb import control_emp_b, all_emp_kb


router = Router()


# вывод всех сотрудников
@router.callback_query(F.data == "empls_b")
async def catalog(call: CallbackQuery, state: FSMContext):
    await update_data(call.from_user.id, state)

    await call.message.edit_text("<b>Выберите сотрудника:</b>", reply_markup=await all_emp_kb())
    await state.set_state(Menu.show_emp)
    await call.answer()


# обработка и вывод инфы по юзеру опираясь на коллбек(в нем юзер айди)
@router.callback_query(Menu.show_emp, F.data != "back")
async def show_user_info(call: CallbackQuery, state: FSMContext):
    user = await get_user_info(int(call.data))

    users = await get_by_user_category("emp")
    # сортировка сотрудников по баллам
    rating_dict = {i.tg_id: i.points for i in users}
    rating_list = sorted(rating_dict.items(), key=lambda x: x[1], reverse=True)  # отсортированный список

    user_rank = 0  # переменная для хранения места в рейтинге
    # функция определяющая место в рейтинге
    for i in range(len(rating_list)):
        if user.tg_id in rating_list[i]:  # находит первое совпадение и на его основе формируется место в рейтинге
            user_rank = i + 1
        break

    # присваивание айди юзера в data чтобы можно было дальше с ним работать
    await state.update_data(choose_user_id=call.data)
    await call.message.edit_text("<b>Информация по сотруднику:</b>"
                                 f"\n\nИмя - {user.name} {user.surname}"
                                 f"\nСсылка - {user.tg_url}"
                                 f"\nРоль - {user.role}"
                                 f"\nДата регистрации в бот - {user.reg_date}"
                                 f"\nБаллы - <b>{user.points}</b>"
                                 f"\nМесто в рейтинге - {user_rank}",
                                 reply_markup=control_emp_b)
    await call.answer()
    await state.set_state(None)