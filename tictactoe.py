import pygame , sys

#to start pygame
#pygame.init()

def game():
    #window and its attributes
    window_width=750
    window_height=900
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
                (200,500),'assets/tictactoe_assets/circle_select.jpeg',0)
    button2=Button('assets/tictactoe_assets/cross_option.jpeg',
                (550,500),'assets/tictactoe_assets/cross_select.jpeg',0)

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
        [(77, 239), (150, 241), (220, 242), 
        (77, 315), (150, 312), (223, 312), 
        (77, 385), (148, 380), (220, 380)], 
        
        [(303, 239), (377, 241), (447, 239), 
        (302, 315), (374, 310), (444, 313), 
        (304, 383), (377, 386), (446, 381)], 
        
        [(527, 236), (601, 244), (671, 239), 
        (528, 310), (602, 312), (672, 310), 
        (531, 381), (596, 382), (665, 386)], 
        
        [(77, 466), (148, 467), (221, 466), 
            (78, 538), (149, 537), (219, 534), 
            (78, 607), (149, 607), (218, 610)], 
            
            [(306, 466), (378, 466), (443, 462), 
            (301, 533), (372, 536), (445, 536), 
            (305, 605), (378, 607), (443, 605)], 
            
            [(528, 461), (601, 463), (668, 463), 
            (529, 537), (603, 534), (671, 532), 
            (532, 601), (603, 604), (670, 604)], 
            
            [(77, 687), (148, 688), (215, 688), 
            (79, 762), (147, 758), (219, 761), 
            (76, 833), (149, 832), (220, 828)], 
            
            [(308, 688), (379, 690), (441, 691), 
                (305, 762), (376, 762), (448, 760), 
                (302, 832), (375, 832), (446, 831)], 
                
                [(533, 686), (601, 687), (673, 687), 
                (531, 762), (600, 759), (672, 759), 
                (527, 831), (602, 833), (675, 831)]
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

