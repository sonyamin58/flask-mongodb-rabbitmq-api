import os
from dotenv import load_dotenv
import pika
import json


class RabbitMQ:

    def connection(self):
        load_dotenv()

        RABBITMQ_USER = os.getenv('RABBITMQ_USER')
        RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
        RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
        RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
        RABBITMQ_URI = os.getenv('RABBITMQ_URI')

        # set amqp credentials
        credentials = pika.PlainCredentials(
            str(RABBITMQ_USER), str(RABBITMQ_PASS))
        # set amqp connection parameters
        parameters = pika.ConnectionParameters(
            host=str(RABBITMQ_HOST),
            port=str(RABBITMQ_PORT),
            credentials=credentials
        )

        # try to establish connection and check its status
        try:
            connection = pika.BlockingConnection(parameters)
            if connection.is_open:
                print(" [*] RabbitMQ OK")
                return connection

        except Exception as err:
            print('RabbitMQ Error Connection:', err)
            exit(1)

        print('RabbitMQ Not OK')

    def publish(self, queue_name, body_msg):
        print("send publish queue name:", queue_name)
        print("with message:", body_msg)

        connection = self.connection()
        if (type(body_msg) == dict):
            body_msg = json.dumps(body_msg)

        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body_msg
        )
        print(" [x] Sent", body_msg)
        connection.close()


rabbitmq = RabbitMQ()
