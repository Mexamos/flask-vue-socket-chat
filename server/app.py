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

clients_ids = set()

@sio.on('connect')
def connect():
  print('connected request.sid', request.sid)
  clients_ids.add(request.sid)


@sio.on('message')
def message(data):
  print('data', data)
  sio.emit('chat_message', data)


@sio.on('disconnect')
def disconnect():
  print('disconnect', request.sid)
  clients_ids.remove(request.sid)


if __name__ == '__main__':
  app.debug = True
  sio.run(app)
