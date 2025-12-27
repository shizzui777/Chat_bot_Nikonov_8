# Легкий образ Python
FROM python:3.11-slim

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Обновляем pip и ставим зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем легкую модель spaCy
RUN python -m spacy download xx_ent_wiki_sm --quiet

# Открываем порт (Render подставит свой)
EXPOSE 10000

# Запуск через Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]






