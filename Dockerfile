FROM python:3.11-slim

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости (нужны для spaCy)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Обновляем pip и ставим зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Скачиваем модель spaCy
RUN python -m spacy download ru_core_news_sm

# Копируем весь проект
COPY . .

# Открываем порт (Render подставит свой)
EXPOSE 10000

# Запуск через gunicorn
CMD gunicorn app:app --bind 0.0.0.0:$PORT


