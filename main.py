import random
import math
import pygame

#Initialize the pygame 
pygame.init()

#create the screen
#  a bracket is added inside set_mode beacuse we are creating a tuple
screen=pygame.display.set_mode((800,600)) #(width,height)


#TITLE AND ICON
pygame.display.set_caption("Space Invader")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#BACKGROUND
background=pygame.image.load('background.jpg')
#Player
playerImg=pygame.image.load('hero.png')
playerX=370
playerY=480
playerX_change=0



#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
number_of_enemies=6
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(20,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

#Bullet
#ready-can't see bullet in screen
#fire-bullet is currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=5
bullet_state="ready"

#score 
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#GAMEOVER TEXT
over_font=pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score=font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
     over_text=over_font.render("Game Over",True,(255,255,255))
     screen.blit(over_text,(200,250)) #middle of screen


def player(x,y):
    #drawing the image of player on the window
    screen.blit(playerImg,(x,y)) 

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
     #to make sure that bullet is fired from the center and top of the spaceship
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#GAME LOOP
#ANY EVENT THAT OCCUR INSIDE GAME IS KEPT INSIDE THIS WHILE LOOP
running=True
while running:

     #RGB=RED,GREEN,BLUE
    screen.fill((37, 35, 36)) #game windows bg color
    #background image
    screen.blit(background,(0,0))
     #getting up the window to continuosly run until cross is clicked.
     #get all the event in this program and loop in it
    for event in pygame.event.get():  
        #if user clicks the cross or quit button close the game window.
        if event.type==pygame.QUIT:  
            running=False

        #if key stroke is pressed check whther its righ or left
        #KEYDOWN IS WHILE PRESSING KEY AND KEYUP IS WHILE RELEASING
           
        if event.type==pygame.KEYDOWN: 
            if event.key==pygame.K_LEFT:
                playerX_change=-0.4 
            if event.key==pygame.K_RIGHT:
                playerX_change=0.4
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready": #it must be in ready state to fire another bullet
                    bulletX=playerX #it makes bullet go from initial xposition of bullet
                    fire_bullet(bulletX,bulletY)
        #if key is released
        if event.type==pygame.KEYUP: 
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT: 
                playerX_change=0

     #Movement of enemy   
    for i in range(number_of_enemies):

        #game over
        if enemyY[i]>440:
            for j in range(number_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i]=1
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-1
            enemyY[i]+=enemyY_change[i]

    #collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,800)
            enemyY[i]=random.randint(20,150)

        enemy(enemyX[i],enemyY[i],i)
    #calling the player here because 1st the bg is filled and then player appears in start of the game.
    playerX += playerX_change
    #adding boundary to the window
    if playerX<=0:
        playerX=0
    #subtraction 64 from 800 as the image size is 64px.  
    elif playerX>=736: 
        playerX=736

    #bullet movement
    #keeping bullet within the screen and resetting
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    #moving bullets from spaceship to outside    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    player(playerX,playerY)
    show_score(textX,textY)
   

    #to make sure the display is updating
    pygame.display.update() 

    #pygame.inti() and pygame.display.update() is mos necessary

