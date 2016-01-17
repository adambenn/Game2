import pygame,time
pygame.init()

class dialog:#the dialog class creates text boxes
    maxL = 50#max length of a text box
    font = pygame.font.Font(None, 24)#font

    def __init__(self,cam,xy,words,duration=5,boxCol=(0,0,255),textCol=(255,255,255)):#constructor
        self.xy = xy
        self.words= words
        self.boxCol = boxCol#box color
        self.textCol = textCol#text color
        self.words = self.parseWords()#parses the words to fit
        self.size = self.getBoxSize()#get size
        self.dur = duration#duration
        self.startTime = int(time.clock())
        self.endTime = self.startTime + duration
        self.cam = cam
    
    def parseWords(self):
        
        if len(self.words) > dialog.maxL:#only do the following if the length of the words axceeds the maximun length
            splitTimes = math.ceil(len(self.words) / dialog.maxL)#how many times words must be split to fit in the box

            newWords = []#empty list
            point = 0#the point where a word has split
            
            for i in range(splitTimes):
                if point + dialog.maxL < len(self.words):
                    if self.words[point+dialog.maxL] == ' ':#only splits on spaces
                        newWords.append(self.words[point:point+dialog.maxL])#adds the sentance
                        point += dialog.maxL#adds the split point
                    else:
                        spot = dialog.maxL#spot is the amount of characters at which the sentance was split
                        for q in reversed(range(len(self.words[point:point+dialog.maxL]))):#works backwards in the sentance
                            if self.words[q] == ' ':#if it finds a space
                                spot = q#save the character point
                                break
                        newWords.append(self.words[point:point + spot])#adds the point
                        point += spot
                                           
                else:
                    newWords.append(self.words[point:len(self.words)])#just puts the words if it doesnt exceed the length

            words = newWords
        else:
            words = []
            words.append(self.words)

        return words

    def getBoxSize(self):#returns size of the box
        sizes = []
        
        for i in range(len(self.words)):
            sizes.append(dialog.font.size(self.words[i]))#adds the sizes

        size = max(sizes)#finds the biggest word
        self.wordSize = size[1]#gets the word height

        height = size[1] * len(self.words)#finds the box height

        return (size[0],height)

    def draw(self):#draws a dialog box
        box = pygame.Surface((self.size[0],self.size[1]))#creates a surface
        box = box.convert()
        box.fill(self.boxCol)#fill it with the color
        self.cam.drawToCamera(box,self.size,self.xy)#draws to the camera
        words = []

        for i in range(len(self.words)):
            line = self.xy[1] + (self.wordSize//2) + ((self.size[1]//len(self.words))* i)#finds the line
            word = dialog.font.render(self.words[i], 1, self.textCol)#gets the rendered word
            pos = word.get_rect()#gets the rectangle
            pos.centerx = self.xy[0] + (self.size[0] // 2)#finds the center x
            pos.centery = line
            self.cam.drawToCamera(word,self.size,pos)#draws

    def displayDialog(self):#displays teh dialog for the set amount of time
        if time.clock() < self.endTime:#if hasnt exceeded time
            self.draw()

    def move(self, newCoord):#moves a text box
        self.xy = newCoord
