from flask import Flask, render_template, send_from_directory 
from flask_socketio import SocketIO, send
from flask_socketio import join_room, leave_room
from datetime import time

import unittest

from battleship import Ship
from battleship import BattleshipGame


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'GreatBigSecret'
socketio = SocketIO(app)
message_history = []
games = []

@app.route('/css/<path:path>', methods=['GET'])
def send_css(path):
  return send_from_directory('css',path)

@app.route('/js/<path:path>', methods=['GET'])
def send_js(path):
  return send_from_directory('js',path)

@app.route('/')
def index():
  return render_template("./index.html")

@socketio.on('join')
def handleJoin(data):
  print("joined " + str(data))

@socketio.on('connect')
def handleConnection():
  room = get_a_room()
  join_room(room)
  for msg in message_history:
    send(msg, room)
  send({
    "type":"chat", 
    "name":"Server", 
    "message":"New Player Connected"}, 
    broadcast=True)

@socketio.on('message')
def handleMessage(msg):
  global message_history
  
  if valid_chat(msg):
    msg["message"] = msg["message"].replace("<", " I'm am Haxxoer! ")
    msg["name"] = msg["name"].replace("<", " I'm am Haxxoer! ")
    send(msg, broadcast=True)
    message_history.append({"name":msg["name"], "message":msg["message"], "type":"chat"})
  elif (msg["type"] == "place-ship"):
    try:
      pass
    except ValueError:
      pass
    else:
      alert_ship_placement(msg)
      send(msg)

  print(msg)

def valid_chat(msg):
  if "name" in msg and "message" in msg and "type" in msg:
    return ( 
      msg["type"] == "chat" 
      and "message" in msg 
      and msg["message"] != ""
      and len(msg["message"]) < 120
      and len(msg["name"]) <= 12
      and len(msg["name"]) > 0 ) 

def get_a_room():
  return "room"

def alert_ship_placement(msg):
  x = (int(msg["location"]) % 10) + 1
  y = (int(msg["location"]) / 10) + 1
  send_alert(
    msg["ship"].title() + " placed. " 
    + msg["direction"].title() + ", at (" 
    + str(x) + "," + str(y) + ").")

def send_alert(message):
  send({"type":"alert", "message":message})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug = True)