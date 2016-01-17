import pygame

class camera:#camera is something that views a game world
    def __init__(self,screen,x,y,fov):#construct requires center x, center y, and feild of view, and a screen
        self.centX = x
        self.centY = y
        self.fov = fov
        self.screen= screen

    def blit_alpha(self,target, source, location, opacity):#draws something with an alpha value
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

    def focus(self,xy):#sets the camera on a certain x and y coordinate
        self.centX = xy[0]
        self.centY = xy[1]

    def getRelative(self,xy):#returns the coordinate on the screen from a coordinate in game
        relX = xy[0] - (self.centX - (self.fov[0]//2))
        relY = xy[1] - (self.centY - (self.fov[1]//2))
        return (relX, relY)
    
    def drawToCamera(self,image,size, xy, opacity = 255):#draws a surface to the screen
        relX = self.getRelative(xy)#finds the relative coordinate
        relY = relX[1]
        relX = relX[0]
        
        if relX+size[0] > 0 and relX < self.fov[0]:#if on screen
            if relY+size[0] > 0 and relY < self.fov[1]:
                if opacity != 255:
                    self.blit_alpha(self.screen,image, (relX, relY),opacity)#draw it
                else:
                    self.screen.blit(image, (relX,relY))

    def changeScreen(self,screen,fov):
        self.screen = screen
        self.fov = fov
