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
