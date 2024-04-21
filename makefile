.PHONY: up down migrate_up make_migrations migrate

up:
	docker compose up -d --build

down:
	docker compose down

migrate_up:
	docker compose exec api python manage.py migrate

make_migrations:
	docker compose exec api python manage.py makemigrations

migrate: make_migrations migrate_up

remove_db:
	cd backend && rm -rf ./db.sqlite3

build: down remove_db up migrate
