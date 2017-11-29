#Name: Brian Truong
#Date: 11/10/2017
#File Name: CPSC386Project3.py
#File Description: All-in-one file that contains a shoot-em-up game
import pygame
import random
import os
from os import path

#TO-DO 11/29 UPDATE:
#   -Finish implementing explosions
#   -Boss Screen
#   -Upgrade Screen
#   -Polish/clean code

#Set up Pygame attributes
window_width = 480
window_height = 600
fps = 60

#RGB colors
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)

#Set up asset's folder
game_folder = os.path.dirname(__file__) #Automatically sets this directory to where the py file is located
image_folder = os.path.join(game_folder, "img") #Allows access to image folders in game folder
sound_folder = os.path.join(game_folder, "sound") #Allows access to sound

#Automatically searches for the given font on the OS
font_name = pygame.font.match_font('timesnewroman')

# Function: draw_text
# Date of code (Last updated): 11/19/2017
# Programmer: Brian Truong
# Description: When called, outputs a string onto the surface
# Input: surface, text, fontSize, x, y
# Output: 
def draw_text(surface, text, fontSize, x, y):
    font = pygame.font.Font(font_name, fontSize)
    text_surface = font.render(text, True, color_white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

# Function: draw_shield_bar
# Date of code (Last updated): 11/29/2017
# Programmer: Brian Truong
# Description: When called, outputs a bar that shows how much life the player has
# Input: surface, x, y, percentage
# Output: 
def draw_shield_bar(surface, x, y, percentage):
    if percentage < 0:  #Prevents green bar from going in opposite direction
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH  #Calculates green bar's length
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)    #Outline for life
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, color_green, fill_rect)
    pygame.draw.rect(surface, color_white, outline_rect, 2)

# Function: Player
# Date of code (Last updated): 11/29/2017
# Programmer: Brian Truong
# Description: Class that details attributes for the player, such as sprites, functions
# Input: Sprite
# Output: 
class Player(pygame.sprite.Sprite):
    #Player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #image of the sprite
        playerImage = pygame.image.load(os.path.join(image_folder, "playerShip1_blue.png")).convert()
        self.image = pygame.transform.scale(playerImage, (50,38))
        self.image.set_colorkey(color_black)    #Ignores RGB value when rendering image, creating transperency
        #rectangle of the sprite
        self.rect = self.image.get_rect()   #obtains rectangle from image

        #Creates radius for accurate hitbox
        self.radius = 23
        #pygame.draw.circle(self.image, color_red, self.rect.center, self.radius)
        self.rect.centerx = (window_width / 2)
        self.rect.bottom = window_height - 10
        self.x_speed = 0
        self.y_speed = 0

        #Player's life/shield
        self.shield = 100

    def update(self):
        #Set stationary speed
        self.x_speed = 0
        self.y_speed = 0

        #Obtains key being pressed
        keystate = pygame.key.get_pressed()

        #Moves sprite to left if A is pressed down
        if keystate[pygame.K_a]:
            self.x_speed = -5
        #Moves sprite to right if D is pressed down
        if keystate[pygame.K_d]:
            self.x_speed = 5
        #Moves sprite up if W is pressed down
        if keystate[pygame.K_w]:
            self.y_speed = -5
        #Moves sprite down if S is pressed down
        if keystate[pygame.K_s]:
            self.y_speed = 5
        #Shoots bullets (invokes function shoot()) if Spacebar is pressed down
        if keystate[pygame.K_SPACE]:
            self.shoot()
            playerShootSFX.play()

        #Updates speed based on keystate
        self.rect.x += self.x_speed    #Moves sprite 5 pixels to the right
        self.rect.y += self.y_speed
        
        #If sprite gets to the bottom of the screen, prevents it from going further
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
        #If sprite reachs the top of the screen, prevents it from going further
        if self.rect.top < 0:
            self.rect.top = 0
        #If sprite moves off screen to the right, prevents it from going further
        if self.rect.right > window_width:
            self.rect.right = window_width
        #If sprite moves off screen to the left, prevents it from going further
        if self.rect.left < 0:
            self.rect.left = 0

    #Allows ship to fire bullets
    def shoot(self):
        bullet = player_Bullet(self.rect.centerx, self.rect.top)   #Spawns bullet in front of ship
        all_sprites.add(bullet) #Adds bullet to sprite group
        #Creates a new sprite group for bullets
        player_bullets.add(bullet)
        #playerShootSFX.play()

# Function: Enemies
# Date of code (Last updated): 11/29/2017
# Programmer: Brian Truong
# Description: Class that contains attributes to the enemy
# Input: 
# Output: 
class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y):
        pygame.sprite.Sprite.__init__(self)

        #image of the sprite
        enemyImage = pygame.image.load(os.path.join(image_folder, "enemyRed2.png")).convert()
        self.image = pygame.transform.scale(enemyImage, (50,38))
        self.image.set_colorkey(color_black)    #Ignores RGB value when rendering image, creating transperency
        #rectangle of the sprite
        self.rect = self.image.get_rect()   #obtains rectangle from image

        #Creates radius to provide an accurate hitbox
        self.radius = int(15)
        #pygame.draw.circle(self.image, color_red, self.rect.center, self.radius)
        

        #Spawn enemies
        self.rect.x = window_width * (enemy_x / 8)  #Spawns enemies in areas proportioned to window size
        self.rect.y = enemy_y * 20  #Static Y area for enemy to spawn (Subject to change)
        self.y_speed = random.randrange(1,3)    #Assigns speed
        self.x_speed = random.randrange(-1,2)  #Not sure if I want enemies to move

        #Creates a delay to determine when enemies can fire; much more responsive than using mod (11/29)
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed

        self.shoot()

        #11/29: Removed; will determine if it is better than current setup
        #Times bullets so player doesn't get swarmed
        #bullet_time = pygame.time.get_ticks()
        #if (bullet_time % 23 == 1):
        #    self.shoot()

        #If enemies go off screen, respawn them; subject to deletion
        if self.rect.top > window_height + 5 or self.rect.left < -25 or self.rect.right > window_width + 25:
            #Spawn enemies
            self.rect.x = random.randrange(window_width - self.rect.width)  #Spawns randomly 
            self.rect.y = random.randrange(-100, -40)
            self.y_speed = random.randrange(1,8)    #Assigns speed

    #Allows enemies to shoot bullets
    def shoot(self):
        #Newer implementation of shoot delay; adjusted through shoot_delay variable; consistent
        now = pygame.time.get_ticks()   #Gets current time
        if now - self.last_shot > self.shoot_delay: #If current time and last fired shot is greater than shoot delay, it will fire a bullet
            self.last_shot = now
            bullet = enemyBullet(self.rect.centerx, self.rect.bottom)   #Spawns bullet in front of ship
            all_sprites.add(bullet)
            #Creates a new sprite group for bullets
            enemy_bullets.add(bullet)
        

# Function: player_Bullet
# Date of code (Last updateu): 11/19/2017
# Programmer: Brian Truong
# Description: Class that details attributes of the bullets player fires
# Input: x, y
# Output: 
class player_Bullet(pygame.sprite.Sprite):
    #Initialization of bullet; x,y are used to spawn bullet in front of player ship
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #image of the sprite
        bulletImage = pygame.image.load(path.join(image_folder, "laserBlue16.png")).convert()
        self.image = pygame.transform.scale(bulletImage, (10, 30))
        #rectangle of the sprite
        self.rect = self.image.get_rect()   #obtains rectangle from image

        #Draws full radius for bullets
        self.radius = 15
        #pygame.draw.circle(self.image, color_red, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -20  #Speed of bullet; subject to change

    #Moves bullet across screen
    def update(self):
        self.rect.y += self.y_speed
        #kill it off it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Function: enemy_Bullet
# Date of code (Last updateu): 11/19/2017
# Programmer: Brian Truong
# Description: Class that details attributes of the bullets enemies fires
# Input: x, y
# Output: 
class enemyBullet(pygame.sprite.Sprite):

    #Initializes bullets; x,y allows bullets to spawn in front of enemy ships
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        #image of the sprite
        bulletImage = pygame.image.load(path.join(image_folder, "laserRed09.png")).convert()
        self.image = pygame.transform.scale(bulletImage, (20, 20))
        self.image.set_colorkey(color_black)
        #rectangle of the sprite
        self.rect = self.image.get_rect()   #obtains rectangle from image

        #Draws radius for enemy bullets
        self.radius = 8
        #pygame.draw.circle(self.image, color_red, self.rect.center, self.radius)
        

        #Set location of enemy bullet
        self.rect.bottom = y
        self.rect.centerx = x

        #Speed of bullet (Subject to change)
        self.y_speed = 3
        self.x_speed = random.randrange(-3, 3)

    def update(self):
        #Update bullet sprite
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        #kill it off it moves off the top of the screen
        if self.rect.bottom < 0 or self.rect.right > window_width + 10 or self.rect.left < -10:
            self.kill()

# Class: Explosion
# Date of code (Last updateu): 11/29/2017
# Programmer: Brian Truong
# Description: Class that details attributes of explosions spawned
# Input: N/A
# Output: 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 24

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#Start up pygame
pygame.init()
pygame.mixer.init()
pygameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Terminating Arc")

#Keeps track of clock
clock = pygame.time.Clock()

#SFX/BGM
playerShootSFX = pygame.mixer.Sound(path.join(sound_folder, 'Laser_Shoot_Player.wav'))
playerShootSFX.set_volume(0.4)
playerExplosionSFX = pygame.mixer.Sound(path.join(sound_folder, 'Explosion_Player.wav'))
enemyExplosionSFX = pygame.mixer.Sound(path.join(sound_folder, 'Explosion_Enemy.wav'))
enemyExplosionSFX.set_volume(0.4)
pygame.mixer.music.load(path.join(sound_folder, 'music_1.ogg'))
pygame.mixer.music.set_volume(0.4)

#Sprites
background = pygame.image.load(path.join(image_folder, "space.jpg")).convert()
background_rect = background.get_rect()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
enemy_Sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

#List for explosion
explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = []

for i in range(8):
    filename = 'explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(image_folder, filename)).convert()
    img.set_colorkey(color_black)
    img_large = pygame.transform.scale(img, (75,75))
    explosion_animation['large'].append(img_large)
    img_small = pygame.transform.scale(img, (45,45))
    explosion_animation['small'].append(img_small)

#Spawn enemies
def spawnEnemies(amountOfEnemies, waves):
    for i in range(amountOfEnemies):
        enemy = Enemies(i, 1)
        all_sprites.add(enemy)
        enemy_Sprites.add(enemy)


#Spawns singular enemies
def newmob():
    enemy = Enemies(random.randint(0, 7),1)
    all_sprites.add(enemy)
    enemy_Sprites.add(enemy)

#Initialize score (Subject to change)
score = 0000000

#Starts game with 8 enemies
spawnEnemies(8,1)
#Game loop
pygame.mixer.music.play(loops=-1)   #Initialize music; makes it loop
isGameRunning = True
while isGameRunning:
    #Keep game loop running at the correct FPS
    clock.tick(fps)
    #Processes input while game is running
    for event in pygame.event.get():
        #If window is closed, turn off the game
        if event.type == pygame.QUIT:
            isGameRunning = False

    #Update
    #update sprites
    all_sprites.update()

    #Check to see if a bullet hit a mob
    enemy_Hits = pygame.sprite.groupcollide(enemy_Sprites, player_bullets, True, True) #First bool is if enemies hit bullets, they get deleted; 2nd bool is if bullets hit enemies, bullets dissapear
    hits = pygame.sprite.groupcollide(enemy_bullets, player_bullets, True, True)    #If player bullets and enemy bullets collide, they both dissappear

    enemiesDefeated = 1
    #Respawns enemies when they die (Subject to change)
    #while(enemiesDefeated != 16):
    for hit in enemy_Hits:
        #Adds to the player score with every enemy hit
        score += 50 - hit.radius
        enemyExplosionSFX.play()
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        newmob()
        enemiesDefeated += 1

    #Check to see if enemies hit player
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle)
    enemy_playerCollision = pygame.sprite.spritecollide(player, enemy_Sprites, True, pygame.sprite.collide_circle)
    
    #If player gets hit, the game is over (Subject to change)
    #11/29: Now if player gets hit, subtracts 20 from his life. If life goes below 0, game is over
    for hit in hits:
        #playerExplosionSFX.play()
        player.shield -= 20
        newmob()
        if player.shield <= 0:
            isGameRunning = False
    for hit in enemy_playerCollision:
        #playerExplosionSFX.play()
        player.shield -= 20
        newmob()
        if player.shield <= 0:
            isGameRunning = False

    #Render game background
    pygameDisplay.fill(color_black)
    pygameDisplay.blit(background, background_rect)
    all_sprites.draw(pygameDisplay) #Draws sprites to screen
    draw_text(pygameDisplay, 'Score: ' + str(score), 18, 50, 0)
    draw_shield_bar(pygameDisplay, 5, window_height - 20, player.shield)
    #Enables double buffering; last thing to code
    pygame.display.flip()

pygame.quit()

#Resources:
#https://www.youtube.com/watch?v=nGufy7weyGY&index=4&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw
#LEFT OFF: https://youtu.be/AdG_ITCFHDI?t=755