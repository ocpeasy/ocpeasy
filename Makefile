POETRY_BIN:=~/.poetry/bin/poetry
FLAKE8_RULES:= E123,W503

install:
	$(POETRY_BIN) config -vvv virtualenvs.create false \
	&& $(POETRY_BIN) install

scaffold:
	$(POETRY_BIN) run python3 src/cli.py scaffold

lint:
	$(POETRY_BIN) run flake8 --select E123,W503 src/* -v

format:
	$(POETRY_BIN) run black src

test:
	$(POETRY_BIN) run pytest __tests__