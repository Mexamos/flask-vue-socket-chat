import random
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
app.config['SECRET_KEY'] = 'secret key'
sio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

clients = []
clients_unique_colors = []

def generate_hex_color():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_color ='#'+ hex_number[2:]
    return hex_color

@sio.on('connect')
def connect():
    color = generate_hex_color()
    while color in clients_unique_colors:
        color = generate_hex_color()
    clients_unique_colors.append(color)

    client = {
      'id': request.sid,
      'color': color
    }

    clients.append(client)
    sio.emit('update_user_list', clients)


@sio.on('message')
def message(data):
    sio.emit('chat_message', data)


@sio.on('disconnect')
def disconnect():
    global clients
    clients = list(filter(lambda client: str(client['id']) != str(request.sid), clients))
    sio.emit('update_user_list', clients)


@sio.on('update_user')
def message(user):
    global clients
    clients = list(map(lambda client: user if client['id'] == user['id'] else client, clients))
    sio.emit('update_user_list', clients)


if __name__ == '__main__':
    app.debug = True
    sio.run(app)
