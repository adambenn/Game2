import AI, random, copy

def shuffle(l):
    lC = copy.deepcopy(l)
    random.shuffle(lC)
    return lC

class characterList:
    def __init__(self,armorPics):
        self.armorPics = armorPics
        villageFaces = [0,18,19]
        villageShirts = [17,1,2]
        self.characters = []
        self.characters.append(('player',armorPics[4],armorPics[shuffle(villageFaces)[0]],armorPics[3],armorPics[shuffle(villageShirts)[0]],'player',None,100,True))
        self.characters.append(('Villager',armorPics[4],armorPics[shuffle(villageFaces)[0]],armorPics[3],armorPics[shuffle(villageShirts)[0]],'Villager',AI.villager,100,False))
        self.characters.append(('Lumberjack',armorPics[4],armorPics[shuffle(villageFaces)[0]],armorPics[3],armorPics[shuffle(villageShirts)[0]],'Villager',AI.lumberJack,100,False))
        self.characters.append(('Builder',armorPics[4],armorPics[shuffle(villageFaces)[0]],armorPics[3],armorPics[shuffle(villageShirts)[0]],'Villager',AI.builder,100,False))
        self.characters.append(('Crafter',armorPics[4],armorPics[shuffle(villageFaces)[0]],armorPics[3],armorPics[shuffle(villageShirts)[0]],'Villager',AI.crafter,100,False))

    def getList(self):
        return self.characters

    def setStats(self,obj, listID):
        if listID == 0:
            obj.setLevel(3)
        elif listID == 1:
            obj.villageRole = 'Villager'
        elif listID == 2:
            obj.inv.addToInventory(5,1)
            obj.inv.addToInventory(6,76)
            obj.villageRole = 'Lumberjack'
        elif listID == 3:
            obj.villageRole = 'Builder'
            obj.mustBuild = None
        elif listID == 4:
            obj.villageRole = 'Crafter'
