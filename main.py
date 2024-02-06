import pygame,sys,subprocess,platform
import car_game , jumper ,FlappyBirdKnockOff, ping_pong , tictactoe ,jumpersingleplayer,shooter,boom
current_os = platform.system()
#to start pygame
pygame.init()
pygame.mixer.init()

#window and its attributes
window_width=900
window_height=514
window_size=(window_width,window_height)
window=pygame.display.set_mode(window_size)
pygame.display.set_caption('THE ARCADE ODYSSEY')

#menu background music
bgm=pygame.mixer.Sound('assets/menu_assets/menu_music.mp3')
bgm.play(loops=-1)

#to regulate framerate
clock=pygame.time.Clock()

#button class to re-use the logic for clicking
class Button:
    #init function is given to get the attributes of the button
    def __init__(self,path1,position,path2) -> None:
        self.image1=pygame.image.load(path1).convert_alpha()
        self.rect1=self.image1.get_rect(center=position)
        self.image2=pygame.image.load(path2).convert_alpha()
        self.rect2=self.image2.get_rect(center=position)

    #drawing , hovering and clicking logic
    def draw(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.rect1.collidepoint(mouse_pos):
            window.blit(self.image2,self.rect2)
            if True in pygame.mouse.get_pressed():
                return True
        else:
            window.blit(self.image1,self.rect1)
            return False

# opening screen of the game
def opening_screen():
    
    background=pygame.image.load('assets/menu_assets/background.png').convert_alpha()
    
    #to animate the button by changing the image
    b_index=0
    b_flag=True
    
    #button attributes and button definition 
    button_xpos=window_width//2
    button_ypos=window_height//2
    button1=Button('assets/menu_assets/start1.png',(button_xpos,button_ypos),'assets/menu_assets/start3.png')
    button2=Button('assets/menu_assets/start2.png',(button_xpos,button_ypos),'assets/menu_assets/start3.png')
    
    #to check if the button was clicked
    clicked=False
    
    #main loop for the opening screen
    while not(clicked):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: #to quit the game
                pygame.quit()
                sys.exit()
        
        window.blit(background,(0,0))
        
        #button animation
        #whenever b_index becomes an int, the b_flag becomes T/F 
        b_index+=0.1
        if int(b_index):
            b_flag=not(b_flag)
            b_index=0
        if b_flag:
            clicked=button1.draw()
        else:
            clicked=button2.draw()
        
        #to update screen and to control fps
        pygame.display.update()
        clock.tick(100)
    
    #to change the screen to main menu
    if clicked:return main_menu()

#main menu of the game
def main_menu():
    
    background=pygame.image.load('assets/menu_assets/background.png').convert_alpha()
    
    #to create 4 buttons
    h=int(160*(2/3))
    kalahalla_button=Button('assets/menu_assets/kalahalla1.png',(250,h),'assets/menu_assets/kalahalla2.png')
    flappy_button=Button('assets/menu_assets/flappy1.png',(650,h),'assets/menu_assets/flappy2.png')
    spidercar_button=Button('assets/menu_assets/spidercar1.png',(250,2*h),'assets/menu_assets/spidercar2.png')
    pong_button=Button('assets/menu_assets/pong1.png',(650,2*h),'assets/menu_assets/pong2.png')
    shooter_button=Button('assets/menu_assets/shooter1.png',(250,3*h),'assets/menu_assets/shooter2.png')
    tictactoe_button=Button('assets/menu_assets/tictactoe1.png',(650,3*h),'assets/menu_assets/tictactoe2.png')
    dino_button=Button('assets/menu_assets/dino1.png',(250,4*h),'assets/menu_assets/dino2.png')
    back_button=Button('assets/menu_assets/back1.png',(650,4*h),'assets/menu_assets/back2.png')
    controls_button=Button('assets/menu_assets/controls_button_1.png',(window_width-23,23),'assets/menu_assets/controls_button_2.png')
    clicked=False

    #main loop of main menu
    while True:
        for event in pygame.event.get():    #to quit the game
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                return opening_screen()
            
        window.blit(background,(0,0))

        #to move to the actual game based on the button clicked by the user
        if kalahalla_button.draw():
            return kalahallachoice()
        
        elif flappy_button.draw():
            bgm.stop()
            return FlappyBirdKnockOff.game_pause_start()
        
        elif spidercar_button.draw():
            bgm.stop()
            return car_game.spooder_car()
        
        elif pong_button.draw():
            bgm.stop()
            return ping_pong.game()
        
        elif shooter_button.draw():
            bgm.stop()
            pygame.quit()
            return shooter.maingame()

        elif tictactoe_button.draw():
            bgm.stop()
            return tictactoe.game()

        elif dino_button.draw():
            bgm.stop()
            boom.game()
            

        elif back_button.draw():
            return opening_screen()
        

        elif controls_button.draw() and not(clicked):
           if current_os == 'Darwin':  # macOS
                subprocess.run(['open', 'assets/CONTROLS.txt'])
           elif current_os == 'Windows':
                    subprocess.run(['start', 'assets/CONTROLS.txt'], shell=True)

        #to update the screen and to control fps
        pygame.display.update()
        ##clock.tick(60)
        ##a+=1;print(a)
        
def kalahallachoice():
    background=pygame.image.load('assets/menu_assets/background.png').convert_alpha()
    singleplayer=Button('assets/menu_assets/single-player1.png',(300,200),'assets/menu_assets/single-player2.png')
    multiplayer=Button('assets/menu_assets/multiplayer1.png',(600,200),'assets/menu_assets/multiplayer2.png')
    #main loop of main menu
    while True:
        for event in pygame.event.get():    #to quit the game
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                return main_menu()
            
        window.blit(background,(0,0))
        issingleplayer = singleplayer.draw()
        ismultiplayer = multiplayer.draw()
        
        if issingleplayer:
            bgm.stop()
            a = jumpersingleplayer.menu()
            
        elif ismultiplayer:
            bgm.stop()
            b = jumper.menu()
            
        #to move to the actual game based on the button clicked by the user
       
        
        
        
        #to update the screen and to control fps
        pygame.display.update()
        ##clock.tick(60)
        ##a+=1;print(a)

flag=opening_screen()   #to check if user wants to return to main menu

#this loop allows the player to return to main menu at any time
while flag:
    pygame.init()
    window=pygame.display.set_mode(window_size)
    pygame.display.set_caption('THE ARCADE ODYSSEY')
    bgm.play(loops=-1)
    main_menu()
