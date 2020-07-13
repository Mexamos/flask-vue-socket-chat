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
sio = SocketIO(app, cors_allowed_origins="*")

clients_ids = []
clients_unique_colors = []

def generate_hex_color():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_color ='#'+ hex_number[2:]
    return hex_color

@sio.on('connect')
def connect():
    print('connected request.sid', request.sid)

    color = generate_hex_color()
    while color in clients_unique_colors:
        color = generate_hex_color()
    clients_unique_colors.append(color)

    client = {
      'id': request.sid,
      'color': color
    }

    clients_ids.append(client)
    sio.emit('update_user_list', clients_ids)
    print('clients_ids', clients_ids)


@sio.on('message')
def message(data):
    print('data', data)
    sio.emit('chat_message', data)


@sio.on('disconnect')
def disconnect():
    print('disconnect', request.sid)
    global clients_ids
    clients_ids = list(filter(lambda client: client['id'] is not request.sid, clients_ids))
    sio.emit('update_user_list', clients_ids)


if __name__ == '__main__':
    app.debug = True
    sio.run(app)
