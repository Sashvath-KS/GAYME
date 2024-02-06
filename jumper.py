import pygame
import os 
import sys
def menu():
    global player1type,player2type
    width = 800
    height = 600 
    #pygame.init()
    fps = pygame.time.Clock()    
    window = pygame.display.set_mode((width,height))
    backgroundimage = pygame.transform.scale(pygame.image.load('assets/jumper_assets/bgimgmenu.jpg'),(width,height))
    defaultfont = pygame.font.Font("assets/pixel_font.ttf",19)
    def drawtext(text,font,x,y,colour = (255,255,255)):
        box = font.render(text,True,colour)

        window.blit(box,(x,y))
      
    class Button:
        #init function is given to get the attributes of the button
        def __init__(self,path1,position) -> None:
            self.image=pygame.image.load(path1).convert_alpha()
            self.image = pygame.transform.scale(self.image,(120,140))
            self.rect=self.image.get_rect(topleft=position)
        #drawing , hovering and clicking logic
        def draw(self):
            mouse_pos=pygame.mouse.get_pos()
            window.blit(self.image,self.rect)
            if self.rect.collidepoint(mouse_pos):
                if True in pygame.mouse.get_pressed():
                    return True
    
    adboy_p1 = Button(path1= r"assets/jumper_assets/Characters/Adboy/Player_Sprite_Walking/Run (1).png",position=(50,10))
    robot_p1 = Button(path1= r"assets/jumper_assets/Characters/Robot/Player_Sprite_Walking/Run (1).png",position=(50,150))
    ninjagirl_p1 = Button(path1= r"assets/jumper_assets/Characters/Ninjagirl/Player_Sprite_Walking/Run__000.png",position=(50,300))
    beedabro_p1 = Button(path1= r"assets/jumper_assets/Characters/Beeda Bro/Player_Sprite_Walking/1.jpg",position=(50,450))
    adboy_p2 = Button(path1= r"assets/jumper_assets/Characters/Adboy/Player_Sprite_Walking/Run (1).png",position=(500,10))
    robot_p2 = Button(path1= r"assets/jumper_assets/Characters/Robot/Player_Sprite_Walking/Run (1).png",position=(500,150))
    ninjagirl_p2 = Button(path1= r"assets/jumper_assets/Characters/Ninjagirl/Player_Sprite_Walking/Run__000.png",position=(500,300))
    beedabro_p2 = Button(path1= r"assets/jumper_assets/Characters/Beeda Bro/Player_Sprite_Walking/1.jpg",position=(500,450))
    player1type = " "
    player2type = " "
    disptext = "Press Space to Play Game"
    while True:
        global gamescreen
        window.blit(backgroundimage,(0,0))
        for event in pygame.event.get():    #to quit the game
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                gamescreen = pygame.display.set_mode((900,514))
                return True
            
            '''elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                return True
            '''
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
             if player1type!=" " and player2type!= "":
                break
             else:
                 disptext = "Select Player 1 and Player 2"
        isadboy = adboy_p1.draw()
        isrobot = robot_p1.draw()
        isninjagirl = ninjagirl_p1.draw()
        isbeedabro = beedabro_p1.draw()
        isbeedabro2 = beedabro_p2.draw()
        isadboy2 = adboy_p2.draw()
        isrobot2= robot_p2.draw()
        isninjagirl2 = ninjagirl_p2.draw()
    
        if isadboy :
            player1type = "Adboy"
        if isrobot :
            player1type = "Robot"
        if isninjagirl:
            player1type = "Ninjagirl"
        if isbeedabro:
            player1type = "Beeda Bro"
        if isadboy2 :

            player2type = "Adboy"
        if isrobot2 :
            player2type = "Robot"
        if isninjagirl2:
            player2type = "Ninjagirl"
        if isbeedabro2:
            player2type = "Beeda Bro"
        

        drawtext(text = f"Selected : {player1type}",font=defaultfont,x=0,y=0)
        drawtext(text = f"Selected : {player2type}",font=defaultfont,x=400,y=0)
        drawtext(text = disptext,font = defaultfont,x = 170,y = 560,colour=(255,255,255))


        pygame.display.update()
    return game()



def game():  
    #pygame.init() 
    blockheight = 50
    blockwidth = 150
    width = 800
    height = 600
    recoilvelocity = 7

    defaultfont = pygame.font.Font("assets/pixel_font.ttf",18)


    def shootsound(filename):
        global bulletsound 
        bulletsound = pygame.mixer.Sound(f"assets/jumper_assets/Music/{filename}.wav")   
    shootsound("gunshot")
    running = True
    walking = False

   


    class Bullets(pygame.sprite.Sprite):
        
        def __init__(self,player,playerside,playertype):
            super().__init__()
            self.characterbullet = playertype
            self.image = pygame.transform.scale(pygame.image.load(f"assets/jumper_assets/Projectiles/{self.characterbullet}/bullet.png"),(50,15)).convert_alpha()
            self.direction = playerside
            
            self.origin = player
            self.rect = self.image.get_rect()
            if self.direction == "right":
                self.rect.left = player.rect.right-30
                self.rect.centery = player.rect.centery
            if self.direction == "left":
                self.rect.left = player.rect.left+30
                self.rect.centery = player.rect.centery
                self.image = pygame.transform.flip(self.image, True, False)
        def update(self):
            if self.direction == "right":
                self.rect.centerx +=15
            if self.direction=="left":
                self.rect.centerx-=15

            if self.rect.left>width+100:
                self.kill()
            if self.rect.left<-100:
                self.kill()
            for ablock in blocksgrp:
                if self.rect.colliderect(ablock):
                    self.kill()
        #Checks if bullet hits any one of the players and reduces health if so 
        def checkhitplayer(self):
            if self.rect.colliderect(player1) and player1.lives>0 and self.origin!=player1:
                player1.health-=5
                #to make player move on being hit by a bullet
                if self.direction=="right":
                    if player1.rect.right<=width:
                        player1.rect.centerx+=recoilvelocity
                elif self.direction=="left":
                    if player1.rect.left>=0:
                        player1.rect.centerx-=recoilvelocity
                gamescreen.blit(bloodimg,(self.rect.left,self.rect.centery-20))
                self.kill()
            if self.rect.colliderect(player2) and player2.lives>0 and self.origin!=player2: 
                player2.health-=5
                
                if self.direction=="right":
                    if player2.rect.right<=width:
                        player2.rect.centerx+=recoilvelocity
                elif self.direction=="left":
                    if player2.rect.left>=0:
                        player2.rect.centerx-=recoilvelocity
                gamescreen.blit(bloodimg,(self.rect.right,self.rect.centery-20))
                self.kill()
            
                
    class Blocks(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            self.image = pygame.image.load('assets/jumper_assets/block.png')
            #scaling image to a suitable size 
            self.image = pygame.transform.scale(self.image,(blockwidth,blockheight))
            #spawns the rectangle at a random location 
            self.rect = self.image.get_rect(center = (x,y))

    class player(pygame.sprite.Sprite):
        

        
        def __init__(self,x,y,playertype):
            walkimglist = []
            idleimglist=[]
            normalattackimglist = []
            self.character = playertype
            for image in os.listdir(f"assets/jumper_assets/Characters/{self.character}/Player_Sprite_Walking"):
                walkimglist.append(image)
            for image in os.listdir(f"assets/jumper_assets/Characters/{self.character}/Player_Sprite_Idle"):
                idleimglist.append(image)
            for image in os.listdir(f"assets/jumper_assets/Characters/{self.character}/Player_Sprite_NormalAttack"):
                normalattackimglist.append(image)
            
            self.health = 100
            self.lives = 5
            self.score = 0 
            self.side = "right"
            self.jumping = False
            self.falling = False
            self.jumpspeed = 30
            self.fallspeed = -0.5
            self.isnormalattack = False
            self.tempside =""
            super().__init__()
            self.walkspriteno = 0 
            self.idlespriteno=0
            self.normalattackspriteno=0
            self.listofwalkingimages = walkimglist
            self.listofidleimages = idleimglist
            self.listofnormalattackimages = normalattackimglist
            self.image = pygame.image.load(fr"assets/jumper_assets/Characters/{self.character}/Player_Sprite_Walking/"+self.listofwalkingimages[self.walkspriteno])
            self.image = pygame.transform.scale(self.image,(100,140))
            
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = height
        def makeplayerfallwhennotonablock(self):
        
            if self.falling == True:
                self.rect.bottom+=self.fallspeed
                self.fallspeed+=0.5
            if self.rect.bottom>=height:
                self.rect.bottom=height
                self.falling = False
                self.fallspeed= 0 
            

        def jumpaction(self):
            nonlocal height,player1
            collisions()
            self.image = pygame.transform.scale(self.image,(100,140))
            if self.side !=self.tempside:
                self.image = pygame.transform.scale(self.image,(100,140))
                self.image = pygame.transform.flip(self.image, True, False)
            
            if self.jumping == True:
                self.rect.bottom -=self.jumpspeed
                self.jumpspeed-=1
            if self.rect.bottom>=height:
                self.rect.bottom=height
                self.jumping = False
            self.tempside = self.side
        
        def walkinganimation(self):
            if 0<=self.walkspriteno<len(self.listofwalkingimages) and not self.jumping:
                posx = self.rect.centerx
                posy = self.rect.centery
                
                self.image = pygame.image.load(fr"assets/jumper_assets/Characters/{self.character}/Player_Sprite_Walking/"+self.listofwalkingimages[int(self.walkspriteno)]).convert_alpha()
                self.image = pygame.transform.scale(self.image,(100,140))
                if self.side == "right":
                    
                    self.image = pygame.transform.scale(self.image,(100,140))
                if self.side == "left":
                    
                    self.image = pygame.transform.scale(self.image,(100,140))
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.centerx = posx
                self.rect.centery = posy
                
                
            else:
                self.walkspriteno = 0
        def normalshootinganimation(self):
                self.image = pygame.transform.scale(self.image,(100,140))
                if self.isnormalattack==  True and self.normalattackspriteno<=len(self.listofnormalattackimages):
                    self.image = pygame.image.load(fr"assets/jumper_assets/Characters/{self.character}/Player_Sprite_NormalAttack/"+self.listofnormalattackimages[int(self.normalattackspriteno)]).convert_alpha()
                    self.image = pygame.transform.scale(self.image,(100,140))
                    if self.side == "right":
                        self.image = pygame.transform.scale(self.image,(100,140))
                    if self.side == "left":
                        self.image = pygame.transform.scale(self.image,(100,140))
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.normalattackspriteno += 0.8
                else :
                    
                    self.normalattackspriteno =0
                    self.isnormalattack = False
                    


            
            
        def idleanimation(self):
                self.image = pygame.transform.scale(self.image,(100,140))
                if not walking and not self.jumping:
                    self.idlespriteno+=0.3
                    if self.idlespriteno<len(self.listofidleimages):
                        posx = self.rect.centerx
                        posy = self.rect.bottom
                        self.image = pygame.image.load(fr"assets/jumper_assets/Characters/{self.character}/Player_Sprite_Idle/"+ self.listofidleimages[int(self.idlespriteno)]).convert_alpha()
                        if self.side == "right":
                            self.image = pygame.transform.scale(self.image,(100,140))
                        if self.side == "left":
                            self.image = pygame.transform.scale(self.image,(100,140))
                            self.image = pygame.transform.flip(self.image, True, False)
                        self.rect = self.image.get_rect()
                        self.rect.centerx = posx
                        self.rect.bottom = posy
                    else:
                        self.idlespriteno=0

        
        def checkhealth(self):
        
            if (self.health == 0 or self.health<=0) and self.lives>0 :
                self.lives-=1
                if self.lives!=0:
                    self.health = 100
            if self.lives==0:
                self.kill()
            
        def recoilplayer(self):
            if self.side=="right":
                if self.rect.left>=0:
                    self.rect.centerx-=recoilvelocity
            elif self.side=="left":
                if self.rect.right<=width:
                    self.rect.centerx+=recoilvelocity
    player1 = player(30,600,playertype=player1type)
    player2 = player(400,600,playertype=player2type)
    block1 = Blocks(650,400)
    block2 = Blocks(150,400)
    block3 = Blocks(400,300)
    gamescreen = pygame.display.set_mode((width,height))
    fps = pygame.time.Clock()       
    player1grp = pygame.sprite.Group()
    bulletsgrp = pygame.sprite.Group()
    blocksgrp = pygame.sprite.Group()
    player1grp.add([player1,player2])
    blocksgrp.add([block1,block2,block3])
    backgroundimage = pygame.transform.scale(pygame.image.load('assets/jumper_assets/bgimg.jpg'),(width,height))
    bg1 = pygame.Rect(10,10,100,10)
    fg1= pygame.Rect(10,10,100,10)
    bg2 = pygame.Rect(10,10,100,10)
    fg2= pygame.Rect(10,10,100,10)
    gamestate = ''
    def collisions():
        #These are temporary lists that store information on whether the player is colliding with the block
        collisionlist1=[]
        collisionlist2 = []
        sidecollisionlist1= []
        sidecollisionlist2=[]
        global stopleft1,stopleft2,stopright1,stopright2
        nonlocal blocksgrp,player1
        #stop variables are used to decide whether the player can move towards the right or left.
        #if a stop variable contains True in the list the player is not allowed to move in the corresponding direction
        stopright1=[]
        stopright2 = []
        stopleft1=[]
        stopleft2=[]

        for ablock in blocksgrp:
            #For PLAYER_1
            #Checks collision of player_1 with the TOP of a block
            if ablock.rect.top-15<player1.rect.bottom<ablock.rect.top+15 and ablock.rect.left<player1.rect.centerx<ablock.rect.right and player1.jumpspeed<0:
                player1.rect.bottom = ablock.rect.top
                player1.jumping=False
                #if player_1 collides add True to collisionlist1 to indicate a collision
                collisionlist1.append(True)
            else:
                collisionlist1.append(False)


            #Checks collision of player_1 with the BOTTOM of a block
            if ablock.rect.top<player1.rect.top+10<ablock.rect.bottom and ablock.rect.left-20<player1.rect.centerx<ablock.rect.right+20 :
                
                player1.jumpspeed=-4
            if ablock.rect.top<player2.rect.top+10<ablock.rect.bottom and ablock.rect.left-20<player2.rect.centerx<ablock.rect.right+20 :
                player2.jumpspeed=-4

            #Checks collision of PLAYER_1 with the sides of a block
            if player1.rect.colliderect(ablock.rect):
                #Stores list of two boolean values in the sidecollision1 list.
                #First boolean value specifies if the player is colliding with a block
                #Second boolean value specifies if the player is towards the left or right of the block
                sidecollisionlist1.append([True,player1.rect.left<ablock.rect.left])
            else:
                sidecollisionlist1.append([False,player1.rect.left<ablock.rect.left])

            
            #For PLAYER_2
            #Checks collision of player_2 with the TOP of a block
            if ablock.rect.top-15<player2.rect.bottom<ablock.rect.top+15 and ablock.rect.left<player2.rect.centerx<ablock.rect.right and player2.jumpspeed<0:
                player2.rect.bottom = ablock.rect.top
                player2.jumping=False
                #if player_2 collides add True to collisionlist2 to indicate a collision
                collisionlist2.append(True)
            else:
                collisionlist2.append(False)


        
            
            if player2.rect.colliderect(ablock.rect):
                #Stores list of two boolean values in the sidecollision1 list.
                #First boolean value specifies if the player is colliding with a block
                #Second boolean value specifies if the player is towards the left or right of the block
                sidecollisionlist2.append([True,player2.rect.left<ablock.rect.left])
            else:
                sidecollisionlist2.append([False,player2.rect.left<ablock.rect.left])

            #Collisions between players 
            if player1.rect.colliderect(player2.rect):
                
                if player1.rect.left<player2.rect.left:
                    stopright1.append(True)
                if player1.rect.left>player2.rect.left:
                    stopleft1.append(True)
                if player2.rect.left<player1.rect.left:
                    stopright2.append(True)
                if player2.rect.left>player1.rect.left:
                    stopleft2.append(True)
        if True not in collisionlist1 and not player1.jumping :
            player1.falling = True
            
        else:
            player1.falling=False
        if True not in collisionlist2 and not player2.jumping :
            player2.falling = True
            
        else:
            player2.falling=False
        
        for x,y in sidecollisionlist1:
            if x == True and y == True:
                stopright1.append(True)
            else :
                stopright1.append(False)
            if x==True and y==False:
                stopleft1.append(True)
            else :
                stopleft1.append(False)
        
        for x,y in sidecollisionlist2:
            if x == True and y == True:
                stopright2.append(True)
            else :
                stopright2.append(False)
            if x==True and y==False:
                stopleft2.append(True)
            else :
                stopleft2.append(False)
    def drawtext(text,font,x,y,colour = (255,255,255)):
        box = font.render(text,True,colour)
        gamescreen.blit(box,(x,y))
        
    noofshiftpresses1 =0 
    noofshiftpresses2 =0
    def moveplayer11(keypressed):
        
        nonlocal walking,player1,noofshiftpresses1
        
        if keypressed[pygame.K_LSHIFT]:
            noofshiftpresses1+=1
            if noofshiftpresses1>=4:

                bulletsgrp.add(Bullets(player=player1,playerside=player1.side,playertype=player1type))
                noofshiftpresses1 = 0 
                bulletsound.play()
                player1.recoilplayer()
                player1.isnormalattack = True
                
        if keypressed[pygame.K_w] and player1.jumping==False:
                player1.jumpspeed = 30
                player1.jumping = True
        if keypressed[pygame.K_d] :
            player1.walkspriteno+=0.4
            player1.walkinganimation()
            player1.side = "right"
            walking = True
            
            if player1.rect.right<=width and True not in stopright1:
                player1.rect.centerx+=15
            
        else:
            if keypressed[pygame.K_a]==False:
                walking = False
        if keypressed[pygame.K_a]:
            player1.side = "left"
            player1.walkspriteno+=0.4
            player1.walkinganimation()
            walking = True
            if player1.rect.left>=0  and True not in stopleft1 :
                player1.rect.centerx-=15
            
        else:
            if keypressed[pygame.K_d]==False:
            
                walking = False
    def moveplayer12(keypressed):
        nonlocal walking,player2,noofshiftpresses2
        if keypressed[pygame.K_RSHIFT]:
            noofshiftpresses2+=1
            if noofshiftpresses2>=4:
                bulletsgrp.add(Bullets(player=player2,playerside=player2.side,playertype=player2type))
                noofshiftpresses2 = 0 
                bulletsound.play()
                player2.recoilplayer()
                player2.isnormalattack =True
        if keypressed[pygame.K_UP] and player2.jumping==False :
                player2.jumpspeed = 30
                player2.jumping = True
                
        if keypressed[pygame.K_RIGHT] :
            player2.side = "right"
            player2.walkspriteno+=0.4
            player2.walkinganimation()
            walking = True
            if player2.rect.right<=width and True not in stopright2  :
                player2.rect.centerx+=15
            
        
        else:
            if keypressed[pygame.K_RIGHT]==False:
            
                walking = False
        if keypressed[pygame.K_LEFT] :
            player2.walkspriteno+=0.4
            player2.walkinganimation()
            walking = True
            if player2.rect.left>=0  and True not in stopleft2  :
                player2.rect.centerx-=15
            player2.side = "left"

        

        
        else:
            if keypressed[pygame.K_RIGHT]==False:
            
                walking = False

    backgroundimage = pygame.transform.scale(pygame.image.load('assets/jumper_assets/bgimg.jpg'),(width,height))
    bloodimg = pygame.transform.scale(pygame.image.load(r"assets/jumper_assets/blood.png"),(70,70)).convert_alpha()

    while running:
        
        gamescreen.blit(backgroundimage,(0,0))
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                running = False
                gamescreen = pygame.display.set_mode((900,514))
                return True
            '''elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                running = False
                return True'''
        #Getting the key pressed 
        keypressed = pygame.key.get_pressed()
        #Drawing the various sprites on the screen
        bulletsgrp.draw(gamescreen)
        blocksgrp.draw(gamescreen)
        player1grp.draw(gamescreen)

        #Placement of scoreboard for player 1
        bg1.left = player1.rect.left
        bg1.centery = player1.rect.centery -75
        fg1.left = player1.rect.left
        fg1.centery = player1.rect.centery -75
        fg1.width = player1.health

        #Placement of scoreboard for player 2
        bg2.left = player2.rect.left
        bg2.centery = player2.rect.centery -75
        fg2.left = player2.rect.left
        fg2.centery = player2.rect.centery -75
        fg2.width = player2.health
        
        #Rendering animations and movements for player1 if it is alive
        if player1.lives>0 :
            pygame.draw.rect(gamescreen,(255,0,0),bg1)
            pygame.draw.rect(gamescreen,(0,255,0),fg1)
            moveplayer11(keypressed)
            player1.jumpaction()
            player1.idleanimation()
            player1.makeplayerfallwhennotonablock()
            player1.checkhealth()
            player1.normalshootinganimation()
       
           
        
        #Rendering animations and movements for player2 if it is alive
        if player2.lives>0 :
            pygame.draw.rect(gamescreen,(255,0,0),bg2)
            pygame.draw.rect(gamescreen,(0,255,0),fg2)
            moveplayer12(keypressed)
            player2.jumpaction()
            player2.idleanimation()
            player2.makeplayerfallwhennotonablock()
            player2.checkhealth()
            player2.normalshootinganimation()
        if player1.lives>0 and player2.lives==0 and player2.health == 0 :
            gamestate = "PLAYER 1 WINS!"
            player2.rect.centerx = width + 300
            drawtext(f"Press ESC to return to main menu",defaultfont,x = 130,y = 140)
        if player2.lives>0 and player1.lives==0 and player1.health == 0 :
            gamestate = "PLAYER 2 WINS!"
            player1.rect.centerx = width + 300
            drawtext(f"Press ESC to return to main menu",defaultfont,x = 130,y = 140)

    
        bulletsgrp.update()

        #Drawing player health and lives left
        drawtext(f"Player 1 health:{player1.health}",defaultfont,10,0,)
        drawtext(f"Player 2 health:{player2.health}",defaultfont,450,0)
        drawtext(f"No of lives left:{player1.lives}",defaultfont,10,40)
        drawtext(f"No of lives left:{player2.lives}",defaultfont,450,40)
        
        if player1.lives>0 or player1.health>0:
            drawtext(f"Player 1",defaultfont,*player1.rect.topleft)
        if player2.lives>0 or player2.health>0:
            drawtext(f"Player 2",defaultfont,*player2.rect.topleft)
        if gamestate:
            drawtext(gamestate,font=defaultfont,x =270,y =100)
        for abullet in bulletsgrp:
            abullet.checkhitplayer()
        pygame.display.flip()
        fps.tick(60)   
    return True
    #pygame.quit()