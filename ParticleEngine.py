import random, time
import pygame
from pygame.locals import *

'''Created By Adam Benn'''
gravity = False
class particles:#particles class stores a particle
    def __init__(self,x,y,xVel,yVel,col,partType, grav):#construct requires x,y,x velocity, y velocity, color, type, and boolean gravity
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.col = col
        self.type = partType
        self.grav = grav

def drawParticles(screen,allParticles):#draws all the particles onto a screen
    for i in range(len(allParticles)):
        if allParticles[i].type == 'Line':#draws a line particle
            xVel = allParticles[i].x + allParticles[i].xVel
            yVel = allParticles[i].y + allParticles[i].yVel
            
            pygame.draw.aaline(screen,allParticles[i].col,(allParticles[i].x,allParticles[i].y),(xVel,yVel ),1)#aaline is anti aliasised line(looks nice)
        if allParticles[i].type == 'Circle Rand':#particle is a circle of varying size
            rad = random.randint (5,25)

            pygame.draw.circle(screen,allParticles[i].col,(allParticles[i].x,allParticles[i].y),rad,0)
            
        if allParticles[i].type == 'Circle':#circle is a particle with set size
            try :
                rad = allParticles[i].rad
                pygame.draw.circle(screen,allParticles[i].col,(allParticles[i].x,allParticles[i].y),rad,0)
            except:
                rad = random.randint (5,25)
                allParticles[i].rad = rad
                pygame.draw.circle(screen,allParticles[i].col,(allParticles[i].x,allParticles[i].y),rad,0)
                
        if allParticles[i].type == 'Dot':#particle is a dot
            pygame.draw.line(screen, allParticles[i].col,(allParticles[i].x,allParticles[i].y),(allParticles[i].x,allParticles[i].y),1)

def drawParticlesToCamera(screen,camera,allParticles):#same as above, but particles are drawn in their relative positions
    for i in range(len(allParticles)):
        if allParticles[i].type == 'Line':
            xVel = allParticles[i].x + allParticles[i].xVel
            yVel = allParticles[i].y + allParticles[i].yVel
            
            pygame.draw.aaline(screen,allParticles[i].col,camera.getRelative((allParticles[i].x,allParticles[i].y)),camera.getRelative((xVel,yVel )),1)
        if allParticles[i].type == 'Circle Rand':
            rad = random.randint (5,25)

            pygame.draw.circle(screen,allParticles[i].col,camera.getRelative((allParticles[i].x,allParticles[i].y)),rad,0)
            
        if allParticles[i].type == 'Circle':
            try :
                rad = allParticles[i].rad
                pygame.draw.circle(screen,allParticles[i].col,camera.getRelative((allParticles[i].x,allParticles[i].y)),rad,0)
            except:
                rad = random.randint (5,25)
                allParticles[i].rad = rad
                pygame.draw.circle(screen,allParticles[i].col,camera.getRelative((allParticles[i].x,allParticles[i].y)),rad,0)
                
        if allParticles[i].type == 'Dot':
            pygame.draw.line(screen, allParticles[i].col,camera.getRelative((allParticles[i].x,allParticles[i].y)),camera.getRelative((allParticles[i].x,allParticles[i].y)),1)
            
        

def controlParticles(screen,allParticles,gravMod,size=None):#main function
    if size == None:#calculates size
        size = screen.get_size()
    for i in range(len(allParticles)):
        try:
            if gravMod.gravity == True or allParticles[i].grav == True:#if particle has gravity
                    if allParticles[i].grav != False:
                        allParticles[i].yVel += 1#apply gravity
        except:
            break
        
        try :
            allParticles[i].x += allParticles[i].xVel#move particles forward
            allParticles[i].y += allParticles[i].yVel

        except:
            break
    
        if allParticles[i].x > size [0] or allParticles[i].x < 0 or allParticles[i].y > size [1] or allParticles[i].y < 0:#if off screen
            del (allParticles[i])#die


class particlePoints:#particle point is a point where particles come from
    def __init__(self,amount,x,y,xRange,yRange,col,partType,partTime, grav):#amount is amount of particles,x,y,range of x speed, range of y speed, color,type,duration
        #and boolean of gravity
        self.amount = amount
        self.x = x
        self.y = y
        self.xRange = xRange
        self.yRange = yRange
        self.col = col
        self.type = partType
        self.partTime = partTime
        self.grav = grav

        if partTime > 0:#set duration by time
            self.timeStart = time.time()
        else:
            self.timeStart = 0

def createParticle (allParticles,allPoints):#creates particles from the particle points
    for r in range (len(allPoints)):#for every point
        self = allPoints[r]
        for i in range(self.amount):#for every particle in that point
            xmin = self.xRange [0]#find the max and min x speed
            xmax = self.xRange [1]
            
            xVel = random.randint(xmin,xmax)#get random x and y speed within the range
            yVel = random.randint(self.yRange[0],self.yRange[1])

            if xVel == 0 and yVel == 0:#assures the particle is moving
                xVel += 1

            allParticles.append(particles(self.x,self.y,xVel,yVel,self.col,self.type,self.grav))#adds a particle

        if time.time() - self.timeStart > float(self.partTime):#lower particle time
            self.partTime = 0
        
        if self.partTime <= 0:
            self.amount = 0#kill them all if no particles

class modifier:#modifier is a class containing attributes that affect all particles
    def __init__(self,modType):
        if modType == 'Gravity':
            self.gravity = False
    def setGravity(self,boolean):#changes gravity
        self.gravity = boolean

    
def kill (allPoints,i):#kills a point
    allPoints.remove(allPoints[i])

gravMod = modifier('Gravity')
particle = []
points = []

def setGravity(boolean):#I made this program early on in the semester, my coding practice wasn't very good back then, compared to now
    gravMod.setGravity(boolean)

def createPoint (amount,x,y,xRange,yRange,col,partType, partTime=0, grav=None):#creates a point. Like I said, made it a while ago.
    if grav==None:
        grav = gravMod.gravity
    points.append(particlePoints(amount,x,y,xRange,yRange,col,partType,partTime,grav))

def main(screen,camera = None,size = None):#main function
    createParticle(particle,points)

    controlParticles(screen,particle,gravMod,size)
    for i in range(len(points)):#kill any points without particles
        if points[i].amount <= 0:
            kill (points,i)
            break

    if camera == None:#draws particles appropriatly
        drawParticles(screen,particle)
    else:
        drawParticlesToCamera(screen,camera,particle)     
 
