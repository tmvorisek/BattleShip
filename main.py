from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send
from datetime import time

import unittest

from battleship import Ship
from battleship import BattleshipGame


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'GreatBigSecret'
socketio = SocketIO(app)
message_history = []

@app.route('/css/<path:path>', methods=['GET'])
def send_css(path):
  return send_from_directory('css',path)

@app.route('/js/<path:path>', methods=['GET'])
def send_js(path):
  return send_from_directory('js',path)

@app.route('/')
def index():
  return render_template("./index.html")

@socketio.on('connect')
def handleConnection():
  for msg in message_history:
    send(msg)

@socketio.on('message')
def handleMessage(msg):
  global message_history
  msg["message"] = msg["message"].replace("<", " I'm am Haxxoer! ")
  msg["name"] = msg["name"].replace("<", " I'm am Haxxoer! ")
  
  if( msg["type"] == "chat" 
    and msg["message"] != ""
    and len(msg["message"]) < 240):
      send(msg, broadcast=True)
      message_history.append({"name":msg["name"], "message":msg["message"], "type":"chat"})
  print(msg)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug = True)