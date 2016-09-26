from flask import Flask
from json import dumps
from flask import render_template
from flask_socketio import SocketIO, send
from threading import Thread
from time import sleep
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_is_for_losers'
app.config['FLASK_DEBUG'] = '1'
socketio = SocketIO(app)


class Player:
    def __init__(self, name):
        self.name = name
        print(name)
        self.thread = Thread(target=self.loop)
        print("Starting Thread")
        self.thread.start()

    def loop(self):
        i = 0
        w = 20
        h = 10
        quadrants = [["#" + str(random.randint(100000, 999999)) for x in range(h + 2)] for y in range(w + 2)]
        while True:
            quadrants[random.randint(0, w)-1][random.randint(0, h)-1] = "#%06x" % random.randint(0, 0xFFFFFF)
            a = dumps(quadrants)
            socketio.emit('data', str(a))
            sleep(2)
            i += 2
            text = "Hráč " + self.name + " je tu už " + str(i) + " sekúnd."
            print(text)
            socketio.emit('message', text)

niekto = Player("Dorf")


print("routujeme")


@app.route('/')
def ghh():
    return render_template('index.html')


@socketio.on('message')
def handlemessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='2323')
