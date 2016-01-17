from Tile import tile

class woodenDoorMiddleClose (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,21,1,255)
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
        elif self.parentWorld.tiles[self.column][self.row + 1][self.z].tileType != 22:
            self.parentWorld.removeTile(self.column,self.row,self.z)
            
        if self.parentWorld.tiles[self.column][self.row - 1][self.z] == None:
            self.parentWorld.removeTile(self.column,self.row,self.z)
        elif self.parentWorld.tiles[self.column][self.row - 1][self.z].tileType != 20:
            self.parentWorld.removeTile(self.column,self.row,self.z)

    def onClick(self,obj):
        self.changeTile(18)
        self.parentWorld.tiles[self.column][self.row - 1][self.z].changeTile(17)
        self.parentWorld.tiles[self.column][self.row + 1][self.z].changeTile(19)
        self.relight()

def setter(parentWorld, colRow):
    x = woodenDoorMiddleClose(parentWorld, colRow)
    return x
