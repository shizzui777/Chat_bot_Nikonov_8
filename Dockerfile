# Легкий образ Python
FROM python:3.11-slim

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Обновляем pip и ставим зависимости + модель spaCy
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт (Render подставит свой)
EXPOSE 10000

# Запуск через Gunicorn с автоматической подстановкой $PORT
# Shell-формат CMD позволяет использовать переменные окружения
CMD gunicorn app:app --bind 0.0.0.0:$PORT










