from Tile import tile

class leaves (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,7,1)
        self.durability = 5
        self.physical = False

    def special(self):
        if self.parentWorld.physics.touchingTile((self.column*32,(self.row-1)*32),False) == False:
            if self.row <= self.parentWorld.rows // 4:
                self.changeTile(9)

def setter(parentWorld, colRow):
    x = leaves(parentWorld, colRow)
    return x
