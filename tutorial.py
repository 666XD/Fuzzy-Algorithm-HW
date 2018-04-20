import sys, pygame
import time
import random

width = 800
higth = 600

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green  = (0, 255, 0)

pygame.init()
gameDisplay = pygame.display.set_mode((width,higth))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

# carImg = pygame.image.load('car.png')
def things(thingx, thingy, thingh, thingw, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingh, thingw])

def car(x, y):
    pygame.draw.rect(gameDisplay, red, [x,y,30,30])
    # gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def crash():
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    textSurf, textRect = text_objects('You Crash', largeText)
    textRect.center = ((width/2), (higth/2))
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)
    gameLoop()

def gameLoop():
    x = (width * 0.45)
    y = (higth * 0.9)
    x_change = 0
    gameExit = False
    thing_startx = random.randrange(0, width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_hight = 100

    while not gameExit:
        for event in pygame.event.get(): # get everything of the game information include mouse position
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: x_change = -5
                elif event.key == pygame.K_RIGHT: x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            #print(event)
        x += x_change
        if x > width-30 or x < 0:
            crash()
            gameExit = True
        if thing_starty > higth: thing_hight = 0
        gameDisplay.fill(white)
        things(thing_startx, thing_starty, thing_hight, thing_width, green)
        thing_starty += 7
        car(x, y)
        pygame.display.update() # update single thing in the ()
        #pygame.display.flip() # update every thing
        clock.tick(60) # 60 fps

gameLoop()
pygame.quit()

quit()