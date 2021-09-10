# Going Home by Alex Zhu
# 6/21/2020

import os

#centre the gameWindow
os.environ['SDL_VIDEO_CENTERED'] = "True"
os.chdir(os.getcwd())

import pygame
from random import randint
from random import randrange
import math
import sys
from AnimatedSprite import *
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=5, buffer=64)

WIDTH  = 800
HEIGHT = 600
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Going Home')

gameIcon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(gameIcon)

font = pygame.font.Font("mylodon-light.otf", 18)
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED = (255,0,0)


#---------------------------------------#
#   functions                           #
#---------------------------------------#
    
def redrawGameWindow(background, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep, boost):
    gameWindow.fill(BLACK)
    gameWindow.blit(levelbackground, (int(-shipXPOS) - 800, int(backgroundY)))

    if deployed:
        gameWindow.blit(statsbackground, (0,0))
        dispTiltAngle(shipAngle)
        dispRotationStep(rotationStep)
        dispShipVy(shipVy)
    else:
        gameWindow.blit(statsbackground0, (0,0))

    if not crashed:
        if not deployed:

            if boost:
                if frame % 2 == 0:
                    gameWindow.blit(flame1, (150,50))
                else:
                    gameWindow.blit(flame2, (150,50))
            
            gameWindow.blit(ship, (shipX - 150,shipY - 150))
                    
        else:
            
            if boost:
                if frame % 2 == 0:
                    gameWindow.blit(flame3, (150,50))
                else:
                    gameWindow.blit(flame4, (150,50))

            #removing the flame when the ship lands
            else:
                dispX(shipXPOS)
                dispAlt(alt)
                dispTiltFuel(tiltFuel)
                dispThrustFuel(thrustFuel)

                if(vehicle == 0):
                    landinganimation0frameORIG = landinganimation0.drawNextImg(gameWindow)
                    landinganimation0frame = rotate(landinganimation0frameORIG, shipAngle)
                    gameWindow.blit(landinganimation0frame, (shipX - 150, shipY - 150))
                    #gameWindow.blit(lship, (shipX - 150,shipY - 150))
                else:
                    gameWindow.blit(lship, (shipX - 150, shipY - 150))

                pygame.display.update()
            
            if(vehicle == 0):
                landinganimation0frameORIG = landinganimation0.drawNextImg(gameWindow)
                landinganimation0frame = rotate(landinganimation0frameORIG, shipAngle)
                gameWindow.blit(landinganimation0frame, (shipX - 150, shipY - 150))
                #gameWindow.blit(lship, (shipX - 150,shipY - 150))
            else:
                gameWindow.blit(lship, (shipX - 150, shipY - 150))

    dispX(shipXPOS)
    dispAlt(alt)
    dispTiltFuel(tiltFuel)
    dispThrustFuel(thrustFuel)
        
        
def dispX(shipXPOS):
    graphics = font.render("X-Pos: " + str(round(shipXPOS)), 1, WHITE)
    gameWindow.blit(graphics, (15, 20))

def dispAlt(alt):
    if level == 0: #distance at time of deployment is 60 km, so multuply values by 5.5
        if alt * 5.5 > 1000:
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round((alt / 1000) * 5.5) ) + " km", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(((alt + 100)/ 1000) * 5.5)) + " km", 1, WHITE)
        else: #apollo lunar lander sprite is higher than the others
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round(alt * 5.5)) + " m", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(alt + 100) * 5.5) + " m", 1, WHITE)
            
    if level == 1: #distance at "high-gate" is 26000 ft (8000m), so multiply values by 0.75
        if alt * 0.75 > 1000:
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round((alt / 1000) * 0.75) ) + " km", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(((alt + 100)/ 1000) * 0.75)) + " km", 1, WHITE)
        else:
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round(alt * 0.75)) + " m", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(alt + 100) * 0.75) + " m", 1, WHITE)

    if level == 2: #distance at time of deployment is 60 km, so multuply values by 5.5
        if alt * 5.5 > 1000:
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round((alt / 1000) * 5.5) ) + " km", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(((alt + 100)/ 1000) * 5.5)) + " km", 1, WHITE)
        else:
            if vehicle != 1:
                graphics = font.render("Y-Pos: " + str(round(alt * 5.5)) + " m", 1, WHITE)
            else:
                graphics = font.render("Y-Pos: " + str(round(alt + 100) * 5.5) + " m", 1, WHITE)

    gameWindow.blit(graphics, (15, 45))

def dispTiltFuel(tiltFuel):
    graphics = font.render("Angle Fuel:   " + str(round(tiltFuel)), 1, WHITE)
    gameWindow.blit(graphics, (15, 70))

def dispThrustFuel(thrustFuel):
    graphics = font.render("Thrust Fuel: " + str(round(thrustFuel)), 1, WHITE)
    gameWindow.blit(graphics, (15, 95))

def dispTiltAngle(shipAngle):
    graphics = font.render("Angle: ", 1, WHITE)
    gameWindow.blit(graphics, (15, 150))
    if (shipAngle % 360) <= 10 or (shipAngle % 360) >= 350:
        pygame.draw.rect(gameWindow, (0, 255, 0), (180, 150, 18, 18), 0)
    else:
        pygame.draw.rect(gameWindow, (255, 0, 0), (180, 150, 18, 18), 0)
    '''+ str(round(shipAngle % 360))'''

def dispRotationStep(rotationStep):
    graphics = font.render("Rotation: ", 1, WHITE)
    gameWindow.blit(graphics, (15, 175))
    if abs(rotationStep) <= 1:
        pygame.draw.rect(gameWindow, (0, 255, 0), (180, 175, 18, 18), 0)
    else:
        pygame.draw.rect(gameWindow, (255, 0, 0), (180, 175, 18, 18), 0)
    '''+ str(round(rotationStep, 1))'''
    
def dispShipVy(shipVy):
    graphics = font.render("Velocity: ", 1, WHITE)
    gameWindow.blit(graphics, (15, 200))
    if shipVy <= 5:
        pygame.draw.rect(gameWindow, (0, 255, 0), (180, 200, 18, 18), 0)
    else:
        pygame.draw.rect(gameWindow, (255, 0, 0), (180, 200, 18, 18), 0)
    '''+ str(round(shipVy * -1)) + " m/s/30"'''
    
def rotate(image, angle):
    # borrowed from mr. g 
    ORIGINALrect = image.get_rect()
    rotatedImage = pygame.transform.rotate(image,angle)
    rotatedRect = ORIGINALrect.copy()
    rotatedRect.center = rotatedImage.get_rect().center
    rotatedImage = rotatedImage.subsurface(rotatedRect).copy()
    return rotatedImage

def dispVictory():
    gameWindow.blit(youwin, (350, 30))
    pygame.display.update()
    
#---------------------------------------#
#   main program                        #
#---------------------------------------#    

#ship sprites
ORIGINALship0 = pygame.image.load("bigbooster.png").convert_alpha()
landingfeet0 = pygame.image.load("tile007.png").convert_alpha()
ship0 = ORIGINALship0.copy() # keep original image so it does not get distorted 
lship0 = landingfeet0.copy()
landinganimation0 = AnimatedSprite("landingfeet.png", 8) #for animated deployment of legs

ORIGINALship1 = pygame.image.load("apollo.png").convert_alpha()
landingfeet1 = pygame.image.load("apollo.png").convert_alpha()
ship1 = ORIGINALship1.copy()              
lship1 = landingfeet1.copy()

ORIGINALship2 = pygame.image.load("starship.png").convert_alpha()
landingfeet2 = pygame.image.load("starship.png").convert_alpha()
ship2 = ORIGINALship2.copy()              
lship2 = landingfeet2.copy()

#sprites that will be overriden with the ship the player chooses
ORIGINALship = pygame.image.load("tobereplaced.png").convert_alpha()
landingfeet = pygame.image.load("tobereplaced.png").convert_alpha()
ship = pygame.image.load("tobereplaced.png")
lship = pygame.image.load("tobereplaced.png")

#flames
ORIGINALflame1 = pygame.image.load("flame1.png").convert_alpha()
ORIGINALflame2 = pygame.image.load("flame2.png").convert_alpha()
ORIGINALflame3 = pygame.image.load("flame3.png").convert_alpha()
ORIGINALflame4 = pygame.image.load("flame4.png").convert_alpha()

flame1 = ORIGINALflame1.copy()
flame2 = ORIGINALflame2.copy()
flame3 = ORIGINALflame3.copy()
flame4 = ORIGINALflame4.copy()

#level backgrounds
background0 = pygame.transform.scale(pygame.image.load("level0.png").convert(), (WIDTH * 3, HEIGHT * 10)) #convert() reduces lag by making the surface the same pixel format as final display
background1 = pygame.transform.scale(pygame.image.load("level1.png").convert(), (WIDTH * 3, HEIGHT * 10))
background2 = pygame.transform.scale(pygame.image.load("level2.png").convert(), (WIDTH * 3, HEIGHT * 10))

levelbackground = pygame.transform.scale(pygame.image.load("tobereplaced.png").convert(), (WIDTH * 3, HEIGHT * 10))

#more graphics
notunlocked = pygame.image.load("notunlockedrocket.png")
crash = pygame.transform.scale(pygame.image.load("crash.png").convert(), (795,22500))
levelselect0 = pygame.transform.scale(pygame.image.load("levelselect0.png").convert(), (WIDTH * 3, HEIGHT))
levelselect1 = pygame.transform.scale(pygame.image.load("levelselect1.png").convert(), (WIDTH * 3, HEIGHT))
levelselect2 = pygame.transform.scale(pygame.image.load("levelselect2.png").convert(), (WIDTH * 3, HEIGHT))
optionsbackground = pygame.transform.scale(pygame.image.load("optionsphototest.png").convert(), (WIDTH, HEIGHT))
menubackground = pygame.transform.scale(pygame.image.load("menubackground.png").convert(), (WIDTH, HEIGHT * 4))
statsbackground = pygame.image.load("statsbackground.png").convert_alpha()
statsbackground0 = pygame.image.load("statsbackground0.png").convert_alpha()
optionscreen = pygame.transform.scale(pygame.image.load("optionscreen.png").convert(), (WIDTH, HEIGHT * 8))
arrow = pygame.image.load("arrow.png").convert_alpha()
tutorialbackground = pygame.transform.scale(pygame.image.load("tutorialscreen.png").convert(), (WIDTH, HEIGHT * 7))
endscreen = pygame.transform.scale(pygame.image.load("endscreen.png").convert(), (WIDTH, HEIGHT))
youwin = pygame.image.load("youwin.png").convert_alpha()

#music is loaded in when it is played :)
pygame.mixer.music.load("gamemusicbyc418.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops = -1)

#sounds
winsound = pygame.mixer.Sound("winsound.ogg")
explosionsound = pygame.mixer.Sound("explosion.ogg")
buttonsound = pygame.mixer.Sound("button.ogg")
deploysound = pygame.mixer.Sound("deploy.ogg")
gas = pygame.mixer.Channel(4)
gassound = pygame.mixer.Sound("airlock.ogg")
strong = pygame.mixer.Channel(3)
strongpropulsion = pygame.mixer.Sound("strongpropulsion.ogg")
weak = pygame.mixer.Channel(2)
weakpropulsion = pygame.mixer.Sound("weakpropulsion.ogg")

#menu variables
vehicle = 0

#options variables
optionY = 0
sound = True

#tutorial variables
tutorialY = 0

#levelselect variables
levelSelected = 0
levelUnlocked = 0
canPlay = False

#game variables
shipX = WIDTH//2
shipY = HEIGHT//2
shipAngle = 0
vTilt = 0
while vTilt == 0:
    vTilt = randint(-2,2) #set random initial tilt
rotationStep = vTilt
alt = 10800
backgroundY = 5400 - alt // 2
shipXPOS = 0
shipVx = 0
shipVy = 0
gravityA = 9.81

tiltFuel = 100
thrustFuel = 100

deployed = False
crashed = False
boosterStrength = 0.654
boost = False

level = 0

#winscreen variables

#screen booleans
menu = True
options = False
tutorial = False
levelSelect = False
game = False
winscreen = False
inPlay = True

#program variables
clock = pygame.time.Clock()
FPS = 30
frame = 0

#---------------------------------------#

while inPlay:


    #CODE THAT SHOULD ALWAYS BE RUN
    mx, my = pygame.mouse.get_pos()
    click = False
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

    clock.tick(FPS)
    frame = (frame + 1) % FPS                
    pygame.display.update()


    #MENU
    if menu:
        
        gameWindow.blit(menubackground, (0, 0))
 
        button_1 = pygame.Rect(95, 225, 242, 54)
        button_2 = pygame.Rect(95, 302, 242, 54)
        button_3 = pygame.Rect(95, 381, 242, 54)

        if button_1.collidepoint((mx, my)):    
            gameWindow.blit(menubackground, (0, -600))
            if click:
                if sound:
                    buttonsound.play()
                levelSelect = True
                click = False #so it doesn't change sound as well
                menu = False
                
        if button_2.collidepoint((mx, my)):
            gameWindow.blit(menubackground, (0, -1200))
            if click:
                if sound:
                    buttonsound.play()
                options = True
                click = False #so it doesn't change sound as well
                menu = False
                
        if button_3.collidepoint((mx,my)):
            gameWindow.blit(menubackground, (0, -1800))
            if click:
                if sound:
                    buttonsound.play()
                inPlay = False

        
    #OPTIONS
    if options:
              
        gameWindow.blit(optionscreen, (0, optionY * -600))

        if vehicle == 0:
            if levelUnlocked >= 0:
                gameWindow.blit((ORIGINALship0), (474, 168))
            else:
                gameWindow.blit((notunlocked), (474,168))
        if vehicle == 1:
            if levelUnlocked >= 1:
                gameWindow.blit((ORIGINALship1), (474, 168))
            else:
                gameWindow.blit((notunlocked), (474,168))
        if vehicle == 2:
            if levelUnlocked >= 2:
                gameWindow.blit((ORIGINALship2), (474, 168))
            else:
                gameWindow.blit((notunlocked), (474,168))
 
        button_1 = pygame.Rect(95, 225, 242, 54)
        button_2 = pygame.Rect(95, 302, 242, 54)
        button_3 = pygame.Rect(95, 381, 242, 54)
        button_4 = pygame.Rect(520, 479, 45, 41)
        button_5 = pygame.Rect(684, 479, 45, 41)
        
        if button_1.collidepoint((mx, my)):
            if sound:
                optionY = 1
            else:
                optionY = 5
            if click:
                if sound:
                    buttonsound.play()
                tutorialY = 0
                tutorial = True
                options = False
            
        elif button_2.collidepoint((mx, my)):
            if sound:
                optionY = 2
                
            else:
                optionY = 6
            if click:
                sound = not sound
                if not sound:
                    pygame.mixer.music.pause()
                if sound:
                    pygame.mixer.music.unpause()
                    buttonsound.play()
            
        elif button_3.collidepoint((mx,my)):
            if sound:
                optionY = 3
            else:
                optionY = 7
            if click:
                if sound:
                    buttonsound.play()
                if vehicle > levelUnlocked:
                    vehicle = levelUnlocked
                menu = True
                options = False

        else:
            if sound:
                optionY = 0
            else:
                optionY = 4
            
        if button_4.collidepoint((mx,my)):
            if click:
                if sound:
                    buttonsound.play()
                vehicle = (vehicle - 1) % 3

        if button_5.collidepoint((mx,my)):
            if click:
                if sound:
                    buttonsound.play()
                vehicle = (vehicle + 1) % 3
 

    #TUTORIAL
    if tutorial:

        if tutorialY == 6 and not button_3.collidepoint((mx,my)):
            tutorialY = 5
            
        gameWindow.blit(tutorialbackground, (0, tutorialY * -600))
        
        button_1 = pygame.Rect(61, 509, 45, 41)
        button_2 = pygame.Rect(696, 509, 45, 41)
        button_3 = pygame.Rect(617, 502, 138, 54)
        
        if button_1.collidepoint((mx, my)):
            
            if click and tutorialY >= 1:
                tutorialY -= 1
                if sound:
                    buttonsound.play()
                
        if button_2.collidepoint((mx, my)) and tutorialY <= 4:
            if click:
                tutorialY += 1
                click = False #prevent skipping the final tutorial slide
                if sound:
                    buttonsound.play()
                    
        if button_3.collidepoint((mx, my)) and tutorialY >= 5:
            tutorialY = 6
            if click:
                if sound:
                    buttonsound.play()
                menu = True
                tutorial = False
                

    #LEVELSELECT
    if levelSelect:

        if levelUnlocked == 0:
            gameWindow.blit(levelselect0, (int(levelSelected * -800), 0))
        if levelUnlocked == 1:
            gameWindow.blit(levelselect1, (int(levelSelected * -800), 0))
        if levelUnlocked == 2:
            gameWindow.blit(levelselect2, (int(levelSelected * -800), 0))
        
        button_1 = pygame.Rect(200,100, 400, 400)
        button_2 = pygame.Rect(0,0,60,60)
        button_3 = pygame.Rect(0,0,50,600)
        button_4 = pygame.Rect(750,0,50,600)
        gameWindow.blit(arrow, (11, 11))

        canPlay = False
        
        if button_1.collidepoint((mx, my)):
            if click:
                if sound:
                    buttonsound.play()
                if levelSelected < 0.2 and levelUnlocked >= 0:
                    level = 0
                    levelbackground = background0
                    canPlay = True
                if levelSelected > 0.8 and levelSelected < 1.2  and levelUnlocked >= 1:
                    level = 1
                    levelbackground = background1
                    canPlay = True
                if levelSelected > 1.8  and levelUnlocked >= 2:
                    level = 2
                    levelbackground = background2
                    canPlay = True
                
                if vehicle == 0:
                    ORIGINALship, landingfeet, ship, lship = ORIGINALship0, landingfeet0, ship0, lship0
                if vehicle == 1:
                    ORIGINALship, landingfeet, ship, lship = ORIGINALship1, landingfeet1, ship1, lship1 
                if vehicle == 2:
                    ORIGINALship, landingfeet, ship, lship = ORIGINALship2, landingfeet2, ship2, lship2 

                if canPlay:
                    #reset standard game variables
                    if level == 0:
                        while vTilt == 0:
                            vTilt = randint(-2,2) #set random initial tilt

                        tiltFuel = 100
                        thrustFuel = 100
                        
                        shipXPOS = 0
                        shipVx = 0
                        shipVy = 0

                        gravityA = 9.81
                        boosterStrength = round((gravityA / 30) * 1.5, 3)
                        
                    elif level == 1:
                        while vTilt == 0:
                            vTilt = randint(-4,4) #set random initial tilt

                        tiltFuel = randint(80, 99)
                        thrustFuel = randint(80, 99)
                        
                        shipXPOS = randint(-300,300)
                        shipVx = randint(-4,4)
                        shipVy = randint(0,4)

                        gravityA = 1.62
                        boosterStrength = round((gravityA / 30) * 1.5, 3)
                        
                    else:
                        while vTilt == 0:
                            vTilt = randint(-6,6) #set random initial tilt

                        tiltFuel = randint(60, 79)
                        thrustFuel = randint(60,79)
                        
                        shipXPOS = randint(-600,600)
                        shipVx = randint(-8, 8)
                        shipVy = randint(0,8)

                        gravityA = 3.71
                        boosterStrength = round((gravityA / 30) * 1.5, 3)
                        
                    shipAngle = randint(0, 360)
                    rotationStep = vTilt
                    alt = 10800
                    backgroundY = 5400 - alt // 2
        
                    deployed = False
                    crashed = False

                    levelSelect = False
                    game = True
                    
        if button_2.collidepoint((mx, my)):
            if click:
                if sound:
                    buttonsound.play()
                menu = True
                levelSelect = False
                
        if button_3.collidepoint((mx, my)):
            levelSelected -= 0.05
                
        if button_4.collidepoint((mx, my)):
            levelSelected += 0.05

        if levelSelected < 0:
                levelSelected = 0
        if levelSelected > 2:
                levelSelected = 2


    #GAME
    if game:

        redrawGameWindow(background0, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep, boost)
        boost = False
         
        #KEYS
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and tiltFuel > 0:
            if sound and not gas.get_busy():
                gas.play(gassound)
            vTilt = randint(1,2) / 10
            rotationStep += vTilt
            tiltFuel -= 1
            
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and tiltFuel > 0:
            if sound and not gas.get_busy():
                gas.play(gassound)
            vTilt = randint(1,2) / 10
            rotationStep -= vTilt
            tiltFuel -= 1

        if (keys[pygame.K_UP] or keys[pygame.K_w])and thrustFuel > 0:
            boost = True
            shipVx -= boosterStrength * math.sin(math.radians(shipAngle % 360)) * 0.5 #just to make it a little easier
            shipVy -= boosterStrength * math.cos(math.radians(shipAngle % 360)) #0.490 = 1.5x gravity
            if not deployed:
                thrustFuel -= 0.1
                if sound and not strong.get_busy():
                    strong.play(strongpropulsion)
            else:
                thrustFuel -= 0.05
                if sound and not weak.get_busy():
                    weak.play(weakpropulsion)
                    
        if keys[pygame.K_SPACE]:
            deployed = True
            if deployed:
                boosterStrength = (gravityA / 31) #slightly more than 31, prevent deploying too early and costs more fuel
            if sound:
                deploysound.play()
                
        #TILTING SHIP
        if rotationStep > 30:
            rotationStep = 30
        if rotationStep < -30:
            rotationStep = -30

        shipAngle = shipAngle + rotationStep
        ship = rotate(ORIGINALship,shipAngle)
        lship = rotate(landingfeet,shipAngle)
        flame1 = rotate(ORIGINALflame1, shipAngle)
        flame2 = rotate(ORIGINALflame2,shipAngle)
        flame3 = rotate(ORIGINALflame3, shipAngle)
        flame4 = rotate(ORIGINALflame4,shipAngle)
        
        #GRAVITY AND MOVING SHIP
        shipVy += (gravityA / 30)
        alt -= shipVy
        shipXPOS += shipVx
        
        #BACKGROUND SHIFT
        backgroundY = -(5400 - (alt // 2))

        #REACHING ENDPOINT
        if (vehicle != 1 and alt < 0) or (vehicle == 1 and alt < -100):
            alt = 0
            backgroundY = -(5400 - (alt // 2))

            if ((shipAngle % 360) <= 10 or (shipAngle % 360) >= 350) and rotationStep <= 1 and shipVy <= 5 and deployed and abs(shipXPOS) <= 300:
                boost = False
                if sound:
                    winsound.play()
                redrawGameWindow(background0, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep, boost)
                dispVictory()
                
                if level + 1 > levelUnlocked:
                    levelUnlocked = level + 1
                    vehicle = level + 1

                if level == 2:
                    levelUnlocked = 2
                    vehicle = 2
                    winscreen = True
                    game = False
                
            else:
                crashed = True
                if sound:
                    explosionsound.play()
                for count in range(75):
                    redrawGameWindow(background0, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep, boost)
                    gameWindow.blit(crash, (3, -210 + count // 3 * -900)) #3 because 800-795 //2
                    pygame.display.update()

            #let player see what happened
            pygame.time.delay(3000)
            menu = True
            game = False


    #WINSCREEN
    if winscreen:
        
        gameWindow.blit(endscreen, (0,0))

        button_1 = pygame.Rect(698, 517, 45, 41)

        if button_1.collidepoint((mx, my)):
            if click:
                if sound:
                    buttonsound.play()
                menu = True
                winscreen = False

        
#---------------------------------------#     
pygame.quit()
sys.exit()
