import pygame,sys
import car_game , jumper ,FlappyBirdKnockOff, ping_pong #, shooter , tictactoe

#to start pygame
pygame.init()

#window and its attributes
window_width=960
window_height=503
window_size=(window_width,window_height)
window=pygame.display.set_mode(window_size)

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
        self.rect1=self.image1.get_rect(topleft=position)
        self.image2=pygame.image.load(path2).convert_alpha()
        self.rect2=self.image2.get_rect(topleft=position)

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
    
    background=pygame.image.load('assets/menu_assets/background_1.png').convert_alpha()
    
    #to animate the button by changing the image
    b_index=0
    b_flag=True
    
    #button attributes and button definition 
    button_xpos=385
    button_ypos=210
    button1=Button('assets/menu_assets/start2.png',(button_xpos,button_ypos),'assets/menu_assets/start1.png')
    button2=Button('assets/menu_assets/start3.png',(button_xpos,button_ypos),'assets/menu_assets/start1.png')
    
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
        ##clock.tick(60)
    
    #to change the screen to main menu
    if clicked:return main_menu()

#main menu of the game
def main_menu():
    
    background=pygame.image.load('assets/menu_assets/background_1.png').convert_alpha()
    
    #to create 4 buttons
    button1=Button('assets/menu_assets/button_spooder-car.png',(115,100),'assets/menu_assets/button_spooder-car(1).png')
    button2=Button('assets/menu_assets/button_kalahalla.png',(650,100),'assets/menu_assets/button_kalahalla(1).png')
    button3=Button('assets/menu_assets/button_flappy-thaav.png',(115,300),'assets/menu_assets/button_flappy-thaav(1).png')
    button4=Button('assets/menu_assets/button_back.png',(650,300),'assets/menu_assets/button_back(1).png')
    ##a=0;print(a)
    #main loop of main menu
    while True:
        for event in pygame.event.get():    #to quit the game
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.blit(background,(0,0))

        #to move to the actual game based on the button clicked by the user
        if button1.draw():
            bgm.stop()
            return car_game.spooder_car()
        
        elif button2.draw():
            return jumper.game()
        
        elif button3.draw():
            bgm.stop()
            return FlappyBirdKnockOff.game_pause_start()
        
        elif button4.draw():
            return opening_screen()
        
        #to update the screen and to control fps
        pygame.display.update()
        ##clock.tick(60)
        ##a+=1;print(a)
        

flag=opening_screen()   #to check if user wants to return to main menu

#this loop allows the player to return to main menu at any time
while flag:
    pygame.init()
    window=pygame.display.set_mode(window_size)
    bgm.play(loops=-1)
    main_menu()