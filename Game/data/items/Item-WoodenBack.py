import Item

class woodenBack(Item.itemBackTile):
    def __init__(self):
        super().__init__('Wooden Back',8,16)
        self.recipe = [(6,1)]
        self.craftAmount = 2


def setter():
    x = woodenBack()
    return x
