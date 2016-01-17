import Item

class stoneBrick(Item.itemTile):
    def __init__(self):
        super().__init__('Stone Brick',0,0)
        self.recipe = [(12,2)]
        self.craftAmount = 1

def setter():
    x = stoneBrick()
    return x
