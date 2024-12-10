FROM python:3.12.5-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы requirements.txt и прото-файлы в контейнер
COPY requirements.txt .
COPY proto/ ./proto/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Генерируем файлы gRPC из .proto в папку proto
RUN python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto ./proto/dron.proto

# Копируем исходный код приложения
COPY app/ ./app/

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH="/app:/app/proto"

# Устанавливаем порт для gRPC-сервера
EXPOSE 50051

# Команда для запуска приложения
CMD ["python", "app/main.py"]
