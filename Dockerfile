FROM python:3.11-alpine
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .
CMD ["python manage.py runserver 0.0.0.0:8000"]
