from Tile import tile

class stone (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,12,1)#parentWorld,colRow,tileID,z
        self.durability = 30
        self.drop = 12
        self.lightBlock = 25

def setter(parentWorld, colRow):
    x = stone(parentWorld, colRow)
    return x
