from Tile import tile

class trunk (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,6,1)
        self.durability = 20
        self.drop = 6
        self.dropAmount = 4
        self.physical = False
        self.tool = "axe"

def setter(parentWorld, colRow):
    x = trunk(parentWorld, colRow)
    return x
