import pygame

SCREEN_WIDTH = 800 #chiều dài
SCREEN_HEIGHT = 576 #chiều rộng

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite): #nguòi chơi
    change_x = 0 #lượng thay đổi x
    change_y = 0 #lượng thay đổi y
    explosion = False #kiểm tra xem có va chạm vs enemies ko
    game_over = False   #Kiểm soát trò chơi có kết thúc hay không
    def __init__(self,x,y,filename): # khởi tạo 
        # Call the parent class (sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert() #Gán hình ảnh với tên filename
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()    
        self.rect.topleft = (x,y) #khởi tạo vị trí góc trên bên trái x,y
        # Load image which will be for the animation
        img = pygame.image.load("walk.png").convert() #hình ảnh khi chạy
        # Create the animations objects
        self.move_right_animation = Animation(img,32,32) #Ảnh quay phải
        self.move_left_animation = Animation(pygame.transform.flip(img,True,False),32,32)#Ảnh quay trái
        self.move_up_animation = Animation(pygame.transform.rotate(img,90),32,32) #Ảnh lên trên
        self.move_down_animation = Animation(pygame.transform.rotate(img,270),32,32) #Ảnh xuốg dưới
        # Load explosion image
        img = pygame.image.load("explosion.png").convert() #Nổ
        self.explosion_animation = Animation(img,30,30) #Ảnh động nổ
        # Save the player image
        self.player_image = pygame.image.load(filename).convert() 
        self.player_image.set_colorkey(BLACK)

    def update(self,horizontal_blocks,vertical_blocks): #update vi trí ....
        if not self.explosion: #Nếu ch nổ
            if self.rect.right < 0: #Nếu ra khỏi màn hình trái 
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:#....
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x #Vị trí x thay đổi lượg chang_x
            self.rect.y += self.change_y#Vi trí y thay đổi lượng y

            # This will stop the user for go up or down when it is inside of the box

            for block in pygame.sprite.spritecollide(self,horizontal_blocks,False): #Nếu va chạm với ô máp ngang
                self.rect.centery = block.rect.centery
                self.change_y = 0 #Sẽ ko thể đi lên trên đc
                #Giải thích False ở cuối:
                #Nếu là True thì khi va chạm player sẽ biến mất còn False thì ko bị
            for block in pygame.sprite.spritecollide(self,vertical_blocks,False): # nếu va chạm với ô máp dọc
                self.rect.centerx = block.rect.centerx
                self.change_x = 0 # Sẽ ko đi trái phải đc

            # This will cause the animation to start
            
            if self.change_x > 0: #Nếu lượng x> 0 sẽ di chuyển sang phải
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else: #nếu nổ
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                pygame.time.wait(500)             
                self.game_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()
            

    def move_right(self): 
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3

    def stop_move_right(self):#Nhả phím sang phải ra thì dừng di chuyển
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):#Tương tự
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image,True,False)
        self.change_x = 0

    def stop_move_up(self):#Tương tự
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,270)
        self.change_y = 0



class Animation(object):# Tạo animation
    def __init__(self,img,width,height):
        # Load the sprite sheet
        self.sprite_sheet = img
        # Create a list to store the images
        self.image_list = []
        self.load_images(width,height)
        # Create a variable which will hold the current image of the list
        self.index = 0
        # Create a variable that will hold the time
        self.clock = 1
        
    def load_images(self,width,height):
        # Go through every single image in the sprite sheet
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                # load images into a list
                img = self.get_image(x,y,width,height)
                self.image_list.append(img)

    def get_image(self,x,y,width,height): # Lấy về hình ảnh
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey((0,0,0))
        # Return the image
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self,fps=30):
        step = 30 // fps
        l = range(1,30,step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0

            
    
        
