from Tile import tile

class grassTile (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,2,1,255)
        self.durability = 15

    def special(self):
        if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),1) == True:
            self.changeTile(4)
        else:
            if self.row <= self.parentWorld.rows // 4:
                self.changeTile(8)        

def setter(parentWorld, colRow):
    x = grassTile(parentWorld, colRow)
    return x
