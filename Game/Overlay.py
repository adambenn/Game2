import pygame, time,math
pygame.init()

class overlay:#overlay is the heads up display that appears onscreen containing information for the user to read
    def __init__(self,screen,font,itemList,obj=None):#costruct requires a screen, a font, and a character object
        self.obj = obj
        self.enemy = None#enemy is a character object which info will be displayed opon mouse hover
        self.screen = screen
        self.items = itemList
        self.font = font
        self.size = screen.get_size()
        self.healthbarLen = 200#length of the health bar
        self.EXPbarLen = 200#length of the experience bar
        self.EXPbarX = (self.size[0] // 2) - (self.healthbarLen // 2)#x coordinate of the exp bar
        self.healthbarX = (self.size[0] // 2) - (self.healthbarLen // 2)#x coordinate of the players health bar
        self.currentHealthLen = 0#length of the player's current health
        self.hovernameColor = (250, 250, 250)#color of the hovered enemie's name
        self.message = None#the message being displayed on screen
        self.slotSize = (32,32)
        self.slotAmount = 0
        self.fullInv = False
        self.invToggleTime = time.time()
        self.invToggleWait = 1
        self.messageQue = []
        self.slots = []
        self.otherSlots = []
        self.maxCrafts = (self.size[0]//2)//self.slotSize[0]
        self.craftSlots = []
        self.craftHighlight = None

    def getHealthbarLen(self,obj):#returns the length of the health bar
        units = self.healthbarLen /obj.maxHealth
        barLen = obj.health * units
        return barLen

    def updateHealthbar(self):#updates the healthbar with the object's health
        self.currentHealthLen = self.getHealthbarLen(self.obj)

    def drawHealthbar(self):#draws the health bar on the screen
        redBar = (self.healthbarX,self.size[1]-30,self.healthbarLen + 4,20)#redbar is a rect object
        greenBar = (self.healthbarX + 2, self.size[1] - 28, self.currentHealthLen, 16)#green bar is a rect object showing a players health
        pygame.draw.rect(self.screen, (200,0,0), redBar)#draws both
        pygame.draw.rect(self.screen, (0,200,0), greenBar)

    def hoverEnemy(self,obj):#assigns enemy to an object
        self.enemy = obj

    def unhover(self):#unassigns enemy
        self.enemy = None

    def drawEnemyHover(self):#draw information about the enemy
        if self.enemy != None:
            greenLen = self.getHealthbarLen(self.enemy)
            name = self.font.render(str.capitalize(self.enemy.name)+' Level: '+str(self.enemy.level), 1, self.hovernameColor)#creates a rendered font of the character's health and level

            nameLoc = name.get_rect()
            nameLoc.centerx = self.size[0]//2#sets the center x and y coordinates of the enemy healthbar
            nameLoc.centery = name.get_size()[1]//2
            name= name.convert_alpha()

            redBar = (self.healthbarX,name.get_size()[1] + 10,self.healthbarLen + 4,20)
            greenBar = (self.healthbarX + 2, name.get_size()[1] + 12, greenLen, 16)

            self.screen.blit(name,nameLoc)#draws the name and the health bars
            pygame.draw.rect(self.screen, (200,0,0), redBar)
            pygame.draw.rect(self.screen, (0,200,0), greenBar)

    def drawLevel(self):#draws the characters level
        level = 'Level: '+str(self.obj.level)
        toDraw = self.font.render(level, 1, (255,255,255))#renders the font

        pos = toDraw.get_rect()
        pos.centerx = self.EXPbarX + (toDraw.get_size()[0]//2)#puts the level in the appropriate position
        pos.centery = (self.size[1] -47) - (toDraw.get_size()[1]//2)
        toDraw = toDraw.convert_alpha()#converts

        self.screen.blit(toDraw, pos)

    def getEXPLen(self):#finds the length of the exp bar
        units = self.EXPbarLen / self.obj.expToLevel
        barLen = self.obj.exp * units
        return barLen

    def drawExpBar(self):#draws the exp bar
        blackBar = (self.EXPbarX,self.size[1]-45,self.EXPbarLen + 4,10)
        yellowBar = (self.EXPbarX + 2, self.size[1] - 43, self.getEXPLen(), 6)#yellow bar is the amount of exp
        pygame.draw.rect(self.screen, (0,0,0), blackBar)
        pygame.draw.rect(self.screen, (250,250,0), yellowBar)        

    def setMessage(self,msg,dur=3,col=(255,255,255)):#sets a message to be drawn on the screen, msg is the message, dur is the duration, and col is the color
        toDraw = self.font.render(msg, 1, col)#renders

        pos = toDraw.get_rect()
        pos.centerx = (self.size[0]//2)#puts in middle of screen
        pos.centery = (self.size[1]//2) - (toDraw.get_size()[1]//2)

        self.message = {'Draw':toDraw, 'Pos':pos, 'Dur':dur, 'Start':time.time()}#sets message attribute

    def addToQue(self,message,dur=3,col=(255,255,255)):
        self.messageQue.append((message,dur,col))

    def drawMoney(self):#draws the character's money
        toDraw = self.font.render('$'+str(self.obj.money),1, (250,250,0))

        pos = toDraw.get_rect()
        pos.bottomleft = (5,self.screen.get_height() - 5)#sets bottom left corner of the font to just above the bottom left corner of the screen
        toDraw.convert_alpha()

        self.screen.blit(toDraw,pos)

    def drawItem(self,itemTup,xy):
        if itemTup[0] != None:
            font = pygame.font.Font(None,18)
            pic = self.items.getPictures()[itemTup[0].ID]
            self.screen.blit(pic,xy)
            if itemTup[1] > 1:            
                toDraw = font.render(str(itemTup[1]),1,(255,255,255))
                self.screen.blit(toDraw,(xy[0]+toDraw.get_width()+2,xy[1] + toDraw.get_height()))
            

    def drawSlot(self,slotNum,xy,font,obj):
        i = slotNum
        slot = pygame.Surface(self.slotSize)
        slot.fill((0,125,200))
        border = (0,0,self.slotSize[0],self.slotSize[1])
        if obj.selectedSlot != i:
            pygame.draw.rect(slot,(0,0,0),border,1)
        else:
            pygame.draw.rect(slot,(255,255,255),border,2)                
        if obj.inv.inventory[i][0] != None:
            pic = self.items.getPictures()[obj.inv.inventory[i][0].ID]
            slot.blit(pic,((self.slotSize[0]//2)-(pic.get_width()//2),(self.slotSize[1]//2)-(pic.get_height()//2)))
            if obj.inv.inventory[i][1] > 1:
                toDraw = font.render(str(obj.inv.inventory[i][1]),1,(255,255,255))
                slot.blit(toDraw,(self.slotSize[0]-toDraw.get_width() - 2,self.slotSize[1]-toDraw.get_height()))
            
        self.screen.blit(slot,xy)#(slot,(self.screen.get_width()-self.slotSize[0],halfScreen+(i*self.slotSize[1])))        

    def drawQuickinventory(self):
        halfScreen = self.screen.get_height() // 2
        slotAmount = halfScreen
        slotAmount = slotAmount//self.slotSize[1]
        self.slotAmount = slotAmount - 1
        if self.slotAmount > 9:
            self.slotAmount = 9
        font = pygame.font.Font(None,18)

        for i in range(slotAmount):
            self.drawSlot(i,(self.screen.get_width()-self.slotSize[0],halfScreen+(i*self.slotSize[1])),font,self.obj)

    def drawFullInventory(self,obj, xStart = None):
        slot = -1
        yStart = self.slotSize[1]
        width = math.ceil(obj.inv.inventorySize/self.slotAmount)*self.slotSize[0]
        if xStart == None:
            xStart = self.screen.get_width()-width-self.slotSize[0]
        font = pygame.font.Font(None,18)
        itemName = obj.selectedSlot
        try:
            if obj.inv.inventory[itemName][0] != None:
                itemName = obj.inv.inventory[itemName][0].name
                self.screen.blit(font.render(itemName,1,(255,255,255)),(xStart,yStart//3))
        except:
            pass
            
        addSlot = False
        addOtherSlot = False
        if self.slots == []:
            addSlot = True

        if self.otherSlots == []:
            addOtherSlot = True
            
        for c in range(math.ceil(obj.inv.inventorySize/self.slotAmount)):
            for r in range(self.slotAmount+1):
                slot += 1
                if slot <= obj.inv.inventorySize:
                    self.drawSlot(slot,(((c*self.slotSize[0]))+xStart,(r*self.slotSize[1])+yStart),font,obj)
                    if addSlot == True and obj == self.obj:
                        self.slots.append(((c*self.slotSize[0])+xStart,(r*self.slotSize[1])+yStart))
                    elif addOtherSlot == True and obj != self.obj:
                        self.otherSlots.append(((c*self.slotSize[0])+xStart,(r*self.slotSize[1])+yStart))
        

    def toggleInv(self):
        if time.time() - self.invToggleTime > self.invToggleWait:
            self.invToggleTime = time.time()
            if self.fullInv == True:
                self.fullInv = False
                self.obj.openInv = False
                self.otherSlots = []
                if self.obj.selectedSlot > self.slotAmount:
                    self.obj.selectedSlot = 0
            else:
                self.fullInv = True

    def drawCraftSlot(self,craftNum,xy,highLight=False):
        slot=pygame.Surface(self.slotSize)
        slot.fill((0,125,200))
        border = (0,0,self.slotSize[0],self.slotSize[1])
        pic = self.items.getPictures()[self.obj.craftable[craftNum]]
        slot.blit(pic,((self.slotSize[0]//2)-(pic.get_width()//2),(self.slotSize[1]//2)-(pic.get_height()//2)))
        if highLight == True:
            pygame.draw.rect(slot,(255,255,255),border,2)
        else:
            pygame.draw.rect(slot,(0,0,0),border,1)
        self.screen.blit(slot,xy)

    def drawCrafts(self):
        xStart = self.size[0]//2
        yStart = self.slotAmount * self.slotSize[1]
        yStart += self.slotSize[1]*3
        draws=0
        self.craftSlots = []
        for i in range(len(self.obj.craftable)):
            item = self.obj.craftable[i]
            if i < self.maxCrafts:
                if self.craftHighlight == i:
                    self.drawCraftSlot(i,(xStart+(draws*self.slotSize[0]),yStart),True)
                else:
                    self.drawCraftSlot(i,(xStart+(draws*self.slotSize[0]),yStart))
                self.craftSlots.append((xStart+(draws*self.slotSize[0]),yStart))
                draws += 1

        if self.craftHighlight != None:
            try:
                name = self.items.getItemByID(self.obj.craftable[self.craftHighlight]).name
                font = pygame.font.Font(None,18)
                name = font.render(name,1,(255,255,255))
                self.screen.blit(name,(xStart,yStart-(self.slotSize[1]//2)))
            except:
                pass

    def draw(self):#draws everything
        self.drawHealthbar()
        self.drawEnemyHover()
        self.drawLevel()
        self.drawExpBar()
        self.drawMoney()
        if self.fullInv == False:
            self.drawQuickinventory()
        else:
            self.drawFullInventory(self.obj)
            if self.obj.openInv == False:
                self.drawCrafts()

        if self.obj.openInv != False:
            self.drawFullInventory(self.obj.openInv,self.slotSize[0])
            self.fullInv = True

        if self.message == None:
            if len(self.messageQue) > 0:
                if self.messageQue[0] != None:
                    self.setMessage(*self.messageQue[0])
        
        if self.message != None:#if there is a message
            if time.time() - self.message['Start'] < self.message['Dur']:#and duration is greater than 0
                self.screen.blit(self.message['Draw'],self.message['Pos'])#draws the message
            else:
                self.message = None
                if len(self.messageQue) > 0:
                    if self.messageQue[0] != None:
                        del(self.messageQue[0])
    def changeScreen(self,screen,size):
        self.screen = screen
        self.size = size
        self.EXPbarX = (self.size[0] // 2) - (self.healthbarLen // 2)#x coordinate of the exp bar
        self.healthbarX = (self.size[0] // 2) - (self.healthbarLen // 2)#x coordinate of the players health bar


