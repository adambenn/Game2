from Tile import tile

class backDirt (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,10,0,255)
        self.durability = 15

def setter(parentWorld, colRow):
    x = backDirt(parentWorld, colRow)
    return x
