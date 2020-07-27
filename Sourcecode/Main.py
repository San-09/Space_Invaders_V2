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

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
         window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)        #inside of bracket checks if on screen. So negate with not to output TRUE if off screen

    def collision(self, obj):
        return collide(self, obj)




class Ship:
    COOLDOWN = 30  # FPS is 60, so 30 is half a second

    def __init__(self, x, y, health = 100):     # Sets default values
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):#
        window.blit(self.ship_img, (self.x, self.y))
      #  pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50)) # This was a test to create a rectangle
        for laser in self.lasers:       #Draw the laser
            laser.draw(window)

    def move_lasers(self, vel, obj):
        # This will be called once a frame and this will increment the cooldown counter when the laser moves and check if we can send another laser. loop through all lasers
        #This will be used for the player and the enemy
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):   # otherwise
                obj.health -= 10
                self.lasers.remove(laser)



    def shoot(self):
        if self.cool_down_counter == 0:     #If cool down counter is 0
            laser = Laser (self.x, self.y, self.laser_img)   # Create a new laser
            self.lasers.append(laser)           # Add to the list of lasers list
            self.cool_down_counter = 1      #Set the cool down counter to increment

    def cooldown(self):
        #If cool down counter is 0 - dont do anything. But if it is greater than 0 and its not passed the time limit then increment by 1
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):   # As ship is defined inside player, the player will inherit the ship
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)      #initialises from the Ship class #Grabs the methods
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) #Mask allows for pixel perfect collision. 
        self.max_health = health

    def move_lasers(self, vel, objs):       #Objs is the list of all enemies
        # This will be called once a frame and this will increment the cooldown counter when the laser moves and check if we can send another laser. loop through all lasers
        # This will be used for the player and the enemy
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):  # otherwise
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                 "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):   # New initialisation
        super().__init__(x,y,health)   # Grabs methods from Ship. Anaything with self.
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel


    def shoot(self):
        if self.cool_down_counter == 0:     #If cool down counter is 0
            laser = Laser (self.x-15, self.y, self.laser_img)   # Create a new laser
            self.lasers.append(laser)           # Add to the list of lasers list
            self.cool_down_counter = 1      #Set the cool down counter to increment

def collide(obj1, obj2):
     offset_x = obj2.x - obj1.x
     offset_y = obj2.y - obj1.y
     return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None   #Will return TRUE if the obj1 and obj2 overalap. Do not reutrun none if they dont overalp. The return will be a tuple (x,y)

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 10

    player = Player(300, 650)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))        #Draws the background screen at (0,0) at the top corner
        #Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10,10))
        #The level label will be on the right edge of the screen. We want this just to the left of the right edge.
        #The following automates this by getting the width of the label text
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost ", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))  #Centres text in the middle of the screen

        pygame.display.update()

    while run:
        clock.tick(FPS)         # This while loop will run at x frames per second.
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1


        if lost:
            if lost_count > FPS * 3:     # 3 second timer so show lost font for this long
                run = False
            else:
                continue            #This continue will not run the rest of the while loop. It'll start again at the while loop

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            #Spawn the enemeies off screen at different positions and they all move down at the same speed
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #If user quits, then stop the game. Set Run as False
                run = False

        #With the following method you will be able to press two keys at the same time. If Event used, then you can
        #only press one key at a time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #Left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #Right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT:  # Down # Only if player is within Height window limit
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()


        for enemy in enemies[:]:     # What does [:] do?
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange (0,120) == 1:         #To get the enemy to have a 50% change of shooting every second, then do FPS (60) * 2
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)



main()