import pygame, random, sys

pygame.init() 


disp = pygame.display.set_mode((900,600))
pygame.display.set_caption('Flappy Bird KnockOff')
clock = pygame.time.Clock()

#class bird
class BirdClass(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/flappy_assets/bird.png'),(60,70))
        self.rect = self.image.get_rect(midbottom = (450,300))
        self.jump = True
        self.speed = 8

    def apply_grav(self):
        self.rect.bottom += 0.10
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.speed = 8
        self.rect.y -= self.speed
        self.speed -=0.8
    
    def collisions(self):
        '''if self.rect.top <= 0:
            self.jump = False
        if self.rect.bottom >= 600:
            self.jump = False
            return False'''
        

        #collisions with pipe and hitbox
        for X in L:
            global iframes
            if self.rect.colliderect(X.hb_rect) and iframes>=90:
                print('collided with hitbox')
                #points += 1
                iframes = 0
            if self.rect.colliderect(X.pipe1_rect) or self.rect.colliderect(X.pipe2_rect) or self.rect.collidepoint(450,600):
                print('collided with pipes')
                iframes = 0
                #notCollidedwithpipes = False

    def new_game(self):
        self.rect.midbottom = (450,300)
        
    def update(self):
        #self.apply_grav()
        self.move()
        self.collisions()


#pipes
'''initial pipe distance and for new game'''
pipe_obj_x_dist = 1000
newgame_x_dist = 1000
'''pipe class'''
class Pipe:
    '''making the pipes and hitboxes'''
    def __init__(self):
        global pipe_obj_x_dist

        self.y = random.randrange(150, 299,10)
        

        #pipe1
        self.pipe1 = pygame.image.load('assets/flappy_assets/pipe1.png')
        self.pipe1_rect = self.pipe1.get_rect(midbottom = (pipe_obj_x_dist,self.y))
        self.pipe1_ogpos = pipe_obj_x_dist

        #pipe2
        self.pipe2 = pygame.image.load('assets/flappy_assets/pipe2.png')
        self.pipe2_rect = self.pipe2.get_rect(midtop = (pipe_obj_x_dist,self.y+200));  '''y is offset by 200 to position it right'''
        self.pipe2_ogpos = pipe_obj_x_dist

        #collision box(points)
        self.hitbox = pygame.transform.scale(pygame.image.load('assets/flappy_assets/powtf.jpg'),(100,90))
        self.hb_rect = self.hitbox.get_rect(midtop =(pipe_obj_x_dist,self.y))
        self.hb_ogpos = pipe_obj_x_dist

        #pipe position checkers n shit
        self.pipe_pos_x = pipe_obj_x_dist
        pipe_obj_x_dist += 300

    '''method to move pipes if it goes out of bounds'''
    def pipemove(self):
        global pipe_obj_x_dist
        if  (self.pipe1_rect.right<=-100):
            '''new x offset between consecutive pipes'''
            pipe_obj_x_dist = 350
            '''new y pos for the moved pipes'''
            new_y = random.randrange(150, 299, 10)

            self.pipe1_rect.midbottom = (1000 + pipe_obj_x_dist,new_y)
            self.pipe2_rect.midtop = (1000 + pipe_obj_x_dist,new_y+200)
            self.hb_rect.midtop = (1000 + pipe_obj_x_dist,new_y)
            print('moved')

    
    '''method to move pipes back for a new game'''
    def pipenewgame(self):
        global newgame_x_dist
        '''random y pos for newgame pipes'''
        new_y = random.randrange(150, 299, 10)

        self.pipe1_rect.midbottom = (newgame_x_dist,new_y)
        self.pipe2_rect.midtop = (newgame_x_dist,new_y+200)
        self.hb_rect.midtop = (newgame_x_dist,new_y)

'''creating 5 pipes'''
L=[]
for x in range(5):
    L.append(Pipe())

#time/files with points/colliders checker and other stuff
iframes = 0
notCollidedwithpipes = False

bird = pygame.sprite.GroupSingle()
bird.add(BirdClass())

while True:
    disp.fill((70,67,89))
    for event in pygame.event.get():

            #quit out option
            if event.type == pygame.QUIT:
                sys.exit()
                run = False
            
            if event.type == pygame.KEYDOWN:

                #newgame space
                if event.key == pygame.K_SPACE:
                    '''resetting pipes location'''
                    for x in L:
                        x.pipenewgame()
                        newgame_x_dist +=300

                    '''resetting the x pos of newgame so it can be done numerous times'''
                    newgame_x_dist = 1000

                    '''resetting the birds pos'''
                    #bird.new_game()
                    #bird_jump = False

                    notCollidedwithpipes = True
                    '''if highpoints<points:
                        filepoints = open('points.txt','w')
                        highpoints = points
                        filepoints.write(str(highpoints))
                        filepoints.close()
                        filepoints = open('points.txt','r')
                    points = 0'''
                    

    
    #rendering of 'gameplay'
    while notCollidedwithpipes:
        disp.fill((70,67,89))
        #general inputs and other stuff
        for event in pygame.event.get():

            '''quit out option'''
            if event.type == pygame.QUIT:
                sys.exit()
                run = False
                notCollidedwithpipes = False

            #keydown check
            '''if event.type == pygame.KEYDOWN:

                #spacebar
                if event.key == pygame.K_SPACE:
                    bird_jump = True
                    birdspeed = 8'''
    

        #bird movement(jump)
        '''if bird_jump == True:
            bird_rect.y -= birdspeed
            birdspeed -=0.5'''


        #pipe movement
        for x in L:
            x.pipe1_rect.right -=3
            x.pipe2_rect.right -=3
            x.hb_rect.right -=3
            x.pipe_pos_x -=3
        
        

    
        #collisions
        '''for X in L:
            if bird_rect.colliderect(X.hb_rect) and iframes>=90:
                print('collided with hitbox')
                points += 1
                iframes = 0
            if .colliderect(X.pipe1_rect) or bird_rect.colliderect(X.pipe2_rect) or bird_rect.collidepoint(450,600):
                print('collided with pipes')
                iframes = 0
                notCollidedwithpipes = False'''


        #object display

        '''displaying the bg'''
        #disp.blit(debg, (0,0))

        '''pipe display and moving pipes'''
        for x in L:
            disp.blit(x.pipe1, x.pipe1_rect)
            disp.blit(x.pipe2, x.pipe2_rect)
 
            x.pipemove()

        '''bird display'''
        bird.draw(disp)
        bird.update()

        '''points'''
        '''point_font = pygame.font.Font(None, 50)
        point_text = point_font.render(str(points), False, (255,0,0))
        disp.blit(point_text, (0,40))

        ogpoint_font = pygame.font.Font(None, 50)
        ogpoint_text = ogpoint_font.render(str(f'high score: {highpoints}'), False, (255,0,0))
        disp.blit(ogpoint_text, (0,0))'''




        #display update
        '''t is for the invincibility frames so no extra points'''
        iframes += 1
        '''updating the screen'''
        pygame.display.update()
        '''framerate fix'''
        clock.tick(60)

    #restart?
    newgame_font = pygame.font.Font(None, 50)
    newgame_text = newgame_font.render('press SPACE to play', False, (77,126,255))
    disp.blit(newgame_text, (300,110))

    #display update
    '''updating the screen'''
    pygame.display.update()
    '''framerate fix'''
    clock.tick(60)
pygame.quit()
