from Tile import tile

class bedRock (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,2,1,255)
        self.durability = 1000
        self.tool = "none"

def setter(parentWorld, colRow):
    x = bedRock(parentWorld, colRow)
    return x
