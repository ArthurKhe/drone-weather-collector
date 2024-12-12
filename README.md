# drone-weather-collector

Приложения для сбора данных о погоде с дронов.

# Запуск сервера

1. Создать файл с переменными окружения ( env.example)
2. Запустить сервер командой `docker compose up -d --build`

Сервер состоит из 3х микросервисов:
1. Сервис аутентификации:
    - Swagger доступен по адресу : `http://0.0.0.0:8000/docs`
2. Административный сервис: 
   - Swagger доступен по адресу : `http://0.0.0.0:8001/docs`
3. Сервис валидации данных
   - валидирует данные с дрона по температуре, влажности и существовании дрона
   - добавляет данные в очередь
   - отправляет валидированные данные для сохранение в базу

# Запуск клиента
1. Устанавливаем зависимости `pip install -r requirements.txt`
2. Создаем конфигурационный файл config.env
3. Задаем необходимые параметры
4. Запускаем клиент: `python  app/main.py`

DRON_ID - id дрона (предварительно необходимо создать дрон)

DRON_NAME - Наименование учетной записи для дрона

DRON_PASS - Пароль для авторизации дрона

PERIOD_SEND_DATA - период отправки данных с дрона

GRPC_SERVER_ADDRESS - адрес соединения gRPC

AUTH_SERVER_URL=адрес сервиса аутентификации

Перед запуском клиента необходимо:
- зарегистрировать учетку дрона
- создать дрон