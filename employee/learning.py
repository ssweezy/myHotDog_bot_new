from time import sleep
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


from utils.kb.inline_kb import emp_menu_kb, back_kb
from utils.FSM import Learning
from utils.database.requests_old import update_file_id

router = Router()


# отправление первичной информации об обучении **ДОРАБОТАТЬ
@router.callback_query(F.data == "learn")
async def start_learning(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.edit_text("в доработке")
    sleep(2)
    await call.message.edit_text(f"<b>MENU</b>", reply_markup=emp_menu_kb)
    await state.set_state(None)
    await call.answer()



