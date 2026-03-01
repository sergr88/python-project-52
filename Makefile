PORT ?= 8000

install:
	uv sync

collectstatic:
	#uv run manage.py collectstatic --noinput
 
makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

makemessages:
	uv run manage.py makemessages -l ru

compilemessages:
	uv run manage.py compilemessages

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

format:
	uv run ruff format

#db-up:
#	docker compose -f __env__/dev/compose.yaml up --build -d
#
#db-down:
#	docker compose -f __env__/dev/compose.yaml down
#
#db-logs:
#	docker compose -f __env__/dev/compose.yaml logs -f
#

test:
	uv run manage.py test

shell:
	uv run manage.py shell

dev:
	uv run manage.py runserver 127.0.0.1:$(PORT)

build:
	make install && make collectstatic && make migrate

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
