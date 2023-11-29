import pygame , sys

#to start pygame
pygame.init()

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
        


opening_screen=pygame.image.load('assets/tictactoe_assets/opening_screen.jpeg')
window.blit(opening_screen,(0,0))
button1=Button('assets/tictactoe_assets/circle_option.jpeg',
               (50,350),'assets/tictactoe_assets/circle_select.jpeg')
button2=Button('assets/tictactoe_assets/cross_option.jpeg',
               (400,350),'assets/tictactoe_assets/cross_select.jpeg')

game_active=False
player_order=None
def player_choice():
    global player_order,game_active
    if button1.draw():
        player_order=[1,-1]
        game_screen=pygame.image.load('assets/tictactoe_assets/tictactoe_2.jpeg')
        window.blit(game_screen,(0,0))
        game_active=True
    elif button2.draw():
        player_order=[-1,1]
        game_screen=pygame.image.load('assets/tictactoe_assets/tictactoe_1.jpeg')
        window.blit(game_screen,(0,0))
        game_active=True

grid_state=[[0,[0 for i in range(9)]] for j in range(9)]
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
for i in range(grid_pos):
    button_list.append([])
    for j in range(9):
        button_list[i].append(Button('path1',grid_pos[i][j],'path2'))

for i in range(len(grid_pos)):
    button_list.append([])
    for j in grid_pos[i]:
        button_list[i].append(
            j
            #Button('path1',j,'path2')
        )

print(button_list)
print(grid_state)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT or event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
    if not(game_active):
        player_choice()

    else:
        pass
    pygame.display.update()
    clock.tick(60)