from Tile import tile

class airBack (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,24,0,1)
        self.durability = 0
        self.lightBlock = 0
        self.lightLevel = 255
        self.canBreak = False
        self.physical = False
        self.tool = "none"

    def special(self):
        if self.parentWorld.lighting != False:
            self.lightLevel = self.parentWorld.baseLightLevel

def setter(parentWorld, colRow):
    x = airBack(parentWorld, colRow)
    return x
