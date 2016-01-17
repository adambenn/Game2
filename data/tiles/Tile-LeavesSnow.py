from Tile import tile

class leavesSnow (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,9,1)
        self.durability = 5
        self.physical = False

    def special(self):
        if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),1) == True:
            self.changeTile(7)

def setter(parentWorld, colRow):
    x = leavesSnow(parentWorld, colRow)
    return x
