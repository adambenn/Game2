class physics:#universal physics(excluding projectiles because i hate them)
    def __init__(self,world,gravity = 2):
        self.gravity = gravity
        self.world = world
        
    def isAtScreenBottom(self,obj):#unused
        if obj.y + obj.size[1] <= screenSize[1]:
            return True
        else:
            return False

    def colliding(self,xy1, size1, xy2, size2):#returns true if two rectangles are touching
        if xy1[0] + size1[0] > xy2[0] and xy1[0] < xy2[0] + size2[0] and xy1[1] + size1[1] > xy2[1] and xy1[1] < xy2[1] + size2[1]:
            return True

    def touchingTile(self,xy,z=1,filtered = True):
        try:
            if self.world.tiles[xy[0]//32][xy[1]//32][z] != None:
                if self.world.tiles[xy[0]//32][xy[1]//32][z].tileType != 24:
                    if filtered == True:
                        return self.world.tiles[xy[0]//32][xy[1]//32][z].physical
                    else:
                        return True
            return False
        except:
            return False
    
    def applyPhys(self,obj):#applies physics to an object
        below = False
        beside = False
        above = False
        if self.touchingTile((obj.x + (obj.legLeft.size[0] * 2),(obj.y + obj.size[1]) + obj.yVel)) == True or self.touchingTile((obj.x + obj.armLeft.size[0],(obj.y + obj.size[1]) + obj.yVel)) == True:
            obj.yVel = 0
            below = True

        if self.touchingTile(((obj.x + obj.size[0] + obj.xVel),obj.y)) == True or self.touchingTile(((obj.x + obj.size[0] + obj.xVel),obj.y + obj.legLeft.size[1])) == True or self.touchingTile(((obj.x + obj.size[0] + obj.xVel),obj.y + obj.size[1] - 2)) == True :
            obj.xVel = 0
            beside = True

        if self.touchingTile(((obj.x + obj.armLeft.size[0]) + obj.xVel,obj.y)) == True or self.touchingTile(((obj.x + obj.armLeft.size[0]) + obj.xVel,obj.y + obj.legLeft.size[1])) == True or self.touchingTile(((obj.x + obj.armLeft.size[0]) + obj.xVel,obj.y + obj.size[1] - 2)) == True :
            obj.xVel = 0
            beside = True

        if self.touchingTile((obj.x + (obj.legLeft.size[0] * 2), obj.y + obj.yVel)) == True or self.touchingTile((obj.x + obj.armLeft.size[0], obj.y + obj.yVel)) == True:
            obj.yVel = 0
            above = True

        if below == False:
            obj.addSpeed(0,self.gravity)
        else:
            if self.touchingTile((obj.x + (obj.legLeft.size[0] * 2), obj.y + obj.size[1] - 1)) == True or self.touchingTile((obj.x + obj.armLeft.size[0],obj.y + obj.size[1] - 1)) == True:
                obj.changeXY(0,-1)

        if beside == True:
            obj.faceTile = True
        else:
            obj.faceTile = False

        if obj.xVel != 0:
            obj.changeXY(obj.xVel)
            obj.walkAnim()
            if obj.xVel > 0:
                obj.xVel -= 1
                if obj.faceRight == False:
                    obj.flip()
            else:
                obj.xVel += 1
                if obj.faceRight == True:
                    obj.flip()

        if obj.yVel != 0:
            obj.changeXY(0,obj.yVel)    
            
        objType = str(type(obj))#find the object type
        objType = objType.split("'")
        objType = objType[1]
        objType = objType.split('.')[1]
        
        if objType == 'character':
            if obj.isJump == True:
                if below == True:#moving down
                    obj.isJump = False#no longer jumping
                    obj.y -= 1#lower the y coordinate to prevent some bad stuff probably
                    obj.limbReset()#reset limbs
                    obj.attacking = False#no attack
                else:
                    obj.fallAnim()#fall
