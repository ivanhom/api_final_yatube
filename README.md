# api_yatube
В данном проекте реализовано API сервиса для публикации авторских постов по категориям с возможностью создания комментариев к постам и подпиской на автора.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```shell
git clone git@github.com:ivanhom/api_final_yatube.git
```

```shell
cd kapi_final_yatube
```
<br>

В корне проекта создать файл `.env` на основе `.env.example`, указав валидные данные.

Cоздать и активировать виртуальное окружение:

- Для linux/mac:
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
- Для Windows:
    ```shell
    python -m venv venv
    .\venv\Scripts\activate
    ```

Установить зависимости из файла requirements.txt:

```shell
python -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

Перейти в дирректорию `yatube_api` и выполнить миграции:

```shell
cd yatube_api
```
```shell
python manage.py migrate
```

Запустить проект:

```shell
python manage.py runserver
```

Далее можно выполнять запросы по эндпоинтам


### Используются следующие эндпоинты:

```
api/v1/jwt/create/ (POST): передаём логин и пароль, получаем JWT токен.
```
```
api/v1/posts/ (GET, POST): получаем список всех постов или создаём новый пост.
```
```
api/v1/posts/{post_id}/ (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем пост по id.
```
```
api/v1/groups/ (GET): получаем список всех групп.
```
```
api/v1/groups/{group_id}/ (GET): получаем информацию о группе по id.
```
```
api/v1/posts/{post_id}/comments/ (GET, POST): получаем список всех комментариев поста с id=post_id или создаём новый, указав id поста, который хотим прокомментировать.
```
```
api/v1/posts/{post_id}/comments/{comment_id}/ (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем комментарий по id у поста с id=post_id.
```
```
api/v1/follow/ (GET, POST): получаем список всех авторов, на которых подписан пользователь или подписываемся на выбранного автора.
```


## ПРИМЕРЫ ЗАПРОСОВ

**1) Пример POST-запроса: добавление нового поста.**
```
POST .../api/v1/posts/
```
```
{
    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",
    "group": 1
}
```
Пример ответа:
```
{
    "id": 14,
    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",
    "author": "anton",
    "image": null,
    "group": 1,
    "pub_date": "2021-06-01T08:47:11.084589Z"
}
```


**2) Пример POST-запроса: отправляем новый комментарий к посту с id=14.**
```
POST .../api/v1/posts/14/comments/
```
```
{
    "text": "тест тест"
}
```
Пример ответа:
```
{
    "id": 4,
    "author": "anton",
    "post": 14,
    "text": "тест тест",
    "created": "2021-06-01T10:14:51.388932Z"
}
```


**3) Пример GET-запроса: получаем информацию о группе.**
```
GET .../api/v1/groups/2/
```
Пример ответа:
```
{
    "id": 2,
    "title": "Математика",
    "slug": "math",
    "description": "Посты на тему математики"
}
```
