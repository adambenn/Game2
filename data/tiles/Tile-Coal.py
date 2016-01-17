from Tile import tile

class coal (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,14,1,255)
        self.durability = 40
        self.drop = 7

def setter(parentWorld, colRow):
    x = coal(parentWorld, colRow)
    return x
