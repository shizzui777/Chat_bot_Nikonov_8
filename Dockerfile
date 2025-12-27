# Используем лёгкий образ Python
FROM python:3.11-slim

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт (Render подставит свой через $PORT)
EXPOSE 10000

# Запуск через Gunicorn с автоматической подстановкой порта
CMD gunicorn app:app --bind 0.0.0.0:$PORT












