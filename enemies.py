import pygame
import random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
sky_blue = (135, 206, 235)
pink = (255, 192, 203)
yellow = (255, 255, 0) 
GREEN = (0,255,0)


class Block(pygame.sprite.Sprite):#Tạo các khối
    def __init__(self,x,y,color,width,height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.muc=1

class Ellipse(pygame.sprite.Sprite):#tạo hình elipse để ăn các hạt
    def __init__(self,x,y,color,width,height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ellipse
        pygame.draw.ellipse(self.image,color,[0,0,width,height]) # có sẵn hàm vẽ
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        

    
        
