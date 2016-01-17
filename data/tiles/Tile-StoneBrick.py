from Tile import tile

class stoneBrick (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,0,1,255)
        self.durability = 30
        self.drop = 0
        self.lightBlock = 25

def setter(parentWorld, colRow):
    x = stoneBrick(parentWorld, colRow)
    return x
