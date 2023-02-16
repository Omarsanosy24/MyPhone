poetry run python3 manage.py createusers
poetry run python3 manage.py loaddevices base
poetry run python3 manage.py dumpdata -o resources/fixtures/full.json --indent=2
