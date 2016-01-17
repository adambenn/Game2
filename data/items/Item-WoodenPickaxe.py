import Item

class woodenPickaxe(Item.tool):
    def __init__(self):
        super().__init__('Wooden Pickaxe',14,5,3,4,'pick','Mining')
        self.recipe = [(6,3),(11,2)]
        self.craftingAmount = 1

def setter():
    #name,itemID,weaponPictureID,damage,power,type,skill
    x = woodenPickaxe()
    return x

