import time

class spawner:#spawners spawn characters
    def __init__(self,world,charID,location,level=1, limit=1, delay=5):#construct requires the list of body parts,name,team,location and other options
        #like AI level and max limit to spawn
        self.location = location
        self.level = level
        self.limit = limit
        self.charID = charID
        self.chardata = world.charList.getList()[charID]
        self.children = []
        self.spawnTime = time.time()
        self.delay = delay
        self.world = world
        self.over = world.over

    def spawn(self):#spawn creates a character
        child = self.world.addCharacter(self.charID)
        child.changeXY(self.location[0],self.location[1])
        child.setLevel(self.level)
        self.children.append(child.ID)#it also appends the character to its list of shildren

    def main(self):#main is the main function for a spawner
        if len(self.children) < self.limit:#if it has less than the limit of children
            if time.time() - self.spawnTime >= self.delay:
                self.spawn()#make another
                self.spawnTime = time.time()

    def killChild(self,ID):
        toKill = None
        for i in range(len(self.children)):
            if self.children[i] == ID:
                toKill = i
                break
        if toKill != None:
            del(self.children[toKill])
            return True
        else:
            return False
