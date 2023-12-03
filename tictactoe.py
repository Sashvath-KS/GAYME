import pygame , sys

#to start pygame
#pygame.init()

def game():
    #window and its attributes
    window_width=500
    window_height=600
    window_size=(window_width,window_height)
    window=pygame.display.set_mode(window_size)

    #to regulate framerate
    clock=pygame.time.Clock()

    #button class to re-use the logic for clicking
    class Button:
        #init function is given to get the attributes of the button
        def __init__(self,path1,position,path2,player) -> None:
            self.image1=pygame.image.load(path1).convert_alpha()
            self.rect1=self.image1.get_rect(center=position)
            self.image2=pygame.image.load(path2).convert_alpha()
            self.rect2=self.image2.get_rect(center=position)

        #drawing , hovering and clicking logic
        def draw(self):
            nonlocal player
            mouse_pos=pygame.mouse.get_pos()
            if self.rect1.collidepoint(mouse_pos):
                if player==0:window.blit(self.image2,self.rect2)
                if True in pygame.mouse.get_pressed():
                    if player==1:
                        window.blit(self.image1,self.rect1)
                    elif player==-1:
                        window.blit(self.image2,self.rect2)
                    return True
            else:
                if player==0:window.blit(self.image1,self.rect1)
                return False
            


    opening_screen=pygame.image.load('assets/tictactoe_assets/opening_screen.jpeg')
    window.blit(opening_screen,(0,0))
    button1=Button('assets/tictactoe_assets/circle_option.jpeg',
                (125,350),'assets/tictactoe_assets/circle_select.jpeg',0)
    button2=Button('assets/tictactoe_assets/cross_option.jpeg',
                (375,350),'assets/tictactoe_assets/cross_select.jpeg',0)

    game_active=False
    game_state=0
    end=False
    player=0
    def player_choice():
        nonlocal player,game_active
        if button1.draw():
            player=1
            game_screen=pygame.image.load('assets/tictactoe_assets/tictactoe_2.jpeg')
            window.blit(game_screen,(0,0))
            game_active=True
            pygame.time.delay(500)
        elif button2.draw():
            player=-1
            game_screen=pygame.image.load('assets/tictactoe_assets/tictactoe_1.jpeg')
            window.blit(game_screen,(0,0))
            game_active=True
            pygame.time.delay(500)

    grid_state=[[0,[0 for i in range(9)],True] for j in range(9)]
    grid_pos=[
        [(51, 159), (100, 160), (146, 161), 
         (51, 210), (100, 208), (148, 208), 
         (51, 256), (98, 253), (146, 253)], 
         
         [(202, 159), (251, 160), (298, 159), 
          (201, 210), (249, 206), (296, 208), 
          (202, 255), (251, 257), (297, 254)], 
          
          [(351, 157), (400, 162), (447, 159), 
           (352, 206), (401, 208), (448, 206), 
           (354, 254), (397, 254), (443, 257)], 
           
           [(51, 310), (98, 311), (147, 310), 
            (52, 358), (99, 358), (146, 356), 
            (52, 404), (99, 404), (145, 406)], 
            
            [(204, 310), (252, 310), (295, 308), 
             (200, 355), (248, 357), (296, 357), 
             (203, 403), (252, 404), (295, 403)], 
             
             [(352, 307), (400, 308), (445, 308), 
              (352, 358), (402, 356), (447, 354), 
              (354, 400), (402, 402), (446, 402)], 
              
              [(51, 458), (98, 458), (143, 458), 
               (52, 508), (98, 505), (146, 507), 
               (50, 555), (99, 554), (146, 552)], 
               
               [(205, 458), (252, 460), (294, 460), 
                (203, 508), (250, 508), (298, 506), 
                (201, 554), (250, 554), (297, 554)], 
                
                [(355, 457), (400, 458), (448, 458), 
                 (354, 508), (400, 506), (448, 506), 
                 (351, 554), (401, 555), (450, 554)]
        ]
    
    button_list=[]
    for i in range(len(grid_pos)):
        button_list.append([])
        for j in grid_pos[i]:
            button_list[i].append(
                Button('assets/tictactoe_assets/circle.png',
                    j,'assets/tictactoe_assets/cross.png',1)
                )
    def refresh(bool):
        for i in range(9):
            if grid_state[i][0]==0:
                grid_state[i][2]=bool

    def capture(i,player):
        flag=False
        if grid_state[i][1][0]==player:
            if grid_state[i][1][1] ==player and  grid_state[i][1][2] == player:
                flag=True
            elif grid_state[i][1][3] ==player and grid_state[i][1][6] == player:
                flag=True
            elif grid_state[i][1][4] == player and grid_state[i][1][8] == player:
                flag=True
        elif grid_state[i][1][1]==player:
            if grid_state[i][1][4]==player and grid_state[i][1][7]==player:
                flag=True
        elif grid_state[i][1][2]==player:
            if grid_state[i][1][4] == player and grid_state[i][1][6] == player:
                flag=True
            elif grid_state[i][1][5]==player and grid_state[i][1][8]==player:
                flag=True
        elif grid_state[i][1][3]==player:
            if grid_state[i][1][4]==player and grid_state[i][1][5]==player:
                flag=True
        elif grid_state[i][1][6]==player:
            if grid_state[i][1][7]==player and grid_state[i][1][8]==player:
                flag=True
        
        if flag and grid_state[i][0]==0:
            grid_state[i][0]=player
            if player==1:
                image=pygame.image.load('assets/tictactoe_assets/circle_global.png').convert_alpha()
                rect=image.get_rect(center=grid_pos[i][4])
                window.blit(image,rect)

            elif player==-1:
                image=pygame.image.load('assets/tictactoe_assets/cross_global.png').convert_alpha()
                rect=image.get_rect(center=grid_pos[i][4])
                window.blit(image,rect)

    def global_capture(player):
            nonlocal game_state , game_active , end
            if grid_state[0][0]==player:
                if grid_state[1][0] == player and grid_state[2][0] == player:
                    game_state=player
                elif grid_state[3][0] == player and grid_state[6][0] == player:
                    game_state=player
                elif grid_state[4][0] ==player and grid_state[8][0] == player:
                    game_state=player
            elif grid_state[1][0]==player:
                if grid_state[4][0]==player and grid_state[7][0]==player:
                    game_state=player
            elif grid_state[2][0]==player:
                if grid_state[4][0] == player and grid_state[6][0] == player:
                    game_state=player
                elif grid_state[5][0]==player and grid_state[8][0]==player:
                    game_state=player
            elif grid_state[3][0]==player:
                if grid_state[4][0]==player and grid_state[5][0]==player:
                    game_state=player
            elif grid_state[6][0]==player:
                if grid_state[7][0]==player and grid_state[8][0]==player:
                    game_state==player

            if game_state==1:
                image=pygame.image.load('assets/tictactoe_assets/circle_win.jpeg')
                window.blit(image,(0,0))
                end=True
            elif game_state==-1:
                image=pygame.image.load('assets/tictactoe_assets/cross_win.jpeg')
                window.blit(image,(0,0))
                end=True
                
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_ESCAPE or end):
                return True
            
        if not(game_active):
            player_choice()

        else:
            for i in range(9):
                for j in range(9):
                    if (0 not in grid_state[i][1] or grid_state[i][0]!=0)and grid_state[i][2]:
                        refresh(True)
                        grid_state[j][2]=False
            
                    if grid_state[i][1][j]==0 and grid_state[i][2]:
                        if button_list[i][j].draw():
                            refresh(False)
                            grid_state[j][2]=True
                            if player==1:
                                grid_state[i][1][j]=1
                                player=-1
                                
                            else:
                                grid_state[i][1][j]=-1
                                player=1
                    capture(i,-1)
                    capture(i,1)

            global_capture(1)
            global_capture(-1)

        pygame.display.update()
        clock.tick(60)

