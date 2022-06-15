# -*- coding: utf-8 -*-

import tkinter
import random

#Constants
WIDTH = 700
HEIGHT = 500
BGCOLOR = 'pink'
ZERO = 0
MAIN_BALL_RADIUS = 18
MAIN_BALL_COLOR = 'blue'
BAD_COLOR = 'red'
COLORS = [BAD_COLOR, 'yellow', 'black', 'grey', 'aqua', 'fuchsia', BAD_COLOR, 'green']
INIT_DX = 1
INIT_DY = 1
DELAY = 5
NUMBER_OF_BALLS = 10


#class of all balls, dx & dy - смещение по осям
class Ball():
    def __init__(self, x, y, r, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy

    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color, outline='white' if self.color != BAD_COLOR else 'black', width=1)

    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=BGCOLOR, outline=BGCOLOR)

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a*a + b*b)**0.5 <= (self.r + ball.r)

    def move(self):

        #colliding with walls
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO):
            self.dy = -self.dy

        #colliding with balls
        for ball in balls:
            if self.is_collision(ball):
                if ball.color != BAD_COLOR:
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:
                    self.dx = self.dy = 0

        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


# count bad balls
def count_bad_balls(list_of_balls):
    res = 0
    for ball in list_of_balls:
        if ball.color == BAD_COLOR:
            res += 1
    return res


#mouse events
def mouse_click(event):
    global main_ball
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Ball(event.x, event.y, MAIN_BALL_RADIUS, MAIN_BALL_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
        else:
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3:
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy
    else:
        main_ball.hide()

#main cicle of game
def main():
    if 'main_ball' in globals():
        main_ball.move()
        if len(balls) - number_of_bad_balls == 0:
            canvas.create_text(WIDTH/2, HEIGHT/2, text='You Won!', font='Arial 20', fill=MAIN_BALL_COLOR)
            main_ball.dx = main_ball.dy = 0
        elif main_ball.dx == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text='You Lose..', font='Arial 20', fill=BAD_COLOR)

    root.after(DELAY, main)


#create a lot of balls
def create_list_of_balls(number):
    balls_list = []
    while len(balls_list) < number:
        next_ball = Ball(random.choice(range(0, WIDTH)),
                         random.choice(range(0, HEIGHT)),
                         random.choice(range(15, 35)),
                         random.choice(COLORS))
        is_collision = False
        for ball in balls_list:
            if next_ball.is_collision(ball):
                is_collision = True
                break
        if not is_collision:
            balls_list.append(next_ball)
            next_ball.draw()
    return balls_list


root = tkinter.Tk()
root.title('Шарики')
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg=BGCOLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-3>', mouse_click, '+')
if 'main_ball' in globals():
    del main_ball
balls = create_list_of_balls(NUMBER_OF_BALLS)
number_of_bad_balls = count_bad_balls(balls)
main()
root.mainloop()