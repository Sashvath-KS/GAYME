import pygame
import random
import pyrebase
pygame.init()
import threading
#The email and password of the user
# For testing purposes i have hardcodede it     
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
            self.image = pygame.transform.scale(pygame.image.load(r"bullet.png"),(50,10)).convert_alpha()
            self.origin= role
            self.rect = self.image.get_rect()
            if role == "host":
                self.rect.centery = y
                self.rect.centerx = hostbox.centerx + 30

            if role == "player":
                self.rect.centery = y
                self.rect.centerx = playerbox.centerx - 30
               
    def update(self):
        if self.origin == "host":
            self.rect.centerx += 5
        if self.origin == "player":
            self.rect.centerx -= 5
        if self.rect.left>=width:
                 self.kill()
        if self.rect.left<=0:
                 self.kill()
    def hitplayer(self):
        global player1score,player2score
        if self.rect.colliderect(hostbox):
            player2score+=1
            self.kill()
        if self.rect.colliderect(playerbox):
            player1score+=1
            self.kill()

       
            
            
                
            
def stremandret():
    def stream_handler(message1):
        global hostpos
        
        hostpos = message1["data"]
        
        hostbox.centery = hostpos[0]   
        if hostpos[1]!=0:
            bulletsgrp.add(Bullets(hostpos[1],role = "host"))
    try:
        db.child(str(gameconnectionid)+"host").stream(stream_handler,user.get("idToken"))
    except:
        pass
    def stream_handler2(message2):
        global playerpos
        playerpos = message2["data"]
        playerbox.centery = playerpos[0]
       
       
        if playerpos[1]!=0:
            bulletsgrp.add(Bullets(playerpos[1],role ="player"))

        
        
    try:
        db.child(str(gameconnectionid)+"player").stream(stream_handler2,user.get("idToken"))
    except:
        pass
  
      

running = True
#Function to push the data
temp = 0

def pushdata():
        global temp,gameconnectionid,bulletpos
        while True:
          db.child(str(gameconnectionid)+role).set((temp,bulletpos),user.get("idToken"))

def varassignment():
    global my_font,height,width,lent,ballx,bally,speed,delay,padding,fontcolour,fps,player1score,player2score
    my_font = pygame.font.SysFont('Calibri', 25,True)
    height = 400
    width = 400
    lent = 150 
    ballx = 8
    bally = 8
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
    role= input("Do you want to be a host or a player").lower()
    if role == "host":
        gameconnectionid = random.randrange(123456,999999)
        print(gameconnectionid)
    if role == "player":
        gameconnectionid= int(input("enter host id to connect to"))
    
config()    
db.child(str(gameconnectionid)+"host").set((100,100),user.get("idToken"))
db.child(str(gameconnectionid)+"player").set((100,100),user.get("idToken"))
gamescreen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
dimension = gamescreen.get_size()[0]
def resizewindow():
    global hostbox,playerbox,dimension,width,height
    dimensionnew = gamescreen.get_size()
    width = dimensionnew[0]
    height = dimensionnew[1]
    playerbox.right = width
    dimension = dimensionnew
    return height
def converttorect():
    global leftscoreboardasrect,rightscoreboardaasrect
    leftscoreboardasrect = player1box.get_rect()
    rightscoreboardaasrect = player2box.get_rect()
    rightscoreboardaasrect.bottomright =(width-padding,height-padding)
    leftscoreboardasrect.bottomleft = (0+padding,height-padding)
def renderfont():
    global player1box,player2box
    player1box = my_font.render("Player 1 Score: "+ str(player1score),True,fontcolour,(66, 245, 176))
    player2box = my_font.render("Player 2 Score: "+ str(player2score),True,fontcolour,(66, 245, 176))      
def blit_and_draw_rect():

    gamescreen.blit(player1box, leftscoreboardasrect)
    gamescreen.blit(player2box, rightscoreboardaasrect)
    pygame.draw.rect(gamescreen, (0, 0, 0), hostbox)
    pygame.draw.rect(gamescreen, (0, 0, 0), playerbox)

bulletsgrp = pygame.sprite.Group()
running = True
hostbox = pygame.Rect(0,(height//2)-100,20,lent)
playerbox = pygame.Rect(width-20,(height//2)-100,20,lent)
bulletpos = 0
def game():
    global running,height,temp,bulletsgrp,bulletpos
    
    while running:
        
        gamescreen.fill((66, 245, 176))
        dimensionnew = gamescreen.get_size()
        renderfont()
        if dimension != dimensionnew:
            resizewindow()       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("empty")
            
                running = False
                 
                db.child(str(gameconnectionid)+"host").remove(user.get("idToken"))
                db.child(str(gameconnectionid)+"player").remove(user.get("idToken"))
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
           
      
        bulletsgrp.draw(gamescreen)
        converttorect()
        blit_and_draw_rect()
        pygame.display.flip()
        fps.tick(60)
       
    pygame.quit()  #Making pushdata function as a thread to reduce downtime

#Making the stream function as a thread to ensure that it is constantly being run 
p1 = threading.Thread(target = pushdata,daemon=True)
p1.start()
p2 = threading.Thread(target = stremandret,daemon=True)
p2.start()


game()
     
