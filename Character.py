import math,random,copy,BodyPart,string,Inventory,Woodcutting,Mining,Item,time,ParticleEngine,Dialog,Crafting
def genID(size=10):
    ID = ''
    for i in range(0,size):
        charType = random.randint(0,2)
        if charType == 0:
            ID += string.ascii_lowercase[random.randint(0,len(string.ascii_lowercase)-1)]
        elif charType == 1:
            ID += str(random.randint(0,9))
        elif charType == 2:
            ID += string.ascii_uppercase[random.randint(0,len(string.ascii_uppercase)-1)]
    return ID

def simpleDist(xy1,xy2):#returns the distance between two points
    dist = abs(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2))
    return dist

def getCoordOnObject(deg,r):#returns where a object must be placed to be on the end of an object rotated deg degress with r length
    theta = math.radians(deg)################################MUST CONVERT TO RADIANS WHEN ROTATING IN PYTHON################################
    y = math.cos(theta) * r
    x = math.sin(theta) * r
    return (x,y)
    
class character:#characters are self.world.entities which interact in the game world
    def __init__(self,world, name, arm, helm, leg, body, team='Green', AI=None, health=100, player=False):#construct requires name, arm pic, helm pic, leg pic, body pic, with options team, AI function, health and wheter or its a player
        self.over = world.over
        self.world = world

        self.body = BodyPart.bodyPart(body,world)#creates the necessary limbs
        self.armLeft = BodyPart.bodyPart(arm,world)
        self.armRight = BodyPart.bodyPart(arm,world)
        self.helm = BodyPart.bodyPart(helm,world)
        self.legLeft = BodyPart.bodyPart(leg,world)
        self.legRight = BodyPart.bodyPart(leg,world)

        self.body.x = self.helm.x#sets the body parts to the proper co-ordinates
        self.body.y = self.helm.y + self.helm.size[1]
        self.armLeft.x = self.body.x - (self.body.size[0]//2)
        self.armLeft.y=self.body.y
        self.legLeft.x = self.body.x
        self.legLeft.y = self.body.y + self.body.size[1]
        self.legRight.x = self.legLeft.x + (self.legLeft.size[0] // 2)
        self.legRight.y = self.legLeft.y
        self.armRight.x = self.armLeft.x + self.body.size[0]
        self.armRight.y = self.armLeft.y
        
        self.name = name
        self.xVel = 0#x and y velocity
        self.yVel = 0
        self.x = self.armLeft.x#initializes x to the left arm x
        self.y = self.helm.y# and y to the helm's y co ordinate

        self.size = ((self.armLeft.size[0]//2) + self.body.size[0] + (self.armRight.size[0]//2), self.helm.size[1] + self.body.size[1] + self.legLeft.size[1])# calculates the size of the character

        self.level = 1# initializes the character's level to one

        self.speedLimit = 5#maximum speedlimit
        self.faceRight = True#facing right
        self.isJump = False#jumping
        self.jumpSpeed = self.size[1]//3#jump speed is a third of the objects's size
        self.attackSpeed = 5#rotation factor for attacks
        self.health = health#sets the health
        self.maxHealth = health
        self.weapon = None#stores a weapon object
        self.attacking = False#bool for attacking
        self.team = team
        self.invincible = False#used for after taking damage
        self.flashDelay = 0#amount of flashes after taking damage
        self.flashAmount = 0
        self.damage = 5#initializes damage to 5
        self.baseDamage = 5#damage without level modifiers
        self.damage = self.damage + (self.damage * (self.level / 10))#modifies damage to be based on the characters level
        self.player = player
        self.headingToPoint = False#boolean for if the character is heading to a point in the world
        self.goal = (0,0)#the goal they are trying to get to
        self.activeSpell = False#if they have a spell flying/doing whatever in the game
        self.spellDelay = 0#delay for shooting spells, dependant on the spell type, Spells.py
        self.faceTile = False#if the character is walking into a tile
        self.dead = False#self explanitory, but if the player is dead
        self.exp = 0#current experience, influences when the character goes up a level
        self.expToLevel = 50#the experience to the next level

        self.moveRight = True#wheter or not the character can move right, unused probably
        self.moveLeft = True
        self.target = False#unused also i think
        self.row = self.x//32#current row in the game world
        self.column = self.y//32
        self.fleeing = False#if they are fleeing(AI.villager)
        self.money = 0#current money

        self.spell = None#current spell function
        self.AI = AI#current AI function
        self.control = True#if the character can be controlled(only used fo the player)

        self.ID = genID()#calculates the character specific ID
        self.AIGoal = None#the goal for the AI, used by AI.py
        self.inv = Inventory.objectInventory(self.world.itemList)
        self.selectedSlot = 0
        self.weaponID = None
        self.tileHitTime = time.time()
        self.tileHitDelay = 0.4
        self.baseTileHitPower = 5
        self.damagedTile = (0,0,0)
        self.drawCrack = None
        self.hitRad = (3,5)
        self.openInv = False
        self.skills = []
        self.mining = Mining.mining(self,self.over)
        self.woodcutting = Woodcutting.woodcutting(self,self.over)
        self.skills.append(self.mining)
        self.skills.append(self.woodcutting)
        self.AIPlaceGoals = []
        self.villageRole = None
        self.mustBuild = None
        self.placeDelay = 0.3
        self.placeTime = time.time()

        self.crafting = Crafting.crafting(self.inv,self.world.itemList)
        self.craftable = []

        self.toCraft = (None,None)
        self.lastCraft = None
        self.toGive = None
        self.toTake = (None,None)
        self.currentBuildingProject =None
        self.requiredResources = []

    def touchingEntity(self,length):#returns any self.world.entities within length distance of a point
        touching = []#a list, since more than one entity may be touching the point

        for i in range(len(self.world.entities)):
            dist = simpleDist((self.world.entities[i].x,self.world.entities[i].y),(self.x,self.y))#gets the distance
            if dist <= length:#if the distance is less than the length
                touching.append(i)#add it to the list
        return touching

    def activateHeldItem(self,mxy, radCheck = True, breakBack = False):
        slot = self.inv.inventory[self.selectedSlot]
        if slot[0] != None:
            slot[0].activate(mxy,self)
        else:
            self.weapon = None
            self.weaponID = None
            self.attack()
            if breakBack == True:
                z = 0
            else:
                z = 1
            if self.world.physics.touchingTile((mxy[0],mxy[1]),z,False) == True:
                self.hitTile((mxy[0],mxy[1],z),self.baseTileHitPower,radCheck = radCheck)

    def updateXY(self):#updates the xp and y co-ordinates, and the column + row
        self.x = self.body.x - self.armLeft.size[0]
        self.y = self.helm.y
        self.column = self.x//32
        self.row = self.y//32

    def draw(self):#draws the character
        self.armRight.draw()
        self.legRight.draw()
        self.legLeft.draw()
        self.body.draw()
        self.helm.draw()
        self.armLeft.draw()
        self.showWeapon(self.armLeft)#shows weapon on teh left arm

    def walkAnim(self):#walking animation
        deg = 25#rotates each leg to 25 degrees

        if self.legLeft.rotation == 0:
            self.legLeft.setRotation(deg, -2)

        if self.legRight.rotation == 0:
            self.legRight.setRotation(-deg, 2)
            

    def changeXY(self, amountX=0, amountY=0):#change the XY and y co-ordinate of the character
        self.body.changeXY(amountX, amountY)
        self.helm.changeXY(amountX, amountY)
        self.legLeft.changeXY(amountX, amountY)
        self.legRight.changeXY(amountX, amountY)
        self.armLeft.changeXY(amountX, amountY)
        self.armRight.changeXY(amountX, amountY)
        try:
            self.world.metaData[self.x//32][self.y//32].remove(self)
        except:
            pass

        self.updateXY()
        self.world.metaData[self.x//32][self.y//32].append(self)

    def addSpeed (self, x=0, y=0, breakLimit=False):#adds x and y velocity, breaklimit being wheter or not to surpass teh speed limit
        
        if breakLimit == False:
            if self.xVel > self.speedLimit:
                newX = 0#adds no speed
            elif self.xVel < self.speedLimit * -1:
                newX = 0
            else:
                newX = x
        else:
            newX = x

        if newX > 0:
            if self.moveRight == False:#almost not used, but makes it available
                newX = 0
        else:
            if self.moveLeft == False:
                newX = 0

        
        self.xVel += newX#increases velocity
        self.yVel += y

        self.updateXY()

    def flip(self):#flips the character horizontally
        self.helm.reflectY()
        self.body.reflectY()
        self.armLeft.reflectY()
        self.armRight.reflectY()
        self.legLeft.reflectY()
        self.legRight.reflectY()
        if self.weapon!= None:
            self.weapon.reflectY()

        if self.faceRight == True:
            self.faceRight = False
            self.armLeft.x = self.armRight.x + (self.armLeft.size[0]//3)#moves body parts to new positions
            self.armRight.x = self.body.x - (self.armLeft.size[0]//3)

            leftPos = self.body.x
            self.legLeft.x = self.legRight.x
            self.legRight.x = leftPos

            if self.weapon!= None:
                self.weapon.x -= self.weapon.size[0] + 5
        else:
            self.faceRight = True
            self.armLeft.x = self.body.x - (self.armLeft.size[0] - (self.armLeft.size[0]//3))
            self.armRight.x = self.armLeft.x + self.body.size[0]

            leftPos = self.legLeft.x
            self.legLeft.x = self.legRight.x
            self.legRight.x = leftPos

            if self.weapon!= None:
                self.weapon.x += self.weapon.size[0] + 5


    def limbReset(self):# resets limbs
        self.helm.reset()
        self.body.reset()
        self.armRight.reset()
        self.armLeft.reset()
        self.legRight.reset()
        self.legLeft.reset()
        
        
    def completeRotations (self):#completes limb rotations
        self.helm.completeRotation()
        self.body.completeRotation()
        self.armRight.completeRotation()
        self.armLeft.completeRotation()
        self.legLeft.completeRotation()
        self.legRight.completeRotation()

    def attack(self):#makes character attack
        if self.isJump == False:#only can attack if not jumping of course
            if self.armLeft.rotation == 0:
                self.armLeft.setRotation(180,-self.attackSpeed)
            if self.weapon != None:
                self.weapon.onScreen = True#makes the weapon visible
            self.attacking = True

    def fallAnim(self):#animation for falling
        self.armLeft.setRotation(-90, 0)
        self.armRight.setRotation(90, 0)
        self.legLeft.setRotation(-30,0)
        self.legRight.setRotation(30,0)

    def jump (self):#makes the character jump
        if self.isJump == False:
            self.changeXY(0,-1)#moves up one so no to touch the tile the charcter is on
            self.addSpeed (0,-self.jumpSpeed)#adds speed upwards
            self.isJump = True

    def speak(self, string, duration=5,boxCol=(0,0,255), textCol=(255,255,255)):#makes character say a message
        self.speach = Dialog.dialog(self.world.cam,(self.x + 25, self.y - 50),string,duration,boxCol,textCol)

    def displaySpeech(self):#displays the characters speach above its head
        try:
            self.speach.move((self.x + 25, self.y - 50))
            self.speach.displayDialog()
        except:
            pass

    def main(self):#main function for the character
        self.world.physics.applyPhys(self)#applys self.world.physics to itself
        self.completeRotations()
        self.displaySpeech()
        self.updateXY()
        self.draw()

        if self.dead == False:
            if self.health <= 0:
                self.die()#dies if health is less than 0

        if self.dead == False:
            if self.attacking == True:
                if self.weapon != None:
                    armLen = self.armLeft.size[1] + self.weapon.size[1]#calculates armlength of touching self.world.entities
                else:
                    armLen = self.armLeft.size[1]
                    
                touch = self.touchingEntity(armLen)#gets an array of self.world.entities its touching
                if len(touch) != 0:
                    for r in range(len(touch)):
                        i = touch[r]
                        if self.world.entities[i].ID != self.ID and self.world.entities[i].team != self.team and self.world.entities[i].dead == False:#if the thing its touching is not itself, not on its team and is alive
                            if self.faceRight == False:
                                distance = -15#gets the distance to send it flying
                            else:
                                distance = 15
                            self.world.entities[i].takeDamage(self.damage,attacker=self,distance = distance)#the entity takes the appropraite amount of damage
                            if self.world.entities[i].health <=0:#if the chracter killed it
                                self.rewardFromKill(self.world.entities[i])#gain exp and money

            if self.invincible == True:
                self.flash()#falshes to show invincibility

            if self.headingToPoint == True:
                self.goToPoint(self.goal)#walks towards its goal

            if self.AI != None and self.world.AIOn == True:
                self.AI(self,self.AIGoal)#runs its AI function

            self.spellControl()#controls its spells

            if abs(self.xVel) + abs(self.yVel) == 0:#if the character is not moving at all
                self.control = True#regain control

            if self.exp >= self.expToLevel:
                diff = self.exp - self.expToLevel#gets the difference between the required exp and the current exp
                self.setLevel(self.level + 1)#increases level
                self.exp += diff#adds the difference

            if self.y> self.world.size[1] or self.y < 0:#left the map
                self.die()#die

            if self.drawCrack != None:
                self.world.cam.drawToCamera(self.world.tileCracks[self.drawCrack-1],(32,32),(self.damagedTile[0]*32,self.damagedTile[1]*32))

            self.craftable = self.crafting.getCrafts()
        else:
            self.health = 0#makes health zero to prevent health bar from being negative
            if self.body.opacity > 0:#current opacity
                self.setOp(self.body.opacity - 1)#fades away
            else:
                column = self.body.x + (self.body.size[0]//2)
                row = self.legLeft.y + (self.legLeft.size[1]//2)
                column = column // 32
                row = row//32
                self.world.addTile(column,row,15)
                self.world.tiles[column][row][1].inv = self.inv
                self.world.killCharacter(self.ID)
                
                

    def changeWeapon(self,wep):#changes the character's weapon
        self.weapon = wep
        self.baseDamage = wep.damage#sets the base damage
        self.damage = self.weapon.damage+math.ceil((self.weapon.damage *(self.level / 10)))#applies the level modifier
        if self.faceRight == False:
            self.weapon.reflectX()

    def showWeapon(self,limb):
        if self.weapon != None and self.weapon.onScreen == True:
            if self.weapon.atkStyle == 'Swing':
                if limb.rotation > 0:#if the limb hasnt reverted to normal rotation
                    self.weapon.rotate(limb.rotation, False, True)#rotate the weapon to its rotation
                    r = limb.size[0] + self.weapon.size[0]#get the size
                    theta = limb.rotation#get theta
                    xy = getCoordOnObject(theta,r)#find the co-ordinates
                    x = xy[0]
                    y = xy[1]
                    
                    if self.faceRight == False:
                        x = -x
                    
                    self.weapon.x = limb.x + x
                    self.weapon.y = limb.y + y
                    self.weapon.draw()#draw
                else:
                    self.weapon.onScreen = False

            if limb.rotation == 0:
                self.attacking = False#if limb rotation is 0, stop attacking
                limb.reset()
            else:
                pass

    def setOp(self,val=255):#sets character opacity
        self.armLeft.opacity = val
        self.armRight.opacity = val
        self.legRight.opacity = val
        self.legLeft.opacity = val
        self.body.opacity = val
        self.helm.opacity = val
        if self.weapon != None:
            self.weapon.opacity = val

    def takeDamage(self,amount,attacker = None, distance=10, flashes=2):#take a certain amount of damage
        if self.invincible == False:

            self.jump()
            self.addSpeed(distance, breakLimit=True)
            self.health -= amount
            self.over.updateHealthbar()
            ParticleEngine.createPoint(50, self.x, self.y, (-10,10), (-10,10), (255,0,0), 'Line', grav=True)#create a blood explosion
            self.control = False

            if self.player == True:
                self.flashes = 5#longer flashing for players
            
            self.invincible = True
            self.flashAmount = flashes

    def flash(self, intervalDelay = 20):#flashes the character
        if self.flashAmount > 0:
            if self.flashDelay <= 0:#flash delay is always increasing
                if self.helm.opacity > 0:
                    self.setOp(0)#set the opacity to 0
                    self.flashDelay = intervalDelay
                    self.flashAmount -= 1#lowers the flash amount to go
                else:
                    self.setOp(255)
                    self.flashDelay = intervalDelay
                    self.flashAmount -= 1
            else:
                self.flashDelay -= 1
        else:
            self.invincible = False
            self.setOp(255)

    def jumpTile(self):#used in AI to jump self.over a tile
        if self.faceTile == True:
            if self.isJump == False:
                self.jump()
                if self.faceRight == True:
                    self.addSpeed(2)#adds foward velocity
                else:
                    self.addSpeed(-2)
                
    def goToPoint(self, xy, speed = 3):#character heads to a point
        dist = simpleDist((self.x,self.y),xy)#calculates the distance
        self.headingToPoint = True
        self.goal = xy

        row = xy[0]//32#finds the row of the goal
        column = xy[1]//32

        if row >= (self.world.size[0]//32) - 1 or row <= 0:#off map
            self.headingToPoint = False

        if self.x // 32 == row:#goal reached
            self.headingToPoint = False
        else :
            if self.x < xy[0]:#must go right
                self.addSpeed(speed)
                self.jumpTile()
            else:
                self.addSpeed(-speed)
                self.jumpTile()

    def castSpell(self,spellName, target=None):#casts a spell
        if self.activeSpell == False:
            spell = Spells.getSpell(spellName)#finds the spell function

            if spell != None:#if spell was found
                spell['Spell'](self,target)#casts the spell
                self.activeSpell = True
                self.spellDelay = spell['Cooldown']

    def spellControl(self):#controls when another spell can be cast
        if self.spellDelay <= 0:
            self.activeSpell = False
        else:
            self.spellDelay -= 1

    def rewardFromKill(self,victim):#rewards character from killing a victim
        self.exp += victim.level * 10#exp is 10 times the character's level
        self.money += victim.money + (victim.level * 3)#money is all of the victim's money and the victim's level times 3
        victim.money = 0#sets the victims money accordingly
        if self.ID == self.over.obj.ID:#if the self.overlay object is the current character
            self.over.addToQue('+ $'+str(victim.money + (victim.level * 3))+'!', col=(250,250,0))#let them know of the money they've gained

    def shootProject(self,picIndex,vel,damage, owner = None, goal= None, impactRad = 10, duration = 100, opacity = 255,grav=False, collisionCheck = True):#shoots a projectile
        if self.faceRight == True:
            x = self.x + self.size[0]
        else:
            x = self.x - (projectilePics[picIndex].get_size()[0]//2)
        y = self.y
        xy = (x,y)
        
        a = projectile(projectilePics[picIndex],xy,vel,damage, owner, goal, impactRad, duration, opacity,grav,collisionCheck)
        
    def shootArrow(self,picIndex,location,damage):#shoots an arrow at a specified location with x damage
        self.shootProject(picIndex,(self.x,self.y),(0,0),damage, owner=self, goal = location,grav = True, collisionCheck = True)

    def closestEntity(self,team=''):#finds the closest entity, in a certain team if specified
        '''closeDist = 100000
        closeIndex = None
        myIndex = 0
        
        for i in range(len(self.world.entities)):
            if self.world.entities[i].ID != self.ID:#dont find self
                dist = simpleDist((self.x,self.y),(self.world.entities[i].x,self.world.entities[i].y))#gets distance
                if dist < closeDist:#if the distance is less than the closest distance
                    if team == '' or self.world.entities[i].team == team:
                        closeDist = dist
                        closeIndex = i
            else:
                myIndex = i#finds its own index, may be helpful, may not be

        if closeIndex != None:
            return self.world.entities[closeIndex]
        else:
            return False'''
        col = self.x // 32
        row = self.y // 32

        for c in range(col - 3,col + 3):
            for r in range(row - 5, row + 5):
                try:
                    for i in range(len(self.world.metaData[c][r])):
                        if self.world.metaData[c][r][i] != self:
                            if team == '' or team == self.world.metaData[c][r][i].team:
                                return self.world.metaData[c][r][i]
                except:
                    pass
        return False

    def die(self):#self explanatory
        ParticleEngine.createPoint(150,self.x,self.y,(-15,15),(-10,40),(255,0,0),'Line',grav = True)#blood/confetti depends on violence is sanctified
        self.dead = True

    def setLevel(self, lvl):#sets level, uses math
        self.level = lvl
        self.damage = self.baseDamage + (self.baseDamage * (self.level // 10))#gets the new damage
        self.expToLevel = 50 * 2**(lvl-1)#uses the explicit geometric equation to find the new exp
        self.exp = 0
        self.maxHealth = 100 + (lvl-1)*20#uses the explicit arithmetic equation to find the new max health
        self.health = self.maxHealth
        ParticleEngine.createPoint(10,self.x,self.y,(-10,10),(-10,10),(0,100,255),'Circle Rand',grav = True)#blue circles of fun are diployed
        if self.ID == self.over.obj.ID:#if the self.overlay character is this character
            self.over.addToQue('You have reached level '+str(lvl)+'!')#say good job

    def hitTile(self,xyz,power,skill = None, radCheck = True):
        col = xyz[0] // 32
        row = xyz[1] // 32
        z = xyz[2]

        if self.damagedTile != (col,row,z):
            self.hitTileDamage = 0

        if skill == 'Mining':
            skill = self.mining
            delay = skill.mineSpeed
        elif skill == 'Woodcutting':
            skill = self.woodcutting
            delay = skill.chopSpeed
        else:
            delay = self.tileHitDelay

        if time.time() - self.tileHitTime >= delay:
            self.tileHitTime = time.time()
            if self.world.tiles[col][row][z] != None:
                if self.withinRad((col,row)) == True or radCheck == False:
                    self.hitTileDamage += power
                    self.damagedTile = (col,row,z)
                    if self.hitTileDamage > 0:
                        self.drawCrack = 1
                    if self.hitTileDamage > self.world.tiles[col][row][z].durability // 2:
                        self.drawCrack = 2
                    if self.hitTileDamage > self.world.tiles[col][row][z].durability -(self.world.tiles[col][row][z].durability // 3):
                        self.drawCrack = 3
                    if self.hitTileDamage >= self.world.tiles[col][row][z].durability:
                        if self.world.tiles[col][row][z].drop != None:
                            self.inv.addToInventory(self.world.tiles[col][row][z].drop,self.world.tiles[col][row][z].dropAmount)
                        if skill != None:
                            skill.addExp(self.world.tiles[col][row][z].durability)
                        self.world.removeTile(col,row,z)
                        self.hitTileDamage = 0
                        self.drawCrack = None

    
    def findTileInRad(self,tileType):
        for c in range(self.column - self.hitRad[0],self.column + self.hitRad[0]):
            for r in range(self.row - self.hitRad[1],self.row + self.hitRad[1]):
                for z in range(0,2):
                    try:
                        canHit = True
                        if z == 0:
                            if self.world.tiles[c][r][1] != None:
                                canHit = False
                                
                        if self.world.tiles[c][r][z] != None and canHit == True:
                            if self.world.tiles[c][r][z].tileType == tileType:
                                return (c,r,z)
                    except:
                        pass
        return False

    def setHelm(self,pic,defense):
        new = armor(pic,defense)
        xy = (self.helm.x,self.helm.y)
        self.helm = new
        self.helm.setXY(xy)

        if self.faceRight == False:
            self.helm.reflectY()

    def setChest(self,pic,defense):
        new = armor(pic,defense)
        xy = (self.chest.x,self.chest.y)
        self.chest = new
        self.chest.setXY(xy)

        if self.faceRight == False:
            self.chest.reflectY()
            
    def setLegs(self,pic,defense):
        new1 = armor(pic,defense)
        new2 = armor(pic,defense)
        xy1 = (self.legLeft.x,self.legLeft.y)
        xy2 = (self.legRight.x,self.legRight.y)
        self.legLeft = new1
        self.legLeft.setXY(xy1)
        self.legRight = new2
        self.legRight.setXY(xy2)

        if self.faceRight == False:
            self.legLeft.reflectY()
            self.legRight.reflectY()


    def setArms(self,pic,defense):
        new1 = armor(pic,defense)
        new2 = armor(pic,defense)
        xy1 = (self.armLeft.x,self.armLeft.y)
        xy2 = (self.armRight.x,self.armRight.y)
        self.armLeft = new1
        self.armLeft.setXY(xy1)
        self.armRight = new2
        self.armRight.setXY(xy2)

        if self.faceRight == False:
            self.armLeft.reflectY()
            self.armRight.reflectY()

    def transferToInv(self,slotNum,inv):
        if self.inv.inventory[slotNum][0] != None:
            inv.addToInventory(self.inv.inventory[slotNum][0].ID,self.inv.inventory[slotNum][1])
            self.inv.removeFromInventory(slotNum,self.inv.inventory[slotNum][1])

    def transferItemsToInv(self,inv,item,amount=1):
        for a in range(amount):
            self.transferToInv(self.inv.findItem(item),inv)
                
    def withinRad(self,colRow):
        if abs(self.column - colRow[0]) <= self.hitRad[0] and abs(self.row - colRow[1]) <= self.hitRad[1]:
                return True
        return False
