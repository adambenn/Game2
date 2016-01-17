from Tile import tile

class invisablock (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,3,1,255)
        self.durability = 1000
        self.tool = "none"

def setter(parentWorld, colRow):
    x = invisablock(parentWorld, colRow)
    return x
