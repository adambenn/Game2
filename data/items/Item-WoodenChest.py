import Item

class woodenChest(Item.itemTile):
    def __init__(self):
        super().__init__('Wooden Chest',9,15)
        self.recipe = [(6,8)]
        self.craftAmount = 1
        self.maxStack = 16

def setter():
    x = woodenChest()
    return x
