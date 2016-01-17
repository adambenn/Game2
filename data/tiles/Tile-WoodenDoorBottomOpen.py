from Tile import tile

class woodenDoorBottomOpen (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,19,1,255)
        self.durability = 20
        self.drop = 10
        self.physical = False
        self.lightBlock = 0
        self.updatePic()
        self.tool = "axe"

    def special(self):
        if self.parentWorld.tiles[self.column][self.row - 1][self.z] == None:
            self.parentWorld.removeTile(self.column,self.row,self.z)
        elif self.parentWorld.tiles[self.column][self.row - 1][self.z].tileType != 18:
            self.parentWorld.removeTile(self.column,self.row,self.z)

    def onClick(self,obj):
        self.changeTile(22)
        self.parentWorld.tiles[self.column][self.row - 1][self.z].changeTile(21)
        self.parentWorld.tiles[self.column][self.row - 2][self.z].changeTile(20)
        self.relight()

def setter(parentWorld, colRow):
    x = woodenDoorBottomOpen(parentWorld, colRow)
    return x
