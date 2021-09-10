import os
#centre the pygame gameWindow
os.environ['SDL_VIDEO_CENTERED'] = "True"
os.chdir(os.getcwd())
import pygame
from random import randint
from random import randrange
import math
import sys
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
WIDTH  = 800
HEIGHT = 600
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

font = pygame.font.SysFont("Courier New", 24)


BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED = (255,0,0)

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def dispAlt(alt):
    graphics = font.render("Altitude: " + str(round(alt) - 1000), 1, WHITE)
    gameWindow.blit(graphics, (50, 50))

def dispX(shipXPOS):
    graphics = font.render("X: " + str(round(shipXPOS)), 1, WHITE)
    gameWindow.blit(graphics, (50, 20))

def dispTiltFuel(tiltFuel):
    graphics = font.render("Tilt Fuel: " + str(round(tiltFuel)), 1, WHITE)
    gameWindow.blit(graphics, (50, 80))

def dispThrustFuel(thrustFuel):
    graphics = font.render("Thrust Fuel: " + str(round(thrustFuel)), 1, WHITE)
    gameWindow.blit(graphics, (50, 110))

def dispTiltAngle(shipAngle):
    graphics = font.render("Tilt Angle: " + str(round(shipAngle % 360)), 1, WHITE)
    gameWindow.blit(graphics, (50, 140))

def dispShipVy(shipVy):
    graphics = font.render("Velocity: " + str(round(shipVy * -1)) + " m/s/30", 1, WHITE)
    gameWindow.blit(graphics, (50, 170))

def dispRotationStep(rotationStep):
    graphics = font.render("Tilt Velo: " + str(round(rotationStep, 1)), 1, WHITE)
    gameWindow.blit(graphics, (50, 200))
    
def redrawGameWindow(background, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep):
    gameWindow.fill(BLACK)
    gameWindow.blit(background, (int(shipXPOS * -1), int(backgroundY)))
    if not crashed:
        if not deployed:
            gameWindow.blit(ship, (shipX - 150,shipY - 150))
        else:
            gameWindow.blit(lship, (shipX - 150,shipY - 150))
    dispX(shipXPOS)
    dispAlt(alt)
    dispThrustFuel(thrustFuel)
    dispTiltAngle(shipAngle)
    dispTiltFuel(tiltFuel)
    dispShipVy(shipVy)
    dispRotationStep(rotationStep)

    if not crashed:
        pygame.display.update()

def winOrLose(worl):
    graphics = font.render((worl), 1, BLACK)
    gameWindow.blit(graphics, (400, 50))
    pygame.display.update()
    
def rotate(image, angle):
    # borrowed from mr. g 
    ORIGINALrect = image.get_rect()
    rotatedImage = pygame.transform.rotate(image,angle)
    rotatedRect = ORIGINALrect.copy()
    rotatedRect.center = rotatedImage.get_rect().center
    rotatedImage = rotatedImage.subsurface(rotatedRect).copy()
    return rotatedImage

def game(frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship, lship, shipXPOS, backgroundY, alt, deployed, crashed, vTilt, ORIGINALship, landingfeet, vehicle):

    #frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship, lship, shipXPOS, backgroundY, alt, deployed, crashed, vTilt = level5()

    inPlay = True

    while inPlay:
        print(vehicle)
        redrawGameWindow(background, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep)
        
        clock.tick(FPS)
        frame = (frame + 1) % FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #KEYS
        pygame.event.clear()                  
        keys = pygame.key.get_pressed()                                         
        if keys[pygame.K_ESCAPE]:           
            pygame.quit()
            sys.exit()
            
        if keys[pygame.K_LEFT] and tiltFuel > 0:
            vTilt = randint(1,2) / 10
            rotationStep += vTilt
            tiltFuel -= 1
            
        if keys[pygame.K_RIGHT] and tiltFuel > 0:
            vTilt = randint(1,2) / 10
            rotationStep -= vTilt
            tiltFuel -= 1

        if keys[pygame.K_UP] and thrustFuel > 0:
            
            shipVx -= boosterStrength * math.sin(math.radians(shipAngle % 360)) * 0.2 # just to make it a little easier
            shipVy -= boosterStrength * math.cos(math.radians(shipAngle % 360)) # 0.654 = twice gravity
            if not deployed:
                thrustFuel -= 0.1
            else:
                thrustFuel -= 0.05
                
        if keys[pygame.K_SPACE]:
            shipState = lship
            deployed = True
            if deployed:
                boosterStrength = (gravityA / 31) #slightly more than 31, prevent deploying too early and costs more fuel

        #TILTING SHIP
        if rotationStep > 30:
            rotationStep = 30
        if rotationStep < -30:
            rotationStep = -30

        shipAngle = shipAngle + rotationStep
        ship = rotate(ORIGINALship,shipAngle)
        lship = rotate(landingfeet, shipAngle)


        ship1 = rotate(ORIGINALship,shipAngle)
        lship = rotate(landingfeet, shipAngle)
        
        #GRAVITY
        shipVy += (gravityA / 30)
        alt -= shipVy
        #print("V: " + str(round(shipVy)))
        shipXPOS += shipVx
        
        #BACKGROUND SHIFT
        backgroundY = -(5400 - (alt // 2))

        if alt < 1000:
            alt = 1000
            backgroundY = -(5400 - (alt // 2))
            if ((shipAngle % 360) <= 10 or (shipAngle % 360) >= 350) and rotationStep <= 1 and shipVy <= 10 and deployed and abs(shipXPOS) <= 300:
                print("W")
                    
                winOrLose("W")
            else:
                crashed = True
                print("L")
                crashsound.play()
                for count in range(75):
                    redrawGameWindow(background, shipXPOS, backgroundY, crashed, deployed, ship, shipX, shipY, lship, alt, tiltFuel, thrustFuel, shipAngle, shipVy, rotationStep)
                    gameWindow.blit(crash, (3, -210 + count // 3 * -900)) #3 because 800-795 //2
                    pygame.display.update()
                    
                winOrLose("L")
            print(shipXPOS)
            pygame.time.delay(5000)
            inPlay = False
            
'''
def level5():
    # in order of frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship, lship, shipXPOS, backgroundY, alt, deployed, crashed, vTilt
    vTilt5 = 0
    while vTilt5 == 0:
        vTilt = randint(-2,2)

    ship5 = pygame.image.load("bigbooster.png").copy()
    lship5 = pygame.image.load("landingfeet.png").copy()
    return 0,100,0,0,100,ship5,0.654,0,ship5,lship5.copy,0,0,10800,False,False,vTilt5
'''

def menu(vehicle):

    click = False

    while True:
        print(vehicle)
        gameWindow.blit(menubackground, (0, 0))
 
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(95, 225, 242, 54)
        button_2 = pygame.Rect(95, 302, 242, 54)
        button_3 = pygame.Rect(95, 381, 242, 54)
        if button_1.collidepoint((mx, my)):
            
            gameWindow.blit(menubackground, (0, -600))
            pygame.draw.rect(gameWindow, (255, 0, 0), button_1, 1)
            if click:
                levelSelect(vehicle)
        if button_2.collidepoint((mx, my)):
            
            gameWindow.blit(menubackground, (0, -1200))
            pygame.draw.rect(gameWindow, (255, 0, 0), button_2, 1)
            if click:
                vehicle = options(vehicle)
        if button_3.collidepoint((mx,my)):
            
            gameWindow.blit(menubackground, (0, -1800))
            pygame.draw.rect(gameWindow, (255, 0, 0), button_3, 1)
            if click:
                pygame.quit()
                sys.exit()
 
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()

def options(vehicle):

    vehicleValue = vehicle
    vehicleValue -= 1

    click = False

    while True:

        gameWindow.blit(optionsbackground, (0, 0))

        if vehicleValue == 0:
            gameWindow.blit((ORIGINALship1), (450, 200))
        if vehicleValue == 1:
            gameWindow.blit((ORIGINALship2), (450, 200))
        if vehicleValue == 2:
            gameWindow.blit((ORIGINALship3), (450, 200))
        if vehicleValue == 3:
            gameWindow.blit((ORIGINALship4), (450, 200))
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(95, 225, 142, 54)
        button_2 = pygame.Rect(95, 302, 142, 54)
        button_3 = pygame.Rect(95, 381, 142, 54)
        button_4 = pygame.Rect(750,275,50,50)
        if button_1.collidepoint((mx, my)):
            if click:
                pass
        if button_2.collidepoint((mx, my)):
            if click:
                pass
        if button_3.collidepoint((mx,my)):
            if click:
                return vehicleValue + 1
                menu(vehicle)
                
        if button_4.collidepoint((mx,my)):
            if click:
                vehicleValue = (vehicleValue + 1) % 4
                print(vehicleValue)
                    
                
        pygame.draw.rect(gameWindow, (255, 0, 0), button_1, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_2, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_3, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_4, 1)
 
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()

def levelSelect(vehicle):

    click = False
    levelSelected = 0

    while True:
 
        gameWindow.blit(levelselect, (int(levelSelected * -800), 0))
        
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(200,100, 400, 400)
        button_2 = pygame.Rect(0,0,50,50)
        button_3 = pygame.Rect(0,0,200,600)
        button_4 = pygame.Rect(600,0,200,600)
        if button_1.collidepoint((mx, my)):
            if click:
                if levelSelected < 0.1:
                    if vehicle == 1:
                        game(frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship1, lship1, shipXPOS, backgroundY, alt, deployed, crashed, vTilt, ORIGINALship1, landingfeet1, vehicle)
                    if vehicle == 2:
                        game(frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship2, lship2, shipXPOS, backgroundY, alt, deployed, crashed, vTilt, ORIGINALship2, landingfeet2, vehicle)
                    if vehicle == 3:
                        game(frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship3, lship3, shipXPOS, backgroundY, alt, deployed, crashed, vTilt, ORIGINALship3, landingfeet3, vehicle)
                    if vehicle == 4:
                        game(frame, rotationStep, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship4, lship4, shipXPOS, backgroundY, alt, deployed, crashed, vTilt, ORIGINALship4, landingfeet4, vehicle)
                    
                    
                if levelSelected > 0.9 and levelSelected < 1.1:
                    game(frame, 0, tiltFuel, shipVx, shipVy, thrustFuel, shipState, boosterStrength, shipAngle, ship2, lship2, shipXPOS, backgroundY, 100000, deployed, crashed, 0, ORIGINALship2, landingfeet2, vehicle)
                if levelSelected > 1.9 and levelSelected < 2.1:
                    game(9990,9990,9990,9990,9990,9990,9990,9990,9990, ship3, lship3, 9990, 9990, 9990, False, False, 0, ORIGINALship3, landingfeet3, vehicle)
        if button_2.collidepoint((mx, my)):
            if click:
                menu(vehicle)
        if button_3.collidepoint((mx, my)):
            levelSelected = round(levelSelected - 0.01, 2)
            if levelSelected < 0:
                levelSelected = 0
        if button_4.collidepoint((mx, my)):
            levelSelected = round(levelSelected + 0.01, 2)
            if levelSelected > 4:
                levelSelected = 4

        pygame.draw.rect(gameWindow, (255, 0, 0), button_1, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_2, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_3, 1)
        pygame.draw.rect(gameWindow, (255, 0, 0), button_4, 1)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        print(vehicle)
        pygame.display.update()

#---------------------------------------#
#   main program                        #
#---------------------------------------#    
ORIGINALship1 = pygame.image.load("bigbooster.png")
landingfeet1 = pygame.image.load("landingfeet.png")
ship1 = ORIGINALship1.copy()              # keep the original image intact, so it does not get distorted 
lship1 = landingfeet1.copy()

ORIGINALship2 = pygame.image.load("dream.png")
landingfeet2 = pygame.image.load("ldream.png")
ship2 = ORIGINALship2.copy()              # keep the original image intact, so it does not get distorted 
lship2 = landingfeet2.copy()

ORIGINALship3 = pygame.image.load("apollo.png")
landingfeet3 = pygame.image.load("apollo.png")
ship3 = ORIGINALship3.copy()              # keep the original image intact, so it does not get distorted 
lship3 = landingfeet3.copy()

ORIGINALship4 = pygame.image.load("starship.png")
landingfeet4 = pygame.image.load("starship.png")
ship4 = ORIGINALship4.copy()              # keep the original image intact, so it does not get distorted 
lship4 = landingfeet4.copy()

vehicle = 1

background = pygame.transform.scale(pygame.image.load("testscreenez.png").convert(), (WIDTH, HEIGHT * 9))
crash = pygame.transform.scale(pygame.image.load("crash.png").convert(), (795,22500))
levelselect = pygame.transform.scale(pygame.image.load("levelselect.png").convert(), (WIDTH * 5, HEIGHT))
optionsbackground = pygame.transform.scale(pygame.image.load("optionsphototest.png").convert(), (WIDTH, HEIGHT))
menubackground = pygame.transform.scale(pygame.image.load("menubackground.png").convert(), (WIDTH, HEIGHT * 4)) #convert() reduces lag by making the surface the same pixel format as final display
crashsound = pygame.mixer.Sound("crashsound.ogg")

shipState = ship1
shipX = WIDTH//2
shipY = HEIGHT//2
shipAngle = 0
vTilt = 0
while vTilt == 0:
    vTilt = randint(-2,2) #ez vs hard
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
boosterStrength = 0.654

crashed = False

print("Hit ESC to end the program.")
clock = pygame.time.Clock()
FPS = 30
frame = 0
#---------------------------------------#

menu(vehicle)

#---------------------------------------#     
pygame.quit()
sys.exit()
    
