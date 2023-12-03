import pygame , sys

#to start pygame
pygame.init()

#window and its attributes
def config():
    global global_grid_pos 
    window_width=500
    window_height=600
    window_size=(window_width,window_height)
    window=pygame.display.set_mode(window_size)
    game_screen=pygame.image.load('assets/tictactoe_1.jpeg')
    window.blit(game_screen,(0,0));pygame.display.update()

    global_grid_pos=[]
    local_grid_pos=[]
    flag=True

    while flag:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                pygame.quit()
                flag=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                local_grid_pos.append(pygame.mouse.get_pos())
                print(local_grid_pos)
                if len(local_grid_pos)==9:
                    global_grid_pos.append(local_grid_pos)
                    local_grid_pos=[]

#print('\n\n\n\n\n\n',global_grid_pos)

def resized_points(list):
    grid_pos=[]
    for i in range(len(list)):
        grid_pos.append([])
        for j,k in list[i]:
            j,k=int(j*(2/3)),int(k*(2/3))
            grid_pos[i].append((j,k))
    print('\n\n',grid_pos)

resized_points(
    [
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
)