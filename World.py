import Camera, random, math, pygame, Lighting, threading, time, Inventory, Physics, Spawner,CharacterList,Character, Town, TileList

class world:
    def __init__(self, size, cam, tilePics,itemList,tileCracks,weaponPics,armorPics,over, unit=32, lighting = True,special=True):
        self.size = size
        self.unit = unit
        self.rows = self.size[1] // self.unit
        self.columns = self.size[0] // self.unit
        self.cam = cam
        self.tilePics = tilePics
        self.startLighting = False
        self.itemList = itemList
        self.special = special
        self.entities = []
        self.physics = Physics.physics(self)
        self.AIOn = True
        self.tileCracks = tileCracks
        self.weaponPics = weaponPics
        self.spawners = []
        self.charList = CharacterList.characterList(armorPics)
        self.over = over
        self.armorPics = armorPics
        self.towns = []
        self.tileList = TileList.tileList()
        if lighting == True:
            self.lighting = Lighting.lighting(self)
            self.baseLightLevel = 255
        else:
            self.lighting = False
        self.resetTiles()
        self.resetMetadata()
        '''if lighting == True:
            lightThread = threading.Thread(target = self.applyLighting, args=())
            lightThread.daemon = True
            lightThread.start()'''
        
    def resetTiles(self):
        self.tiles = []
        for i in range(self.columns):
            self.tiles.append([])
            for r in range(self.rows):
                self.tiles[i].append([None,None])

        for c in range(self.columns):
            for r in range(self.rows):
                self.addTile(c,r,24)

    def resetMetadata(self):
        self.metaData = []
        for c in range(self.columns):
            self.metaData.append([])
            for r in range(self.rows):
                self.metaData[c].append([])
                

    def __constrictZ(self,z):
        newZ = z
        if newZ > 1:
            newZ = 1
        elif newZ < 0:
            newZ = 0
        return newZ

    def addTile(self,column, row, tileType):
        try:
            if self.lighting!= False:
                opacity = 0
            else:
                opacity = 255
            tile = self.tileList.getTileByType(self,tileType)(self,(column,row))
            tile.opacity=opacity
            self.tiles[column][row][tile.z] = tile
        except:
            return False
        if self.startLighting == True:
            self.lighting.lightSection(column -10,column+10,row-10,row+10)

    def removeTile(self,column, row, z=1):
        z = self.__constrictZ(z)
        try:
            self.tiles[column][row][z] = None
            if z == 0:
                self.addTile(column,row,24)
        except:
            return False
        if self.startLighting == True:
            self.lighting.lightSection(column -10,column+10,row-10,row+10)
        
    def fill(self,tileType, z = 0, opacity=255):
        z = self.__constrictZ(z)
        for c in range(self.columns):
            for r in range(self.rows):
                self.addTile(c,r,tileType)

    def fillColumn(self,column,tileType, z=0,opacity=255,lightLevel=0,lightBlock=50):
        z = self.__constrictZ(z)
        for r in range(len(self.tiles[column])):
            self.addTile(column,r,tileType)

    def fillRow(self,row,tileType, z=0,opacity=255,lightLevel=0,lightBlock=50):
        z = self.__constrictZ(z)
        for c in range(self.columns):
            self.addTile(c,row,tileType)

    def genPatch(self, tileType, colRow, z=1, opacity=255, randsize=(5,20)):
        z = self.__constrictZ(z)
        maxW = random.randint(randsize[0],randsize[1])
        maxH = random.randint(randsize[0],randsize[1])

        prevRow = 5

        for w in range(maxW):
            height = random.randint(maxH//2,maxH)
            rowStart = (maxH - height)//2
            for h in range(height):
                if tileType == None:
                    self.removeTile(colRow[0] + w,colRow[1] + rowStart + h, z)
                else:
                    try:
                        self.addTile(colRow[0] + w,colRow[1] + rowStart + h,tileType)
                    except:
                        pass

    def topFilledRow(self,column, z):
        z= self.__constrictZ(z)
        for r in range(self.rows):
            if self.tiles[column][r][z]!= None:
                if self.tiles[column][r][z].tileType != 24:
                    return r

    def __hill(self, colRow, tileType, surfaceTile, size='rand'):#hybrid void function which places a hill and also returns the width of the hill
        #tileType is the filling tile type while surface tile is the tiletype that will be on the hill's surface
        if size == 'rand':
            maxW = random.randint(5,100)#creates a random sized hill with a width ranging from 5 to 50 blocks
        else:
            maxW = size

        maxH = math.ceil(maxW/2)#max height is the width divided by 2, rounded up

        width = maxW + 2#width decreases by 2 everytime in the following for loop, so it is initialized as max width + 2
        offset = -1#offset is the rows from the starting row
        for r in range(maxH):
            width -= 2#width decreases
            offset += 1#offset increases
            for c in range(width):
                if c == 0 or c == width - 1:#if open to the sky
                    tile = surfaceTile#place a surface tile
                else:
                    tile = tileType
                try:
                    self.addTile(colRow[0] + c + offset,colRow[1] - r, tile)#places the specified tile
                except:
                    pass
        return maxW

    def applyLighting(self):
        while True:
            for c in range(self.columns):
                for r in range(self.rows):
                    for z in range(0,2):
                        if self.tiles[c][r][z] != None:
                            self.tiles[c][r][z].opacity = self.lighting.getLighting(c,r,z)            
                    
    def worldGen(self, biome = None):
        if biome == 'Grassland':
            seaLevel = self.rows//2
            for i in range(seaLevel,self.rows):
                self.fillRow(i,4, z=1)

            for i in range(seaLevel + 4,self.rows):
                self.fillRow(i,10, z=0)

            '''for i in range(self.columns):
                value = (self.rows*perlinNoise(i)) + seaLevel
                value = int(value)

                if value > seaLevel:
                    for t in range(seaLevel,value + 1):
                        self.addTile(i,t,4,z=1)
                else:
                    for t in range(value,seaLevel + 1):
                        self.addTile(i,t,4,z=1)     '''           

            for i in range(seaLevel + self.rows//4,self.rows):
                self.fillRow(i,12,z=1,lightBlock = 75)
                self.fillRow(i,13,z=0, lightBlock = 75)
                
            hillAmt = random.randint(5,10)#gets a random amount of hills
            hillWX = []#gets a list of hills, this is used to try and prevent hills from formin, creating super hills

            for i in range(hillAmt):#loops through the hills
                x = random.randint(0,self.columns)#picks a random x coord

                for i in range(len(hillWX)):#checks previous hills to prevent hill merging
                    if x < hillWX[i][0] + hillWX [i][1] and x > hillWX[i][0]:
                        x -= hillWX[i][1]
                width = self.__hill((x,seaLevel),4,2)
                hillWX.append((x,width))#addds the hill to the list

            treeAmt = random.randint(10,20)

            for i in range(treeAmt):
                col = random.randint(1,self.columns-1)
                row = self.topFilledRow(col,1)
                self.tree(col,row)

            emptyAmount = random.randint(50,100)

            for i in range(emptyAmount):
                col = random.randint(0,self.columns)
                row = random.randint(seaLevel + (seaLevel//3),self.rows)

                self.genPatch(None,(col,row))

            coalAmount = random.randint(50,100)

            for i in range(coalAmount):
                col = random.randint(0,self.columns)
                row = random.randint(seaLevel + (seaLevel//3),self.rows)

                self.genPatch(14,(col,row),randsize=(3,6))

            copperAmount = random.randint(25,75)

            for i in range(coalAmount):
                col = random.randint(0,self.columns)
                row = random.randint(seaLevel + (seaLevel//3),self.rows)

                self.genPatch(25,(col,row),randsize=(2,4))
                
        self.fillRow(self.rows -1, 1,1)
        self.fillColumn(0,3,1)
        self.fillColumn(self.columns-1,3,1)
        col = random.randint(15,self.columns-15)
        row = self.topFilledRow(col,1)-1
        self.placeTown('Testville',(col,row))
        for c in range(self.columns):
            for r in range(self.rows):
                for z in range(2):
                    if self.tiles[c][r][z] != None:
                        self.tiles[c][r][z].special()
        if self.lighting!= False:
            self.startLighting = True
            self.lighting.lightSection(0,self.columns,0,self.rows)
    
    def draw(self):
        colStart = self.cam.centX - (self.cam.fov[0]//2)
        colStart = colStart // self.unit

        rowStart = self.cam.centY - (self.cam.fov[1]//2)
        rowStart = rowStart // self.unit

        colLength = self.cam.fov[0] // self.unit
        rowLength = self.cam.fov[1] // self.unit
        for c in range(colStart, colStart + colLength + 1):
            if c < self.columns and c >= 0 :
                for r in range(rowStart, rowStart + rowLength + 2):
                    if r < self.rows and r >= 0 :
                        for z in range(len(self.tiles[c][r])):
                            if z == 0 and self.tiles[c][r][1] != None:
                                toDraw = False
                            else:
                                toDraw = True
                            if self.tiles[c][r][z] != None:
                                if toDraw == True:
                                    if self.tiles[c][r][z].opacity != 255:
                                        self.cam.drawToCamera(self.tiles[c][r][z].dark,(self.unit,self.unit), (c*self.unit,r*self.unit), 255)
                                    if self.tiles[c][r][z].opacity > 0:
                                        self.cam.drawToCamera(self.tiles[c][r][z].pic, (self.unit,self.unit), (c*self.unit,r*self.unit), self.tiles[c][r][z].opacity)
                                    if self.special == True:
                                        self.tiles[c][r][z].special()

    def saveWorld(self, fileName):
        file = open(fileName, 'w')

        for c in range(self.columns):
            for r in range(self.rows):
                for z in range(0,2):
                    if self.tiles[c][r][z] != None:
                        file.write(str(self.tiles[c][r][z].tileType))
                    else:
                        file.write('0')
            if c != self.columns - 1:
                file.write('\n')
        file.close()

    def loadWorld(self,fileName):
        self.resetTiles()
        try:
            file = open(fileName, 'r')
        except:
            return False
        c = -1
        while True:
            data = str.strip(file.readline())
            c+=1
            if data == '':
                break

            r = 0
            for i in range(0,len(data),2):
                if int(data[i]) != 0:
                    self.addTile(c,r,int(data[i]))
                if int(data[i+1]) != 0:
                    self.addTile(c,r,int(data[i+1]))
                r += 1
        file.close()

    def tree(self, column, row):#creates a tree
        size = random.randint(5,12)#random size from 5 to 12 tiles high

        for i in range(size):#builds trunk
            self.addTile(column,row-i,6)#z is negative so player can walk past the tile

        for v in range(3):
            for h in range(3):
                self.addTile((column-1)+h,(row-i)-v,7)

    def placeDoor(self,column,row,doorType='Wooden'):
        if doorType == 'Wooden':
            self.addTile(column,row,20)
            self.addTile(column,row+1,21)
            self.addTile(column,row+2,22)
        if self.startLighting == True:
            self.lighting.lightSection(column -10,column+10,row-10,row+10)

    def addSpawner(self,charID,location,level=1, limit=1, delay=5):
        self.spawners.append(Spawner.spawner(self,charID,location,level,limit,delay))

    def addCharacter(self,characterID,focus=False):
        temp = Character.character(self,*self.charList.getList()[characterID])
        if focus == True:
            self.over.obj = temp
        self.charList.setStats(temp,characterID)
        self.entities.append(temp)
        return temp
    
    def killCharacter(self,ID):
        toKill = None
        for i in range(len(self.spawners)):
            if self.spawners[i].killChild(ID) == True:
                break
            
        for i in range(len(self.entities)):
            if self.entities[i].ID == ID:
                toKill = i
                break

        if toKill != None:
            del(self.entities[toKill])
            return True
        else:
            return False

    def placeTown(self,name,colRow,parent=None):
        self.towns.append(Town.town(self,name,colRow,parent))

    def changeCam(self,newCam):
        self.cam = newCam

