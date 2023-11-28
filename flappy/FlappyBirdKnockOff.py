import pygame
import random
pygame.init()

#initialising stuff
display1 = pygame.display.set_mode((900, 600))
pygame.display.set_caption('Flappy Bird KnockOff')
clock = pygame.time.Clock()
run = True
p=0
point_font = pygame.font.Font(None, 50)
point_text = point_font.render(str(p), False, (0,0,0))

#bg
debg = pygame.image.load('bg.jpg')
debg = pygame.transform.scale(debg, (900,600))

#bird
bird = pygame.image.load('bird.png')
bird = pygame.transform.scale(bird,(60, 70))
bird_rect = bird.get_rect(midbottom = (450,300))
bird_jump = False
birdspeed = 8



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
        self.pipe1 = pygame.image.load('pipe1.png')
        self.pipe1_rect = self.pipe1.get_rect(midbottom = (pipe_obj_x_dist,self.y))
        self.pipe1_ogpos = pipe_obj_x_dist

        #pipe2
        self.pipe2 = pygame.image.load('pipe2.png')
        self.pipe2_rect = self.pipe2.get_rect(midtop = (pipe_obj_x_dist,self.y+200));  '''y is offset by 200 to position it right'''
        self.pipe2_ogpos = pipe_obj_x_dist

        #collision box(points)
        self.hitbox = pygame.image.load('powtf.jpg')
        self.hitbox = pygame.transform.scale(self.hitbox,(100,90))
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

filepoints = open('points.txt', 'r')
points = 0
highpoints = int(filepoints.read())



#actual game rendering
while run:

    for event in pygame.event.get():

            #quit out option
            if event.type == pygame.QUIT:
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
                    bird_rect.midbottom = (450,300)
                    bird_jump = False

                    notCollidedwithpipes = True
                    if highpoints<points:
                        filepoints = open('points.txt','w')
                        highpoints = points
                        filepoints.write(str(highpoints))
                        filepoints.close()
                        filepoints = open('points.txt','r')
                    points = 0
                    

    
    #rendering of 'gameplay'
    while notCollidedwithpipes:

        #general inputs and other stuff
        for event in pygame.event.get():

            '''quit out option'''
            if event.type == pygame.QUIT:
                run = False
                notCollidedwithpipes = False

            '''keydown check'''
            if event.type == pygame.KEYDOWN:

                '''spacebar'''
                if event.key == pygame.K_SPACE:
                    bird_jump = True
                    birdspeed = 8
    

        #bird movement(jump)
        if bird_jump == True:
            bird_rect.y -= birdspeed
            birdspeed -=0.5


        #pipe movement
        for x in L:
            x.pipe1_rect.right -=3
            x.pipe2_rect.right -=3
            x.hb_rect.right -=3
            x.pipe_pos_x -=3
        

    
        #collisions
        for X in L:
            if bird_rect.colliderect(X.hb_rect) and iframes>=90:
                print('collided with hitbox')
                points += 1
                iframes = 0
            if bird_rect.colliderect(X.pipe1_rect) or bird_rect.colliderect(X.pipe2_rect) or bird_rect.collidepoint(450,600):
                print('collided with pipes')
                iframes = 0
                notCollidedwithpipes = False


        #object display
        '''displaying the hitbox  before everything else so it cant be seen'''
        for X in L:
            display1.blit(X.hitbox, X.hb_rect)

        '''displaying the bg'''
        display1.blit(debg, (0,0))

        '''pipe display and moving pipes'''
        for x in L:
            display1.blit(x.pipe1, x.pipe1_rect)
            display1.blit(x.pipe2, x.pipe2_rect)
 
            x.pipemove()

        '''bird display'''
        display1.blit(bird, bird_rect)

        '''points'''
        point_font = pygame.font.Font(None, 50)
        point_text = point_font.render(str(points), False, (255,0,0))
        display1.blit(point_text, (0,40))

        ogpoint_font = pygame.font.Font(None, 50)
        ogpoint_text = ogpoint_font.render(str(f'high score: {highpoints}'), False, (255,0,0))
        display1.blit(ogpoint_text, (0,0))




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
    display1.blit(newgame_text, (300,110))

    #display update
    '''updating the screen'''
    pygame.display.update()
    '''framerate fix'''
    clock.tick(60)


filepoints.close()


pygame.quit()
