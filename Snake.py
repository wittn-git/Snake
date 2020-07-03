from tkinter import * 
import tkinter
import random

def loop():
    canvas.delete('all')
    food.show()
    snake.move()
    snake.show()
    score = len(snake.position)
    global highscore
    if highscore <= score:
        highscore = score
    root.wm_title('Highscore: {} | Score: {}'.format(highscore, score))
    if snake.dead:
        open('highscore.txt', 'w').write(str(highscore))
        root.destroy()
    root.after(280, loop)

class Snake():

    def __init__(self):
        self.position = []
        for i in range(3):
            self.position.append((10, 10+i))
        self.dir = 1
        self.dead = False
        self.eaten = False

    def show(self):
        for coord in self.position:
            canvas.create_rectangle(
                size*coord[0],
                size*coord[1],
                size*coord[0]+size,
                size*coord[1]+size,
                fill='green'
            )
    
    def move(self):
        new_x = self.position[0][0]
        if self.dir == 1: new_x+=1
        if self.dir == 3: new_x-=1
        new_y = self.position[0][1]
        if self.dir == 2: new_y+=1
        if self.dir == 4: new_y-=1
        if new_x < 0 or new_x >= fields or new_y < 0 or new_y >= fields or (new_x, new_y) in self.position:
            self.dead = True
        self.position.insert(0, (new_x, new_y))
        if (food.x, food.y) in self.position:
            self.eaten = True
            food.eaten = True
        if not self.eaten:
            del self.position[len(self.position)-1]
        self.eaten = False

    def change_dir(self, dir):
        if dir == self.dir:
            self.move()
        self.dir = dir

class Food:

    def __init__(self):
        self.x, self.y = int(random.uniform(0, fields-1)), int(random.uniform(0, fields-1))
        self.eaten = False
    
    def show(self):
        if self.eaten:
            self.eaten = False
            self.x, self.y = int(random.uniform(0, fields-1)), int(random.uniform(0, fields-1))
        canvas.create_rectangle(
                size*self.x,
                size*self.y,
                size*self.x+size,
                size*self.y+size,
                fill='red'
        )

root = tkinter.Tk()
fields = 20
size = (root.winfo_screenheight()-100)/fields
root.geometry('%dx%d+0+0' % (size*fields, size*fields))

canvas = Canvas(root, background='black')
canvas.place(width=size*fields, height=size*fields)

snake = Snake()
food = Food()

score = len(snake.position)
highscore = int(open('highscore.txt').read())
root.wm_title('Highscore: {} | Score: {}'.format(highscore, score))

root.bind('w', lambda x: snake.change_dir(4))
root.bind('s', lambda x: snake.change_dir(2))
root.bind('d', lambda x: snake.change_dir(1))
root.bind('a', lambda x: snake.change_dir(3))

loop()
root.mainloop()