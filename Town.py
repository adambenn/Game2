import Spawner, AI, Blueprints

class citizenSpawner(Spawner.spawner):
    def __init__(self,world,charID,location,town,level=1, limit=1, delay=5):
        super().__init__(world,charID,location,level,limit,delay)
        self.town = town
        self.world.spawners.append(self)

    def spawn(self):
        child = self.world.addCharacter(self.charID)
        child.changeXY(self.location[0],self.location[1])
        child.setLevel(self.level)
        self.town.citizens.append(child)
        child.town = self.town
        child.team = self.town.name
        self.children.append(child.ID)        

class town:
    def __init__(self,world,name,colRow,parentTown = None):
        self.world = world
        self.name = name
        self.column = colRow[0]
        self.row = colRow[1]
        self.width = 15
        self.buildings = []
        self.citizens = []
        self.enemyTowns = []
        self.spawners = []
        self.storage = []
        self.mustBuild = []
        self.mustBuild.append(1)
        self.addSpawner(4,(self.column * 32,self.row *32))
        self.addSpawner(3,(self.column * 32+32,self.row *32))
        self.addSpawner(2,(self.column * 32-32,self.row *32))
        self.addTownChest(colRow)
        

    def addSpawner(self,charID,location,level=1, limit=1, delay=5):
        self.spawners.append(citizenSpawner(self.world,charID,location,self,level,limit,delay))

    def addTownChest(self,colRow):
        self.world.addTile(colRow[0],colRow[1],15)
        self.world.tiles[colRow[0]][colRow[1]][1].canBreak = False
        self.storage.append(self.world.tiles[colRow[0]][colRow[1]][1])

    def findClosestVillager(self,colRow,role):
        closest = None
        closestVil = None
        for i in range(len(self.citizens)):
            if self.citizens[i].villageRole == role:
                dist = abs(self.citizens[i].column - colRow[0])
                if closest == None:
                    closest = dist
                    closestVil = self.citizens[i]
                elif dist < closest:
                    closest = dist
                    closestVil = self.citizens[i]

        return closestVil

    def findClosestChest(self,colRow):
        closest = None
        closestChest = None
        for i in range(len(self.storage)):
            dist = abs(self.storage[i].column - colRow[0])
            if closest == None:
                closest = dist
                closestChest = self.storage[i]
            elif dist < closest:
                closest = dist
                closestChest = self.storage[i]

        return closestChest       

    def getVillagersByRole(self,role):
        found = []
        for i in range(len(self.citizens)):
            if self.citizens[i].villageRole == role:
                found.append(self.citizens[i])
        return found

    def transferToNearestChest(self,citizen,itemID,amount=1):
        chest = self.findClosestChest((citizen.column,citizen.row))

        citizen.transferItemsToInv(chest.inv,itemID,amount)

    def main(self):
        for i in range(len(self.citizens)):
            if self.citizens[i].villageRole == 'Lumberjack':
                if self.citizens[i].toGive == None:
                    self.citizens[i].AI = AI.lumberJack
                if self.citizens[i].toGive == None:
                    if self.citizens[i].inv.findItemAmount(6) >= 80:
                        closeCraft = self.findClosestVillager((self.citizens[i].column,self.citizens[i].row),'Crafter')
                        if closeCraft != None:
                            self.citizens[i].AI = AI.give
                            self.citizens[i].AIGoal = closeCraft
                            self.citizens[i].toGive = 6
            elif self.citizens[i].villageRole == 'Builder':
                if self.citizens[i].toTake == (None,None):
                    self.citizens[i].AI = AI.builder
                if len(self.mustBuild) > 0:
                    if self.citizens[i].currentBuildingProject == None:
                        self.citizens[i].mustBuild = self.mustBuild[0]
                        del(self.mustBuild[0])
                if self.citizens[i].currentBuildingProject != None:
                    if AI.hasResources(self.citizens[i],self.citizens[i].currentBuildingProject) == False:
                        if self.citizens[i].requiredResources == []:
                            blues = Blueprints.blueprintList()
                            blue = blues.getBlueprint(self.citizens[i].currentBuildingProject)
                            req = blue.getRequiredResources()
                            for r in range(len(req)):
                                if self.citizens[i].inv.findItemAmount(req[r][0]) < req[r][1]:
                                    self.citizens[i].requiredResources.append((req[r][0],req[r][1] - self.citizens[i].inv.findItemAmount(req[r][0])))
                        else:
                            if self.citizens[i].toTake == (None,None):
                                chests = self.storage
                                for l in range(len(chests)):
                                    if len(self.citizens[i].requiredResources) > 0:
                                        if chests[l].inv.findItemAmount(self.citizens[i].requiredResources[0][0]) >= self.citizens[i].requiredResources[0][1]:
                                            self.citizens[i].toTake = (self.citizens[i].requiredResources[0][0],self.citizens[i].requiredResources[0][1])
                                            self.citizens[i].AIGoal = chests[l]
                                            self.citizens[i].AI = AI.take
                                            del(self.citizens[i].requiredResources[0])
                                            break
            elif self.citizens[i].villageRole == 'Crafter':
                if self.citizens[i].inv.findItemAmount(6) >= 80:
                    self.citizens[i].crafting.craftItem(8,20)
                    self.citizens[i].crafting.craftItem(9,1)
                    self.citizens[i].crafting.craftItem(10,1)
                    self.transferToNearestChest(self.citizens[i],8,40)
                    self.transferToNearestChest(self.citizens[i],9,1)
                    self.transferToNearestChest(self.citizens[i],10,1)
                    self.transferToNearestChest(self.citizens[i],6,20)

    
