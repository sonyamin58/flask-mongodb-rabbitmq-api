import json
from uuid import uuid4

from src.config.rabbitmq import rabbitmq
from src.config.mongo import db

from src.modules.v1.transaction.transaction_service import TransactionService
from src.modules.v1.auth.auth_service import AuthService


def consume(queue_name):
    connection = rabbitmq.connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        data = json.loads(body)

        error = True
        # transfer_received
        if data["job"] == "transfer_received":
            authService = AuthService(db)
            trxService = TransactionService(db)

            target_user_id = str(data["target_user_id"])
            me = authService.who(target_user_id)
            print('me', me)
            if me != False:
                amount = int(data["amount"])
                balance_before = int(me["balance"])
                balance_after = int(balance_before) + int(amount)
                params = {
                    "transfer_id": str(uuid4()),
                    "user_id": str(me["user_id"]),
                    "amount": amount,
                    "remarks": str("Transfer Masuk"),
                    "balance_before": balance_before,
                    "balance_after": balance_after,
                    "reference_id": str(data["transfer_id"])
                }
                print('params', params)
                credit = trxService.credit(params)
                print('credit', credit)
                if credit != False:
                    update_success = trxService.update_status(
                        {
                            "transfer_id": str(data["transfer_id"])
                        },
                        "SUCCESS"
                    )
                    print('update_success', update_success)
                    if update_success != False:
                        print("Transfer success")
                        error = False

            # kalau ada error gagal TF, balikin uang nya
            if error == True:
                update_failed = trxService.update_status(
                    {
                        "transfer_id": str(data["transfer_id"])
                    },
                    "FAILED"
                )
                print('update_failed', update_failed)
                if update_failed != False:
                    print("Transfer gagal")
                    error = True

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print(' [*] Consume queue_name', queue_name)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
