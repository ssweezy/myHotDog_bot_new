from utils.database.models import async_session
from utils.database.models import User, Video, Role, BanList
from sqlalchemy import select, update


# получение всех доступных ролей
async def get_roles():
    async with async_session() as session:
        return await session.scalars(select(Role))


# получение пароля по названию роли
async def get_role_password(role_name):
    async with async_session() as session:
        return await session.scalar(select(Role.role_password).where(Role.role_name == role_name))


# получение названия по паролю роли
async def get_role_by_password(role_password):
    async with async_session() as session:
        return await session.scalar(select(Role.role_name).where(Role.role_password == role_password))


# изменение пароля по паролю роли
async def change_role_password(role_password, new_role_password):
    async with async_session() as session:
        await session.execute(update(Role).where(Role.role_password == role_password).values(
            role_password=new_role_password))
        await session.commit()


# добавление роли в бд
async def add_role(role_name, role_password):
    async with async_session() as session:
        session.add(Role(role_name=role_name,
                         role_password=role_password
                    ))
        await session.commit()


# удаление роли по ее паролю
async def del_role(role_password):
    async with async_session() as session:
        role = await session.scalar(select(Role).where(Role.role_password == role_password))
        await session.delete(role)
        await session.commit()

