import math,pygame
pygame.init()

class bodyPart:#body part is a body part of a character
    def __init__(self,pic,world):#constructer, requires a picture
        self.x = 0
        self.y = 0
        self. pic = pic
        self.world = world
        self.cam = self.world.cam
        self.orig = pic #original picture that way if its changed after tranforms
        self.size = pic.get_size()#body part size in a tuple
        self.reflectedX = False#has been reflected on the x axis
        self.rotation = 0#how much rotation has occured
        self.rotationFactor = -1#how much the object rotates
        self.faceRight = True#is the object facing right
        self.movedRot = (0,0)#distance moved from rotation
        self.opacity = 255
        self.createMask()

    def createMask(self):
        self.mask = pygame.Surface(self.size,pygame.locals.SRCALPHA)
        self.mask.fill((0,0,0,0))
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.pic.get_at((x,y)) != (0,0,0,0):
                    self.mask.set_at((x,y),(0,0,0,255))
        self.mask = self.mask.convert_alpha()
        #self.mask.set_colorkey((0,0,0))
        self.maskOrig = self.mask
        self.maskOp = 0

            
    def draw(self):#draws the body part
        '''dark = pygame.Surface(self.size)
        dark.fill((0,0,0))
        dark = dark.convert()
        self.cam.drawToCamera(dark,self.size,(self.x, self.y),255)'''
        if self.world.tiles[int(self.x//32)][int(self.y//32)][0] != None:
            if self.world.tiles[int(self.x//32)][int(self.y//32)][0].lightLevel == 0:
                self.maskOp = 255 - self.world.tiles[int(self.x//32)][int(self.y//32)][0].opacity
            else:
                self.maskOp = 255 - self.world.tiles[int(self.x//32)][int(self.y//32)][0].lightLevel
        else:
            self.maskOp = 255 - self.world.baseLightLevel
        if self.maskOp < 255:
            self.cam.drawToCamera(self.pic,self.size,(self.x, self.y),self.opacity)#draws the body part to the camera
        if self.maskOp > 0:
            self.cam.drawToCamera(self.mask,self.size,(self.x, self.y),self.maskOp)

    def reflectX(self):#reflects the body part on the x axis
        if self.reflectedX == False:#if it hasnt been reflected
            self.y -= self.size[1] // 2#move it up
            self.reflectedX = True
        else:
            self.y += self.size[1] // 2#move down
            self.reflectedX = False

    def reflectY(self):#reflects the obdy part on the y axis
        if self.faceRight == False:
            self.pic = pygame.transform.flip(self.pic, True, False)#transforms the picture to be flipped horizontally
            self.mask = pygame.transform.flip(self.mask, True, False)
            self.faceRight = True
        else:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.mask = pygame.transform.flip(self.mask, True, False)
            self.faceRight = False
        self.reset()# resets the limbs rotation
            

    def rotate(self, deg=0, flippedH=False, flippedV=False):#rotate the limb
        self.pic = self.orig#resets the picture
        self.mask = self.maskOrig
        self.x += self.movedRot[0]#move the limb to its original position
        self.y += self.movedRot[1]

        if self.faceRight == False:#if the body part faces left
            deg = -deg# invert the degrees
            flippedH = True#flip it horizontally

        if flippedH == True:
            self.pic = pygame.transform.flip(self.pic, True, False)#flip the picture
            self.mask = pygame.transform.flip(self.mask, True, False)

        if flippedV == True:
            self.pic = pygame.transform.flip(self.pic, False, True)
            self.mask = pygame.transform.flip(self.mask, False, True)
                
        self.pic = pygame.transform.rotate(self.pic, deg)#rotate the picture by the degrees
        self.mask = pygame.transform.rotate(self.mask, deg)
       
        if deg > 90 or deg < -90:
            if self.reflectedX == False:
                self.reflectX()

            if deg < -90:
                distX = self.pic.get_rect().center[0] - self.orig.get_rect().center[0]#distance to move on teh x plane is the difference between the center of the original center and the new center
            else:
                distX = 0
                
            distY = self.pic.get_rect().center[1] - self.orig.get_rect().center[1]

        else:
            if self.reflectedX == True:
                self.reflectX()

            if deg < 0:
                distX = self.pic.get_rect().center[0] - self.orig.get_rect().center[0]
            else:
                distX = 0

            distY = 0

        self.x -= distX#moves it backwards
        self.y -= distY
        
        self.movedRot = (distX, distY)#sets the distance moved caused by the rotation

    def reset(self):#resets a body part
        self.pic = self.orig
        self.mask = self.maskOrig

        self.x += self.movedRot[0]
        self.y += self.movedRot[1]
        
        self.movedRot = (0,0)

        self.rotation = 0
        if self.reflectedX == True:
            self.reflectX()

        if self.faceRight == False:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.mask = pygame.transform.flip(self.mask, True, False)


    def completeRotation(self):#if the body part is set to rotate a certain amount, complete the rotation
        
        if self.rotation >= 360 or self.rotation <= -360 :#limits the rotation from exceeding 360
            self.rotation = 0
            self.reset()
        
        if self.rotation != 0:
            if self.rotation + self.rotationFactor < 0 and self.rotation > 0:#if it passed its goal
                self.rotation = 0
                self.reset()
            elif self.rotation + self.rotationFactor > 0 and self.rotation < 0:
                self.rotation = 0
                self.reset()
            else:# if not
                self.rotate(self.rotation + self.rotationFactor)#rotate
                self.rotation += self.rotationFactor

        else:
            self.reset()


    def setRotation(self, deg=0, factor=-1):#sets the body part to rotate a certain amount
        self.rotation = deg
        self.rotationFactor = factor

    def changeXY(self,x, y=0):#change the coordinates of the body part
        self.x += x
        self.y += y

    def setXY(self,xy):
        self.x = xy[0]
        self.y = xy[1]

class weapon(bodyPart):#weapon extends bodyPart and deal extra damage to enemies
    def __init__(self,pic,world,damage, atkStyle = 'Swing'):#constructor that overwrites bodypart's constructor
        super().__init__(pic,world)
        self.onScreen = False
        self.damage = damage#sets the damage
        self.atkStyle = atkStyle#and the attack style

class armor(bodyPart):
    def __init__(self,pic,world,defense):
        super().__init__(pic,cam)
        self.defense = defense

