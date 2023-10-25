import pygame, sys

#from pygame.sprite import _Group

pygame.init()

disp1 = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('player_images\character1.png'),(66,129))
        self.rect = self.image.get_rect(midbottom = (0,600))
        p2 = pygame.transform.scale(pygame.image.load('player_images\character2.png'),(66,129))
        p3 = pygame.transform.scale(pygame.image.load('player_images\character3.png'),(66,129))
        self.player_sprites = [self.image, p2, p3]
        self.player_anim_index = 0

        self.look = 'right'

        self.grav = 0.29
        self.jump_action = True

        #self.bullet = pygame.transform.scale_by(pygame.image.load('bullet.png'),0.01)
        #self.bullet_rect = self.bullet.get_rect()


    
    def player_animations(self):
        self.player_anim_index += 0.06
        if self.player_anim_index >len(self.player_sprites):
            self.player_anim_index = 0
        self.image = self.player_sprites[int(self.player_anim_index)]

    
    def keybinds_check_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            for x in range(len(self.player_sprites)):
                if self.look != 'right':
                    self.player_sprites[x] = pygame.transform.flip(self.player_sprites[x],True,False)
            self.look = 'right'
            self.rect.right += 5

        if keys[pygame.K_a]:
            for x in range(len(self.player_sprites)):
                if self.look != 'left':
                    self.player_sprites[x] = pygame.transform.flip(self.player_sprites[x],True,False)
            self.look = 'left'
            self.rect.left -= 5

        if keys[pygame.K_SPACE] and self.jump_action:
            self.jump_action = False
            self.grav = 10
            self.rect.bottom -= self.grav

    '''def mouse_stuff(self):
        mouse_keys = pygame.mouse.get_pressed()
        
        #if mouse_keys[0]:
        #    if self.look == 'right':'''
                



    
    def apply_grav(self):
        if self.rect.bottom < 600:
            self.grav -= 0.4
            self.rect.bottom -= self.grav
        
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.jump_action = True
    
    def update(self):
        self.player_animations()
        self.keybinds_check_player()
        self.apply_grav()



class Blocks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale_by(pygame.image.load('ledge.png'),10)
        self.rect = self.image.get_rect(midbottom = (x,y))
        


    def update():
        8+9

block1 = pygame.sprite.Group()
block1.add(Blocks(200,200))


player = pygame.sprite.GroupSingle()
player.add(Player())



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    disp1.fill((70,67,89))
    player.draw(disp1)
    player.update()

    block1.draw(disp1)

    pygame.display.update()
    clock.tick(60)


a=7