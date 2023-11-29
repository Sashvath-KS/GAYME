import pygame , sys

#to start pygame
pygame.init()

#window and its attributes
window_width=750
window_height=900
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

print('\n\n\n\n\n\n',global_grid_pos)