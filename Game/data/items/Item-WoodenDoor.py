import Item

class woodenDoor(Item.item):
    def __init__(self):
        super().__init__('Wooden Door',10)
        self.recipe = [(6,12)]
        self.craftAmount = 1
        self.maxStack = 1

    def activate(self,xy,obj):
        if obj.world.physics.touchingTile(xy,1,False) == False and obj.world.physics.touchingTile((xy[0],xy[1]+32),1,False) == False and obj.world.physics.touchingTile((xy[0],xy[1]+64),1,False) == False:
            obj.world.placeDoor(xy[0]//32,xy[1]//32,"Wooden")        

def setter():
    x = woodenDoor()
    return x
