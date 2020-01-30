# Тестовое задание для Softlogirus

 

# Как установить

Склонируйте репозиторий
```bash
git clone https://github.com/kratorr/softlogic_test
```
Для работы необоходим Python3. 
Установите зависимости с помощью pip:
```bash
pip3 install -r requirements.txt
```
Для лучшей изоляции  рекомендуется использовать виртуальное окружение.


# Quickstart

Применим миграции для БД
```bash
$ python3 manage.py migrate
```

Запуск на встроенном сервере Django
```bash
$ python3 manage.py runserver
```

# Как использовать

## Список id всех Person

### Request

`GET /person/`

    curl --request GET http://localhost:8000/person/  -H 'Content-Type: application/json'



## Создать нового Person

### Request

`POST /person/`

    curl --request POST  http://localhost:8000/person/  -H 'Content-Type: application/json' -d '{"last_name":"Foo","first_name":"Bar"}'

## Получить информацию о Person

### Request

`GET /person/id/`

    curl --request GET 'http://localhost:8000/person/ecebd15e-fa62-43ce-9fe9-9bf95c81921b/' -H 'Content-Type: application/json'


## Обновить ветор по конкретному Person

### Request

`PUT /person/id/`

    curl --request PUT 'http://localhost:8000/person/ecebd15e-fa62-43ce-9fe9-9bf95c81921b/' --form 'image=@./image.jpg' -H 'Content-Type: multipart/form-data'

 

## Удалить Person по id

### Request

`DELETE /person/id/`

    curl --request DELETE 'http://localhost:8000/person/ecebd15e-fa62-43ce-9fe9-9bf95c81921b/' -H 'Content-Type: application/json'



## Сравнить вектора двух Person 

### Request

`GET person/id/compare/id2/`

    curl --request GET 'http://localhost:8000/person/5af44f20-ec06-437f-8423-467ed9407971/compare/5af44f20-ec06-437f-8423-467ed940797c/' -H 'Content-Type: application/json'
