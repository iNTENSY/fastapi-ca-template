## Шаблон по созданию проекта
___

Данный шаблон является базовой необходимой структурой
проекта, включающий основные сценарии работы с пользователем
с использованием FastAPI и PostgreSQL по мнению автора.
Тут предоставлен лэйаут проекта с использованием
принципов Clean Architecture и Dependency Injection, и код,
базово необходимый для работы с пользователем.

### Технологический стек:
___

- Язык программирования: Python 3.11+
- База данных: PostgreSQL
- Контейнеризация: Docker
- Веб-фреймворк: FastAPI
- Драйвер для PostgreSQL: Psycopg + Asyncpg
- Фреймворк для внедрения зависимостей: Dishka
- Библиотека для тестирования: pytest

### Запуск проекта используя контейнеризацию (Docker system)
___
1. Клонируйте репозиторий: `https://github.com/iNTENSY/fastapi-ca-template.git`
2. Запустите Docker в вашей системе: `sudo systemctl start docker`
3. Установите файл с переменными окружения (`.env`) в каталоге `./doker`. <br>
Для примера используемых переменных окружения обратитесь в файл `.env.production.example`
4. Перейдите в каталог с конфигурационными файлами docker-compose и nginx: `cd ./docker`
5. Соберите контейнеры и запустите их с параметром -d: `sudo docker compose up --build`
6. Проверьте миграции внутри контейнера: `sudo docker compose exec backend alembic revision --autogenerate`
7. Примените миграции: `sudo docker compose exec backend alembic upgrade head`
8. Сайт доступен по данному url: http://localhost:8001/docs

### Контакты:
___

- Автор: Даценко Дмитрий Игоревич <br>
- Telegram: https://t.me/dmitriydatsenko <br>
- Электронная почта: dmitriydatsenko@inbox.ru <br>
- GitHub: https://github.com/iNTENSY

