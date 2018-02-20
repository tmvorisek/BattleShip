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
  if( msg["type"] == "chat" ):
    msg["message"] = msg["message"].replace("<", " I'm am Haxxoer! ")
    send(msg, broadcast=True)
  print(msg)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug = True)