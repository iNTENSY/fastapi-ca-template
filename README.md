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

### Комментарии автора
___
Данный шаблон не является панацеей для всех проектов на FastAPI, но он демонстрирует
реализацию Чистой Архитектуры (Clean Arch.) предоставленным Робертом Мартином в своей одноименной книге.

Проект строится на IoC-контейнере в связке с DI-фреймворком (dishka) и именно поэтому,
если вы хотите добавить или удалить какую-то составляющую проекта, убедитесь, что вы
правильно реализовали поведение самого контейнера (./app/infrastructure/di/).

Для запуска тестов используется команда `pytest` с настройками тестовой среды (pytest.ini).
Убедитесь что все указанные парамеры присутствуют.

Интегрированные технологии в проекте: 
- JWT (cookie with HTTPOnly), Session Auth
- SQLAdmin
- Email
- Background tasks (Celery + Redis)
- Rate limiter (slowapi)
- Cache (fastapi-cache2 + Redis)
- Logger (logging)

Используемые шаблоны и паттерны проектирования:
- IoC-контейнеры
- Dependency Injection
- Repository
- Value Objects
- Domain Model
- Mappers
- Adapters
- Data Transfer Objects
- Transaction Manager
- Factory


### Контакты:
___

- Автор: Даценко Дмитрий Игоревич <br>
- Telegram: https://t.me/dmitriydatsenko <br>
- Электронная почта: dmitriydatsenko@inbox.ru <br>
- GitHub: https://github.com/iNTENSY

