from Tile import tile
import Inventory

class woodenChest (tile):
    def __init__(self,parentWorld,colRow):
        super().__init__(parentWorld,colRow,15,1,255)
        self.durability = 20
        self.physical = False
        self.inv = Inventory.objectInventory(self.parentWorld.itemList,9)
        self.selectedSlot = 0
        self.drop = 9
        self.updatePic()
        self.tool = "axe"

def setter(parentWorld, colRow):
    x = woodenChest(parentWorld, colRow)
    return x
