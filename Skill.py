class skill:
    def __init__(self,name,owner,overlay,maxLevel=99):
        self.exp = 0
        self.baseExp = 80
        self.expToLevel = self.baseExp
        self.level = 1
        self.name = name
        self.maxLevel = maxLevel
        self.over = overlay
        self.messages = []
        self.owner = owner
        for i in range(1,100):
            self.messages.append('You have reached level '+str(i)+' in '+self.name+'!')

    def addExp(self,amount):
        self.exp += amount
        if self.exp >= self.expToLevel:
            self.levelUp()
            self.addExp(self.exp)

    def setLevel(self,lvl):
        self.level = lvl
        self.exp = self.exp - self.expToLevel
        if self.exp < 0:
            self.exp = 0
        self.expToLevel = self.baseExp * 2**(lvl-1)
        if self.over.obj == self.owner:
            self.over.addToQue(self.messages[lvl])

    def levelUp(self):
        if self.level < self.maxLevel:
            self.setLevel(self.level+1)
