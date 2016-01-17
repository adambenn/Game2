from Tile import tile

class woodenDoorTopClose (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,20,1,255)
        self.durability = 20
        self.drop = 10
        self.physical = True
        self.drawBack = True
        self.lightBlock = 25
        self.updatePic()
        self.tool = "axe"

    def special(self):
        if self.parentWorld.tiles[self.column][self.row + 1][self.z] == None:
            self.parentWorld.removeTile(self.column,self.row,self.z)
        elif self.parentWorld.tiles[self.column][self.row + 1][self.z].tileType != 21:
            self.parentWorld.removeTile(self.column,self.row,self.z)

    def onClick(self, obj):
        self.changeTile(17)
        self.parentWorld.tiles[self.column][self.row + 1][self.z].changeTile(18)
        self.parentWorld.tiles[self.column][self.row + 2][self.z].changeTile(19)
        self.relight()      

def setter(parentWorld, colRow):
    x = woodenDoorTopClose(parentWorld, colRow)
    return x
