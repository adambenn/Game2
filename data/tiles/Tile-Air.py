from Tile import tile

class air (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,23,1,1)
        self.durability = 0
        self.lightBlock = 0
        self.canBreak = False
        self.physical = False
        self.tool = "none"

def setter(parentWorld, colRow):
    x = air(parentWorld, colRow)
    return x
