# Модуль Store
Товары

Основной url - /store/
***

##### Получение единичного товара
Метод Get  
url - /get_product/?id=1
***
Ответ
```json
{
    "id": 1,
    "title": "Майка2",
    "icons": "/media/%5B%3CTemporaryUploadedFile%3A%20P1010001.JPG%20(image/jpeg)%3E%5D",
    "price": 1000,
    "in_stock": true
}
```
***

##### Получение списка товаров
Метод GET  
Требует авторизации  
url - http://127.0.0.1:8000/api/store/get_products_list/?page=0&limit_of_set=10
***
Ответ
```json
[
    {
        "id": 1,
        "title": "Майка2",
        "icons": "/media/%5B%3CTemporaryUploadedFile%3A%20P1010001.JPG%20(image/jpeg)%3E%5D",
        "price": 1000,
        "in_stock": true
    }
]
```
***

##### Покупка продукта
Метод POST  
Требует авторизации  
url - /api/store/buy/
***
Запрос - передается id продукта
```json
{
    "id": "1"
}
```
Ответ
```json
{
    "id": 2,
    "product": {
        "id": 1,
        "title": "Майка2",
        "icons": "/media/%5B%3CTemporaryUploadedFile%3A%20P1010001.JPG%20(image/jpeg)%3E%5D",
        "price": 1000,
        "in_stock": true
    },
    "price": 1000,
    "date_time": "2022-11-26T10:07:27.475665Z"
}
```
Ответ если недостаточно средств
```json
{
    "error": "You can't buy this product"
}
```
***
