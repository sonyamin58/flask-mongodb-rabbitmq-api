# Flask Mongo RabbitMq (Ewallet)

### Getting started

```bash
git clone https://github.com/sonyamin58/flask-mongodb-rabbitmq-api

cd flask-mongodb-rabbitmq-api
```

### Run Application

running application three methods manually, using docker or via Makefile

- Manually :

```bash
# Copy enviroment variables from .env.sample to .env
cp .env.sample .env

# Install package
pip3 install -r requirements.txt

# Run Application
python3 app.py

# Or with gunicorn
gunicorn -w 4 --bind 0.0.0.0:5000 app:app
```

- Via Docker :

```bash
# Copy enviroment variables from .env.sample to .env
cp .env.sample .env

# Build application
docker-compose -f docker-compose-dev.yml up --build --remove-orphans --force-recreate

# Stop aplication
CTRL+C
# then
docker-compose -f docker-compose-dev.yml down

# After build you can run command with this
docker-compose -f docker-compose-dev.yml up

# Or you can hide log with command
docker-compose -f docker-compose-dev.yml up -d
```

- Via Make :

```bash
# Copy enviroment variables from .env.sample to .env
cp .env.sample .env

# Build application
make docker-build

# Stop aplication
CTRL+C
# then
make docker-down

# start application and others service
make docker-start

# stop application and others service
make docker-stop
```

## Run Listener

running application three methods manually, using docker or via Makefile

- Manually :

```bash
python3 transfer_listener.py
```

- Via Docker :

```bash
docker exec -it flask_test python3 transfer_listener.py
```

- Via Make :

```bash
make listener
#or
make docker-listener

```

### Logical Test

Manual

```bash
python3 logical-test/soal-1.py
python3 logical-test/soal-2.py
python3 logical-test/soal-3.py
python3 logical-test/soal-4.py
```

Makefile

```bash
make soal-1
make soal-2
make soal-3
make soal-4
```
