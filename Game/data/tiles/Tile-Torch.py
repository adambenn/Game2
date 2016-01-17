from Tile import tile

class torch (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,11,1,255)
        self.durability = 1
        self.physical = False
        self.lightLevel = 255
        self.lightBlock = 0
        self.updatePic()
        

def setter(parentWorld, colRow):
    x = torch(parentWorld, colRow)
    return x
