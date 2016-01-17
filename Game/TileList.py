import Importer
Importer.loadImports('data/tiles/')
from data.tiles import *

class tileList:
    def __init__(self):
        self.tiles = []
        self.finderList = []
        key = None
        for key in globals().keys():
            if key.split('-')[0] == 'Tile':
                self.tiles.append(globals()[key].setter)

    def getTileByType(self,world,tType):
        if self.finderList == []:
            for i in range(len(self.tiles)):
                self.finderList.append(self.tiles[i](world, (0,0)))
        for i in range(len(self.finderList)):
            if self.finderList[i].tileType == tType:
                return self.tiles[i]
