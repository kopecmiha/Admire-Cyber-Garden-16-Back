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