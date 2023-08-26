from listeners.rabbimq_listener import consume
from src.utils.const import MQ, colors

print(colors.DEBUG, '[*] Init Listener', colors.END)
try:
    consume(MQ["queue"]["transfer"])
except Exception as err:
    print(colors.DEBUG, 'Error Listener:', err, colors.END)
