#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import *
import random
import time
import pygame,sys
from player import Player
from enemies import *

pygame.init()
import tkinter
from tkinter import messagebox
from button import Button
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
dem=0
muc=1# kiểm soát level 
click_sound = pygame.mixer.Sound("assets/munch_2.wav") #Click chuot
power=pygame.mixer.Sound("res/sound/power_pellet.wav") #Âm thanh khi ăn viên đỏ

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
sky_blue = (135, 206, 235)
pink = (255, 192, 203)
yellow = (255, 255, 0) 
GREEN = (0,255,0)
zzz=0 #Lưu mức dẽ, vừa, khó....
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
lives=3 #Mạng 
class Slime(pygame.sprite.Sprite): #Tạo lớp slime
    def __init__(self,x,y,change_x,change_y,filename):#Vị trí, tên hình ảnh
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the direction of the slime
        self.change_x = change_x
        self.change_y = change_y
        self.kkk = False
        self.kkk1= False
        self.kkk2 = False
        self.kkk3=0
        self.kkk4=0
        # Load image
        self.image = pygame.image.load(filename).convert_alpha() #Lấy hình ảnh
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def get_intersection_position(self): # Trả về ngã 4: có thể đi 4 hướng đều được
        items = []        
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 3:# vị trí  trong environment = 3 tương đươg vs ngã 4
                    items.append((j*32,i*32))
       
        return items
    def kiemtrahang(self): # trả về các hàng ko thể đi lên trên, dưới
        items = []        
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    items.append((j*32,i*32))
        return items
    def kiemtracot(self): #trả về các cột ko thể đi sang ngang
        items = []        
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 2:
                    items.append((j*32,i*32))
        return items
    def update(self,horizontal_blocks,vertical_blocks,xx,yy,zz): #update vị trí
        #xx, yy là vị trí của người chơi(xx,yy)
        #zz là biến kiểm tra xem người chơi đã ăn viên đỏ ch?
        self.rect.x += self.change_x #slime thay doi luong x
        self.rect.y += self.change_y #y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        if zz==False: #Nếu ch ăn viên đỏ poss sẽ đuổi theo mình
            if self.kkk==True:#Ban đầu kkk = False nhảy xuống else
                #đoạn code sẽ làm cho boss phaỉ bắt buộc sang trái hoặc phảior trên dưới cho đến khi gặp ngã 4
                #nếu ko nó sẽ ko di chuyển được 
                if self.kkk1==True:#vị trí boss đag ở hàng tại vị trí cùng x với player
                    if self.kkk3==0:#chỉ vào đây 1 lần lần sau kkk3 đều = 1
                        self.kkk4=random.choice([1,2]) #random(1,2)
                        self.kkk3=1
                    else:
                        if self.kkk4==1 and (not self.rect.topleft in self.get_intersection_position()):
                            self.change_y=0#sang trái
                            self.change_x=-2
                        elif self.kkk4==2 and (not self.rect.topleft in self.get_intersection_position()):
                            self.change_y=0#sang phải
                            self.change_x=2
                        elif self.rect.topleft in self.get_intersection_position():
                            self.kkk = False
                            self.kkk1=False
                            self.kkk2=False
                            self.kkk3=0
                elif self.kkk2:#vị trí boss đang ở cột tại vị trí cùng y với player
                    if self.kkk3==0:
                        self.kkk4=random.choice([1,2])
                        self.kkk3=1
                    else:
                        if self.kkk4==1 and (not self.rect.topleft in self.get_intersection_position()):
                            self.change_y=-2#chỉ lên trên
                            self.change_x=0
                        elif self.kkk4==2 and (not self.rect.topleft in self.get_intersection_position()):
                            self.change_y=2
                            self.change_x=0
                        elif self.rect.topleft in self.get_intersection_position():
                            self.kkk = False
                            self.kkk1=False
                            self.kkk2=False
                            self.kkk3=0

            else:
                if self.rect.topleft in self.get_intersection_position(): #Kiểm tra boss ở ngã 4
                    ff=True # boss có cùng hàng cùng cột vs ngươi chơi ko
                    if self.rect.y==yy: #nếu player ở cùng hàng vs boss 
                        self.change_y=0#ko di lên trên
                        if self.rect.x<xx: # boss ở bên trái người chơi
                            if (self.rect.x+(800-xx)) <xx-self.rect.x: #nếu đi qua bên trái để quay
                                self.change_x=-2                       #ngược lại ngắn hơn qua bên phải
                                ff=False #đã di chuyển
                            else:
                                self.change_x=2 #ko thì đi sang phải
                                ff=False# đánh dấu tìm được đường đi
                        elif self.rect.x>xx:#boss bên phải người chơi
                            if (800-self.rect.x+xx) < self.rect.x-xx:
                                self.change_x=2
                                ff=False
                            else:
                                self.change_x=-2
                                ff=False
                        else:
                            self.change_x=random.choice([-2,2])
                            ff=False
                    elif self.rect.x==xx: #nếu boss ở cùng cột với người chơi
                        self.change_x=0   #Tương tự trên
                        if self.rect.y<yy:
                            if (self.rect.y+(576-yy)) <yy-self.rect.y:
                                self.change_y=-2
                                ff=False
                            else:
                                self.change_y=2
                                ff=False
                        elif self.rect.y>yy:
                            if (576-self.rect.y+yy) < self.rect.y-yy:
                                self.change_y=2
                                ff=False
                            else:
                                self.change_y=-2
                                ff=False
                        else:
                            self.change_y=random.choice([-2,2])
                            ff=False
                    if ff: # nếu boss ko cùng hàng cùng cột vs ngươi choi
                        d1=self.rect.x # vị trí x của boss
                        d2=self.rect.y #vị trí y cua boss
                        self.change_x = -2 #thu đi sang trái
                        self.change_y =0 
                        c1=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                        #vị trí từ người chs đến khi boss sang trái
                        self.rect.x=d1
                        self.rect.y=d2
                        #về vi trí ban dầu để thử tiếp
                        self.change_x = 2 #sang phải
                        self.change_y = 0
                        c2=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                        self.rect.x=d1
                        self.rect.y=d2
                        self.change_x = 0# lên trên
                        self.change_y = -2
                        c3=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                        self.rect.x=d1
                        self.rect.y=d2
                        self.change_x = 0
                        self.change_y = 2#xuống dưới
                        c4=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                        self.rect.x=d1
                        self.rect.y=d2
                        c5=min(c1,c2,c3,c4) #tìm khoảng cách min 4 TH
                        if c5==c1: #Nếu c5 là c1: sang trái
                            self.change_x = random.choice([-2, -2,-2,-4]) # cho random thỉnh thoảng boss đi nhanh hơn
                            self.change_y =0                             #để khi boss đuổi nếu cùng vị trí nó sẽ đè lên nhau 
                                                                #không nhìn thấy cho nó đi lên để tách ra
                        elif c5==c2: #Nếu sang phải là min
                            self.change_x = random.choice([2, 2,2,4])
                            self.change_y = 0
                        elif c5==c3:
                            self.change_x = 0
                            self.change_y = random.choice([-2,-2,-2,-4])
                        else:
                            self.change_x = 0
                            self.change_y = random.choice([2,2, 2,4])
                    
                elif self.rect.topleft in self.kiemtrahang(): # Nếu boss ko ở ngã 4 nhảy vào đây
                    #Nếu boss ở hàng
                    if yy==self.rect.y:   #Kiểm tra cùng hàng vơi player              
                        if self.rect.x<xx: #Tương tự
                            if (self.rect.x+(800-xx)) <xx-self.rect.x:
                                self.change_x=-2                    
                            else:
                                self.change_x=2              
                        elif self.rect.x>xx:
                            if (800-self.rect.x+xx) < self.rect.x-xx:
                                self.change_x=2          
                            else:
                                self.change_x=-2       
                        else:
                            self.change_x=random.choice([-2,2])  
                    else: #nếu ko chỉ ở hàng nào đó
                        tmp = 1 
                        d1=self.rect.x
                        d2=self.rect.y
                        #lấy ra vi trí boss
                        if d1==xx: #vi trí khác hàng cùng cột nhưng đang ở trong hàng 
                            self.kkk=True# nhảy vào if đầu tiên vì đây là vị trí boss sẽ ko di chuyển đc
                            self.kkk1=True#phải xử lý cách khác
                            tmp=0#đánh dấu để ko thực hiện ì dưới
                            self.change_x=0
                            self.change_y=0
                        if tmp==1:
                            #nếu vào đây: tính khoảng cách tìm đường đi tiếp
                            self.change_x = -2
                            self.change_y =0 
                                
                            c1=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                            self.rect.x=d1
                            self.rect.y=d2
                            self.change_x = 2
                            self.change_y = 0
                                    
                            c2=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                            self.rect.x=d1
                            self.rect.y=d2
                            c3 = min(c1,c2)
                            if c3==c1:
                                self.change_x = random.choice([-2, -2,-2,-4])
                                self.change_y =0 
                            else:
                                self.change_x = random.choice([2, 2,2,4])
                                self.change_y =0
                elif self.rect.topleft in self.kiemtracot(): #tương tự với kiểm tra hàng
                    if xx==self.rect.x:
                        if self.rect.y<yy:
                            if (self.rect.y+(576-yy)) <yy-self.rect.y:
                                self.change_y=-2
                            else:
                                self.change_y=2
                        elif self.rect.y>yy:
                            if (576-self.rect.y+yy) < self.rect.y-yy:
                                self.change_y=2
                            else:
                                self.change_y=-2
                        else:
                            self.change_y=random.choice([-2,2])
                    else: 
                        tmp = 1
                        d1=self.rect.x
                        d2=self.rect.y
                        if d2==yy:   #vị trí cũng đánh dấu kkk = true
                            #cùng hàng khác cột
                            self.kkk=True
                            self.kkk2=True
                            tmp=0 
                            self.change_x=0
                            self.change_y=0  
                        if tmp==1:
                            self.change_x =0
                            self.change_y =-2
                            c1=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                            self.rect.x=d1
                            self.rect.y=d2
                            self.change_x = 0
                            self.change_y = 2
                            c2=sqrt((xx-(self.rect.x+self.change_x))**2+(yy-(self.rect.y+self.change_y))**2)
                            self.rect.x=d1
                            self.rect.y=d2
                            c3 = min(c1,c2)
                            if c3==c1:
                                self.change_x = 0
                                self.change_y =random.choice([-2,-2,-2,-4])
                            else:
                                self.change_x = 0
                                self.change_y =random.choice([2,2,2,4])

        else: # dây là khi player đã ăn được viên đỏ
            if self.rect.topleft in self.get_intersection_position():#Nếu gặp ngã 4
                direction = random.choice(("left","right","up","down"))#random 4 hướng để chạy
                if direction == "left" and self.change_x == 0:
                    self.change_x = -2
                    self.change_y = 0
                elif direction == "right" and self.change_x == 0:
                    self.change_x = 2
                    self.change_y = 0
                elif direction == "up" and self.change_y == 0:
                    self.change_x = 0
                    self.change_y = -2
                elif direction == "down" and self.change_y == 0:
                    self.change_x = 0
                    self.change_y=2      
                

def enviroment():
        #ma trận: 0 là ko đi vào đó được, 3 là vị trí ngã 4, 2 là nét vẽ dọc, 1 là nét vẽ ngang
        if muc%3==1:#level 1
            grid = ((0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1,3,1,1,1),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0),
                    (0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0))
            
        elif muc%3==2:
            grid = ((0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0),
                    (1,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,3,1,1,1),
                    (0,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,2,0,0,0))
            
        else:
            grid = ((0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0,0,2,0,0,0,2,0),
                    (1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1,1,3,1,1,1,3,1))


        return grid


def draw_enviroment(screen):# vẽ máp
    global muc
    if muc%7==1:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                    pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
                elif item == 2:
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
    elif muc%7==2:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    pygame.draw.line(screen, GREEN , [j*32, i*32], [j*32+32,i*32], 3)
                    pygame.draw.line(screen, GREEN, [j*32, i*32+32], [j*32+32,i*32+32], 3)
                elif item == 2:
                    pygame.draw.line(screen, GREEN , [j*32, i*32], [j*32,i*32+32], 3)
                    pygame.draw.line(screen, GREEN , [j*32+32, i*32], [j*32+32,i*32+32], 3)
    elif muc%7==3:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    pygame.draw.line(screen, yellow , [j*32, i*32], [j*32+32,i*32], 3)
                    pygame.draw.line(screen, yellow, [j*32, i*32+32], [j*32+32,i*32+32], 3)
                elif item == 2:
                    pygame.draw.line(screen, yellow , [j*32, i*32], [j*32,i*32+32], 3)
                    pygame.draw.line(screen, yellow, [j*32+32, i*32], [j*32+32,i*32+32], 3)     
    else:
        #nếu hoàn thành 3 level
        screen.fill("black")
        image = pygame.image.load("phong5.png")
        screen.blit(image,(0,0))

                     
class Game(object): 
    def __init__(self):
        self.font = pygame.font.Font(None,40) #font
        self.about = False 
        self.game_over = True   #Kiểm soát trò chơi
        # Create the variable for the score
        global dem,lives
        self.check = False #kiểm soats ăn viên đỏ ch

        self.tmp=0 # để sau này xóa hết viên trắng chỉ hiện viên đỏ
        if dem==0: #nếu đếm =0 thì reset lv về 1 mang về 3(khi khơi tao tro choi moi)
            self.score = 0
            self.lv=1
            self.mang=3
        else:
            self.mang=lives# nếu ko mạg sẽ = lives
        global muc
        if self.lv==1:  #nếu lv=1 thì muc = 1 đễ vẽ máp
            muc=1
        
        self.enemies = pygame.sprite.Group()  #tạo nhóm các enemies   
        self.keu = 1 #để khi ăn viên đỏ song chỉ kêu 1 lần ko kêu lên 2
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()     
        self.vertical_blocks = pygame.sprite.Group()
        #lưu hàng, cột
        # Create a group for the dots on the screen
        self.dots_group = pygame.sprite.Group()   #tạo nhóm các viên để ăn            
        # Set the enviroment:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Create the enemies
        if self.lv==3:
        # # Add the dots inside the game
            for i, row in enumerate(enviroment()):
                for j, item in enumerate(row):
                    if item != 0:
                        self.dots_group.add(Ellipse(j*32+12,i*32+12,BLUE,8,8))   
                        #máp 3 nhì các viên khó nhìn đổi màu khác             
        else:
            for i, row in enumerate(enviroment()):
                for j, item in enumerate(row):
                    if item != 0:
                        self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))
        # Load the sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg") #âm thanh khi ăn hạt
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg") #game over
        self.nangcap_sound = pygame.mixer.Sound("res/sound/intermission.wav") #âm thanh nâg cấp
        
    def ktao1(self): 
        global zzz
        zzz=1 #kiểm soát mức, dễ , vừa , khó....    
        if self.lv==1:
                self.player = Player(32,128,"player.png")
                self.enemies.add(Slime(416,448,0,2,"slime.png"))
                self.enemies.add(Slime(460,64,2,0,"slime.png"))
                
                self.enemies.add(Slime(288,320,0,-2,"slime.png")) 
                self.enemies.add(Slime(288,96,0,2,"slime.png"))
        elif self.lv==2:
            self.player = Player(160,448,"player.png")
            self.enemies.add(Slime(288,96,0,2,"blue.png"))
            self.enemies.add(Slime(288,320,0,-2,"blue.png")) 
            self.enemies.add(Slime(448,448,-2,0,"blue.png"))
            self.enemies.add(Slime(672,256,0,-2,"blue.png"))
            self.enemies.add(Slime(640,128,-2,0,"blue.png"))
            
        elif self.lv==3:
            self.player = Player(512,64,"player.png")
            self.enemies.add(Slime(288,96,0,2,"cam.png"))
            self.enemies.add(Slime(288,320,0,-2,"cam.png")) 
            self.enemies.add(Slime(512,448,0,-2,"cam.png"))           
            self.enemies.add(Slime(320,320,-2,0,"cam.png"))
            self.enemies.add(Slime(64,512,0,2,"cam.png"))            
            self.enemies.add(Slime(320,512,-2,0,"cam.png"))  
             
    def ktao2(self):
        global zzz
        zzz=2
              
        if self.lv==1:
            self.player = Player(32,128,"player.png")
            self.enemies.add(Slime(288,96,0,2,"slime.png"))
            self.enemies.add(Slime(288,320,0,-2,"slime.png")) 
            self.enemies.add(Slime(416,448,0,2,"slime.png"))
            self.enemies.add(Slime(460,64,2,0,"slime.png"))
            self.enemies.add(Slime(288,448,2,0,"slime.png"))
                
        elif self.lv==2:
            self.player = Player(160,448,"player.png")
            self.enemies.add(Slime(288,96,0,2,"blue.png"))
            self.enemies.add(Slime(288,320,0,-2,"blue.png")) 
            self.enemies.add(Slime(448,448,-2,0,"blue.png"))
            self.enemies.add(Slime(672,256,0,-2,"blue.png"))
            self.enemies.add(Slime(640,128,-2,0,"blue.png"))
            self.enemies.add(Slime(64,128,2,0,"blue.png"))
    
        elif self.lv==3:
            self.player = Player(512,64,"player.png")
            self.enemies.add(Slime(288,96,0,2,"cam.png"))
            self.enemies.add(Slime(288,320,0,-2,"cam.png")) 
            self.enemies.add(Slime(512,448,0,-2,"cam.png"))           
            self.enemies.add(Slime(320,320,-2,0,"cam.png"))
            self.enemies.add(Slime(64,512,0,2,"cam.png"))          
            self.enemies.add(Slime(320,512,-2,0,"cam.png"))
            self.enemies.add(Slime(448,320,2,0,"cam.png"))
    def ktao3(self):
        global zzz
        zzz=3
        if self.lv==1:
            self.player = Player(32,128,"player.png")
            self.enemies.add(Slime(288,96,0,2,"slime.png"))
            self.enemies.add(Slime(288,320,0,-2,"slime.png")) 
            self.enemies.add(Slime(416,448,0,2,"slime.png"))
            self.enemies.add(Slime(460,64,2,0,"slime.png"))
            self.enemies.add(Slime(288,448,2,0,"slime.png"))
            self.enemies.add(Slime(320,320,-2,0,"slime.png"))
                
        elif self.lv==2:
            self.player = Player(160,448,"player.png")
            self.enemies.add(Slime(288,96,0,2,"blue.png"))
            self.enemies.add(Slime(288,320,0,-2,"blue.png")) 
            self.enemies.add(Slime(448,448,-2,0,"blue.png"))
            self.enemies.add(Slime(672,256,0,-2,"blue.png"))
            self.enemies.add(Slime(640,128,-2,0,"blue.png"))
            self.enemies.add(Slime(64,128,2,0,"blue.png"))
            self.enemies.add(Slime(256,288,-2,0,"blue.png"))
               
        elif self.lv==3:
            self.player = Player(512,64,"player.png")
            self.enemies.add(Slime(288,96,0,2,"cam.png"))
            self.enemies.add(Slime(288,320,0,-2,"cam.png")) 
            self.enemies.add(Slime(512,448,0,-2,"cam.png"))           
            self.enemies.add(Slime(320,320,-2,0,"cam.png"))
            self.enemies.add(Slime(64,512,0,2,"cam.png"))            
            self.enemies.add(Slime(320,512,-2,0,"cam.png"))
            self.enemies.add(Slime(448,320,2,0,"cam.png"))
            self.enemies.add(Slime(288,64,0,-2,"cam.png"))
    def ktao4(self):
        global zzz
        zzz=4
        if self.lv==1:
            self.player = Player(32,128,"player.png")
            self.enemies.add(Slime(288,96,0,2,"slime.png"))
            self.enemies.add(Slime(288,320,0,-2,"slime.png")) 
            self.enemies.add(Slime(416,448,0,2,"slime.png"))
            self.enemies.add(Slime(460,64,2,0,"slime.png"))
            self.enemies.add(Slime(288,448,2,0,"slime.png"))
            self.enemies.add(Slime(320,320,-2,0,"slime.png"))
            self.enemies.add(Slime(448,192,2,0,"slime.png"))
        elif self.lv==2:
            self.player = Player(160,448,"player.png")
            self.enemies.add(Slime(288,96,0,2,"blue.png"))
            self.enemies.add(Slime(288,320,0,-2,"blue.png")) 
            self.enemies.add(Slime(448,448,-2,0,"blue.png"))
            self.enemies.add(Slime(672,256,0,-2,"blue.png"))
            self.enemies.add(Slime(640,128,-2,0,"blue.png"))
            self.enemies.add(Slime(64,128,2,0,"blue.png"))
            self.enemies.add(Slime(256,288,-2,0,"blue.png"))
            self.enemies.add(Slime(352,288,2,0,"blue.png"))
        elif self.lv==3:
            self.player = Player(512,64,"player.png")
            self.enemies.add(Slime(288,96,0,2,"cam.png"))
            self.enemies.add(Slime(288,320,0,-2,"cam.png")) 
            self.enemies.add(Slime(512,448,0,-2,"cam.png"))           
            self.enemies.add(Slime(320,320,-2,0,"cam.png"))
            self.enemies.add(Slime(64,512,0,2,"cam.png"))           
            self.enemies.add(Slime(320,512,-2,0,"cam.png"))
            self.enemies.add(Slime(448,320,2,0,"cam.png"))
            self.enemies.add(Slime(288,64,0,-2,"cam.png"))
            self.enemies.add(Slime(288,448,0,2,"cam.png")) 
    def process_events(self): 
        if self.lv==4:# nếu vượt qua hết 3 level
            self.player.explosion = True  #đánh dấu nổ = true                       
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                sys.exit()
            # self.menu.event_handler(event)
            if self.game_over: #nếu gameover return(biến done sẽ = true trong hàm main để break)
                return True
            elif event.type == pygame.KEYDOWN: # nếu nhấn phím
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                
                elif event.key == pygame.K_ESCAPE:# nếu nhấn esc thoát 
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:# nếu nhả phím ra thì dừng di chuyển
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()   
        return False

    def run_logic(self):            
        global dem,lives # khi dem=0 là để khởi tạo, lives là mạg còn lại
        global zzz# kiểm soát mức dễ, vừa, khó...
        if self.score%25==0 and self.score>0 : #nếu điểm đã đủ 25
            self.player.update(self.horizontal_blocks,self.vertical_blocks) #update để player có thê di chuyển 
            self.game_over= self.player.game_over         
            if self.tmp==0: # xóa hết các viên thường để chỉ còn viên đỏ
                self.dots_group.empty()# xóa hết
                non_zero_positions = [] 
                for i, row in enumerate(enviroment()):
                    for j, item in enumerate(row):
                        if item != 0:                         
                            non_zero_positions.append((i, j))
                random_position = random.choice(non_zero_positions)
                i1, j1 = random_position   # vị trí random tại các vị trí mảng !=0            
                self.dots_group.add(Ellipse(j1*32+6,i1*32+6,RED,20,20))# thêm duy nhất 1 viên đỏ vào
            if self.check==False:  # nếu chưa ăn được viên đỏ                          
                block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)  
                #kiểm soát xem va chạm giữa người chơi và viên đỏ ch
                # biến true ở cuối là nếu = true viên đỏ biến mất                              
                if len(block_hit_list)>0:# nếu danh sách lớn hơn 0 là đã ăn dc
                # Here will be the sound effect                                        
                    self.check= True # đánh dấu đã ăn
                    self.pacman_sound.play()                  
            self.tmp=1# để ko nhảy vào tmp=0 nx chỉ vào 1 lần thôi
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks,self.player.rect.x,self.player.rect.y,self.check)
            #cập nhật vị trí các enemies nêú ko sẽ đứg yên
            if not self.game_over:#nếu trong quá trình đi ăn viên đỏ ch chết
                #self.player.update(self.horizontal_blocks,self.vertical_blocks)
                if self.check==False:#nếu ch ăn đc
                    block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
                    #nếu player và enemies va chạm vs nhau
                    if len(block_hit_list) > 0:#lớn hơn 0 là va chạm
                        self.player.explosion = True # nổ = true
                        if self.mang==1: # nếu còn mạg cuối
                            self.game_over_sound.play()    # thì chết             
                            dem=0
                            lives=3
                        else:
                            #ko thì mất 1 mạg
                            self.mang-=1
                            lives-=1
                            self.enemies.empty() #xóa hết các enemies thừa
                            if zzz==1:
                                self.ktao1()
                            elif zzz==2:
                                self.ktao2()
                            elif zzz==3:
                                self.ktao3()
                            elif zzz==4:
                                self.ktao4()
                                                                                
                    self.game_over = self.player.game_over 
                else:# vào đay là đã ăn đươc viên đỏ
                    if self.keu==1:#kêu 1 lần
                            self.nangcap_sound.play()
                            self.keu=2   #gán = 2 để ko kêu nx                                
                    if len(self.enemies)>0:
                        #kiểm tra va chạm người chs vs enemies
                        # = true ở cuối là nếu va chạm enemies biến mất
                        block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True) 
                        #self.pacman_sound.play()                   
                                          
                    if len(self.enemies)==0:   # nếu ko còn enemies thì qua màn              
                        dem+=1
                        self.tmp=0
                        self.check=False
                        self.lv+=1
                        global muc
                        muc+=1
                        self.score+=1           
                        self.__init__()
                        
                        if zzz==1:
                            self.ktao1()
                        elif zzz==2:
                            self.ktao2()
                        elif zzz==3:
                            self.ktao3()
                        elif zzz==4:
                            self.ktao4()
                        self.game_over=False                                        
                           
        if not self.game_over and (self.score%25!=0 or self.score==0):
            # đây laf trường hợp ch đủ 25 điểm
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            # các hàm tương tự bên trên
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)    
            if len(block_hit_list) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            
            if len(block_hit_list) > 0:
                self.player.explosion = True
                if self.mang==1:
                    self.game_over_sound.play()                 
                    dem=0
                    lives=3
                else:
                    self.mang-=1
                    lives-=1
                    self.enemies.empty()
                    if zzz==1:
                        self.ktao1()
                    elif zzz==2:
                        self.ktao2()
                    elif zzz==3:
                        self.ktao3()
                    elif zzz==4:
                        self.ktao4()                                                       
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks,self.player.rect.x,self.player.rect.y,self.check)
             
    
    def display_frame(self,screen):# đều là lệnh vẽ ra màn hình
        # First, clear the screen to white. Don't put other drawing commands
        if not self.game_over:   #vẽ phông         
            if self.lv==1:
                image = pygame.image.load("phong1.png")
            elif self.lv==2:
                image = pygame.image.load("phong4.png")
            elif self.lv==3:
                image = pygame.image.load("phong6.png")
            # else:
            #     image = pygame.image.load("phong5.png")           
        # else:
        #     image = pygame.image.load("phong.png")
            if self.lv!=4:
                screen.fill(BLACK)
                screen.blit(image, (0,0))        
        # --- Drawing code should go here
        if not self.game_over:
            # --- Draw the game here ---
            # self.horizontal_blocks.draw(screen)
            # self.vertical_blocks.draw(screen)
            #nếu game ch kết thúc vẽ máp vẽ viên để ăn, vẽ enemies.....
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            #screen.blit(text, (30, 650))
            # Render the text for the score
            if self.lv%3==2:
                text = self.font.render("Score: " + str(self.score),True,RED)
                # Put the text on the screen
                screen.blit(text,[0,80])
                level =self.font.render("Level: "+str(self.lv),True,RED)
                screen.blit(level,[0,240])
                res=self.font.render("Mang: "+str(self.mang),True,RED)
                screen.blit(res,[0,400])
            elif self.lv==1:
                text = self.font.render("Score: " + str(self.score),True,GREEN)
                # Put the text on the screen
                screen.blit(text,[64,20])
                level =self.font.render("Level: "+str(self.lv),True,GREEN)
                screen.blit(level,[320,20])
                res =self.font.render("Mang: "+str(self.mang),True,GREEN)
                screen.blit(res,[580,20])
            else:
                text = self.font.render("Score",True,RED)
                # Put the text on the screen
                screen.blit(text,[200,20])
                text = self.font.render(str(self.score),True,RED)
                # Put the text on the screen
                screen.blit(text,[220,60])
                level =self.font.render("Level",True,RED)
                screen.blit(level,[424,20])
                level =self.font.render(str(self.lv),True,RED)
                screen.blit(level,[450,60])
                res =self.font.render("Mang",True,RED)
                screen.blit(res,[650,20])
                res =self.font.render(str(self.mang),True,RED)
                screen.blit(res,[670,60])
        else:
            if self.lv==4:
                image = pygame.image.load("phong.png")
                screen.blit(image, (0,0))
                s =self.font.render("Ban da chien thang tro choi",True,RED) 
                screen.blit(s,[230,100]) 
                pygame.display.flip()
                global dem
                dem=0 
            else:
                image = pygame.image.load("phong.png")
                screen.blit(image, (0,0))
                s =self.font.render("GAME OVER",True,RED)
                screen.blit(s,[330,200])
                s =self.font.render("Score: "+str(self.score),True,RED)
                screen.blit(s,[350,240])
                s =self.font.render("Ban chet o level: "+str(self.lv),True,RED) 
                screen.blit(s,[290,280])
                s =self.font.render("Bam space de choi lai",True,BLUE) 
                screen.blit(s,[260,320])                  
        pygame.display.flip()

