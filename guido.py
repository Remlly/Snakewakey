# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 23:24:34 2021

@author: remlly
"""
import pygame
import random
import sys

class square:
    
    def __init__(self, pose = None, colour = None):
        
        if colour is None:
            colour = (127,127,127)
            
        if pose is None:
            pose = [0,0]
            
        self._pose = pose
        self.colour = colour 
            
        def goto(self, x, y):
            self._pose[0] = x
            self._pose[1] = y
            
        def getpose(self):
            x = self._pose[0]
            y = self._pose[1]
            return [x,y]
        
        def getsquare(self):
            return pygame.Rect(self._pose[0], self._pose[1], 20, 20)


class segment:
    "the snake V2"
    
    def __init__(self, pose = None, colour = None):
        
        if pose is None:
            pose = [200,200]
        
        if colour is None:
            self.colour = (44,44,44)
        
        self.pose = pose
        self.prev_pose = 0;
        self.dx = 0
        self.dy = 0
        
    def __str__(self):
        return f'pose{self.pose}\n dx,dy[{self.dx},{self.dy}]\n colour [{self.colour}]'
        
    def goto(self, x, y):
        self.pose[0] = x
        self.pose[1] = y
        
    def getpose(self):
        x = self.pose[0]
        y = self.pose[1]
        return [x,y]
    
    def getsquare(self):
        return pygame.Rect(self.pose[0], self.pose[1], 20, 20)

    def getcollision(self, collide):
        collision = pygame.Rect.colliderect(self.getsquare(), collide)
        return collision
    
    def update_head(self):

        self.pose[1] += self.dy
        self.pose[0] += self.dx
        
    def detect_key(self,event):
        if event.key == pygame.K_UP:
            #cant go up if youre going down
            if(self.dy == 0):
                self.dy = -40
                self.dx = 0
        if event.key == pygame.K_DOWN:
            #cant go down if youre going up
            if(self.dy == 0):
                self.dy = 40
                self.dx = 0
        if event.key == pygame.K_LEFT:
            #same for left and right
            if(self.dx == 0):
                self.dx = -40
                self.dy = 0
        if event.key == pygame.K_RIGHT:
            if(self.dx == 0):
                self.dx = 40
                self.dy = 0
  
def init_snake(snake_len):
    "initializer function for the snake"
    snake = [None] * snake_len
    for x in range(len(snake)):
        snake[x] = segment()
        snake[x].goto(200+x*40, 200)
        
        
    snake[0].dx = -40
    snake[0].colour = (125,0,0)
    
    return snake

def collide_snake(snake, game_over):
    "modifier that checks the collision on the snake, and modifies a game over status"
    for x in range(len(snake)):
        #collision detection on snake
        if snake[0].getcollision(snake[x].getsquare()):
            if x != 0:
                game_over = True
            if not snake[x].getcollision(screen_area):
                game_over = True
        else:
            game_over = False
        

def update_pose(snake):
    
    for x in reversed(range(len(snake))): 
        #Because for some reason, negative array indexes loop back around, we need
        #to check bounds and make sure the head does not get assigned to the back 
        #when x reaches 0 and x-1 becomes -1. litterally getting your head out of your ass
        if x > 0:
            snake[x].pose = snake[x-1].getpose()
        if x == 1:
            snake[0].update_head()
    
    return snake
    
    
  
class food:
    "FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOD"
    def __init__(self, pose = None, food = None, colour = None):
        if colour is None:
            colour = (127,127,127)
            
        if pose is None:
            pose = [0,0]
            
        self._pose = pose
        self.colour = colour
        self.exists = False
    
    def goto(self, x, y):
        self._pose[0] = x
        self._pose[1] = y
        
    def getpose(self):
        x = self._pose[0]
        y = self._pose[1]
        return [x,y]
    
    def getsquare(self):
        return pygame.Rect(self._pose[0], self._pose[1], 20, 20)
    
        

def randomize_food(food):
        x = random.randrange(0,460,40)
        y = random.randrange(0,460,40)
        food.goto(x,y)
        return food
    
def collide_apple(snake, apple, player):
    
    if snake[0].getcollision(apple.getsquare()):
        snake.append(segment())      
        player1.score +=10
        apple = randomize_food(apple)
        snake = update_pose(snake)
    
        

class player:
    "player. its an object because OOP snake :)"
    def __init__(self, player, score = None):
        
        self.name = str(player)
        self.score = 0
        
        self.font = pygame.font.SysFont(None, 25)
        
            
    
    def __str__(self):        
        data = str(self.player) + "\n" + str(self.score)
        return data
        
    def GetScore(self):
        
        return self.score
        
    def GetscoreImg(self):
        string = str(self.name) + " score:" + str(self.score)
        img = self.font.render(string, False, (70,130,180))
        return img


class button:
    "this is just an ordinary button"
    def __init__(self, text, height, width, pose = None, colour = None, tcolour = None):
        if pose == None:
            self.pose = pose
        
        if colour == None:
            self.colour = (0,0,0)
        
        if tcolour == None:
            self.tcolour = (0,0,0)
        
        self.pose = pose
        self.font = pygame.font.SysFont('stylus', 25)
        self.height = height
        self.width = width
        self.name = text
        
    def getsquare(self):
        return pygame.Rect(self.pose[0], self.pose[1], self.width, self.height)
    
    def getcollidepoint(self, pose):
        collision = pygame.Rect.collidepoint(self.getsquare(), pose[0], pose[1])
        return collision
    
    def goto(self, pose):
        self.pose[0] = pose[0]
        self.pose[1] = pose[1]
    
    def getrender(self):
        img = self.font.render(self.name, False, self.tcolour)
        return img
    
    def drawbutton(self, screen):
        pygame.draw.rect(screen, self.colour, self.getsquare())
        screen.blit(self.getrender(), [self.pose[0]+(self.width/4), self.pose[1]+(self.height/4)])



#main--------------------------------------------------------------------------
pygame.init()
#screen variables
(width, height) = (500, 500)
Background_colour = (255,255,255)

#initialize screen
screen = pygame.display.set_mode((width, height))
screen.fill(Background_colour)

#screen area
screen_area = pygame.Rect(0, 0, width, height)

#initialize fonts
pygame.font.init()

#some colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
SOFT_BLUE = (147,202,237)
SOFT_PURPLE = (175,143,233)
GREEN = (0,255,0)
RED = (255,0,0)

Start = button("Start", 50, 100, [125,250])
Start.colour = SOFT_BLUE
Start.Tcolour = BLACK

Quit = button("quit", 50, 100,[275,250])
Quit.colour = SOFT_BLUE
Quit.Tcolour = BLACK



player1 = player("Remon")

def main_screen():
    Running = True
    while Running:
        mouse_pos = pygame.mouse.get_pos()
        left, middle, right = pygame.mouse.get_pressed()
        
     
        for event in pygame.event.get():
 
            if Start.getcollidepoint(mouse_pos):
                Start.colour = SOFT_PURPLE
                if left: 
                    main_snake()
            else: 
                Start.colour = SOFT_BLUE
            
            if Quit.getcollidepoint(mouse_pos):
                Quit.colour = SOFT_PURPLE
                if left: 
                    Running = False
            else: 
                Quit.colour = SOFT_BLUE
    
   
            if event.type == pygame.QUIT:
                Running = False
                
                
        screen.fill(Background_colour)
        Start.drawbutton(screen)
        Quit.drawbutton(screen)
        pygame.display.update()
        
def main_snake():
    
    pygame.display.flip()
    FPS = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    random.seed()
    
    snake = init_snake(4)
    
    apple = food()
    apple = randomize_food(apple)

    game_over = False
    while not game_over:
        
        
        collide_snake(snake, game_over)
        collide_apple(snake, apple, player1)
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                snake[0].detect_key(event)
                
            if event.type == pygame.USEREVENT:
                
                    snake = update_pose(snake)
                
                    
                
            if event.type == pygame.QUIT:
                game_over = True
        
        #drawing screen-----------------------------------------------------------   
        screen.fill(Background_colour)
        pygame.draw.rect(screen, apple.colour, apple.getsquare())
        
        for i in range(len(snake)):
            pygame.draw.rect(screen, snake[i].colour, snake[i].getsquare())
            #print("\nindex:", i, snake[i])
            
        
        screen.blit(player1.GetscoreImg(), (0,0) )
        pygame.draw.rect(screen, (255,0,0), screen_area,  4)
        pygame.draw.rect(screen, snake[0].colour, snake[0].getsquare())
        pygame.display.update()

        
        FPS.tick(60)

    
def game_over():
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
      
            
        screen.fill(Background_colour)
        screen.blit(player1.GetscoreImg(), (250,250) )
        pygame.display.update()
    
    


main_screen()


pygame.display.quit()
pygame.quit()
sys.exit(None)