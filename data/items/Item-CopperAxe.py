import Item

class copperAxe(Item.tool):
    def __init__(self):
        super().__init__('Copper Axe',15,6,4,4,'axe','Woodcutting')
        self.recipe = [(25,2),(11,2)]
        self.craftingAmount = 1

def setter():
    x = copperAxe()
    return x
