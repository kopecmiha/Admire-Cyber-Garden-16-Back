# Модуль Statistic
Статистика по играм пользователей

Основной url - /statistic/
***

##### Запись игровой сессии
Метод POST  
url - /add_game_session/
***
Запрос
```json
{
    "duration": 100,
    "points": 10,
    "game_type": "full-name",
    "try_count": 1
}
```

Ответ
```json
{
    "id": 23,
    "finished": "2022-11-26T01:23:46.964403Z",
    "points": 10,
    "game_type": "full-name",
    "try_count": 1,
    "duration": 100
}
```
***

##### Запрос очков пользователя
Метод GET  
Требует авторизации  
url - /get_user_balance/
***
Ответ
```json
{
    "balance": 10
}
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
***
