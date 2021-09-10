import os
#centre the pygame screen
os.environ['SDL_VIDEO_CENTERED'] = "True"
os.chdir(os.getcwd())
import pygame
from random import randint
from random import randrange
import math
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
def dispAlt():
    graphics = font.render("Altitude: " + str(round(alt) - 1000), 1, WHITE)
    gameWindow.blit(graphics, (50, 50))

def dispX():
    graphics = font.render("X: " + str(round(shipXPOS)), 1, WHITE)
    gameWindow.blit(graphics, (50, 20))

def dispTiltFuel():
    graphics = font.render("Tilt Fuel: " + str(round(tiltFuel)), 1, WHITE)
    gameWindow.blit(graphics, (50, 80))

def dispThrustFuel():
    graphics = font.render("Thrust Fuel: " + str(round(thrustFuel)), 1, WHITE)
    gameWindow.blit(graphics, (50, 110))

def dispTiltAngle():
    graphics = font.render("Tilt Angle: " + str(round(shipAngle % 360)), 1, WHITE)
    gameWindow.blit(graphics, (50, 140))

def dispShipVy():
    graphics = font.render("Velocity: " + str(round(shipVy * -1)) + " m/s/30", 1, WHITE)
    gameWindow.blit(graphics, (50, 170))

def dispRotationStep():
    graphics = font.render("Tilt Velo: " + str(round(rotationStep, 1)), 1, WHITE)
    gameWindow.blit(graphics, (50, 200))
    
def redrawGameWindow():
    gameWindow.fill((0,0,0))
    gameWindow.blit(background, (int(shipXPOS * -1), int(backgroundY)))
    if not crashed:
        if not deployed:
            gameWindow.blit(ship, (shipX - 150,shipY - 150))
        else:
            gameWindow.blit(lship, (shipX - 150,shipY - 150))
    dispX()
    dispAlt()
    dispThrustFuel()
    dispTiltAngle()
    dispTiltFuel()
    dispShipVy()
    dispRotationStep()

    if not crashed:
        pygame.display.update()

def winOrLose(worl):
    graphics = font.render((worl), 1, WHITE)
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

def game():

    ORIGINALship = pygame.image.load("bigbooster.png")
    background = pygame.transform.scale(pygame.image.load("testscreenez.png").convert(), (WIDTH, HEIGHT * 9))
    landingfeet = pygame.image.load("landingfeet.png")
    crash = pygame.transform.scale(pygame.image.load("crash.png").convert(), (795,22500))
    ship = ORIGINALship.copy()              # keep the original image intact, so it does not get distorted 
    lship = landingfeet.copy()

    crashsound = pygame.mixer.Sound("crashsound.ogg")


    shipState = ship
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

    FPS = 30
    frame = 0



    inPlay = True

    while inPlay:
        redrawGameWindow()
        clock.tick(FPS)
        frame = (frame + 1) % FPS

        #KEYS
        pygame.event.clear()                  
        keys = pygame.key.get_pressed()                                         
        if keys[pygame.K_ESCAPE]:           
            inPlay = False
            
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
                    redrawGameWindow()
                    gameWindow.blit(crash, (3, -210 + count // 3 * -900)) #3 because 800-795 //2
                    pygame.display.update()
                    
                winOrLose("L")
            print(shipXPOS)
            pygame.time.delay(5000)
            inPlay = False

#---------------------------------------#
#   main program                        #
#---------------------------------------#    
ORIGINALship = pygame.image.load("bigbooster.png")
background = pygame.transform.scale(pygame.image.load("testscreenez.png").convert(), (WIDTH, HEIGHT * 9))
landingfeet = pygame.image.load("landingfeet.png")
crash = pygame.transform.scale(pygame.image.load("crash.png").convert(), (795,22500))
ship = ORIGINALship.copy()              # keep the original image intact, so it does not get distorted 
lship = landingfeet.copy()

crashsound = pygame.mixer.Sound("crashsound.ogg")

shipState = ship
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

FPS = 30
frame = 0
#---------------------------------------#
clock = pygame.time.Clock()
game()

#---------------------------------------#     
pygame.quit()
    
