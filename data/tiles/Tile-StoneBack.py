from Tile import tile

class stoneBack (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,13,0,255)
        self.durability = 30

def setter(parentWorld, colRow):
    x = stoneBack(parentWorld, colRow)
    return x
