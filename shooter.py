import pygame
import random
import pyrebase
import threading

import subprocess
mainfile = "main.py"
def maingame():

    
    #The email and password of the user
    # For testing purposes i have hardcodede it     
    pygame.init()
    email = "a@gmail.com"
    password = "123456"
    #the config dict with all the neccessary details required to connect to the databse
    databaseconfig = {
    "apiKey": "AIzaSyC01ZyPhEcSn0pwpnSX6YevzHx2TfwtLoA",
    "authDomain": "game2-9ecb2.firebaseapp.com",
    "databaseURL": "https://game2-9ecb2-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "game2-9ecb2",
    "storageBucket": "game2-9ecb2.appspot.com",
    "messagingSenderId": "461270065748",
    "appId": "1:461270065748:web:b86dfefa6c5328c9db43c1"

    } 
    #this is the firebase object
    firebasey = pyrebase.initialize_app(databaseconfig)
    # db is the database
    db = firebasey.database()

    #auth is the object used for autehnitcation
    auth = firebasey.auth()

    #authentication of user 
    user = auth.sign_in_with_email_and_password(email, password)

    #listening to the notifications
    class Bullets(pygame.sprite.Sprite):
        global player1score
        def __init__(self,y,role):
        
                super().__init__()
                self.image = pygame.transform.scale(pygame.image.load(r"assets/shooter_assets/bullet.png"),(50,10)).convert_alpha()
                self.origin= role
                self.rect = self.image.get_rect()
                if role == "host":
                    self.rect.centery = y
                    self.rect.left = hostbox.right

                if role == "player":
                    self.rect.centery = y
                    self.rect.right = playerbox.left
                
        def update(self):
            if self.origin == "host":
                self.rect.centerx += 30
            if self.origin == "player":
                self.rect.centerx -= 30
            if self.rect.left>=width:
                    self.kill()
            if self.rect.left<=0:
                    self.kill()
        def hitplayer(self):
            global player1score,player2score
            if self.rect.colliderect(hostbox):
                player2score+=1
                gamescreen.blit(explosionimg,(self.rect.left,self.rect.centery))
                self.kill()
            if self.rect.colliderect(playerbox):
                player1score+=1
                gamescreen.blit(explosionimg,(self.rect.left,self.rect.centery))
                self.kill()

        
                
                
                    
    hostscore = 0          
    playerscore = 0     
    def stremandret():
        def stream_handler(message1):
            global hostpos
            nonlocal hostscore
            
            hostpos = message1["data"]
            
            hostbox.centery = hostpos[0]   
            if hostpos[1]!=0:
                bulletsgrp.add(Bullets(hostpos[1],role = "host"))
                
            hostscore = hostpos[2]
        try:
            db.child(str(gameconnectionid)+"host").stream(stream_handler,user.get("idToken"))
        except:
            pass
        def stream_handler2(message2):
            global playerpos
            nonlocal playerscore
            playerpos = message2["data"]
            playerbox.centery = playerpos[0]
        
        
            if playerpos[1]!=0:
                bulletsgrp.add(Bullets(playerpos[1],role ="player"))

            playerscore = playerpos[3]
            
        try:
            db.child(str(gameconnectionid)+"player").stream(stream_handler2,user.get("idToken"))
        except:
            pass

        

    running = True
    #Function to push the data
    temp = 0

    def pushdata():
            nonlocal temp
            global gameconnectionid
            nonlocal bulletpos
            while running:
                db.child(str(gameconnectionid)+role).set((temp,bulletpos,player1score,player2score),user.get("idToken"))

    def varassignment():
        global my_font,height,width,lent,speed,delay,padding,fontcolour,fps,player1score,player2score
        my_font = pygame.font.SysFont('Calibri', 25,True)
        height = 600
        width = 800
        lent = 150 

        speed = 8 
        delay = 500
        padding = 10
        fontcolour = (0,0,0)
        fps = pygame.time.Clock()
        player1score = 0
        player2score = 0 
    varassignment()
    def config():
        global gameconnectionid,role
        role= input("Do you want to be a host or a player: ").lower()
        if role == "host":
            gameconnectionid = random.randrange(123456,999999)
            print(gameconnectionid)
        if role == "player":
            gameconnectionid= int(input("enter host id to connect to"))
        
    config()    
    db.child(str(gameconnectionid)+"host").set((100,100,0,0),user.get("idToken"))
    db.child(str(gameconnectionid)+"player").set((100,100,0,0),user.get("idToken"))
    gamescreen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
    defaultfont = pygame.font.Font("assets/pixel_font.ttf",19)
    backgroundimage = pygame.transform.scale(pygame.image.load('assets/shooter_assets/bgimg.jpg'),(width+400,height))
    explosionimg = pygame.transform.scale(pygame.image.load(r"assets/shooter_assets/explosion.png"),(50,50)).convert_alpha()
    def drawtext(text,font,x,y,colour = (255,255,255)):
            box = font.render(text,True,colour)

            gamescreen.blit(box,(x,y))


    def blit_and_draw_rect():
        
        drawtext(text ="Player 1 Score: "+ str(hostscore),font=defaultfont,x = 0,y = 580)
        
        
        drawtext(text ="Player 2 Score: "+ str(playerscore),font=defaultfont,x = 450,y = 580)

        

        


        
        gamescreen.blit(hostimg,hostbox)
        gamescreen.blit(playerimg,playerbox)

    bulletsgrp = pygame.sprite.Group()
    running = True
    hostimg = pygame.transform.scale((pygame.image.load("assets/shooter_assets/spaceship.png")),(80,90))
    playerimg = pygame.transform.scale((pygame.image.load("assets/shooter_assets/spaceship.png")),(80,90))
    playerimg = pygame.transform.flip(playerimg, True, False)
    hostbox = hostimg.get_rect()
    playerbox = playerimg.get_rect()
    hostbox.left = 10
    playerbox.right = width -10
    bulletpos = 0
    def game():
        global height
        nonlocal running,temp,bulletsgrp,bulletpos
        
        while running:
            
            gamescreen.blit(backgroundimage,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                   running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if role == "host":
                
                        bulletpos = hostbox.centery
                    if role == "player":
                        bulletpos = playerbox.centery
                else:
                    bulletpos = 0    
                
            
            keypressed = pygame.key.get_pressed()
            if role == "host":
                if keypressed[pygame.K_w]:
                        temp = hostbox.centery-30
                elif keypressed[pygame.K_s]:
                        temp = hostbox.centery+30
            elif role == "player":
                if keypressed[pygame.K_w]:
                        temp = playerbox.centery-30
                elif keypressed[pygame.K_s]:
                        temp = playerbox.centery+30

            

        
            
        
            for abullet in bulletsgrp:
                abullet.update()
                abullet.hitplayer()
            
        
            
            blit_and_draw_rect()
            bulletsgrp.draw(gamescreen)
        
            pygame.display.flip()
            fps.tick(60)
            
        pygame.quit() 
        db.child(str(gameconnectionid)+"host").remove(user.get("idToken"))
        db.child(str(gameconnectionid)+"player").remove(user.get("idToken")) #Making pushdata function as a thread to reduce downtime
    
    #Making the stream function as a thread to ensure that it is constantly being run 
    p1 = threading.Thread(target = pushdata,daemon=True)
    p1.start()
    p2 = threading.Thread(target = stremandret,daemon=True)
    p2.start()
    game()
    return True
    




