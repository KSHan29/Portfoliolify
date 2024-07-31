FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    poppler-utils \
    curl \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT

# CMD python manage.py runserver 0.0.0.0:$PORT