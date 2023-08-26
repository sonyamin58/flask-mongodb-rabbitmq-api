#ganti compose file sesuai environment
compose-file = docker-compose-dev.yml

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
image-pull:
	docker-compose -f $(compose-file) pull
