import random, math, Blueprints#math is fun

def simpleDist(xy1,xy2):#calculates distance between to xy coords
    dist = abs(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2))
    return dist

def follow(obj,target):#makes a character object follow another character
    if obj.x < target.x:#if behind
        if obj.faceRight == False:#if not facing
            obj.flip()#turn around
        obj.addSpeed(2)#walk that way
        obj.jumpTile()#jump over a tile if faced with one
    else:
        if obj.faceRight == True:
            obj.flip()
        obj.addSpeed(-2)
        obj.jumpTile()

def give(obj,target):
    if simpleDist((obj.x,obj.y),(target.x,target.y)) > 100:
        follow(obj,target)
    else:
        item = obj.inv.findItem(obj.toGive)
        obj.transferToInv(item,target.inv)
        obj.toGive = None

def take(obj,target):
    if simpleDist((obj.column,obj.column),(target.column,target.column)) > 2:
        follow(obj,target)
    else:
        print(obj.name)
        target.inv.transferItemsToInv(obj.inv,obj.toTake[0],obj.toTake[1])
        obj.toTake = (None,None)

def goRandLoc(obj):#sends a character object to a random coordinate
    if obj.headingToPoint == False:#if heading no where
        randLoc = random.randint(obj.x - 1000, obj.x + 1000)#create random location

        obj.goToPoint((randLoc,obj.y))#head there

def setBluePrint(obj,blueID,colRow):
    blues = Blueprints.blueprintList()
    blue = blues.getBlueprint(blueID)
    obj.AIPlaceGoals = blue.getRel(colRow)

def hasResources(obj,blueID):
    blues = Blueprints.blueprintList()
    blue = blues.getBlueprint(blueID)
    req = blue.getRequiredResources()

    for i in range(len(req)):
        if obj.inv.findItemAmount(req[i][0])< req[i][1]:
            return False
    return True
        
def ghost (ghst, obj):#ai function for ghosts
    if obj == None or obj == False:#varies
        test = ghst.closestEntity('player')#finds the closest entity on the player's team
        if test != False:#if one was found
            ghst.AIGoal = test#target it
            obj = test
    if obj != False and obj != None:#if a target is available
        dist = simpleDist((obj.x , obj.y),(ghst.x,ghst.y))#find distance between

        if dist > obj.armLeft.size[0]:#when beside it
            if ghst.x < obj.x:#if behind
                if obj.faceRight == True:#if the targeted object is facing away
                    ghst.jumpTile()#run at it while jumping blocks
                    ghst.addSpeed(2)
                    ghst.setOp(125)#make opacity half of full
                else:
                    ghst.setOp(10)#if object is facing ghost go almost invisible
                    if dist < 50:#if distance between the two is 50 however
                        ghst.addSpeed(4, breakLimit=True)#run full speed
                        ghst.setOp()#go visible
            else:
                if obj.faceRight == False:
                    ghst.jumpTile()
                    ghst.addSpeed(-2)
                    ghst.setOp(125)
                else:
                    ghst.setOp(10)
                    if dist < 50:
                        ghst.setOp()
                        ghst.addSpeed(-4, breakLimit=True)

        else:
            ghst.setOp()#if within hitting distance
            ghst.attack()#turn visible and attack
    else:
        goRandLoc(ghst)
        ghst.setOp(125)
        
        
def mage(mage, obj):#ai for mages
    if obj == None or obj == False:#if no goal
        test = mage.closestEntity('player')#find a player
        if test != False:
            mage.AIGoal = test#set goal
            obj = mage.AIGoal
    if obj != None and obj != False:
        dist= simpleDist((obj.x , obj.y),(mage.x,mage.y))#finds distance from the goal
        if dist < 300:#if distance is less than 300
            mage.headingToPoint = False#stop wandering
            if obj.x < mage.x:#turn to face the target
                if mage.faceRight == True:
                    mage.flip()
            else:
                if mage.faceRight == False:
                    mage.flip()

            mage.jumpTile()#jump any tiles in the way
            mage.castSpell('Fireblast',obj)#shoot
            mage.target = True#has a target
        else:
            if mage.target == False:#if has no target
                if mage.headingToPoint == False:#not wandering
                    randLoc = random.randint(mage.x - 1000, mage.x + 1000)#find random point

                    mage.goToPoint((randLoc,mage.y))#head there
            else:
                follow(mage,obj)#if has a target, follow them
    else:
        goRandLoc(mage)#if no goal, wander

def villager(obj,null):#AI for villagers
    nearbyEnt = obj.closestEntity()#finds closest entity

    if nearbyEnt != False:#if found someone
        if nearbyEnt.villageRole == None:
            dist = simpleDist((obj.x,obj.y),(nearbyEnt.x,nearbyEnt.y))#get distance
            if obj.headingToPoint == False:#if not wandering
                obj.fleeing = False#dont run

            if dist < 200:#if the distance between the villager and its goal is less than 200
                if nearbyEnt.team == 'Enemy':#if its an enemy
                    obj.speak('Ahhhhh!!!')#scream
                    if nearbyEnt.x > obj.x:
                        point = obj.x - 1000#find a point in the opposite direction
                    else:
                        point = obj.x + 1000
                    obj.goToPoint((point,obj.y))#go there
                    obj.fleeing = True#edit, run there
                elif nearbyEnt.team == 'player':#if sees a player
                    if obj.fleeing == False:#and not running for its life
                        obj.headingToPoint = False#stop wandering
                        obj.speak('Hello '+nearbyEnt.name+'!')#greet the player
        else:
            if nearbyEnt.team == obj.team:
                if nearbyEnt.villageRole == 'Villager':
                    obj.speak('Hi')
            goRandLoc(obj)
    else:        
        goRandLoc(obj)#if distance is greater than 200, wander

def adventurer(obj,null):#AI for the adventurer
    if obj.AIGoal != None:#if has a goal
        obj.headingToPoint = False#stop wandering
        dist = simpleDist((obj.x , obj.y),(obj.AIGoal.x,obj.AIGoal.y))#find distance

        if dist > obj.size[0]:#if far
            follow(obj,obj.AIGoal)#follow
        else:
            obj.attack()#if close attack
    else:
        test = obj.closestEntity('Enemy')# if has no goal find an enemy
        if test == False or test == None:
            goRandLoc(obj)#wander if nothing was found
        else:
            obj.AIGoal = test#target if found

def lumberJack(obj,null):
    trunk = obj.findTileInRad(6)

    if trunk == False:
        goRandLoc(obj)
    else:
        hit= False
        if obj.inv.inventory[obj.selectedSlot][0] != None:
            if obj.inv.inventory[obj.selectedSlot][0].itemType == 'Axe':
                obj.headingToPoint = False
                obj.activateHeldItem((trunk[0]*32,trunk[1]*32,trunk[2]))
                hit = True

        if hit == False:
            found = obj.inv.findItemType('Axe')
            if found == False:
                goRandLoc(obj)
                obj.speak('I have no axe! :(')
            else:
                obj.selectedSlot = found
                
    close = obj.closestEntity('Villager')
    if close != False and close != None:
        if close.villageRole != None and close.team == obj.team:
            if close.villageRole == 'Villager':
                obj.speak('Hi!')

def builder(obj,null):
    if obj.AIPlaceGoals == [] and obj.mustBuild != None and obj.yVel ==0:
        if obj.mustBuild != None:
            lowest = obj.world.topFilledRow(obj.column,1)
            blues = Blueprints.blueprintList()
            blue = blues.getBlueprint(obj.mustBuild)
            for i in range(blue.width):
                if obj.world.topFilledRow(obj.column + i,1) > lowest:#lower rows have higher row values
                    lowest = obj.world.topFilledRow(obj.column + i,1)
            
            setBluePrint(obj,obj.mustBuild,(obj.column,lowest))
            obj.currentBuildingProject = obj.mustBuild
            obj.mustBuild = None
            obj.buildStage = 1
            obj.toBreak = []
            for i in range(len(obj.AIPlaceGoals)):
                obj.toBreak.append((obj.AIPlaceGoals[i][1],obj.AIPlaceGoals[i][0]))
    else:
        if obj.AIPlaceGoals != []:
            if obj.buildStage == 1:
                if obj.toBreak != []:
                    if obj.world.tiles[obj.toBreak[0][0]][obj.toBreak[0][1]][1] != None and obj.world.tiles[obj.toBreak[0][0]][obj.toBreak[0][1]][1].canBreak == True:
                        obj.selectedSlot = obj.inv.findEmpty()
                        obj.activateHeldItem((obj.toBreak[0][0]*32,obj.toBreak[0][1]*32,1),radCheck = False)
                    else:
                        if obj.world.tiles[obj.toBreak[0][0]][obj.toBreak[0][1]][0] != None and obj.world.tiles[obj.toBreak[0][0]][obj.toBreak[0][1]][0].canBreak == True:
                            obj.selectedSlot = obj.inv.findEmpty()
                            obj.activateHeldItem((obj.toBreak[0][0]*32,obj.toBreak[0][1]*32,1),radCheck = False, breakBack = True)
                        else:
                            del(obj.toBreak[0])
                else:
                    if hasResources(obj,obj.currentBuildingProject) == True:
                        obj.buildStage = 2
                        
            if obj.buildStage == 2:
                if obj.inv.findItemAmount(obj.AIPlaceGoals[0][3]) > 0:
                    obj.selectedSlot = obj.inv.findItem(obj.AIPlaceGoals[0][3])
                    if obj.activateHeldItem((obj.AIPlaceGoals[0][1]*32,obj.AIPlaceGoals[0][0]*32,1),radCheck=False) == True:
                        del(obj.AIPlaceGoals[0])
                    else:
                        obj.selectedSlot = obj.inv.findEmpty()
                        obj.activateHeldItem((obj.AIPlaceGoals[0][1]*32,obj.AIPlaceGoals[0][0]*32,1),radCheck =False)
                else:
                    obj.speak("I'm missing an item."+str(obj.AIPlaceGoals[0][3]))
        else:
            obj.buildStage = 0
            if obj.town != None:
                obj.town.buildings.append(obj.currentBuildingProject)
            obj.currentbuildingProject = None

def crafter(obj,null):
    if obj.toCraft[0] != None:
        for i in range(obj.toCraft[1]):
            if obj.craftable.count(obj.toCraft[0]) > 0:
                obj.crafting.craftItem(obj.toCraft[0])
                obj.toCraft = (obj.toCraft[0],obj.toCraft[1]-1)
                if obj.toCraft[0] <= 0:
                    obj.lastCraft = obj.toCraft[0]
                    obj.toCraft = (None,None)
                    break
        
