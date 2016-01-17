import Item

class torch(Item.itemTile):
    def __init__(self):
        super().__init__('Torch',2,11)
        self.recipe = [(11,1),(7,1)]
        self.craftAmount = 4

def setter():
    x = torch()
    return x
