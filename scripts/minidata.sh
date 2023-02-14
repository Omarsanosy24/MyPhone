poetry run python3 manage.py createusers
poetry run python3 manage.py loaddevices csv --minimal
poetry run python3 manage.py dumpdata -o resources/fixtures/mini.json --indent=2
