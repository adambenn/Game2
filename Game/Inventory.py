import copy

class objectInventory:
    def __init__(self,items,inventorySize=40):
        self.itemList = items
        self.inventorySize = inventorySize
        self.resetInventory()
        
    def resetInventory(self):
        self.inventory = []
        for i in range(0,self.inventorySize+1):
            self.inventory.append((None,None))

    def addToInventory(self,itemID,amount=1):
        for a in range(amount):
            placed = False
            for i in range(len(self.inventory)):
                if self.inventory[i][0] != None:
                    if self.inventory[i][0].ID == itemID:
                        if self.inventory[i][1] < self.itemList.getItemByID(itemID)().maxStack:
                            self.inventory[i] = (self.itemList.getItemByID(itemID)(),self.inventory[i][1]+1)
                            placed = True
                            break
                        
            if placed == False:        
                for i in range(len(self.inventory)):
                    if self.inventory[i][0] == None:
                        self.inventory[i] = (self.itemList.getItemByID(itemID)(),1)
                        placed = True
                        break
                    
            if placed == False:
                return False
        return True


    def removeFromInventory(self,slotNum,amount=1):
        for i in range(amount):
            if self.inventory[slotNum][0] != None:
                if self.inventory[slotNum][1] > 0:
                    self.inventory[slotNum] = (self.inventory[slotNum][0],self.inventory[slotNum][1]-1)
                if self.inventory[slotNum][1] <= 0:
                    self.inventory[slotNum] = (None,None)

    def removeItemFromInventory(self,itemID,amount=1):
        self.removeFromInventory(self.findItem(itemID))
                    

    def findItem(self,itemID):
        for i in range(len(self.inventory)):
            if self.inventory[i][0] != None:
                if self.inventory[i][0].ID == itemID:
                    return i
        return False

    def findItemType(self,itemType):
        for i in range(len(self.inventory)):
            if self.inventory[i][0] != None:
                if self.inventory[i][0].itemType == itemType:
                    return i
        return False
    
    def findItemAmount(self,itemID):
        amount = 0
        for i in range(len(self.inventory)):
            if self.inventory[i][0] != None:
                if self.inventory[i][0].ID == itemID:
                    amount += self.inventory[i][1]
        return amount

    def findEmpty(self):
        for i in range(len(self.inventory)):
            if self.inventory[i][0] == None:
                return i
        return None

    def transferToInv(self,slotNum,inv):
        if self.inventory[slotNum][0] != None:
            inv.addToInventory(self.inventory[slotNum][0].ID,self.inventory[slotNum][1])
            self.removeFromInventory(slotNum,self.inventory[slotNum][1])

    def transferItemsToInv(self,inv,item,amount=1):
        for a in range(amount):
            self.transferToInv(self.findItem(item),inv)
