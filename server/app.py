import socketio
import random

from gevent import pywsgi

sio = socketio.Server(cors_allowed_origins="*", async_mode='gevent_uwsgi')
app = socketio.WSGIApp(sio)

clients = []
clients_unique_colors = []

def generate_hex_color():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_color ='#'+ hex_number[2:]
    return hex_color

@sio.on('connect')
def connect(sid, environ):
    color = generate_hex_color()
    while color in clients_unique_colors:
        color = generate_hex_color()
    clients_unique_colors.append(color)

    client = {
      'id': sid,
      'color': color
    }

    clients.append(client)
    sio.emit('update_user_list', clients)


@sio.on('message')
def message(sid, data):
    sio.emit('chat_message', data)


@sio.on('disconnect')
def disconnect(sid):
    global clients
    clients = list(filter(lambda client: str(client['id']) != str(sid), clients))
    sio.emit('update_user_list', clients)


@sio.on('update_user')
def update_user(sid, user):
    global clients
    clients = list(map(lambda client: user if client['id'] == user['id'] else client, clients))
    sio.emit('update_user_list', clients)


if __name__ == '__main__':
    pywsgi.WSGIServer(('', 5000), app).serve_forever()
