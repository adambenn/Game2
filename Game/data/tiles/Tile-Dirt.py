from Tile import tile

class dirtTile (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,4,1,255)
        self.durability = 15
        self.drop = 4

    def special(self):
        if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),1) == False:
            if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),0) == False:
                self.changeTile(2)

def setter(parentWorld, colRow):
    x = dirtTile(parentWorld, colRow)
    return x
