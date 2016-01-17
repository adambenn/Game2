class crafting:
    def __init__(self,inv,items):
        self.inv = inv
        self.items = items

    def getCrafts(self):
        itemsChecked = []
        itemAmounts = []
        for i in range(len(self.inv.inventory)):
            if self.inv.inventory[i][0] != None:
                item = self.inv.inventory[i]
                if itemsChecked.count(item[0].ID) == 0:
                    itemsChecked.append(item[0].ID)
                    itemAmounts.append(item[1])
                else:
                    s = itemsChecked.index(item[0].ID)
                    itemAmounts[s] += item[1]

        craftable = []

        for i in range(len(self.items.getItems())):
            item = self.items.getItems()[i]()
            if item.recipe != None:
                canCraft = True
                for r in range(len(item.recipe)):
                    if itemsChecked.count(item.recipe[r][0]) > 0:
                        ri = itemsChecked.index(item.recipe[r][0])
                        if itemAmounts[ri] >= item.recipe[r][1]:
                            pass
                        else:
                            canCraft = False
                            break
                    else:
                        canCraft = False
                        break

                if canCraft == True:
                    craftable.append(item.ID)
        return craftable

    def craftItem(self,itemID,times=1):
        for t in range(times):
            craftable = self.getCrafts()
            if craftable.count(itemID) > 0:
                item = self.items.getItemByID(itemID)()
                for i in range(len(item.recipe)):
                    self.inv.removeItemFromInventory(item.recipe[i][0],item.recipe[i][1])
                self.inv.addToInventory(item.ID,item.craftAmount)
