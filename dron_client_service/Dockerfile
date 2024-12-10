FROM python:3.12.5-slim

WORKDIR /app
ENV PYTHONPATH="/app:/app/proto"
# Установить зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем основной код приложения
COPY proto/ ./proto/
COPY app/ ./app/

RUN python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto ./proto/dron.proto


# Установить рабочую директорию для приложения
WORKDIR /app

# Команда для запуска клиента
CMD ["python", "app/main.py"]
