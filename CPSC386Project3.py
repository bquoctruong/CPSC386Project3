import pygame
import random
import os

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
image_folder = os.path.join(game_folder, "img") #Allows access to folders in game folder
class Player(pygame.sprite.Sprite):
    #Player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #image of the sprite
        self.image = pygame.image.load(os.path.join(game_folder, "testSprite.png")).convert()
        self.image.set_colorkey(color_white)    #Ignores RGB value when rendering image, creating transperency
        #rectangle of the sprite
        self.rect = self.image.get_rect()   #obtains rectangle from image
        self.rect.centerx = (window_width / 2)
        self.rect.bottom = window_height - 10
        self.x_speed = 0
        self.y_speed = 0

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
#Start up pygame
pygame.init()
pygame.mixer.init()
pygameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game")

#Keeps track of clock
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#Game loop
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
    #Render game background
    pygameDisplay.fill(color_green)
    all_sprites.draw(pygameDisplay) #Draws sprites to screen

    #Enables double buffering; last thing to code
    pygame.display.flip()

pygame.quit()

#Resources:
#https://www.youtube.com/watch?v=nGufy7weyGY&index=4&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw