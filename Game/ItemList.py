import copy, Importer
Importer.loadImports('data/items/')
from data.items import *

class itemList:
    def __init__(self,itemPictures):
        self.itemPictures = itemPictures
        self.items = []
        self.finderList = []
        key = None
        for key in globals().keys():
            if key.split('-')[0] == 'Item':
                self.items.append(globals()[key].setter)

    def getItems(self):
        return self.items

    def getItemByID(self,ID):
        if self.finderList == []:
            for i in range(len(self.items)):
                self.finderList.append(self.items[i]())
        for i in range(len(self.finderList)):
            if self.finderList[i].ID == ID:
                return self.items[i]
    
    def getPictures(self):
        return self.itemPictures
