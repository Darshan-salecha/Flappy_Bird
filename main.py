#Flappy Bird Game on 15/6/2020 by Darshan Salecha
#install pygame library

import random  # for generating random numbers
import sys   # wwe will use sys.exit to exit the program
import pygame
import time
from pygame.locals import *


# GlOBAL VARIABALES for game
FPS=32
SCREENWIDTH=289   #screen size
SCREENHEIGHT=511


SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='Gallery/pics/bird.png'
BACKGROUND='Gallery/pics/background.png'               #Define path of pictures
PIPE='Gallery/pics/pipe.png'

#welcome message screen
def welcomeScreen():
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    time.sleep(1)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
        SCREEN.blit(GAME_SPRITES['base'],(basex,int(GROUNDY)))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

class example:    #define class for high score in every play
  HIGHSCORE = 0       #highscore as static variable
instance = example()



#main game function
def mainGame():

    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    # create pipes
    newpipe1=getrandomPipe()
    newpipe2=getrandomPipe()

    upperpipes=[
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[0]['y']},
    ]

    lowerpipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[1]['y']},

    ]
    pipeVelx = -4

    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1


    playerFlapAccv=-8
    playerFlaped=False

    while True:
       for event in pygame.event.get():
          if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
          if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
              if playery>0:
                  playerVelY=playerFlapAccv
                  playerFlaped=True
                  GAME_SOUNDS['wing'].play()

       crashtest=isCollide(playerx,playery,upperpipes,lowerpipes)
       if crashtest:
           return

       #check for scrore
       playerMidpos=playerx+GAME_SPRITES['player'].get_width()/2
       for pipe in upperpipes:
           pipeMidpos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
           if pipeMidpos <= playerMidpos <(pipeMidpos+4):
               score+=1
               #print(f"your score is{score}")
               GAME_SOUNDS['point'].play()
               if instance.HIGHSCORE<score:
                   instance.HIGHSCORE=score

       if playerVelY<playerMaxVelY and not playerFlaped:
           playerVelY+=playerAccY

       if playerFlaped:
           playerFlaped=False
       playerHeight=GAME_SPRITES['player'].get_height()
       playery=playery+min(playerVelY,GROUNDY-playery-playerHeight)

       for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
           upperpipe['x']+=pipeVelx
           lowerpipe['x']+=pipeVelx

       if 0<upperpipes[0]['x'] <5:
           newpipe=getrandomPipe()
           upperpipes.append(newpipe[0])
           lowerpipes.append(newpipe[1])
       #if pipe is out of screen remove it
       if upperpipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
           upperpipes.pop(0)
           lowerpipes.pop(0)
       #blits sprite
       SCREEN.blit(GAME_SPRITES['background'],(0,0))
       for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
           SCREEN.blit(GAME_SPRITES['pipe'][0], (int(upperpipe['x']), int(upperpipe['y'])))
           SCREEN.blit(GAME_SPRITES['pipe'][1], (int(lowerpipe['x']), int(lowerpipe['y'])))

       SCREEN.blit(GAME_SPRITES['base'],(basex,int(GROUNDY)))
       SCREEN.blit(GAME_SPRITES['player'],(int(playerx),int(playery)))
       SCREEN.blit(GAME_SPRITES['highscore'],(20,465))

       myDigits=[int(x) for x in list(str(score))]
       HighDigits=[int(x) for x in list(str(instance.HIGHSCORE))]

       width=0
       for digit in myDigits:
           width+=GAME_SPRITES['numbers'][digit].get_width()
       xoffset=(0)
       xoffset1=20

       for digit in myDigits:
           SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,int(SCREENHEIGHT*0.12)))
           xoffset+=GAME_SPRITES['numbers'][digit].get_width()
       for HighDigit in HighDigits:
           SCREEN.blit(GAME_SPRITES['numbers'][HighDigit],(xoffset1+100,460))
           xoffset1+=GAME_SPRITES['numbers'][HighDigit].get_width()
       pygame.display.update()
       FPSCLOCK.tick(FPS)



def isCollide(playerx,playery,upperpipes,lowerpipes):
    if playery>GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeHeight+pipe['y'] and abs(playerx-pipe['x'])<(GAME_SPRITES['pipe'][0].get_width()-26)):
            #print(GAME_SPRITES['pipe'][0].get_width())
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx-pipe['x'])<(GAME_SPRITES['pipe'][0].get_width()-26) :
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getrandomPipe():

    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipeX,'y':-y1},#upper pipe
        {'x':pipeX,'y':y2}#lower pipe
    ]
    return pipe




if __name__ == '__main__':
    HIGHSCORE = 0
    #this is the main function from where our game will start
    pygame.init()#initialize all pygame's modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Darshan ')
    GAME_SPRITES['numbers']=(
        pygame.image.load('Gallery/pics/0.png').convert_alpha(),
        pygame.image.load('Gallery/pics/1.png').convert_alpha(),
        pygame.image.load('Gallery/pics/2.png').convert_alpha(),
        pygame.image.load('Gallery/pics/3.png').convert_alpha(),
        pygame.image.load('Gallery/pics/4.png').convert_alpha(),
        pygame.image.load('Gallery/pics/5.png').convert_alpha(),
        pygame.image.load('Gallery/pics/6.png').convert_alpha(),
        pygame.image.load('Gallery/pics/7.png').convert_alpha(),
        pygame.image.load('Gallery/pics/8.png').convert_alpha(),
        pygame.image.load('Gallery/pics/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = (pygame.image.load('Gallery/pics/message.png').convert_alpha())
    GAME_SPRITES['base'] = (pygame.image.load('Gallery/pics/base.png').convert_alpha())
    GAME_SPRITES['highscore'] = (pygame.image.load('Gallery/pics/highscore.png').convert_alpha())
    GAME_SPRITES['pipe'] = (
                            pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
                            pygame.image.load(PIPE).convert_alpha()
                           )


    GAME_SOUNDS['die']=pygame.mixer.Sound('Gallery/sound/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('Gallery/sound/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('Gallery/sound/point.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('Gallery/sound/wing.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('Gallery/sound/swoosh.wav')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

# game to continue loop
    while True:
        welcomeScreen() #shows welcome screen to user until he presses a button
        #
        mainGame()
