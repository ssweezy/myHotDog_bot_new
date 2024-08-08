import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils import config, fucntions
from utils.config import TOKEN
from utils.database.models import async_main
from utils.database.requests.roles_req import add_role


from utils.fucntions import router as r1  # добавлять в dp_include самым последним, потому что содержит функцию
# del_trash, если импортировать не последним, то вызывает баги в работе бота
from utils.reg import router as r2
from employee.learning import router as r3
from employee.cabinet import router as r4
from admins.actions_with_emp.emp_list import router as r5
from admins.actions_with_emp.send_points import router as r6
from admins.actions_with_emp.take_back_points import router as r7
from admins.actions_with_emp.send_msg import router as r8
from admins.actions_with_emp.send_to_all import router as r9
from admins.actions_with_emp.rating import router as r10
from boss.actions_settings.settings import router as r11
from boss.actions_settings.learning_settings import router as r12
from boss.actions.adm_list import router as r_boss1
from boss.actions.fire import router as r_boss2
from boss.actions.emp_list import router as r_boss3
from boss.actions_settings.role_settings import router as r_boss4


# срабатывает на запуске, основная функция
async def main():
    await async_main()  # создание бд
    # добавление ролей по умолчанию
    await add_role('повар', 'povar!@#')
    await add_role('бариста', 'barista!@#')
    await add_role('кассир', 'kassir!@#')

    # остальная часть
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))
    dp = Dispatcher(cofig=config)
    dp.include_routers(r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r_boss1, r_boss2, r_boss3, r_boss4, r1)

    await bot.send_message(chat_id=892980299, text="✅started")
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')



"""надо решитт проблему с обновлением данных, вроде все решается через диспетчер, туда запихать функцию обнов инфы """
