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
    "password":"12345",
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
first_name  
last_name  
patronymic  
avatar - картинку передавать в form-data по ключу "avatar"  

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