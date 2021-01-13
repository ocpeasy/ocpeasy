POETRY_BIN:=~/.poetry/bin/poetry

install:
	$(POETRY_BIN) config -vvv virtualenvs.create false \
	&& $(POETRY_BIN) install

scaffold:
	$(POETRY_BIN) run python3 cli.py scaffold

test:
	$(POETRY_BIN) run testify __tests__