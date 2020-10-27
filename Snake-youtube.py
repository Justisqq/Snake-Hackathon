# with great help from https://www.youtube.com/watch?v=9bBgyOkoBQ0

import pygame
import sys
import random

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]    #starts in the center
        self.direction = random.choice([up, down, left, right])         #points in random direction
        self.color = (17, 24, 47)

    def get_head_position(self):
        return self.positions[0]           #updates where the snake is

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:   #if snake length is more than 1 it can go just in 3 directions 
            return
        else:
            self.direction = point   
    
    def move(self):
        cur = self.get_head_position()  
        x, y = self.direction             #current direction of a snake
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)  #new position of snake
        if len(self.positions) > 2 and new in self.positions[2:]:      #if snake touches itself gameover
            self.reset()
        else:
            self.positions.insert(0, new)             #else we will reposition snake
            if len(self.positions) > self.length:
                self.positions.pop()                  

    def reset(self):
        self.length = 1
        self.position = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)               #we will draw rect of snake head
            pygame.draw.rect(surface, (93, 216, 228), r, 1)        #draw the rest of body

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:        #player wants to quit
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:        #if player pressed Keys turn snake acordingly
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)  #randomly position food

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))   #draw a rect of food in randomized position
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if(x + y) % 2 == 0:
                r = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))     
                pygame.draw.rect(surface, (93, 216, 228), r)                           #Draws a rect on even coordinates
            else:
                rr = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (84, 194, 205), rr)                          #Draws even darker rect on odd coordinates


screen_width = 480
screen_height = 480

gridsize = 20                                     #rect size
grid_width = screen_width / gridsize              #number of rect on x axis
grid_height = screen_width / gridsize             #number of rect on y axis

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)      #displays the main screen

    surface = pygame.Surface(screen.get_size())      
    surface = surface.convert()
    drawGrid(surface)                             #draws rect on main screen

    snake = Snake()                               #snake class obj
    food = Food()                               #food class obj

    myfont = pygame.font.SysFont("monospace", 16)

    score = 0

    while(True):                                  #this never terminates
        clock.tick(10)                            #10 frames per second
        snake.handle_keys()                       #hande the event when key is pressed
        drawGrid(surface)                         #overlay main screen with rect
        snake.move()                              #move snake acording to key pressed
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()
        
        snake.draw(surface)                       #draws snake
        food.draw(surface)                        #draws food

        screen.blit(surface, (0, 0))              #overlays main screen with event or smth
        text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))            #create a text of score
        screen.blit(text, (5, 10))                #displays text(score)
        pygame.display.update()

main()



