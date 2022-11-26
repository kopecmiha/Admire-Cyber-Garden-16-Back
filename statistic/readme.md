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
url - /get_user_points/
возможно запросить очки другого пользователя get параметр user_uuid
http://127.0.0.1:8000/api/statistic/get_user_points/?user_uuid=750de923-48ee-46ff-b6ab-c54b09824d79
***
Ответ
```json
{
    "points_sum": 10
}
```
Ошибка при неавторизованном запросе
```json
{
    "detail": "Authentication credentials were not provided."
}
```
***
