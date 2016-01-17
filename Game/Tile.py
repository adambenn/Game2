import pygame

class tile:
    def __init__(self,parentWorld,colRow, tileType, z = 0,opacity = 255, lightBlock=25, lightLevel = 0, physical = True):
        self.tileType = tileType
        self.origPic = parentWorld.tilePics[tileType]
        self.pic = parentWorld.tilePics[tileType]
        dark = pygame.Surface((parentWorld.unit,parentWorld.unit))
        dark.fill((0,0,0))
        dark = dark.convert()
        self.dark = dark
        self.z = z
        self.opacity = opacity
        self.column = colRow[0]
        self.row = colRow[1]
        self.parentWorld = parentWorld
        self.lightBlock = lightBlock
        self.lightLevel = lightLevel
        self.physical = physical
        self.drop = None
        self.dropAmount = 1
        self.inv = None
        self.selectedSlot = None
        self.drawBack = False
        self.canBreak = True
        self.tool = 'pick'
            
    def changeTile(self,tileType):
        self.parentWorld.addTile(self.column,self.row,tileType)
        self.updatePic()

    def gravity(self):
        if self.parentWorld.tiles[self.column][self.row + 1][self.z] == None:
            self.parentWorld.addTile(self.column,self.row+1,self.tileType,self.z)
            self.parentWorld.removeTile(self.column,self.row,self.z)

    def special(self):
        pass
    
    def updatePic(self):
        if self.physical == False or self.drawBack == True:
            if self.parentWorld.tiles[self.column][self.row][0] != None and self.z == 1:
                if self.parentWorld.tiles[self.column][self.row][0].tileType != 24:
                    self.pic = pygame.Surface((self.parentWorld.unit,self.parentWorld.unit))
                    self.pic.blit(self.parentWorld.tiles[self.column][self.row][0].pic,(0,0))
                    self.pic.blit(self.origPic,(0,0))        

    def relight(self):
        self.parentWorld.lighting.lightSection(self.column -10,self.column+10,self.row-10,self.row+10)
        
    def onClick(self,obj):
        pass
