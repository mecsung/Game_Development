# My first python game
import pygame, sys, random
import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from pygame.math import Vector2

pygame.init()

width = 500
height = 500
cols = 25
rows = 20

class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(0,96,255)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # Arrow keys: Left, Right, Up, Down
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake():
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow():
    global win
    win.fill((175,215,70))      # bg color
    drawGrass(width, rows, win) # grass pattern
    
    # Score Board
    font = pygame.font.Font(None, 20)
    score = len(s.body) - 2
    text = font.render('Score: ' + str(score), False, (0, 0, 0))
    win.blit(text, (40,15))
    
    apple = pygame.image.load('apple.png').convert_alpha()
    win.blit(apple, (0,0))

    
    s.draw(win)                 # draw window
    snack.draw(win)             # draw the snack
    pygame.display.update()
    pass


def drawGrass(w, rows, surface):
    grass_color = (161,209,61)
    size = 500
    
    for row in range(rows):
        if row % 2 == 0:
            for col in range(rows):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cols, row * cols, cols, cols)
                    pygame.draw.rect(surface, grass_color, grass_rect)
        else:
            for col in range(rows):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cols, row * cols, cols, cols)
                    pygame.draw.rect(surface, grass_color, grass_rect)			


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)

def popup(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    res = messagebox.askyesno(subject, content)
    if res == True:
        pygame.quit()
        sys.exit()
    else:
        pass
        
    
sroot = tk.Tk()     # globalize splash window
def splash_screen():
    
    sroot.title("SNAKE and APPLES")
    sroot.configure(bg="lightgreen")
    sroot.geometry("500x500")
    
    
    panel = Label(sroot, text="Snake and Apples", bg="lightgreen",
              height=2, font=("Bradley Hand ITC", 20), fg='darkgreen'
              ).pack()
    
    start_button = tk.Button(sroot, height = 2, width = 25,
                      text = "Start",cursor="mouse",
                      bg="green", fg="white", command = master).pack()
    
    image = Image.open("keyboard.png")
    resize_image = image.resize((300, 300))
    img = ImageTk.PhotoImage(resize_image)

    icon = Label(sroot, image = img, bg="lightgreen")
    icon.image = img
    icon.pack()


def master():
    sroot.destroy()
    
    global s, snack, win
    win = pygame.display.set_mode((width,height))   # game window
    pygame.display.set_caption('Snake and Apples')
    
    s = snake((255,0,0), (10,10))                   # position start at middle
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(255,0,0))
    flag = True
    clock = pygame.time.Clock()
    
    while flag:
        
        pygame.time.delay(50)
        clock.tick(10) # 10 frames per second / > num ?> speed
        s.move()
        headPos = s.head.pos
        # SNAKE
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            score = len(s.body) - 2
            popup("Better luck next time!", "Quit Game?\nYour Score : " + str(score))
            s.reset((10, 10))

        # SNACK
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(255,0,0))
        # SCORE
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                score = len(s.body) - 2
                popup("Better luck next time!", "Quit Game?\nYour Score : " + str(score))
                s.reset((10,10))
                break
       
        redrawWindow()
     
def main():
    splash_screen()
    
if __name__ == "__main__":
    main()






















