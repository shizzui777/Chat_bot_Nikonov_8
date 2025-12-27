# Базовый образ Python
FROM python:3.11-slim

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости для spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем модель spaCy (русскую)
RUN python -m spacy download ru_core_news_sm --quiet

# Открываем порт (Render подставит свой)
EXPOSE 10000

# Запуск через Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]




