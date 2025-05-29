# Проект API YamDB
## Описание проекта:
**API YamDB** - Проект собирает отзывы пользователей на произведения. Сами произведения в YamDB не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
## Стек:
- Python 3.9
- Django 3.2
- Django REST Framework 3.12
- Simple JWT (токены)
## Возможности:
- Создание и управление отзывами на произведения
- Комментирование отзывов
- Оценка произведений по шкале от 1 до 10
- Категоризация произведений (фильмы, книги, музыка и т.д.)
- Жанровая классификация произведений
- Система ролей пользователей с разными уровнями доступа
## Установка и запуск:
1. Клонировать репозиторий и перейти в него:
```
git clone https://github.com/sijey06/api_yamdb.git
```
```
cd api_final_yatube
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Создать и применить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
5. Запустить проект:
```
python manage.py runserver
```
## Работа с API
### Регистрация пользователей
Отправьте POST-запрос с email и username на эндпоинт /api/v1/auth/signup/
YamDB отправит код подтверждения на указанный email
Получите JWT-токен, отправив POST-запрос с username и confirmation_code на эндпоинт /api/v1/auth/token/
### Аутентификация
Для доступа к API необходимо передавать токен в заголовке каждого запроса:
```Authorization: Bearer <ваш_токен>```
### Пользовательские роли
Аноним — может просматривать описания произведений, читать отзывы и комментарии
Пользователь — может публиковать отзывы, ставить оценки произведениям, комментировать отзывы
Модератор — те же права, что и у пользователя, плюс право удалять и редактировать любые отзывы и комментарии
Администратор — полные права на управление контентом проекта
### Основные эндпоинты API
/api/v1/auth/signup/ (POST): Регистрация пользователя
/api/v1/auth/token/ (POST): Получение JWT-токена
/api/v1/users/ (GET, POST): Пользователи
/api/v1/users/me/ (GET, PATCH): Профиль пользователя
/api/v1/categories/ (GET, POST): Категории произведений
/api/v1/genres/ (GET, POST): Жанры произведений
/api/v1/titles/ (GET, POST): Произведения
/api/v1/titles/{title_id}/reviews/ (GET, POST): Отзывы
/api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST): Комментарии
### Примеры запросов
### Регистрация нового пользователя
```
POST /api/v1/auth/signup/
{
    "email": "user@example.com",
    "username": "string"
}
```
### Получение JWT-токена
```
POST /api/v1/auth/token/
{
    "username": "string",
    "confirmation_code": "string"
}
```
### Получение списка всех произведений
```
GET /api/v1/titles/
```
### Добавление отзыва
```
POST /api/v1/titles/{title_id}/reviews/
{
    "text": "string",
    "score": 1
}
```
### Добавление комментария к отзыву
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
    "text": "string"
}
```
### Получение категорий
```
GET /api/v1/categories/
```
## Документация:
Полная документация доступна по адресу:
http://127.0.0.1:8000/redoc/
## Автор:
### Игорь Журавлев(Иван Вилохин, Александр Захаров)
Ссылка на GitHub:
https://github.com/sijey06

