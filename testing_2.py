import pygame, sys
#from pygame.sprite import _Group

pygame.init()

#setting a display and framrate
disp1 = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()


#class for player
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        #assigning player images and rects and player's animation list
        self.image = pygame.transform.scale_by(pygame.image.load('player_images/character1.png'),3)
        self.rect = pygame.Rect((600,200),(1,129))
        p2 = pygame.transform.scale_by(pygame.image.load('player_images/character2.png'),3)
        p3 = pygame.transform.scale_by(pygame.image.load('player_images/character3.png'),3)
        self.player_sprites = [self.image, p2, p3]
        self.player_anim_index = 0
        self.mask = pygame.mask.from_surface(self.image)

        #player looking direction
        self.look = 'right'

        #grav and 'allowing for jump'
        self.grav = 0.29
        self.jump_action = False

        '''self.b = True'''

        '''self.bullet = pygame.transform.scale_by(pygame.image.load('bullet.png'),0.01)
        self.bullet_rect = self.bullet.get_rect()'''


    #player animation. cycles through images from a list containing those images
    def player_animations(self):
        self.player_anim_index += 0.06
        #if player index is out of range then reset it to 0 and starts the cycle again
        if self.player_anim_index >len(self.player_sprites):
            self.player_anim_index = 0
        #updation of image
        self.image = self.player_sprites[int(self.player_anim_index)]


    #keys to check player movement
    def keybinds_check_player(self):
        #gets keys in a dictionary type from keyboard in a 1 or 0 fashion
        keys = pygame.key.get_pressed()

        #moving right
        if keys[pygame.K_d]:
            #if the player isnt looking right, this makes him look right
            for x in range(len(self.player_sprites)):
                if self.look != 'right':
                    self.player_sprites[x] = pygame.transform.flip(self.player_sprites[x],True,False)
            self.look = 'right'
            #actual movement towards right
            self.rect.right += 5

        #moving left
        if keys[pygame.K_a]:
            #if the player isnt looking left, this makes him look left
            for x in range(len(self.player_sprites)):
                if self.look != 'left':
                    self.player_sprites[x] = pygame.transform.flip(self.player_sprites[x],True,False)
            self.look = 'left'
            #actual movement towards left
            self.rect.left -= 5

        #jump
        #jumpaction here says 'allowed to jump only if player is on the ground/box, if in air or just jumped, then they cannot jump
        if keys[pygame.K_SPACE] and self.jump_action:
            #player cannot jump
            self.jump_action = False
            #setting grav to 10 for specific player and decrementing their bottom value
            self.grav = 10
            self.rect.bottom -= self.grav


    #gravity and position of player if he collides with a box
    def apply_grav(self):
        #if the player is not collidiing with any of the boxes
        if not pygame.sprite.spritecollide(self,block_group, False, pygame.sprite.collide_mask):
                self.grav -= 0.4
                self.rect.bottom -= self.grav

        #if the player collides with any of the boxes
        if pygame.sprite.spritecollide(self,block_group, False, pygame.sprite.collide_mask):
                    #if yes, then player bottom position if the respective box's top position
                    a = pygame.sprite.spritecollideany(self,block_group)
                    if a != None:
                        a = pygame.sprite.spritecollideany(self,block_group).rect.top
                        self.rect.bottom = a
                        self.jump_action = True
                        self.grav = 0.29
    
    def player_collision(self):
          if pygame.sprite.spritecollideany(self,block_group):
                a=pygame.sprite.spritecollideany(self,block_group)
                if a.rect.right == self.rect.right:
                    print(True)
    
    #function to update the player with its respective functions
    def update(self):
        self.player_animations()
        self.keybinds_check_player()
        self.apply_grav()
        #self.player_collision()


#class to create boxes
class Blocks(pygame.sprite.Sprite):
    #taking x and y position for differen box positions
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale_by(pygame.image.load('ledge.png'),10)
        self.rect = self.image.get_rect(bottomleft = (x,y))
        self.mad = pygame.mask.from_surface(self.image)
        

    #useless for now
    def update():
        8+9

#boxes group
block_group = pygame.sprite.Group()
block_group.add(Blocks(0,600))
block_group.add(Blocks(500,550))
block_group.add(Blocks(200,300))


#since a player will be unique, group single
player = pygame.sprite.GroupSingle()
player.add(Player())


#game running
while True:
    for event in pygame.event.get():
        #if quit then quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #filling the display
    disp1.fill((70,67,89))

    #drawing the boxes group
    block_group.draw(disp1)

    #drawing the player and updating their functions
    player.draw(disp1)
    player.update()

    #updating the screen and framrate
    pygame.display.update()
    clock.tick(60)

#end