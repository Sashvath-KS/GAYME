import pygame,sys

def game():
    # pygame.init()
    pygame.font.init()
    clock=pygame.time.Clock()


    screenw=800
    screenh=600
    screen=pygame.display.set_mode((screenw,screenh))

    surface=pygame.Surface((screenw,screenh ))
    ball=pygame.Rect(screenw/2,screenh/2,20,20)
    player=pygame.Rect(screenw-20,screenh/2-50,10,100)
    opponent=pygame.Rect(10,screenh/2-50,10,100)
    grey=(200,200,200)
    ballspeedx=6
    ballspeedy=6
    font=pygame.font.Font("assets/pixel_font.ttf",20)
    playerscore=opponentscore=0

    def ballanimation():
        nonlocal ballspeedx,ballspeedy,playerscore,opponentscore
        ball.x+=ballspeedx
        ball.y+=ballspeedy
        
        if ball.top<=0 or ball.bottom>=screenh:
            ballspeedy*=-1
        
        if ball.left <=0 or ball.right>=screenw:
            ballspeedx*=-1

        if ball.colliderect(player) or ball.colliderect(opponent):ballspeedx*=-1

        
        
    def score():
        nonlocal opponentscore,playerscore
        global gameover
        if ball.left<=0:
            playerscore+=1
            ball.x=screenw/2
            ball.y=screenh/2
        
        if ball.right>=screenw:
            opponentscore+=1
            ball.x=screenw/2
            ball.y=screenh/2

        if playerscore==3:
            player1=font.render("Player 1 wins",False,"white")
            screen.blit(player1,(screenw/2,screenh/2))
        
        if opponentscore==3:
            player2=font.render("Player 2 wins",False,"white")
            screen.blit(player2,(screenw/2,screenh/2))
            

    def playeranimation():
        key=pygame.key.get_pressed()

        if key[pygame.K_UP]:
            player.y-=5
        elif key[pygame.K_DOWN]:
            player.y+=5

        if key[pygame.K_w]:
            opponent.y-=5
        elif key[pygame.K_s]:
            opponent.y+=5
        
        if player.bottom>=screenh:player.bottom=screenh
        if opponent.bottom>=screenh:opponent.bottom=screenh
        if player.top<=0:player.top=0
        if opponent.top<=0:opponent.top=0   



            



    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                return True
        
        ballanimation()
        playeranimation()
        score()
        screen.blit(surface,(0,0))
        
        pygame.draw.rect(screen,grey,player)
        pygame.draw.rect(screen,grey,opponent)
        pygame.draw.ellipse(screen,grey,ball)

        playerscoresurface=font.render(f"{playerscore}",False,'white')
        screen.blit(playerscoresurface,((screenw/2)+50,screenh/2))
        opponentscoresurface=font.render(f"{opponentscore}",False,'white')
        screen.blit(opponentscoresurface,((screenw/2)-50,screenh/2))

        pygame.display.flip()
        clock.tick(60)
