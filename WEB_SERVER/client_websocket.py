# from django.test import TestCase
import json
from sys import version
import json

# Create your tests here.
import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print("ERRor")
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("OPEN new Websocket")


#     ws.send('''{
#   "Message":"Hello"
# }''')
# ws.send('{ "type": "ChatConsumer.SetData"}')
# def run(*args):
#     for i in range(3):
#         time.sleep(1)
#         ws.send("Hello %d" % i)
#     time.sleep(1)
#     ws.close()
#     print("thread terminating...")
# thread.start_new_thread(run, ())
token = "910244e5-3f00-4957-a417-924b2d1baf84"
version = "0.03"
extra_header = {"token": token, "version": version}
header = {"extra-header": json.dumps(extra_header)}
print(header)

websocket.enableTrace(True)
# address = input('address: ')
# address = "localhost:8000"
address = "0362419b1a1080.localhost.run"
ws = websocket.WebSocketApp(
    f"ws://{address}",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    header=header,
)

# ws.send('Hello world')
ws.on_open = on_open
ws.run_forever()
