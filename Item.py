import BodyPart, time

class item:
    def __init__(self,name,ID):
        self.name = name
        self.itemType = ''
        self.ID = ID
        self.maxStack = 80
        self.recipe = None
        self.craftAmount = 1

    def activate(self,xy,obj):
        pass


class itemTile(item):
    def __init__(self,name,ID,tileID):
        super().__init__(name,ID)
        self.itemType = "Tile"
        self.tileID = tileID

    def activate(self,xy,obj):
        if time.time() - obj.placeTime >= obj.placeDelay:
            obj.placeTime = time.time()
            if obj.world.physics.touchingTile(xy,1,False) == False:
                obj.world.addTile(xy[0]//32,xy[1]//32,self.tileID)
                obj.inv.removeFromInventory(obj.selectedSlot)
                return True
            else:
                return False

class itemBackTile(itemTile):
    def activate(self,xy,obj):
        if time.time() - obj.placeTime >= obj.placeDelay:
            obj.placeTime = time.time()
            if obj.world.physics.touchingTile(xy,0,False) == False:
                obj.world.addTile(xy[0]//32,xy[1]//32,self.tileID)
                obj.inv.removeFromInventory(obj.selectedSlot)
                return True
            else:
                return False

class weaponItem(item):
    def __init__(self,name,ID,weaponID,damage,attackStyle = "Swing"):
        super().__init__(name,ID)
        self.damage = damage
        self.attackStyle = attackStyle
        self.maxStack = 1
        self.weaponID = weaponID

    def activate(self,xy,obj):
        if obj.weaponID != self.ID:
            obj.weaponID = self.ID
            pic = obj.world.weaponPics[self.weaponID]
            obj.changeWeapon(BodyPart.weapon(pic,obj.world,self.damage,self.attackStyle))
            if obj.faceRight == False:
                obj.weapon.reflectY()
        obj.attack()

class tool(weaponItem):
    def __init__(self,name,ID,weaponID,damage,power,toolType,skill,attackStyle = "Swing"):
        super().__init__(name,ID,weaponID,damage,attackStyle)
        self.power = power
        self.toolType = toolType
        self.skill = skill

    def activate(self,xy,obj,radCheck=True):
        super().activate(xy,obj)
        if obj.world.physics.touchingTile(xy,1,False) == True:
            if obj.world.tiles[xy[0]//32][xy[1]//32][1].tool == self.toolType:
                obj.hitTile((xy[0],xy[1],1),self.power,self.skill,radCheck)

    
