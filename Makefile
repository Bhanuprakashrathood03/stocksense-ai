.PHONY: up down build logs clean

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

clean:
	docker compose down -v

restart:
	docker compose restart

ps:
	docker compose ps

db-shell:
	docker compose exec db psql -U user -d stocksense

redis-shell:
	docker compose exec redis redis-cli

api-logs:
	docker compose logs -f api

web-logs:
	docker compose logs -f web
