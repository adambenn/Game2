from Tile import tile

class copper (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,25,1)#parentWorld,colRow,tileID,z
        self.durability = 45
        self.drop = 13
        self.lightBlock = 25

def setter(parentWorld, colRow):
    x = copper(parentWorld, colRow)
    return x
