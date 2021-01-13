POETRY_BIN:=~/.poetry/bin/poetry

install:
	$(POETRY_BIN) config -vvv virtualenvs.create false \
	&& $(POETRY_BIN) install

scaffold:
	$(POETRY_BIN) run python3 src/cli.py scaffold

lint:
	$(POETRY_BIN) run flake8 --select E123,W503 src/* -v

test:
	$(POETRY_BIN) run pytest __tests__