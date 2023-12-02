import pygame, sys, random, pickle

pygame.init()

def starting():
    global disp, clock, og_disp, quit_button_image, start_button_image, reset_button_image, quit_button_rect, start_button_rect, quit_game, reset_button_rect
    #display, clock(frames per second), caption, icon, bg
    disp = pygame.display.set_mode((900,600))
    clock = pygame.time.Clock()
    pygame.display.set_caption('FlappyBirdKnockOff')
    pygame.display.set_icon(pygame.image.load('assets/flappy_assets/bird_icon.png').convert_alpha())
    #og_disp = pygame.display.get_window_size()                              #og disp to resize if needed later
    quit_game = False

    #images for the buttons in the menu screen for flappy
    start_button_image = pygame.image.load('assets/flappy_assets/start_button.png').convert_alpha()
    start_button_image = pygame.transform.scale(start_button_image, (202,120))

    quit_button_image = pygame.image.load('assets/flappy_assets/quit_button.png').convert_alpha()
    quit_button_image = pygame.transform.scale(quit_button_image, (202,119))

    reset_button_image = pygame.image.load('assets/flappy_assets/reset_button.png').convert_alpha()
    reset_button_image = pygame.transform.scale(reset_button_image, (200,121))


    #rectangles for the respective buttons
    start_button_rect = start_button_image.get_rect(midbottom = (446,530))
    quit_button_rect = quit_button_image.get_rect(midbottom = (150,390))
    reset_button_rect = reset_button_image.get_rect(midbottom = (750,390))


#bird class
class Bird():

    def __init__(self):
        #getting the image,rect and transforming it
        self.image = pygame.image.load('assets/flappy_assets/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,60))
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
#pipe class
class Pipe:
    #making the pipes and hitboxes
    def __init__(self):
        global pipe_obj_x_dist

        #random y position for beginning of the game for each pipe
        self.y = random.randrange(150, 299,10)
        

        #pipe1(upper)
        self.pipe1 = pygame.transform.flip(pygame.image.load('assets/flappy_assets/pipe.png').convert_alpha(),False, True)
        self.pipe1_rect = self.pipe1.get_rect(midbottom = (pipe_obj_x_dist,self.y))

        #pipe2(bottom)
        self.pipe2 = pygame.image.load('assets/flappy_assets/pipe.png').convert_alpha()
        self.pipe2_rect = self.pipe2.get_rect(midtop = (pipe_obj_x_dist,self.y+200)) #y is offset by 200 to position it wrt
                                                                            #the first pipe(this is the space that the bird passes through)

        #hitbox
        self.hitbox = pygame.image.load('assets/flappy_assets/powtf.jpg').convert_alpha()      #just a placeholder image for the space between the pipes for collision
        self.hitbox = pygame.transform.scale(self.hitbox,(100,90))
        self.hb_rect = self.hitbox.get_rect(midtop =(pipe_obj_x_dist,self.y))

        #pipe position checkers n shit
        #self.pipe_pos_ref = pipe_obj_x_dist#
        pipe_obj_x_dist += 300     #adding to seperate the pipes from each other and prevent overlapping


        #speed at which pipes move
        self.pipe_speed =5


    #method to move pipes if it goes out of bounds
    def pipemove(self):
        global pipe_obj_x_dist

        #moving the specific pipe towards the left side
        self.pipe1_rect.right -= self.pipe_speed
        self.pipe2_rect.right -= self.pipe_speed
        self.hb_rect.right -= self.pipe_speed

        #removing the pipe that went out of bounds
        if  (self.pipe1_rect.right<=-290):

            Pipe_list.pop(Pipe_list.index(self))

            #new x offset between the new pipe and the final pipe to maintain same distance between pipes
            final_pipe_pos = Pipe_list[-1].pipe1_rect.x +340 #approximately the same(there is a small difference of 0.1cm)
            pipe_obj_x_dist = final_pipe_pos

            #creating a new pipe 
            Pipe_list.append(Pipe())


    

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



#bg class
class MovingBG:
    def __init__(self):
        global bg_pos_start, first_few_initializing_bg_counter
        self.image = pygame.transform.scale(pygame.image.load('assets/flappy_assets/bg.png').convert_alpha(), pygame.display.get_window_size())
        self.rect = self.image.get_rect(topleft =bg_pos_start)
        if first_few_initializing_bg_counter<= 5:
            bg_pos_start = (pygame.Surface.get_width(self.image)+bg_pos_start[0]-5,0)
            first_few_initializing_bg_counter+=1


    def out_of_bounds(self):
        global bg_pos_start

        if self.rect.x <= -3600:
            bg_pos_start = (pygame.Surface.get_width(self.image)+BG_list[-1].rect.topleft[0]-5, BG_list[-1].rect.topleft[-1])
            BG_list.remove(self)
            BG_list.append(MovingBG())
            print(BG_list)
    
    def bg_move(self):
        self.rect.x -=5

    def display_on_screen(self):
        disp.blit(self.image,self.rect)

    #def resize(self):
    #    global og_disp
    #    if og_disp != pygame.display.get_window_size():
    #        og_disp = pygame.display.get_window_size()
    #        for x in BG_list:
    #            x.image = pygame.transform.scale(pygame.image.load('bg.png'),pygame.display.get_window_size())

    def update(self):
        self.bg_move()
        self.out_of_bounds()
        self.display_on_screen()
        #self.resize()



#points function[update = to update the highscore with the update_point if its point is higher than previous highscore
# reset = if the player wishes the high score to be reset]
#done with binary files
def points_file(update = False, update_point = 0 ,reset = False, High_read = False, current_score = False):
    global points

    #if reset, then reset high score to 0
    if reset:
        file = open('assets/flappy_assets/point.bin','wb')
        pickle.dump(0,file)
    
    #to update points 
    if update:
            try:
                #if file exists continue to compare the scores
                file = open('assets/flappy_assets/point.bin', 'rb+')
                d=pickle.load(file)
                file.close()
                if update_point > d:
                    file.seek(0,0)
                    d = update_point
                    pickle.dump(d, file)
                    file.seek(0,0)

                file.close()
                #to disp the highscore in game
                return d

            except:
                    #if file does not exist, then create a file with the given update_point argument
                    file = open('assets/flappy_assets/point.bin','wb')
                    pickle.dump(update_point,file)
                    file.close()
    
    #to disp highscore
    if High_read:
        file = open('assets/flappy_assets/point.bin', 'rb')
        d= pickle.load(file)
        file.close()
        return d
    
    #current points got during game
    if current_score:
        return points
                


#new game func
def new_game():
    global Pipe_list, pipe_obj_x_dist, bird, points, collided_with_pipes, iframes, BG_list, bg_pos_start,first_few_initializing_bg_counter, start_game
    #to start a new game

    #redoing/assigning objects

    first_few_initializing_bg_counter=0             #to initialise a few bg counter
    bg_pos_start = (0,0)                            #bg pos var
    BG_list = [MovingBG() for x in range(5)]          #list containing the bgs

    points =0           #normal points to be reset when game begins

    pipe_obj_x_dist = 1000                      #pipe dist
    Pipe_list =[Pipe() for x in range(6)]       #list containing pipes

    bird = Bird()                               #bird object

    #collision with bird and pipes and ground
    collided_with_pipes = False

    #time/files with points/colliders checker and other stuff
    iframes = 0

    #so that the game doesnt start immediately 
    start_game = False



#flappybird main menu
def start_menu():
    global start_button_image, start_button_rect, quit_button_image, quit_button_rect, quit_game, reset_button_image, reset_button_rect, start_game, quit

    #if player chooses start then start the game
    if pygame.mouse.get_pressed()[0]:
            if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                start_game = True
    
    #if player chooses to quit, then exit
    if pygame.mouse.get_pressed()[0]:
            if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                quit_game = True
    
    #if player chooses to reset highschore, then reset
    if pygame.mouse.get_pressed()[0]:
            if reset_button_rect.collidepoint(pygame.mouse.get_pos()):
                points_file(reset = True)


    #displaying all the menu items
    disp.blit(pygame.transform.scale(pygame.image.load('assets/flappy_assets/starting_bg.png'),pygame.display.get_window_size()), (0,0))
    disp.blit(start_button_image,start_button_rect)
    disp.blit(reset_button_image,reset_button_rect)
    disp.blit(quit_button_image,quit_button_rect)
    disp_text_points(menu = True)



def disp_text_points(menu = False, game = False):

    #only for menu disp menu_text
    if menu == True:
        #font for text
        font_text = pygame.font.Font('assets/flappy_assets/UNISPACE_BD.ttf', 30)
        #menu text
        menu_text = font_text.render(f'HIGH SCORE:{points_file(High_read = True)} ',False, 'magenta')

        disp.blit(menu_text, (620,220))
    
    #for game disp both menu_text and game_text
    if game == True:
        #font for text
        font_text = pygame.font.Font('assets/flappy_assets/UNISPACE_BD.ttf', 52)

        #menu and game texts 
        menu_text = font_text.render(f'HIGH SCORE:{points_file(High_read = True)} ',False, 'magenta')
        game_text = font_text.render(f'SCORE:{points_file(current_score = True)} ',False, 'green')

        disp.blit(game_text,(0,52))
        disp.blit(menu_text, (0,0))



#func that runs flappy 
def game_run():
    global iframes, quit_game
    
    running = True
    while running:

        for event in pygame.event.get():
            
            #if the player chooses to close the game
            if event.type == pygame.QUIT:
                quit_game = True
                return None
            
            #if the player chooses to exit to flappy menu
            if (event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE):
                running = False
                


        #background update
        for x in BG_list:
            x.update()

        #point update
        points_file(update_point = points, update = True)
        disp_text_points(game = True)


        #bird updates
        bird.update()

        #pipe updates
        for x in Pipe_list:
            x.update()


        #clock,disp,iframes update
        pygame.display.update()
        clock.tick(60)
        iframes +=1
        
        #to check if the player has foolishly lost
        if collided_with_pipes:
            running = False



#func that runs flappy with a sort of entry screen
def game_pause_start():
    global collided_with_pipes, points, start_game

    starting()
    while True:

        for event in pygame.event.get():

            #if the player wishes to opt out using the X or Escape
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE) or quit_game:
                return True

        #new_game() is now initialized here so that it doesnt mess with start_menu() as start_menu needs a few variables
        new_game()
        start_menu()

        #if the player chooses to play then run the game, after loosing, update the high score if the new score is higher than it
        #and make collided_with_pipe as false to not immediately close the game once the player chooses to play again
        #start_game is set to false so the player can 'choose' to play instead of it being automatic
        if start_game == True:

            game_run()
            points_file(update = True, update_point = points)

            collided_with_pipes = False
            start_game = False

        
        #display update and framerate
        pygame.display.update()
        clock.tick(60)



