from flask import Flask, render_template, send_from_directory 
from flask_socketio import SocketIO, send
from flask_socketio import join_room, leave_room
from datetime import time
from uuid import uuid4

import unittest

from battleship import Ship
from battleship import BattleshipGame


debug = True
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'GreatBigSecret'
socketio = SocketIO(app)
message_history = []
games = {}
players = {}
player_numbers = {}
player_ships = {}


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
  for msg in message_history:
    send(msg)
  send({
    "type":"chat", 
    "name":"Server", 
    "message":"New Player Connected"}, 
    broadcast=True)

@socketio.on('message')
def handleMessage(msg):
  if check_valid_chat(msg):
    handle_chat(msg)
  elif (msg["type"] == "place-ship"):
    handle_place_ship(msg)
  elif (msg["type"] == "hand-shake"):
    handle_hand_shake(msg)
  elif (msg["type"] == "fire"):
    handle_fire(msg)
  print(msg)

def check_valid_chat(msg):
  if "name" in msg and "message" in msg and "type" in msg:
    return ( msg["type"] == "chat" and "message" in msg 
      and msg["message"] != "" and len(msg["message"]) < 120
      and len(msg["name"]) <= 12 and len(msg["name"]) > 0 ) 

def handle_chat(msg):
  msg["message"] = msg["message"].replace("<", " I'm am Haxxoer! ")
  msg["name"] = msg["name"].replace("<", " Great Haxxoer! ")
  send(msg, broadcast=True)
  message_history.append({
    "name":msg["name"], 
    "message":msg["message"], 
    "type":"chat"})

def handle_place_ship(msg):
  if msg["ship"] in player_ships[msg["id"]]:
    send_alert(msg["ship"].title()+" already placed.")
    return
  else:
    player_ships[msg["id"]].append(msg["ship"])
  try:
    player_id = msg["id"]
    player_no = player_numbers[player_id]
    game = games[players[player_id]]
    ship = Ship(
      int(msg["location"]), 
      type=msg["ship"], 
      direction=msg["direction"])
    game.addShip(player_no, ship)
  except ValueError as e:
    send_alert(str(e))
  else:
    alert_ship_placement(msg)
    send(msg)
    if game.ready():
      send_alert("All ships placed... Player 1 ready to fire!", 
        players[player_id])
      send({"type":"game-begun"},room=players[player_id])

def handle_hand_shake(msg):
    players[msg["id"]] = get_a_game(msg["id"])
    player_ships[msg["id"]] = []
    send({
      "type":"room-join",
      "number":player_numbers[msg["id"]],
      "room":players[msg["id"]]})

def get_a_game(player_id):
  if len(players)%2 == 0:
    game = str(uuid4().hex)
    games[game] = BattleshipGame()
    player_numbers[player_id] = 1
    join_room(game)
    send_alert("New Game started waiting on player two.")
    return game
  else:
    seen_games = {}
    for (player,game) in players.items():
      if game in seen_games:
        seen_games[game]= seen_games[game] + 1
      else:
        seen_games[game]=1
    for (game, count) in seen_games.items():
      if count == 1:
        player_numbers[player_id] = 2
        join_room(game)
        send_alert("Game ready, place ships!", game)
        return game

def send_shot(rm, player_no, locations, hit, shot):
  send({"type":"fire", "shot":shot,"player_no":player_no,
    "locations":locations, "hit":hit}, room=rm)

def handle_fire(msg):
  try:
    player_id = msg["id"]
    player_no = player_numbers[player_id]
    game = games[players[player_id]]
    locations = [int(msg["location"])]
    hit = False
    if player_no == game.current_player:
      if msg["shot"] == "normal":
        hit = game.fire([locations[0]])
      send_shot(players[player_id], player_no, 
        locations, hit, msg["shot"])
      if game.checkGameOver(3-player_no):
        send_alert("GAME OVER, PLAYER " + str(player_no) + " WINS!!",
          players[player_id])
        send({"type":"game-over"},players[player_id])
    else:
      send_alert("Wait your turn!")
  except ValueError as e:
    send_alert(str(e))

def alert_ship_placement(msg, rm=None):
  x = (int(msg["location"]) % 10) + 1
  y = (int(msg["location"]) / 10) + 1
  send_alert(
    msg["ship"].title() + " placed. " 
    + msg["direction"].title() + ", at (" 
    + str(x) + "," + str(y) + ").", rm)

def send_alert(message, rm=None):
  send({"type":"alert", "message":message}, room=rm)

if __name__ == '__main__':
  if debug == True:
    socketio.run(app, host='0.0.0.0', port=8080, debug = True)
  else:    
    socketio.run(app, host='0.0.0.0', port=80)

