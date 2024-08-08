from utils.database.models import async_session
from utils.database.models import User, Video, Role, BanList
from sqlalchemy import select, update


# добавление сотрудника в бд
async def set_user(data):
    tg_id, tg_url, tg_username, role, category, name, surname, birthday, phone, reg_date, msg_id, chat_id = data
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             tg_url=tg_url,
                             tg_username=tg_username,
                             role=role,
                             category=category,
                             name=name,
                             surname=surname,
                             birthday=birthday,
                             phone=phone,
                             reg_date=reg_date,
                             msg_id=msg_id,
                             chat_id=chat_id
                             ))
            await session.commit()


# получение кол-ва баллов сотрудника
async def get_points(tg_id):
    async with async_session() as session:
        points = await session.scalar(select(User.points).where(User.tg_id == tg_id))
        return points


# проверка зареган юзер или нет
async def user_exists(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return True if user else False  # однострочное условие возвращает True/False,


# получение всю информацию о пользователе с помощью его ID
async def get_user_info(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


# получение всех пользователей по выбранной категории
async def get_by_user_category(category: str):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.category == category))


# получение всех сотрудников
async def get_all_users():
    async with async_session() as session:
        emp = await session.scalars(select(User).where(User.category == "emp"))
        adm = await session.scalars(select(User).where(User.category == "adm"))
        return emp, adm


# получение подопечных управляющего
async def get_adm_empls(role):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.category == "emp" and User.role == role))


# меняет количество очков пользователя используя его айди
async def update_user_points(tg_id, new_value: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(points=new_value))
        await session.commit()


async def update_msg_id(tg_id, new_value):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(msg_id=new_value))
        await session.commit()


# получение file_id выбранного видео
async def get_file_id(video_num):  # параметр video это число видео по порядку
    async with async_session() as session:
        return await session.scalar(select(Video.file_id).where(Video.id == video_num))


# изменение выбранного видео
async def update_file_id(video_num: int, new_file_id):
    async with async_session() as session:
        await session.execute(update(Video).where(Video.id == video_num).values(file_id=new_file_id))
        await session.commit()


# функция удаления из бд
async def del_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await session.delete(user)
        await session.commit()


# добавление в банлист
async def add_to_banlist(tg_id):
    async with async_session() as session:
        session.add(BanList(tg_id=tg_id))
        await session.commit()


# получение всех, кто в банлисте
async def get_banlist():
    async with async_session() as session:
        return await session.scalars(select(BanList.tg_id))



# остановились на увольнении, нужно доработать функцию в boss/ations/fire.
# также добавить обработку на коллбеки boss(там стоят префиксы для доп функций)