# Модуль Accounts
Регистрация, авторизация, действия с профилем пользователя

Основной url - 
***

##### Регистрация пользователя
Метод POST  
url - /create_user/
***
Запрос
```json
{
    "email": "test@test.com",
    "password":"12345"
}
```

Ответ
```json
{
    "message": "User succesfully created"
}
```
***

##### Аутинтификация
Метод POST

url - /obtain_token/
***
Запрос
```json
{
    "login":"test@test.com",
    "password":"12345"
}
```
в login передавать email или username

Ответ
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IkRlY2FuVGVzdCIsImV4cCI6MTY0NTkwMDM0OSwiZW1haWwiOiJ0ZXN0LmRlY2FuQHRlc3QucnUifQ.iJNMXNW3d2q5HTaIqKLSdeR43ULITj7rqr9veOufZlc"
}
```
Ошибка при неверных логине или пароле
```json
{
    "error": "Please provide right login and a password"
}
```
***
##### Авторизация
Полученный токкен передавать в заголовках по ключу Authorization в формате:  
JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IkRlY2FuVGVzdCIsImV4cCI6MTY0NTkwMDM0OSwiZW1haWwiOiJ0ZXN0LmRlY2FuQHRlc3QucnUifQ.iJNMXNW3d2q5HTaIqKLSdeR43ULITj7rqr9veOufZlcJWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IkRlY2FuVGVzdCIsImV4cCI6MTY0NTkwMDM0OSwiZW1haWwiOiJ0ZXN0LmRlY2FuQHRlc3QucnUifQ.iJNMXNW3d2q5HTaIqKLSdeR43ULITj7rqr9veOufZlc
***

##### Редактирование профиля
Метод PUT  
Требует авторизации  
url - /update_profile/
***
Запрос
```json
{
    "first_name":"Вася"
}
```
доступные поля для редактирования:  
first_name;  
last_name;  
patronymic;  
specialization;  
grade - возможные значения - "SENIOR", "MIDDLE", "JUNIOR";  
avatar - картинку передавать в form-data по ключу "avatar";   

Ответ
```json
{
    "uuid": "f0d4568f-c938-480a-8564-d95e95b5af4a",
    "username": "Test",
    "email": "test@test.ru",
    "first_name": "Вася",
    "last_name": null,
    "patronymic": null,
    "avatar": null
}
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
Ошибка при недоступном для редактирования поле
```json
{
    "detail": "Invalid signature."
}
```
***

##### Запрос профиля
Метод GET  
Требует авторизации  
url - /get_profile/
***
Ответ
```json
{
    "uuid": "f0d4568f-c938-480a-8564-d95e95b5af4a",
    "username": "DecanTest",
    "email": "test.decan@test.ru",
    "first_name": null,
    "last_name": null,
    "patronymic": null,
    "avatar": null
}
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
***

##### Запрос профилей
Метод GET  
Требует авторизации  
url - /list_of_users/
***
Ответ
```json
[
    {
        "first_name": "Надежда",
        "last_name": "Абрамова",
        "patronymic": "Тимуровна",
        "email": "test1@test.com",
        "uuid": "45e07bbb-6c71-431b-81a4-880426f909b1",
        "token": "",
        "avatar": null,
        "grade": "JUNIOR",
        "specialization": "Бекенд-разработчик"
    },
    {
        "first_name": "Марк",
        "last_name": "Акимов",
        "patronymic": "Львович",
        "email": "test2@test.com",
        "uuid": "df9e49b9-3c08-4aff-a315-aeb2df01bb16",
        "token": "",
        "avatar": null,
        "grade": "MIDDLE",
        "specialization": "Бекенд-разработчик"
    }
]
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
***
##### Фильтрация пользователей
Метод GET  
Требует авторизации  
url - /list_of_users_filter/
Доступные фильтры:
page - номер страницы, 
limit_of_set - количество объектов на странице
список доступных полей для фильтрации -  email, first_name, last_name, patronymic, grade, specialization
список доступных полей для упорядочивания -  email, first_name, last_name, patronymic, grade, specialization, random
not_empty - исключает записи со значением null и "" в любом из полей для фильтрации, принимает только значение true, остальные игнорируются

Пример запроса 
```
http://127.0.0.1:8000/api/user/list_of_users_filter?order=random&not_empty=true&limit_of_set=100&first_name=Алиса&page=0
```
***
Ответ
```json
[
    {
        "id": 30,
        "first_name": "Алиса",
        "last_name": "Губанова",
        "patronymic": "Павловна",
        "email": "test7@test.com",
        "token": "",
        "avatar": null,
        "grade": "SENIOR",
        "specialization": "Бекенд-разработчик",
        "date_birthday": "2002-11-18",
        "department": {},
        "uuid": "2d14ffc8-153a-433d-84b8-523d7ab7f43b"
    },
    {
        "id": 33,
        "first_name": "Алиса",
        "last_name": "Егорова",
        "patronymic": "Дамировна",
        "email": "test10@test.com",
        "token": "",
        "avatar": null,
        "grade": "MIDDLE",
        "specialization": "Дизайнер",
        "date_birthday": "1989-01-05",
        "department": {},
        "uuid": "ed1bf3b3-b66b-4182-8d99-d417cfb25d63"
    }
]
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
***
добавить поля city и online 
сгенерить города(10 разных)
40% пользователей в офисах, 60% - удаленщики
в городах с офисом в основном удаленщик

##### Сменить пароль
Метод POST  
url - /change_password/
***
Запрос
```json
{
    "old_password": "12345",
    "new_password": "123456"
}
```

Ответ
```json
{
    "message": "Successfully change password"
}
```

Ответ неверный страый пароль
```json
{
    "error": "Not valid password"
}
```
***

##### Текстовый поиск
Метод Get  
url - /search_text/
query параметры:  
search_text - текст который проверяется на вхождение
page - страница
limit_of_set - количество объектов на странице
***
Запрос
```
http://127.0.0.1:8000/api/user/text_search/?search_text=али&page=0&limit_of_set=5
```

Ответ
```json
[
    {
        "id": 29,
        "first_name": "Милана",
        "last_name": "Васильева",
        "patronymic": "Дмитриевна",
        "email": "test6@test.com",
        "token": "",
        "avatar": "/media/avatars/e5b8ffee-37b1-473a-805c-8e18101f4f4a_7aR2E2p.jpg",
        "grade": "MIDDLE",
        "specialization": "Веб-аналитик",
        "date_birthday": "1994-03-17",
        "department": {
            "id": 8,
            "title": "Веб разработка",
            "chief_id": 26,
            "chief_name": "Александров Артём"
        },
        "uuid": "ee3c5cb9-f043-4f4c-96aa-598597cfd5f9",
        "fact1": "Спортсменка",
        "fact2": "IQ выше 200",
        "fact3": "Съедает 45 кг шоколада в год",
        "city": "Ростов-на-Дону",
        "online": false
    },
    {
        "id": 30,
        "first_name": "Алиса",
        "last_name": "Губанова",
        "patronymic": null,
        "email": "test7@test.com",
        "token": "",
        "avatar": "/media/avatars/e4e8114a-2cb5-4d38-aa9e-9eecb2436d7b_e9JCy0x.jpg",
        "grade": "SENIOR",
        "specialization": "Бекенд-разработчик",
        "date_birthday": "2002-11-18",
        "department": {
            "id": 8,
            "title": "Веб разработка",
            "chief_id": 26,
            "chief_name": "Александров Артём"
        },
        "uuid": "2d14ffc8-153a-433d-84b8-523d7ab7f43b",
        "fact1": "Работала в почтовом отделении",
        "fact2": "Отпечатки ее пальцев похожи на отпечатки пальцев Коалы",
        "fact3": "Фанатка Арндольда Шварцнегера",
        "city": "Армавир",
        "online": true
    },
    {
        "id": 33,
        "first_name": "Алиса",
        "last_name": "Егорова",
        "patronymic": "Дамировна",
        "email": "test10@test.com",
        "token": "",
        "avatar": "/media/avatars/b262eb1b-5775-4a6f-9002-2e5a552871fd_fCle0IN.jpg",
        "grade": "MIDDLE",
        "specialization": "Дизайнер",
        "date_birthday": "1989-01-05",
        "department": {
            "id": 11,
            "title": "Диджитал контент",
            "chief_id": 39,
            "chief_name": "Котов Александр"
        },
        "uuid": "ed1bf3b3-b66b-4182-8d99-d417cfb25d63",
        "fact1": "Хочет быть космонавтом и брать с собой в космос оружие",
        "fact2": "Верит в НЛО",
        "fact3": "Дотягивается языком до локтя",
        "city": "Москва",
        "online": true
    },
    {
        "id": 53,
        "first_name": "Аглая",
        "last_name": "Романова",
        "patronymic": "Тимофеевна",
        "email": "test30@test.com",
        "token": "",
        "avatar": "/media/avatars/27c9e143-7b13-4928-a4ab-10107e00ae1e_t3vytEl.jpg",
        "grade": "MIDDLE",
        "specialization": "Системный аналитик",
        "date_birthday": "1994-02-18",
        "department": {
            "id": 8,
            "title": "Веб разработка",
            "chief_id": 26,
            "chief_name": "Александров Артём"
        },
        "uuid": "8a7f199c-829a-4309-9ac2-eb7f9fae33a3",
        "fact1": "Знает все созвездия",
        "fact2": "Не любит варенный лук",
        "fact3": "прекрасно жарит шашлык",
        "city": "Ставрополь",
        "online": true
    },
    {
        "id": 52,
        "first_name": "Кристина",
        "last_name": "Попова",
        "patronymic": "Давидовна",
        "email": "test29@test.com",
        "token": "",
        "avatar": "/media/avatars/31c40e92-6fe9-478c-a154-8238f23c7d12_qTWiYlp.jpg",
        "grade": "JUNIOR",
        "specialization": "Системный аналитик",
        "date_birthday": "1994-05-19",
        "department": {
            "id": 8,
            "title": "Веб разработка",
            "chief_id": 26,
            "chief_name": "Александров Артём"
        },
        "uuid": "75fecd73-24f4-4a67-9d02-8bfbc989b03f",
        "fact1": "Любит клубничное мороженное",
        "fact2": "Фанат ММА боев",
        "fact3": "Выросла с корейцами в Чечне",
        "city": "Таганрог",
        "online": false
    }
]
```

***