install:
	poetry config -vvv virtualenvs.create false \
	&& poetry install

start:
	poetry run python3 cli.py say_hello