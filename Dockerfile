FROM python:3.11-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock scripts/build.sh ./

RUN sh build.sh
RUN poetry add gunicorn
COPY . .

CMD ["poetry", "run", "poe", "start"]
