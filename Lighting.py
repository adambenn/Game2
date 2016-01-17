class lighting:
    def __init__(self,world):
        self.world = world

    def getLighting(self,column,row,z):
        if self.world.tiles[column][row][z] != None:
            op = self.world.tiles[column][row][z].lightLevel
        else:
            op = 0
        topLight = 0
        for c in range(column - 1, column + 2):
            for r in range(row-1,row+2):
                for z in range(0,2):
                    try:
                        if z == 0 and self.world.tiles[c][r][1] != None:
                            pass
                        else:
                            if self.world.tiles[c][r][z] != None and self.world.tiles[c][r][z] != self.world.tiles[column][row][z]:
                                if self.world.tiles[c][r][z].lightLevel == 0:
                                    reduce = self.world.tiles[c][r][z].lightBlock
                                    if z == 0:
                                        reduce = reduce // 2
                                    light = self.world.tiles[c][r][z].opacity - reduce
                                else:
                                    light = self.world.tiles[c][r][z].lightLevel
                            elif self.world.tiles[c][r][0] == None and self.world.tiles[c][r][1] == None:
                                light = self.world.baseLightLevel
                            if light > topLight:
                                topLight = light
                                if topLight == 255:
                                    break
                    except:
                        pass
        op += topLight
        if op > 255:
            op = 255
        elif op < 0:
            op = 0
        return op

    def lightSection(self,columnStart,columnStop,rowStart,rowStop):
        for c in range(columnStart, columnStop):
            for r in range(rowStart, rowStop):
                for z in range(0,2):
                    try:
                        if self.world.tiles[c][r][z] != None:
                            self.world.tiles[c][r][z].opacity = 0
                    except:
                        pass
        
        for c in range(columnStart, columnStop):
            for r in range(rowStart, rowStop):
                for z in range(0,2):
                    try:
                        if self.world.tiles[c][r][z] != None:
                            self.world.tiles[c][r][z].opacity = self.getLighting(c,r,z)
                    except:
                        pass
                    
        for c in reversed(range(columnStart,columnStop)):
            for r in reversed(range(rowStart,rowStop)):
                for z in range(0,2):
                    try:
                        if self.world.tiles[c][r][z] != None:
                            self.world.tiles[c][r][z].opacity = self.getLighting(c,r,z)
                    except:
                        pass
