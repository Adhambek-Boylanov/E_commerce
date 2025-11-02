# Python bazasi
FROM python:3.12-slim

# Python konfiguratsiya
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ishchi katalog
WORKDIR /app

# Zarur kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password appuser

COPY . .

# Statik fayllarni yig‘ish
RUN python manage.py collectstatic --noinput

# Foydalanuvchini almashtirish (root emas)
USER appuser

# Django’ni Gunicorn orqali ishga tushirish
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
