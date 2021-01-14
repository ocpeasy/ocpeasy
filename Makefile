POETRY_BIN:=~/.poetry/bin/poetry
FLAKE8_RULES:= E123,W503
SOURCE_PATH:=src

install:
	$(POETRY_BIN) config -vvv virtualenvs.create false \
	&& $(POETRY_BIN) install

scaffold:
	$(POETRY_BIN) run python3 cli.py scaffold

lint:
	$(POETRY_BIN) run flake8 --select $(FLAKE8_RULES) $(SOURCE_PATH)/* -v

format:
	$(POETRY_BIN) run black $(SOURCE_PATH)

test:
	$(POETRY_BIN) run pytest $(SOURCE_PATH)