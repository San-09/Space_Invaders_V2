#Rules
#Constants will be capatalised

#import modules
import pygame
import os
import time
import random

#fonts in pygame need to be initialised at the beginning of code
pygame.font.init()


WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #Width and height are a tuple
pygame.display.set_caption("Space Shooter Tutorial")


#Load images from asset folder
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

#Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Background image
#Transform.scale will scale the background image to the size of the Width and Height. load will load the image
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))

class Ship:
    def __init__(self, x, y, health = 100):     # Sets default values
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))



def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    player_vel = 5

    ship = Ship(300, 650)
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))        #Draws the background screen at (0,0) at the top corner
        #Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10))
        #The level label will be on the right edge of the screen. We want this just to the left of the right edge.
        #The following automates this by getting the width of the label text
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        ship.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #If user quits, then stop the game. Set Run as False
                run = False

        #With the following method you will be able to press two keys at the same time. If Event used, then you can
        #only press one key at a time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: #Left
            ship.x -= player_vel

        if keys[pygame.K_d]: #Right
            ship.x += player_vel
        if keys[pygame.K_w]:  # Up
            ship.y -= player_vel
        if keys[pygame.K_s]:  # Down
            ship.y += player_vel



main()