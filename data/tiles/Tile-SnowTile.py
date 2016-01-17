from Tile import tile

class snowTile(tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,8,1,255)
        self.durability = 15

    def special(self):
        if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),1) == True:
            self.changeTile(4)

def setter(parentWorld, colRow):
    x = snowTile(parentWorld, colRow)
    return x
