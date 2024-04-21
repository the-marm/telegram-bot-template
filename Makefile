
project_dir := .
bot_dir := ./telegram_bot
locales_dir := $(bot_dir)/locales/

.PHONY: lint
lint:
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

.PHONY: reformat
reformat:
	@poetry run ruff check $(project_dir) --fix

.PHONY: i18n
i18n:
	poetry run i18n multiple-extract \
		--input-paths $(bot_dir) \
		--output-dir $(locales_dir) \
		-k i18n -k L --locales $(locale) \
		-cm

.PHONY: migration
migration:
	poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_next_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate:
	poetry run alembic upgrade head
