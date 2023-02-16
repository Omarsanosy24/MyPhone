FROM python:3.11-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock scripts/build.sh ./

RUN sh build.sh
RUN poetry add gunicorn
COPY . .
<<<<<<< HEAD

CMD ["poetry", "run", "poe", "start"]
=======
CMD ['poetry run gunicorn --bind 0.0.0.0:8000 myphone.wsgi']
>>>>>>> beab26469cc01d8529975f452627b27e33e22f35
