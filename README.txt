Это будет как инструкция по коду

==================ЛОГИКА==================
1. ОДНО СООБЩЕНИЕ
Все основные действия происходят в одном сообщении, которое постоянно меняется.
Оно меняется путем обращения к его msg_id, поэтому очень важно постоянно сохранять msg_id в бд.

2. ИЕРАРХИЯ
В боте структура по идее 4 ступенчатая:
владелец -> заведение -> управляющий -> сотрудник

Пока что мы разработаем 3 ступенчатую(без заведений)


===========================================================
1. ЧТО ТАКОЕ DATA?
*data - условное обозначение, вы можете назвать ее как хотите*

Если в общих чертах то дата - это вся инфа по пользователю(категория, роль и тд), и дата постоянно обновляется
и сохраняется в бд чтобы данные были актуальными

Иногда дата импортируется из бд, это сделано для того чтобы получить 100% гарантию, что инфа не пустая(при перезапуске
все слетает т.к data хранится в оперативке)

Импорт с бд выглядит так:
user_data = await get_user_info(message.from_user.id)   *запросы в бд -> utils/database/requests*

Обновление текущих данных data на данные из бд:
await update_data(message.from_user.id, state) - эта функция есть почти во всех хендлерах чтобы все работало четко

data = await state.get_data() - это строка получения всей информации по юзеру чтобы работать с ней

ИНФОРМАЦИЯ В ДАТА
--постоянная--
 tg_id
 tg_username
 role
 category
 name
 surname
 birthday
 phone
 msg_id
 chat_id
--переменная--
 choose_user_id - в нем хранится tg_id выбранного пользователя (используется в admins/actions/emp_list, boss/actions/adm_list)
 msg_to_send - в нем хранится сообщение для отправки (используется в admins/actions_with_emp/send_msg)
 msg_to_send_with_points - сообщения для отправки вместе с баллами (admins/actions_with_emp/send_points или take_back_points)
 points_to_send - количество начисляемых баллов (admins/actions_with_emp/send_points или take_back_points)
 chosen_role - пароль выбранной роли для ее настройки (boss/actions_settings/role_settings)
 new_role_name - название новой роли (boss/actions_settings/role_settings)
 new_role_password - пароль новой роли (boss/actions_settings/role_settings)
================================================