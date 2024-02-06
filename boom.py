import pygame, sys, random

pygame.init()

def game():
    #global exited
    sc_ht = 900
    sc_w = 514
    #exited = False
    screen = pygame.display.set_mode((sc_ht, sc_w))

    #assets
    background=pygame.image.load("assets/boom_assets/bg.png")
    run=[pygame.image.load("assets/boom_assets/run1.png"),
        pygame.image.load("assets/boom_assets/run2.png")]
    cactus_small=[pygame.image.load("assets/boom_assets/small cactus.png"),
                pygame.image.load("assets/boom_assets/big cacts 2.png")]
    cactus_big=[pygame.image.load("assets/boom_assets/big cactus 1.png"),
                pygame.image.load("assets/boom_assets/big cactus 3.png")]
    bird=[pygame.image.load("assets/boom_assets/bird.png")]
    jump=pygame.image.load("assets/boom_assets/jump.png")
    dunk=pygame.image.load("assets/boom_assets/dunk.png")
    dead=pygame.image.load("assets/boom_assets/dunk.png")



    class BGMOVE:
         def __init__(self,pos):
            self.image=background
            self.rect=self.image.get_rect()
            self.rect.left=pos
         
             
         def update(self):
             screen.blit(self.image,self.rect)
             
             self.rect.left -= 5
    
    class Dino:
        X_pos=0
        Y_pos=400
        Y_pos_duck=430
        JUMP_VEL=8.5


        def __init__(self, run):
            
            self.duck_img=dunk
            self.run_img=run
            self.jump_img=jump

            self.dino_duck=False
            self.dino_run=True
            self.dino_jump=False


            self.step_index=0
            self.jump_vel=self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect=self.image.get_rect()
            self.dino_rect.x=self.X_pos
            self.dino_rect.y=self.Y_pos
        


        def update(self, user_input):
            if self.dino_duck:self.duck()
            if self.dino_run:self.run1()
            if self.dino_jump:self.jump()

            if self.step_index>=10:
                self.step_index=0

            if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.dino_jump:
                self.dino_duck=False
                self.dino_run=False
                self.dino_jump=True

            elif user_input[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck=True
                self.dino_run=False
                self.dino_jump=False
            elif not (user_input[pygame.K_DOWN] or self.dino_jump):
                self.dino_duck=False
                self.dino_run=True
                self.dino_jump=False
        


        def run1(self):
            self.image=self.run_img[self.step_index//5]
            self.dino_rect=self.image.get_rect()
            self.dino_rect.x=self.X_pos
            self.dino_rect.y=self.Y_pos
            self.step_index+=1
        
        def duck(self):
            self.image=self.duck_img
            self.dino_rect=self.image.get_rect()
            self.dino_rect.x=self.X_pos
            self.dino_rect.y=self.Y_pos_duck
            
        def jump(self):
            self.image=self.jump_img
            if self.dino_jump:
                self.dino_rect.y-=self.jump_vel *4
                self.jump_vel-=0.8
            if self.jump_vel<-self.JUMP_VEL:
                self.dino_jump=False
                self.jump_vel=self.JUMP_VEL
            
        def draw(self, screen):
            screen.blit(self.image,self.dino_rect)


    class Obstacle:
        def __init__(self, image, type):
            self.image=image
            self.type=type
            self.rect=self.image[self.type].get_rect()
            self.rect.x=sc_ht
            
        def update(self):
            self.rect.x-=game_speed
            if self.rect.x<-self.rect.width:
                obstacles.pop()

        def draw(self, screen):
            screen.blit(self.image[self.type],self.rect)

    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type=random.randint(0,1)
            super().__init__(image,self.type)
            self.rect.y=445

    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type=random.randint(0,1)
            super().__init__(image,self.type)
            self.rect.y=445

    class Chicken(Obstacle):
        def __init__(self,image):
            self.type=0
            super().__init__(image,self.type)
            self.rect.y=400
            self.index=0
        
        def draw(self,screen):
            screen.blit(self.image[0],self.rect)
            
        
    def main():
        global game_speed,points,obstacles #,exited
        running=True
        
        clock=pygame.time.Clock()
        player=Dino(run)
        game_speed=14
        points=0
        obstacles=[]
        font=pygame.font.Font('freesansbold.ttf',20)
        death_count=0

        def score():
            global points, game_speed
            #global exited
            points+=1
            if points%100==0:
                game_speed+=1
            
            text=font.render('Score:'+str(points),True,(0,0,0))
            textRect=text.get_rect()
            textRect.center=(1000,40)
            screen.blit(text,textRect)
        bg1 = BGMOVE(0*sc_ht) 
        bg2 = BGMOVE(1*sc_ht)
        bg3 = BGMOVE(2*sc_ht)
        while running:
            bg1.update()
            bg2.update()
            bg3.update()
            
            
            if bg1.rect.left<-1500:
                bg1.rect.left = bg3.rect.right
            if bg2.rect.left<-1500:
                bg2.rect.left = bg1.rect.right
            if bg3.rect.left<-1500:
                bg3.rect.left = bg2.rect.right
                    

            #if exited:
            #    return True
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    #exited =  True
                    return True
            onscreenpoints=font.render("Your Score: "+ str(points),True,(255,255,255))
            onscreenpointsrect = onscreenpoints.get_rect()
            onscreenpointsrect.topleft= (0,0)
            
            
            user_input=pygame.key.get_pressed()

            
            
            
            player.draw(screen)
            player.update(user_input)
            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(cactus_small))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(cactus_big))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Chicken(bird))

            for obstacle in obstacles:
                obstacle.draw(screen)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(200)
                    death_count+=1
                    menu(death_count)

            score()
            screen.blit(onscreenpoints, onscreenpointsrect)
            clock.tick(30)
            pygame.display.update()
        

    def menu(death_count):
        global points #,exited
        rrun=True
        while rrun:
            #if exited:
            #    return True
            screen.fill((255,255,255))
            font=pygame.font.Font('freesansbold.ttf',30)
            if death_count==0:
                text=font.render('Press any key to start',True,(0,0,0))

            elif death_count>0:
                text= font.render("Press any key to start", True, (0,0,0))
                score=font.render('Your score:'+str(points),True,(0,0,0))
                scoreRect=score.get_rect()
                scoreRect.center = (sc_ht // 2, sc_w // 2 + 200)
                screen.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (sc_ht // 2,sc_w // 2)
            screen.blit(text, textRect)
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    #exited = True
                    return True
                if event.type == pygame.KEYDOWN:
                    main()

            


    menu(death_count=0)
    return True
#game()