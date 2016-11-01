from flask import Flask
from json import dumps
from flask import render_template
from flask_socketio import SocketIO, send
from threading import Thread
from time import sleep
import random
""" comment """
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_is_for_losers'
app.config['FLASK_DEBUG'] = '1'
socketio = SocketIO(app)

w = 20
h = 10


class Character:
    x = 1
    y = 1
    name = "rover"
    color = "#%06x" % random.randint(0, 0xFFFFFF)

    def __init__(self):
        self.char_type = "npc"
        self.speed = 1
        # self.name = "npcecko2"
        self.color = "#%06x" % random.randint(0, 0xFFFFFF)


class Quadrant:
    color = "009900"

    def __init__(self, x, y):
        self.color = "70554f"
        self.x = x
        self.y = y
        a = random.randint(0, 4)
        self.stuff = []
        self.names = "nothing"
        if a == 0:
            self.name = "extra-terra incognita"
            self.type = "plain"
            self.water = 0.4
            self.wind = 0.2
            self.soil = 0.3
            self.color = "70554f"
        elif a == 1:
            self.name = "extra-terra incognita"
            self.type = "mountain"
            self.water = 0.1
            self.wind = 0.2
            self.soil = 0.1
            self.color = "3a2a26"
        elif a == 2:
            self.name = "extra-terra incognita"
            self.type = "lake bed"
            self.water = 0.5
            self.wind = 0.1
            self.soil = 0.5
            self.color = "724c44"
        elif a == 3:
            self.name = "extra-terra incognita"
            self.type = "glacier"
            self.water = 0.9
            self.wind = 0.4
            self.soil = 0.0
            self.color = "918684"
        else:
            self.name = "extra-terra incognita"
            self.type = "glacier"
            self.water = 0.9
            self.wind = 0.4
            self.soil = 0.0
            self.color = "918684"

# generate default map
quadrant = [[Quadrant(x, y) for y in range(0, h + 2)] for x in range(0, w + 2)]

# create npc's
npc = [Character for i in range(0, 6)]

# place npc's
quadrant[2][3].stuff.append(npc[0])
quadrant[2][4].stuff.append(npc[1])
quadrant[2][5].stuff.append(npc[2])
quadrant[2][6].stuff.append(npc[3])
quadrant[2][7].stuff.append(npc[4])
quadrant[2][8].stuff.append(npc[5])

# summarize stuff in quadrants
for i in range(0, h+1):
    for j in range(0, w+1):
        s = ""
        k = quadrant[j][i].stuff.__len__()
        if k > 0:
            for k in range(0, k):
                s = s + quadrant[j][i].stuff[k].name + ", "
            quadrant[j][i].names = s
        else:
            quadrant[j][i].names = "empty"

# quadrants = [["#" + str(random.randint(111111, 999999)) for x in range(h + 2)] for y in range(w + 2)]
# quadrants = [[next(random_terrain()) for x in range(h + 2)] for y in range(w + 2)]
# random color: "#%06x" % random.randint(0, 0xFFFFFF)


class Player:
    def __init__(self, name):
        self.name = name
        self.curs_x = 10
        self.curs_y = 6
        print(name)

niekto = Player("MenoHraca")


def loop():
    count = 0
    while True:
        if count == 0:
            a = dumps([["#" + quadrant[x][y].color for y in range(h + 2)] for x in range(w + 2)])
            socketio.emit('data', str(a))

        # kurzor
        c = quadrant[niekto.curs_x][niekto.curs_y]

        # text pod mapou
        b = "x,y:" + str(c.x) + "," + str(c.y) + " Soil:" + str(c.soil) + " Type:" + str(c.type)
        b = b + " Wind:" + str(c.wind) + " Water:" + str(c.water) + " Stuff:" + c.names
        socketio.emit('text', str(b))

        sleep(1/10)
        count += 1
        if count >= 9:
            count = 0


@app.route('/')
def ghh():
    return render_template('index.html')


@socketio.on('message')
def handlemessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@socketio.on('cursor')
def handle_cursor(cur_x, cur_y):
    niekto.curs_x = int(cur_x)
    niekto.curs_y = int(cur_y)

thread = Thread(target=loop)
print("Starting Thread")
thread.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='2323')


