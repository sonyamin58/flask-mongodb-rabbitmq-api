#!make
include .env
export $(shell sed 's/=.*//' .env)

#ganti compose file sesuai environment
compose-file = docker-compose-dev.yml

run:
	gunicorn -w 4 --bind 0.0.0.0:$(APP_PORT) app:app
listener:
	python3 transfer_listener.py

docker-listener:
	docker exec -it flask_test python3 transfer_listener.py
docker-start:
	docker-compose -f $(compose-file) up -d
docker-start-watch:
	docker-compose -f $(compose-file) up
docker-build:
	docker-compose -f $(compose-file) up --build --remove-orphans --force-recreate -d
docker-build-watch:
	docker-compose -f $(compose-file) up --build --remove-orphans --force-recreate
docker-stop:
	docker-compose -f $(compose-file) stop
docker-down:
	docker-compose -f $(compose-file) down


soal-1:
	python3 logical-test/soal-1.py
soal-2:
	python3 logical-test/soal-2.py
soal-3:
	python3 logical-test/soal-3.py
soal-4:
	python3 logical-test/soal-4.py
