from Tile import tile

class woodPlank (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,5,1,255)
        self.durability = 20
        self.drop = 6
        self.tool = "axe"

def setter(parentWorld, colRow):
    x = woodPlank(parentWorld, colRow)
    return x
