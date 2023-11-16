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
        self.image = pygame.transform.scale_by(pygame.image.load('player_images/character1.png'),3).convert_alpha()
        self.rect = self.image.get_rect(center=(200,200))
        

        #player looking direction
        self.look = 'right'

        #grav and 'allowing for jump'
        self.grav = 0.29
        self.jump_action = False

        #player vel and boolean for vel direction
        self.vel = [0,0]
        self.left = False
        self.right = False
        self.jump = False


    def apply_grav(self):
        self.rect.y += self.grav
        self.grav += 0.4


    #keys to check player movement
    def movement(self):
        if self.right or self.left:
            self.rect.x += self.vel[0]

        if self.jump:
            self.rect.y += self.vel[1]
        

        self.vel = [0,0]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.right = True
            self.vel[0]=5
        else:
            self.right = False

        if keys[pygame.K_a]:
            self.left = True
            self.vel[0]=-5
        else:
            self.left = False

        if keys[pygame.K_SPACE]:
            self.jump = True
            self.vel[1] = -10
        else:
            self.jump = False


    def collision(self):
        l=pygame.sprite.spritecollide(self,block_group,False)
        for box in l:
            if self.vel[0] > 0:
                self.rect.right = box.rect.left-6

            if self.vel[0] < 0:
                self.rect.left = box.rect.right +6
            
            if self.rect.bottom < box.rect.top:
                self.rect.bottom = box.rect.top

    
    #function to update the player with its respective functions
    def update(self):
        self.movement()
        self.collision()
        #self.apply_grav()


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
