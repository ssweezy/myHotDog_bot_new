from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# создание файла
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)


# создание подключения
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# таблица данных пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tg_url: Mapped[str] = mapped_column(String(50))
    tg_username: Mapped[str] = mapped_column(String(30), default=f'')
    role: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))
    reg_date: Mapped[str] = mapped_column(String(40))
    msg_id: Mapped[int] = mapped_column(default=0)
    chat_id: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=0)


# таблица забаненных пользователей
class BanList(Base):
    __tablename__ = 'banned_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


# # таблица с настройками текста и тд
# class Setting(Base):
#     __tablename__ = 'settings'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     adm_menu_text: Mapped[str] = mapped_column(String(300), default="<b>В вашем распоряжении следующие функции</b>")
#     emp_menu_text: Mapped[str] = mapped_column(String(300), default="<b>МЕНЮ</b>")
#
#
# таблица ролей и паролей
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(30))
    role_password: Mapped[str] = mapped_column(String(20))


# таблица с file_id видео обучения
class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[str] = mapped_column(String(500))
    # video_name: Mapped[str] = mapped_column(String(20))
    # video_caption: Mapped[str] = mapped_column(String(500), default=None)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # =========УБРАТЬ ПОСЛЕ ЗАПУСКА!!
        await conn.run_sync(Base.metadata.create_all)
