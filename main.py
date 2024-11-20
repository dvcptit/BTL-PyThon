
import pygame, sys
from game2 import *
from button import Button
SCREEN_WIDTH = 800 #chieu dai
SCREEN_HEIGHT = 576 #chieu rong
BLACK =(0,0,0)
pygame.init()  #khoi tao
WHITE=(255,255,255)
click_sound = pygame.mixer.Sound("assets/munch_2.wav") #nhac khi click chuot
begin=pygame.mixer.Sound("res/sound/begin.wav") #nhac bat dau tro choi
score_Super_hard, score_Hard, score_normal, score_Easy=0,0,0,0 # luu diem
bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard=0,0,0,0 #luu bestscore
chon=0 # Danh dau chọn mức dễ=1, vừa=2 , khó=3,siêu khó =4

def rule():
    while True:
        RULE_MOUSE_POS = pygame.mouse.get_pos() #tra ve vi tri chuot
        screen.fill("black") #xoa man hinh           
        image = pygame.image.load("phong.png") #load phong nen
        screen.blit(image,(0,0))            
        s =game.font.render("Nhóm 12:",True,RED)
        screen.blit(s,[330,150])
        s =game.font.render("Ban can tranh enemies va kiem 25 diem",True,RED)
        screen.blit(s,[200,180]) 
        s =game.font.render("Ban se co 3 mang de vuot qua 3 lv",True,RED)
        screen.blit(s,[200,210])
        s =game.font.render("Choi ngay nao!",True,RED) 
        screen.blit(s,[300,240])  

        RULE_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(40), base_color="white", hovering_color="Green")
        #Tao nut Back de quay ve
        RULE_BACK.changeColor(RULE_MOUSE_POS) #Doi mau khi di chuot den back
        RULE_BACK.update(screen)  # update

        for event in pygame.event.get():   #Kiem tra cac su kien
            if event.type == pygame.QUIT:   #Bam but x thoat game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:   #Kiem tra click chuot
                click_sound.play()                     #Phat ra tieng
                if RULE_BACK.checkForInput(RULE_MOUSE_POS):#Kiem tra click nut back
                    main_menu()

        pygame.display.update()       #Cap nhat man hinh
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
    # Set the width and height of the screen [width, height]
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
pygame.display.set_caption("PACMAN")
    
#Loop until the user clicks the close button.
pacman_screen_play = pygame.image.load("assets/pacman_screen.jpg") #gan hinh anh
pacman_screen_play_width,pacman_screen_play_height =pacman_screen_play.get_size() #Lay chieu dai,chieu rong
scale_x_P= (SCREEN_WIDTH/pacman_screen_play_width)*0.6
scale_y_P= (SCREEN_HEIGHT/pacman_screen_play_height)*0.6
#Gan hinh anh theo dinh dang
scaled_image_pacman = pygame.transform.scale(pacman_screen_play, (int(pacman_screen_play_width * scale_x_P), int(pacman_screen_play_height * scale_y_P)))   

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Create a game object
game = Game()   
   
def play():
    global chon #luu chon muc de,kho,...
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()   #Lay kich thuoc chuot
        screen.fill("black")     #xoa man hinh
        screen.blit(scaled_image_pacman,(165,150)) #IN man hinh vi tri 165,150
        
        EASY_BUTTON = Button(image=None, pos=(400, 50), 
                            text_input="EASY_MODE", font=get_font(25), base_color="White", hovering_color="Green")
        #Tao button easy
        EASY_BUTTON.changeColor(PLAY_MOUSE_POS)
        EASY_BUTTON.update(screen)
        #normal
        NORMAL_BUTTON = Button(image=None, pos=(400, 100), 
                            text_input="NORMAL_MODE", font=get_font(25), base_color="White", hovering_color="Green")
        NORMAL_BUTTON.changeColor(PLAY_MOUSE_POS)
        NORMAL_BUTTON.update(screen)
        #hard
        HARD_BUTTON = Button(image=None, pos=(400, 150), 
                            text_input="HARD_MODE", font=get_font(25), base_color="White", hovering_color="Green")
        HARD_BUTTON.changeColor(PLAY_MOUSE_POS)
        HARD_BUTTON.update(screen)
        #super_hard 
        SUPER_HARD_BUTTON = Button(image=None, pos=(400, 200), 
                            text_input="SUPER_HARD_MODE", font=get_font(25), base_color="White", hovering_color="Green")
        SUPER_HARD_BUTTON.changeColor(PLAY_MOUSE_POS)
        SUPER_HARD_BUTTON.update(screen)
        PLAY_BACK = Button(image=None, pos=(400, 500), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
        #black
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)
        for event in pygame.event.get(): #Kiem tra su kien
            if event.type == pygame.QUIT: #Kiem tra bam x
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #Click chuot
                click_sound.play() 
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS): #Click easy
                    # Easy.reset() 
                    game.__init__() #khoi tao game
                    chon=1     #Danh dau chon mức dễ =1
                    game.ktao1() #Khoi tao muc de
                    game.game_over=False   #Danh dau game ch ket thuc
                    easy_mode()  #goi ham    
                if NORMAL_BUTTON.checkForInput(PLAY_MOUSE_POS): #Tuong tu easy
                    # normal.reset() 
                    chon=2           
                    game.__init__()
                    game.ktao2()
                    game.game_over=False
                    normal_mode()
                if HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    # Hard.reset()
                    chon=3
                    game.__init__()
                    game.ktao3()
                    game.game_over=False
                    hard_mode()
                if SUPER_HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    # Super_hard.reset()
                    chon=4
                    game.__init__()
                    game.ktao4()
                    game.game_over=False
                    super_hard_mode()
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):# bam back de ve menu
                    main_menu()

        pygame.display.update() #Cap nhat man hinh
def Score(check):
    global bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard
    global score_Super_hard, score_Hard, score_normal, score_Easy
    s="SCORE "
    ok=0 #kiem tra co tao ki luc moi hay ko
    if check == 1: #muc de
        score_Easy = game.score #Lay ra diem
        if(score_Easy > bestScore_easy): #Cap nhat bestscore
            bestScore_easy = score_Easy
            ok = 1 #Danh dau da co ki luc moi
        s = s + "EASY: " + str(score_Easy)
    elif check == 2:#muc vua
        score_normal = game.score
        if(score_normal > bestScore_normal):
            bestScore_normal = score_normal
            ok = 1
        s += "NORMAL: " + str(score_normal)
    elif check == 3:#muc kho
        score_Hard = game.score
        if(score_Hard > bestScore_hard):
            bestScore_hard = score_Hard
            ok = 1
        s += "HARD: " + str(score_Hard)
    else: #muc sieu kho
        score_Super_hard = game.score
        if(score_Super_hard > bestScore_Super_hard):
            bestScore_Super_hard = score_Super_hard
            ok = 1
        s += "SUPER HARD: " + str(score_Super_hard)
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos() #Lay con tro chuot
        screen.fill("black") #Xoa man hinh
        screen.blit(scaled_image_pacman,(165,150)) #In hinh anh
        if(ok == 1): #In ki luc:
            tmp = Button(image=None, pos=(410, 60), 
                            text_input="Ban da tao duoc ki luc moi !!!", font=get_font(15), base_color="yellow", hovering_color="Green")
            tmp.changeColor(PLAY_MOUSE_POS)
            tmp.update(screen)
        cur_score = Button(image=None, pos=(415, 35), 
                            text_input=s , font=get_font(10), base_color="pink", hovering_color="Green")
        #Hien thi xau s duoi dang button
        cur_score.changeColor(PLAY_MOUSE_POS)
        cur_score.update(screen)
        #H.
        KY_LUC = Button(image=None, pos=(415, 100), 
                            text_input="BEST SCORE" , font=get_font(20), base_color="GREEN", hovering_color="Green")
        KY_LUC.changeColor(PLAY_MOUSE_POS)
        #Hien thi button noi dung best score
        KY_LUC.update(screen)

        EASY = Button(image=None, pos=(415, 125), 
                            text_input="EASY: " + str(bestScore_easy) , font=get_font(15), base_color="GREEN", hovering_color="Green")
        EASY.changeColor(PLAY_MOUSE_POS)
        #Hien thi button easy
        EASY.update(screen)

        NORMAL = Button(image=None, pos=(415, 150), 
                            text_input="NORMAL: " + str(bestScore_normal) , font=get_font(15), base_color="GREEN", hovering_color="Green")
        #Tuong tu
        NORMAL.changeColor(PLAY_MOUSE_POS)
        NORMAL.update(screen)

        HARD = Button(image=None, pos=(415, 175), 
                            text_input="HARD: " + str(bestScore_hard) , font=get_font(15), base_color="GREEN", hovering_color="Green")
        HARD.changeColor(PLAY_MOUSE_POS)
        HARD.update(screen)

        SUPER_HARD = Button(image=None, pos=(415, 200), 
                            text_input="SUPER HARD: " + str(bestScore_Super_hard) , font=get_font(15), base_color="GREEN", hovering_color="Green")
        SUPER_HARD.changeColor(PLAY_MOUSE_POS)
        SUPER_HARD.update(screen)
        PLAY_BACK = Button(image=None, pos=(30, 515), 
                            text_input="BACK", font=get_font(10), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get(): #Kiem tra su kien
            if event.type == pygame.QUIT: #Bam x
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:# Kiem tra click chuot
                click_sound.play() 
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):# quay lai play
                    play()

        pygame.display.update() 
def easy_mode():
    global bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard
    global chon
    begin.play() #phat nhac bat dau game
    if game.check:        
        pygame.mixer.stop()
    done=False #Kiem soat da chet hay ch
    while not done:
            done = game.process_events() #Tra ve true false de thoat vong lap
            game.run_logic() # cac chuong trinh cua game
            game.display_frame(screen) #Cap nhat man hinh
            clock.tick(40)  #Toc do cap nhat khung hinh 
    while True:
        EASY_MOUSE_POS = pygame.mouse.get_pos() #Lay ra con tro chuot
        EASY_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        #Tao button back
        EASY_BACK.changeColor(EASY_MOUSE_POS)
        EASY_BACK.update(screen)
        
        
        for event in pygame.event.get(): #Kiem tra su kien
            if event.type == pygame.QUIT: # thoat game
                pygame.quit()
                sys.exit()
                # play()
            if event.type == pygame.KEYDOWN: #kiem tra bấm bàn phím
                if event.key == pygame.K_SPACE: # Kiểm tra có nhấn space de choi lai ko
                    if chon==1: #Neu dang o muc de
                        if game.score > bestScore_easy: #Cap nhat bestscore o day vi khi nhan space choi lai ko vao ham score
                            bestScore_easy=game.score
                    elif chon==2:  #Neu dang o mua vua
                        if game.score> bestScore_normal:
                            bestScore_normal=game.score
                    elif chon==3:
                        if game.score>bestScore_hard:
                            bestScore_hard=game.score
                    else:
                        if game.score> bestScore_Super_hard:
                            bestScore_Super_hard=game.score
                    game.__init__() #khoi tao lai tro choi khi choi lai
                    game.game_over=False   #danh dau tro choi ch ket thuc
                    if chon==1: #Neu dang o muc de thì gọi khởi tạo 1
                        game.ktao1()
                    elif chon==2:
                        game.ktao2()
                    elif chon==3:
                        game.ktao3()
                    else:
                        game.ktao4()
                    easy_mode() # goi lai choi tiep
            if event.type == pygame.MOUSEBUTTONDOWN: #Neu click chuot
                click_sound.play() 
                if EASY_BACK.checkForInput(EASY_MOUSE_POS):
                    Score(1) #In diem va bestscore
        pygame.display.update() #Cap nhat man hinh
    
def normal_mode():#Tuong tu easy mode
    global bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard
    global chon
    begin.play()
    if game.check:         
        pygame.mixer.stop()
    done=False
    while not done:
            done = game.process_events()
            game.run_logic()
            game.display_frame(screen)
            clock.tick(40)   
            
    while True:
        NORMAL_MOUSE_POS = pygame.mouse.get_pos()
        
        NORMAL_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        NORMAL_BACK.changeColor(NORMAL_MOUSE_POS)
        NORMAL_BACK.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if chon==1:
                        if game.score > bestScore_easy:
                            bestScore_easy=game.score
                    elif chon==2:
                        if game.score> bestScore_normal:
                            bestScore_normal=game.score
                    elif chon==3:
                        if game.score>bestScore_hard:
                            bestScore_hard=game.score
                    else:
                        if game.score> bestScore_Super_hard:
                            bestScore_Super_hard=game.score
                    game.__init__()
                    game.game_over=False
                    if chon==1:
                        game.ktao1()
                    elif chon==2:
                        game.ktao2()
                    elif chon==3:
                        game.ktao3()
                    else:
                        game.ktao4()
                    normal_mode()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play() 
                if NORMAL_BACK.checkForInput(NORMAL_MOUSE_POS):
                    Score(2) 
        pygame.display.update()
def hard_mode(): #Tuong tu easy mode
    global bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard
    global chon
    begin.play()
    if game.check:         
        pygame.mixer.stop()
    done=False
    while not done:
            done = game.process_events()
            game.run_logic()
            game.display_frame(screen)
            clock.tick(40)   
            
        # main_menu
    while True:
        HARD_MOUSE_POS = pygame.mouse.get_pos()
        # screen.fill("black")
        # screen.blit(scaled_image_pacman,(165,100))
        HARD_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        HARD_BACK.changeColor(HARD_MOUSE_POS)
        HARD_BACK.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if chon==1:
                        if game.score > bestScore_easy:
                            bestScore_easy=game.score
                    elif chon==2:
                        if game.score> bestScore_normal:
                            bestScore_normal=game.score
                    elif chon==3:
                        if game.score>bestScore_hard:
                            bestScore_hard=game.score
                    else:
                        if game.score> bestScore_Super_hard:
                            bestScore_Super_hard=game.score
                    game.__init__()
                    game.game_over=False
                    if chon==1:
                        game.ktao1()
                    elif chon==2:
                        game.ktao2()
                    elif chon==3:
                        game.ktao3()
                    else:
                        game.ktao4()
                    hard_mode()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play() 
                if HARD_BACK.checkForInput(HARD_MOUSE_POS):
                    Score(3) 
        pygame.display.update()
def super_hard_mode(): #Tuong tu easy mode
    global bestScore_easy, bestScore_normal, bestScore_hard, bestScore_Super_hard
    global chon
    begin.play()
    if game.check:         
        pygame.mixer.stop()
    done=False
    while not done:
            done = game.process_events()
            game.run_logic()
            game.display_frame(screen)
            clock.tick(40)   
            
        # main_menu
    while True:
        SUPER_HARD_MOUSE_POS = pygame.mouse.get_pos()
        # screen.fill("black")
        # screen.blit(scaled_image_pacman,(165,100))
        SUPER_HARD_BACK = Button(image=None, pos=(400, 400), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        SUPER_HARD_BACK.changeColor(SUPER_HARD_MOUSE_POS)
        SUPER_HARD_BACK.update(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if chon==1:
                        if game.score > bestScore_easy:
                            bestScore_easy=game.score
                    elif chon==2:
                        if game.score> bestScore_normal:
                            bestScore_normal=game.score
                    elif chon==3:
                        if game.score>bestScore_hard:
                            bestScore_hard=game.score
                    else:
                        if game.score> bestScore_Super_hard:
                            bestScore_Super_hard=game.score
                    game.__init__()
                    game.game_over=False
                    if chon==1:
                        game.ktao1()
                    elif chon==2:
                        game.ktao2()
                    elif chon==3:
                        game.ktao3()
                    else:
                        game.ktao4()
                    super_hard_mode()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play() 
                if SUPER_HARD_BACK.checkForInput(SUPER_HARD_MOUSE_POS):
                    Score(4) 
        pygame.display.update()
def main_menu(): 
    # BG = pygame.image.load("phong.png")
    BG = pygame.image.load("assets/Background_pacman.png") #Gan hinh anh
    BG_width,BG_height = BG.get_size() #Lay ra kich thuoc
    scale_x_BG= (SCREEN_WIDTH/BG_width)
    scale_y_BG= (SCREEN_HEIGHT/BG_height)
    #Lay hinh anh theo dinh dang
    scaled_image_BG = pygame.transform.scale(BG, (int(BG_width * scale_x_BG),
                int(BG_height * scale_y_BG)))
    while True:
        screen.blit( scaled_image_BG, (0, 0)) #In hinh anh len man hinh
        MENU_MOUSE_POS = pygame.mouse.get_pos() #Lay ra con tro chuot
        PLAY_BUTTON = Button(image=None, pos=(400, 355), 
                                text_input="PLAY", font=get_font(25), base_color="#FF0000", hovering_color="White")
        #tao button play
        RULE_BUTTON = Button(image=None, pos=(400, 400), 
                                text_input="RULES", font=get_font(25), base_color="#FF0000", hovering_color="White")
        #tao butto rule
        QUIT_BUTTON = Button(image=None, pos=(400, 450), 
                                text_input="QUIT", font=get_font(25), base_color="#FF0000", hovering_color="White")
        #tao button quit
        for button in [PLAY_BUTTON, RULE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
                                
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play() 
                if game.game_over and not game.about:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): #Neu click vao choi thì play()   
                        play()                                                                             
                    if RULE_BUTTON.checkForInput(MENU_MOUSE_POS):
                            # --- ABOUT ------
                        rule()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                            # --- EXIT -------
                            # User clicked exit
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
if __name__ == '__main__':
    main_menu()
