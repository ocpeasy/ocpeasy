POETRY_BIN:=~/.poetry/bin/poetry
# https://lintlyci.github.io/Flake8Rules
FLAKE8_RULES:= E123,W503
SOURCE_PATH:=ocpeasy
COVERAGE_BADGE_PATH:=badges/coverage.svg

install:
	$(POETRY_BIN) config -vvv virtualenvs.create false \
	&& $(POETRY_BIN) install

config_precommit:
	$(POETRY_BIN) run pre-commit install

scaffold:
	$(POETRY_BIN) run python3 $(SOURCE_PATH) scaffold

buildStageDev:
	export POETRY_DEV_PATH=/Users/home/david/ocpeasy-test && $(POETRY_BIN) run python3 $(SOURCE_PATH) buildStage --stageId=dev

buildStageProd:
	$(POETRY_BIN) run python3 $(SOURCE_PATH) buildStage --stageId=prod

lint:
	$(POETRY_BIN) run flake8 --select $(FLAKE8_RULES) $(SOURCE_PATH)/* -v

format:
	$(POETRY_BIN) run black $(SOURCE_PATH)

tree:
	$(POETRY_BIN) show --tree 

test:
	$(POETRY_BIN) run pytest --cov=$(SOURCE_PATH)

test_html_report:
	$(POETRY_BIN) run pytest --cov=$(SOURCE_PATH) --cov-report html

generate_coverage_badge:
	rm -rf $(COVERAGE_BADGE_PATH) && $(POETRY_BIN) run coverage-badge -o $(COVERAGE_BADGE_PATH)

build:
	$(POETRY_BIN) build

publish:
	$(POETRY_BIN) publish