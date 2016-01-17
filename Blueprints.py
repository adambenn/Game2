import Importer
Importer.loadImports('data/blueprints/')
from data.blueprints import *

class blueprint:
    def __init__(self,ID,width,height,tiles):
        self.ID = ID
        self.tiles = tiles
        self.width = width
        self.height = height

    def getRel(self,colRow):
        toRet = []

        for t in range(len(self.tiles)):
            toRet.append((colRow[1]-self.tiles[t][0],self.tiles[t][1] + colRow[0],self.tiles[t][2],self.tiles[t][3]))

        return toRet

    def getRequiredResources(self):
        req = []

        for t in range(len(self.tiles)):
            found = False
            for i in range(len(req)):
                if req[i][0] == self.tiles[t][3]:
                    found = True
                    
            if found == True:
                for l in range(len(req)):
                    if req[l][0] == self.tiles[t][3]:
                        req[l] = (req[l][0],req[l][1]+1)
            else:
                req.append((self.tiles[t][3],1))

        return req

class blueprintList:
    def __init__(self):
        self.blueprints = []
        key = None
        for key in globals().keys():
            if key.split('-')[0] == 'Blueprint':
                self.blueprints.append(blueprint(globals()[key].ID,globals()[key].w,globals()[key].h,globals()[key].blueprint))

    def getList(self):
        return self.blueprints

    def getBlueprint(self,ID):
        for i in range(len(self.blueprints)):
            if self.blueprints[i].ID == ID:
                return self.blueprints[i]
        return None

if __name__ == '__main__':
    x = blueprintList()
