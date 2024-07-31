FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y poppler-utils && \
    apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000

# ENTRYPOINT ["/entrypoint.sh"]