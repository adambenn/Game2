import Item

class stick(Item.item):
    def __init__(self):
        super().__init__('Stick',11)
        self.recipe = [(6,2)]
        self.craftAmount = 4


def setter():
    x = stick()
    return x
