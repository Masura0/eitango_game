import pyxel
import random

class Ball:
    def __init__(self):
        self.x = random.randint(0, 199)
        self.y = 0
        self.vx = 0.866
        self.vy = 0.5

def generate_ball():
    return Ball()

class Pad:
    def __init__(self):
        self.x = 100

    def update(self):
        self.x = pyxel.mouse_x

pyxel.init(200, 200)

balls = [generate_ball() for _ in range(3)]
pad = Pad()
speed = 1
score = 0

def update():
    global speed, score

    for ball in balls:
        ball.x += ball.vx * speed
        ball.y += ball.vy * speed

        if ball.x <= 0 or ball.x >= 200:
            ball.vx *= -1

        if ball.x + 10 >= pad.x - 20 and ball.x - 10 <= pad.x + 20 and ball.y + 10 >= 195:
            score += 1
            angle = random.uniform(30, 150)
            ball.vx = pyxel.cos(angle)
            ball.vy = pyxel.sin(angle)
            ball.x = random.randint(0, 199)
            ball.y = 0

        if ball.y >= 200:
            angle = random.uniform(30, 150)
            ball.vx = pyxel.cos(angle)
            ball.vy = pyxel.sin(angle)
            ball.x = random.randint(0, 199)
            ball.y = 0

    pad.update()

def draw():
    pyxel.cls(7)
    
    for ball in balls:
        pyxel.circ(ball.x, ball.y, 10, 6)

    pyxel.rect(pad.x - 20, 195, 40, 5, 14)
    pyxel.text(100, 100, str(score), 0)

pyxel.run(update, draw)
