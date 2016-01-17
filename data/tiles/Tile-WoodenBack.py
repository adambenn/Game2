from Tile import tile

class woodenBack (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,16,0,255)
        self.durability = 20
        self.drop = 8
        self.tool = "axe"

def setter(parentWorld, colRow):
    x = woodenBack(parentWorld, colRow)
    return x
