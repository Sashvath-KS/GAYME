import pygame, sys, random, pickle

pygame.init()

#display, clock(frames per second), caption, icon
disp = pygame.display.set_mode((900,600), pygame.RESIZABLE )
clock = pygame.time.Clock()
pygame.display.set_caption('FlappyBirdKnockOff')
bg = pygame.transform.scale(pygame.image.load('assets/flappy_assets/bg.jpg'), (900,600))
#pygame.display.set_icon()

#bird class
class Bird():

    def __init__(self):
        #getting the image,rect and transforming it
        self.image = pygame.image.load('assets/flappy_assets/bird.png')
        self.image = pygame.transform.scale(self.image, (30,35))
        self.rect = self.image.get_rect(midbottom = (450,300))
        #to make sure bird doesnt fly 'fly'
        self.jump_pressed = True
        #timer before which anothe r jump can be performed
        self.jump_counter = 0
        #gravity
        self.grav = 0.49

    #jumping function
    def jumping(self):
        keys = pygame.key.get_pressed()


        if keys[pygame.K_SPACE] and self.jump_pressed == True:
            #setting birds gravity to +8
            self.grav = 9 
            self.jump_pressed = False
        #if the bird has jumped, a timer will begin before and only after that can the bird be allowed to jump again
        if self.jump_pressed == False:
            self.jump_counter +=1
            if self.jump_counter >=20:
                self.jump_pressed = True
                self.jump_counter = 0

        #applying gravity
        self.rect.bottom -=self.grav
        self.grav -=0.49

    #drawing the bird
    def screen_draw(self):
        disp.blit(self.image, self.rect)

    #birds collision with the top and bottom of the window
    def bird_collisions(self):
        global collided_with_pipes
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            collided_with_pipes = True
    
    #function that updates the bird's action on display with the previously written functions
    def update(self):
        self.jumping()
        self.screen_draw()
        self.bird_collisions()



#pipes
#initial pipe distance and for new game
pipe_obj_x_dist = 1000
newgame_x_dist = 1000
#pipe class
class Pipe:
    #making the pipes and hitboxes
    def __init__(self):
        global pipe_obj_x_dist

        #random y position for beginning of the game for each pipe
        self.y = random.randrange(150, 299,10)
        

        #pipe1(upper)
        self.pipe1 = pygame.image.load('assets/flappy_assets/pipe1.png')
        self.pipe1_rect = self.pipe1.get_rect(midbottom = (pipe_obj_x_dist,self.y))

        #pipe2(bottom)
        self.pipe2 = pygame.image.load('assets/flappy_assets/pipe2.png')
        self.pipe2_rect = self.pipe2.get_rect(midtop = (pipe_obj_x_dist,self.y+200)) #y is offset by 200 to position it wrt
                                                                            #the first pipe(this is the space that the bird passes through)

        #hitbox
        self.hitbox = pygame.image.load('assets/flappy_assets/powtf.jpg')         #just a placeholder image for the space between the pipes for collision
        self.hitbox = pygame.transform.scale(self.hitbox,(100,90))
        self.hb_rect = self.hitbox.get_rect(midtop =(pipe_obj_x_dist,self.y))

        #pipe position checkers n shit
        #self.pipe_pos_ref = pipe_obj_x_dist#
        pipe_obj_x_dist += 300     #adding to seperate the pipes from each other and prevent overlapping


        #speed at which pipes move
        self.pipe_speed =3


    #method to move pipes if it goes out of bounds
    def pipemove(self):
        global pipe_obj_x_dist

        #moving the specific pipe towards the left side
        self.pipe1_rect.right -= self.pipe_speed
        self.pipe2_rect.right -= self.pipe_speed
        self.hb_rect.right -= self.pipe_speed

        #removing the pipe that went out of bounds
        if  (self.pipe1_rect.right<=-290):

            L.pop(L.index(self))

            #new x offset between the new pipe and the final pipe to maintain same distance between pipes
            final_pipe_pos = L[-1].pipe1_rect.x +340 #approximately the same(there is a small difference of 0.1cm)
            pipe_obj_x_dist = final_pipe_pos

            #creating a new pipe 
            L.append(Pipe())


    

    #displaying the specific pipe
    def pipedraw(self):
            disp.blit(self.pipe1, self.pipe1_rect)
            disp.blit(self.pipe2, self.pipe2_rect)
    
    #collisions with parts of the pipe pipe and the bird
    def pipe_collisions(self, bird):
        global iframes, collided_with_pipes, points

        #to check if the bird collided with any of the pipes(up and bottom)
        if (bird.rect.colliderect(self.pipe1_rect) or bird.rect.colliderect(self.pipe2_rect)):
            
            collided_with_pipes = True
            
        #if the bird collides with the hitbox and its invincibility frames are over 70 then a point is 
        #granted(if iframes not there then multiple points granted which is not cool)
        if (bird.rect.colliderect(self.hb_rect) and iframes >= 70):
            points +=1
            iframes = 0

    #update the pipe with it's respective functions to work
    def update(self):
        self.pipemove()
        self.pipedraw()
        self.pipe_collisions(bird)


#points function[update = to update the highscore with the update_point if its point is higher than previous highscore
# reset = if the player wishes the high score to be reset]
#done with binary files
def points_file(update = False, update_point = 0 ,reset = False):
    if reset:
        file = open('assets/flappy_assets/point.bin','wb')
        pickle.dump(0,file)
    if update:
            try:
                #if file exists continue to compare the scores
                file = open('assets/flappy_assets/point.bin', 'rb')
                d=pickle.load(file)
                if update_point > d:
                    d = update_point
                    file.close()
                    file =open('assets/flappy_assets/point.bin', 'wb')
                    pickle.dump(d, file)
                file.close()
            except:
                    #if file does not exist, then create a file with the given update_point argument
                    file = open('assets/flappy_assets/point.bin','wb')
                    pickle.dump(update_point,file)
                


#new game func
def new_game():
    global L, pipe_obj_x_dist, bird, points, collided_with_pipes, iframes, disp, clock
    disp = pygame.display.set_mode((900,600), pygame.RESIZABLE )
    clock = pygame.time.Clock()
    pygame.display.set_caption('FlappyBirdKnockOff')
    #to start a new game
    points =0
    pipe_obj_x_dist = newgame_x_dist
    L =[Pipe() for x in range(6)]
    bird = Bird()
    #collision with bird and pipes and ground
    collided_with_pipes = False

    #time/files with points/colliders checker and other stuff
    iframes = 0


#func that runs flappy 
def game_run():
    global iframes
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        disp.fill((3,5,6))

        disp.blit(bg,(0,0))

        #bird updates
        bird.update()

        #pipe updates
        for x in L:
            x.update()

        #clock,disp,iframes update
        pygame.display.update()
        clock.tick(60)
        iframes +=1
        
        #to check if the player has foolishly lost
        if collided_with_pipes:
            running = False


#func that runs flappy with a sort of pause screen
def game_pause_start():
    global collided_with_pipes, points
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            

            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_ESCAPE:
                    return True
                
                #run the game if this
                if event.key == pygame.K_SPACE:
                    new_game()
                    game_run()
                    points_file(update = True, update_point = points)
                    collided_with_pipes = False

                if event.key == pygame.K_r:
                    points_file(reset = True)

        disp.fill((70,70,70))
        pygame.display.update()
        clock.tick(60)
