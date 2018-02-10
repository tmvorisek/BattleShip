from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send

import unittest


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'GreatBigSecret'
socketio = SocketIO(app)

@app.route('/css/<path:path>', methods=['GET'])
def send_css(path):
  return send_from_directory('css',path)

@app.route('/js/<path:path>', methods=['GET'])
def send_js(path):
  return send_from_directory('js',path)

@app.route('/')
def index():
  return render_template("./index.html")


@socketio.on('message')
def handleMessage(msg):
  # print(msg)
  if( msg.type == "chat" ):
    send(msg, broadcast=True)

if __name__ == '__main__':
  socketio.run(app, debug = True)

## User Stories
Story | Todd points | Jason points | total
--- | --- | --- | ---
I, Player, want to be able play battleship with another human player | 9 | 10 | **19**
I, Player, want benefits based on what ships are in play | 8 | 10 | **18**
I, Player, want to be able to pick my ship roster | 7 | 7 | **14**
I, Player, want to be able to move ships | 6 | 8 | **14**
I, Player, want a mine sweeper shot from a ship (3x1) | 5 | 8 | **13**
I, Player, want to be able to chat over a network | 8 | 10 | **12**
I, Player, want to be able move a fast moving ship (2x1) | 5 | 7 | **12**
I, Player, want to have a mine placing ship | 7 | 5 | **12**
I, Player, want a carrier ship with a 3x1 attack (5x1) | 5 | 5 | **10**
I, Player, want a 4x1 anticipation ship that cannot move(5x1) | 5 | 5 | **10**
I, Queued player, want to be able to watch on going games | 6 | 4 | **10**
I, Player, want to be able to participate in king of the hill style tourneys| 3 | 5 | **8**
I, Player, want to be able to face an AI | 2 | 3 | **5**

