# Сервис заказов

Сервис написан на Python/FastAPI. Используется для работы
с сущностями заказов

## Начало установки

### Stack
- Python 3.8
- FastAPI 0.63
- Database: PostgreSQL

Перед началом установки проекта в системе должен быть установлен Python

## Установка

### 1. Перейти в папку проекта
*Это папка с файлом `main.py`
Все дальшейшие действия совершаются внутри неё*

### 2. Создать и активировать виртуальное окружение
```
python -m venv venv
source venv/bin/activate
```
*venv - путь к папке виртуального окружения
можно оставить просто venv, и тогда папка создастся в текущей*

### 3. Установить зависимости
```
pip install -r requirements.txt
```

### 4. Добавить переменные окружения
```
source .env
```

* IS_LOCAL: флаг, показывающий запускается ли проект локально(для разработки, не на сервере)
* LOCAL_ROOT_PATH: префикс проксирования, если проект запускается локально
* SERVER_ROOT_PATH: префикс проксирования, если проект запускается на сервере

* REDIS_HOST: хост, на котором находится Редис
* REDIS_PORT: порт Редиса
* REDIS_PASSWORD: пароль к Редису
* REDIS_DB_NUMBER: номер БД в Редисе. Должен быть такой же, как и в сервисе каталогов

* DB_NAME: имя БД
* DB_USER: имя пользователя БД
* DB_PASSWORD: пароль пользователя
* DB_HOST: хост БД
* DB_PORT: порт БД

* ACCOUNT_SERVICE_ADDRESS: адрес сервиса аккаунтов
* GET_USER_BY_BUSINESS_ID_ENDPOINT: эндпоинт для получения данных юзера по id его бизнес-профиля
* CHATS_SERVICE_ADDRESS: адрес сервиса чатов
* SEND_CHAT_MESSAGE_ENDPOINT: эндпоинт для отправки сообщения в чат
* CATALOGS_SERVICE_ADDRESS: адрес сервиса каталогов
* UPDATE_STOCK_ENDPOINT: эндпоинт для обновления стока продуктов

* ORDERS_TELEGRAM_BOT_TOKEN: токен для управления Телеграм ботом
* ORDERS_TELEGRAM_CHAT_ID: id чата, в который отправляются данные заказа

### 5. Добавить RedisJSON модуль для Redis

1. Скачать или сбилдить модуль
2. Добавить в redis.conf `loadmodule /путь/к/модулю/rejson.so`
3. Перезапустить Redis сервер

* [Ссылка на скачивание готово модуля](https://redislabs.com/redis-enterprise-software/download-center/modules/?_ga=2.219621337.1506766300.1613398605-576581971.1613398605)
* [Ссылка на репозиторий для билда](https://github.com/RedisJSON/RedisJSON.git)
* [Документация модуля](https://oss.redislabs.com/redisjson/)

### 6. Накатить миграции
```
aerich upgrade
```

### 7. Стартовать Uvicorn(Python ASGI Server) из папки проекта
```
uvicorn main:app --host <host> --port <port>
```
