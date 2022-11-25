# Модуль Accounts
Регистрация, авторизация, действия с профилем пользователя

Основной url - https://testing-backend.admire.social/user/

#####Регистрация декана
Метод POST  
url - /create_dekan/  
***
Запрос
```json
{
    "email":"test.decan@test.ru",
    "username":"DecanTest",
    "password":"12345",
    "code":"04dc9581-0ab3-410a-a990-dd277713b1be"
}
```
code - поле для ввода пригласительного кода

Ответ
```json
{
    "message": "User succesfully created"
}
```
Ошибка
```json
{
    "error": "Wrong invite code"
}
```
Если код не передан или передан неверный
***

#####Регистрация преподавателя или студента
Метод POST  
url - /create_user/
***
Запрос
```json
{
    "username":"TeacherTest",
    "password":"12345",
    "status":"TEACHER"
}
```
status - поле отвечающее за тип аккаунта  
TEACHER - преподаватель  
STUDENT - студент  
DEAN - декан  

Ответ
```json
{
    "message": "User succesfully created"
}
```
Ошибка при попытке регистрации со статусом декана
```json
{
    "error": "You can create dean account only with invite code"
}
```
***

#####Аутинтификация
Метод POST

url - /obtain_token/
***
Запрос
```json
{
    "login":"test.decan@test.ru",
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
#####Авторизация
Полученный токкен передавать в заголовках по ключу Authorization в формате:  
JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IkRlY2FuVGVzdCIsImV4cCI6MTY0NTkwMDM0OSwiZW1haWwiOiJ0ZXN0LmRlY2FuQHRlc3QucnUifQ.iJNMXNW3d2q5HTaIqKLSdeR43ULITj7rqr9veOufZlcJWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IkRlY2FuVGVzdCIsImV4cCI6MTY0NTkwMDM0OSwiZW1haWwiOiJ0ZXN0LmRlY2FuQHRlc3QucnUifQ.iJNMXNW3d2q5HTaIqKLSdeR43ULITj7rqr9veOufZlc
***

#####Редактирование профиля
Метод PUT  
Требует авторизации  
url - /update_profile/
***
Запрос
```json
{
    "username":"Student",
    "first_name":"Вася"
}
```
доступные поля для редактирования:
username  
first_name  
last_name  
patronymic  
avatar - картинку передавать в form-data по ключу "avatar"  

Ответ
```json
{
    "uuid": "f0d4568f-c938-480a-8564-d95e95b5af4a",
    "username": "Student",
    "status": "DEAN",
    "email": "test.decan@test.ru",
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

#####Запрос профиля
Метод GET  
Требует авторизации  
url - /get_profile/
***
Ответ
```json
{
    "uuid": "f0d4568f-c938-480a-8564-d95e95b5af4a",
    "username": "DecanTest",
    "status": "DEAN",
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