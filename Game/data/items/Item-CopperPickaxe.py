import Item

class copperPickaxe(Item.tool):
    def __init__(self):
        super().__init__('Copper Pickaxe',16,6,4,5,'pick','Mining')
        self.recipe = [(13,3),(11,2)]
        self.craftingAmount = 1

def setter():
    x = copperPickaxe()
    return x
