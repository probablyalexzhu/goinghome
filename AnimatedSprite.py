import pygame
from random import randint

#framework borrowed from suyu, modified majorly
class AnimatedSprite():
    
    def __init__(self, spritesheetImg, rows):
        self.sheet = pygame.image.load(spritesheetImg).convert_alpha()
        self.rows = rows
        self.rowH = self.sheet.get_height()/rows
        self.currentRow = 0
        self.currentSprite = self.sheet.subsurface(0, 0, 299, self.rowH)
        self.transformedCurrentSprite = self.currentSprite
        self.angle = 0

    def drawNextImg(self, surf):
        self.currentRow = (self.currentRow + 1)
        if self.currentRow == self.rows:
            self.currentRow = self.rows - 1
        
        self.currentSprite = self.sheet.subsurface((0, self.currentRow*self.rowH, 299, int(self.rowH - 1))) # -1 to account for rounding error
        return self.currentSprite
##      self.boi = self.rotate(self.currentSprite, 270)
##      surf.blit(self.boi, (250,150)) #subsurface? transformed?

    def rotate(self, image, angle):
        # borrowed from mr. g 
        ORIGINALrect = image.get_rect()
        rotatedImage = pygame.transform.rotate(image,angle)
        rotatedRect = ORIGINALrect.copy()
        rotatedRect.center = rotatedImage.get_rect().center
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()
        return rotatedImage
