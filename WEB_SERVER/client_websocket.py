import json
from sys import version
import json
import base64
from threading import Thread
from time import sleep

# Create your tests here.
import websocket


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print("ERRor")
    print(error)


def on_close(ws, *args):
    print("### closed ###")


def on_open(ws):
    print("OPEN new Websocket")


data = '{"token" :"624ae81e-9017-42b3-a842-d636361d4e0a", "version": "0.01"}'.encode(
    "ascii"
)
data = base64.b64encode(data)
data = data.decode("ascii")

header = {"extra-header": data}
print(header)

websocket.enableTrace(True)
address = "127.0.0.1:8000"
# address = "157.90.9.193:8080"
ws_clients = []


def new_client():
    ws = websocket.WebSocketApp(
        f"ws://{address}",
        # on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=header,
    )
    # ws.send('Hello world')
    # ws.on_open = on_open
    ws.run_forever()


for i in range(1, 2):
    print(f"Clinet : {i}")
    Thread(target=new_client).start()
    sleep(0.2)
