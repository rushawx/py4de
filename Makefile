SHELL := /bin/bash
PY = .venv/bin/python

build_all:
	docker-compose --env-file .env.example -f ./docker-compose-db.yml up --build -d \
	&& docker-compose --env-file .env.example -f ./docker-compose-af.yml up --build -d

destroy_all:
	docker-compose --env-file .env.example -f ./docker-compose-af.yml down --volumes \
	&& docker-compose --env-file .env.example -f ./docker-compose-db.yml down --volumes \
