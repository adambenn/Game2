'''
By Adam Benn
Contact at: adambenn22@gmail.com
Game Title: TBA for now its "Game 2"

Dear Future Adam,

    If you ever successfully document this program, please go to the hospital, because in the event that documentation
is complete I suspect your hands will be shattered and your ears bleeding.'''

import sys,random, time, math, os, os.path
import pygame
import ParticleEngine#the particle engine
from pygame.locals import *
import AI, operator, Spells, Camera, Overlay, World, Item,copy,Inventory, Mining, Woodcutting,CharacterList, Character, BodyPart, Physics,ItemList
import ctypes
activeLighting = True

# size of the screen
pygame.init()# initialize pygame
screen = pygame.display.set_mode((640,480))#create the screen
#screen = pygame.display.set_mode((1920,1080),FULLSCREEN|HWSURFACE|DOUBLEBUF)

screenSize = screen.get_size()

spawners = []#global list containing the spawners
def simpleDist(xy1,xy2):#returns the distance between two points
    dist = abs(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2))
    return dist

def touchingEntity(x,y,length):#returns any worldBack.entities within length distance of a point
    touching = []#a list, since more than one entity may be touching the point

    for i in range(len(worldBack.entities)):
        dist = simpleDist((worldBack.entities[i].x,worldBack.entities[i].y),(x,y))#gets the distance
        if dist <= length:#if the distance is less than the length
            touching.append(i)#add it to the list
    return touching

#below I attempted a binary search algorithm to do the same thing, it failed

def getCoordOnObject(deg,r):#returns where a object must be placed to be on the end of an object rotated deg degress with r length
    theta = math.radians(deg)################################MUST CONVERT TO RADIANS WHEN ROTATING IN PYTHON################################
    y = math.cos(theta) * r
    x = math.sin(theta) * r

    return (x,y)
def quitGame ():#exits the game
    pygame.quit()
    sys.exit()

def blit_alpha(target, source, location, opacity):#blits with an alpha value (opacity), target being the surface source the surface to be blitted
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()# creates a temporary surface
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)#sets the opacity
    target.blit(temp, location)

def loadPic(imgName):#loads a picture with name imgName
    try:
        img = pygame.image.load(imgName)
        img = img.convert_alpha()#convert makes it draw faster
        return img
    except:
        print('Image Load Error:',imgName)
        return False    
                
class projectile:#this class is for any projectiles shot in the game world
    gravity = 2#gravity modifier
    #http://www.sauropodstudio.com/dev-diary-number-eight/
    def __init__(self,pic, xy, vel, damage, owner = None, goal= None, impactRad = 10, duration = 100, opacity = 255, grav=False, collisionCheck = True):#constructor, contains plenty of options
        self.pic = pic
        self.orig = pic
        self.size = self.pic.get_size()
        self.x = xy[0]
        self.y = xy[1]
        self.xVel = vel[0]
        self.yVel = vel[1]
        self.speed = vel[0]
        self.owner = owner#owner being the character that shot the projectile
        self.damage = damage
        self.goal = goal#the goal of the projectile
        self.impactRad = impactRad#impact radius
        self.duration = duration#duration
        self.opacity = opacity
        top = 0

        for i in range(len(projectiles)):
            if projectiles[i].ID >= top:#if the ID is greater than or equal to the highest ID
                top = worldBack.entities[i].ID + 1#make top higher than it
        self.ID = top

        self.faceRight = False
        self.grav = grav#gravity boolean
        self.collisionCheck = collisionCheck#if collisions with tiles are allowed
        projectiles.append(self)

        if self.goal != None and self.grav == True:
            try:#this is failed projectile physics, ignore
                x = abs((self.x + self.size[0]) - goal[0])
                y = abs(self.y - goal[1])
                g = projectile.gravity
                #angle = math.atan(self.speed**2 + math.sqrt(abs((self.speed**4-g*(g*x**2+2*y*self.speed**2))/g*x)))
                power = math.sqrt(0.5*projectile.gravity*x**2*(math.tan(math.radians(45))**2+1) / x*math.tan(math.radians(45)) + y)
                self.xVel = power* math.cos(math.radians(45))
                if self.goal[0] < self.x:
                    self.xVel = -self.xVel
                self.yVel = power* math.sin(math.radians(45))
            except:
                pass

    def killSelf(self):#destroys current projectile
        for i in range(len(projectiles)):
            if projectiles[i].ID == self.ID:
                projectiles.remove(projectiles[i])
                break

    def applyPhysics(self):#apply physics to itself
        if self.grav == True:
            self.yVel -= projectile.gravity
        
        self.x += self.xVel
        self.y -= self.yVel

        if self.collisionCheck == True:
            if physics.touchingTile((self.x,self.y)):#die if touching a tile
                self.killSelf()

    def draw(self):#draw to the camera
        mainCamera.drawToCamera(self.pic,self.size,(self.x, self.y),self.opacity)

    def reflectY(self):#flip
        if self.faceRight == False:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.faceRight = True
        else:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.faceRight = False            

    def main(self):#main function
        self.applyPhysics()

        if self.xVel > 0 and self.faceRight == False:
            self.reflectY()

        if self.xVel < 0 and self.faceRight == True:
            self.reflectY()

        touch = touchingEntity(self.x, self.y,self.impactRad)
            
        if len(touch) != 0:#below is smae as character impact
            for i in range(len(touch)):
                if worldBack.entities[touch[i]].ID != self.owner.ID and worldBack.entities[touch[i]].team != self.owner.team and worldBack.entities[touch[i]].invincible == False:
                    if self.faceRight == False:
                        distance = -15
                    else:
                        distance = 15
                    worldBack.entities[touch[i]].takeDamage(self.damage,distance=distance)
                    if worldBack.entities[touch[i]].health <=0 and self.owner != None:
                        self.owner.rewardFromKill(worldBack.entities[touch[i]])
                    self.killSelf()#excpet for this line of course

        self.duration -= 1

        if self.duration <= 0:
            self.killSelf()

        self.draw()
            
def makeText(font,text,col=(255,255,255)):#returns a rendered font
    toDraw = font.render(text, 1, col)
    return toDraw

class button:#creates a button for use in menus
    def __init__(self,screen,font,text, xy, col, func, hoverCol = (250,250,0)):#construct requires a surface, font, text, color, string saying what to do when clicked
        #and the option of what color the text is when hovered default yellow
        self.screen= screen
        self.font = font
        self.text = text
        self.col = col
        self.hoverCol = hoverCol
        self.default = makeText(self.font,text, col)#rendered font without hovered
        self.hovered = makeText(self.font,text, hoverCol)#rendered font when hovered
        self.size = self.default.get_size()#size
        self.xy = (xy[0] - (self.size[0]//2),xy[1] - (self.size[1]//2))
        self.hover = False#boolean for being hovered or not
        self.func = func#click function is a string

    def changeText(self,newText):
        self.text = newText
        self.default = makeText(self.font,newText, self.col)#rendered font without hovered
        self.hovered = makeText(self.font,newText, self.hoverCol)#rendered font when hovered        

    def draw(self):#draw a button
        if self.hover == False:#if not hovered
            self.screen.blit(self.default, self.xy)#draw normal
        else:
            self.screen.blit(self.hovered, self.xy)#draw hovered

class mainMenu:#just a menu
    def __init__(self,screen):#construct requires a surface
        self.screen = screen
        self.toDraw = []#what needs to be drawn
        self.buttons = []#any buttons

    def newTitle(self, font, text, xy, col = (255,255,255)):#creates a title and places it at xy
        toDraw = makeText(font,text,col)

        size = toDraw.get_size()
        newXY= (xy[0] - (size[0]//2),xy[1] - (size[1]//2))#places on its center
        toDraw = {'Draw':toDraw, 'XY':newXY}#dictionary of what to draw and where is appended to the list
        self.toDraw.append(toDraw)

    def newButton(self, font, text, xy, col = (255,255,255), func = None, hoverCol = (250,250,0)):#creates a button
        self.buttons.append(button(self.screen,font,text,xy,col,func))#adds the new button to the button list

    def draw(self):#draws the menu
        for i in range(len(self.toDraw)):
            self.screen.blit(self.toDraw[i]['Draw'],self.toDraw[i]['XY'])#draws eveything need drawing excluding buttons

        for i in range(len(self.buttons)):#draws buttons
            self.buttons[i].draw()

    def buttonHovers(self, mxy, click):#checks for button hovers and ajusts them accordingly, mxy is mouse coord and click is a boolean for clicking
        for i in range(len(self.buttons)):
            if physics.colliding(mxy,(1,1),self.buttons[i].xy,self.buttons[i].size) == True:#checks if the mouse is colliding
                self.buttons[i].hover = True
                if click == True:
                    exec(self.buttons[i].func)#if they clicked run the function stored in the button
            else:
                self.buttons[i].hover = False
                
def loadPictures(path):#loads every picture in a directory
    files = os.listdir(path)#gets the direcotry
    images = []#init empty image list

    for i in range(len(files)):
        imagePath = path + files[i]#gets the path of each file
        pic = loadPic(imagePath)

        if pic != False:
            images.append(pic)#loads the picture and adds it to a list


    return images
itemList = ItemList.itemList(loadPictures('data/images/Items/'))
weaponPics = loadPictures('data/images/Weapons/')#empty list of weapons
armorPics = loadPictures('data/Images/Armor/')

play = False#play is a boolean for whether the play has ppressed play

pygame.display.set_caption('Game2')#adds caption
pygame.mouse.set_visible(1)#makes mouse visible

#pygame.key.set_repeat(1,10)#allows keys to be held down
font = pygame.font.Font(pygame.font.match_font('bitstreamverasans'), 24)#creates a default font
buttonFont = pygame.font.Font(pygame.font.match_font('bitstreamverasans'), 36)#creates a button font
clock = pygame.time.Clock()#creates a game clock
background = pygame.Surface(screen.get_size())#creates a background
background = background.convert()

tileCracks = []
tileCracks.append(loadPic('data/images/Effects/Crack1.gif'))
tileCracks.append(loadPic('data/images/Effects/Crack2.gif'))
tileCracks.append(loadPic('data/images/Effects/Crack3.gif'))

mainCamera = Camera.camera(screen,screenSize[0]//2,screenSize[1]//2,screenSize)#creates a camera for viewing the menu
background.fill((150, 150, 150))#gray background
menBack = World.world(screenSize,mainCamera,loadPictures('data/images/tiles/'),itemList,tileCracks,weaponPics,armorPics,None,32,False,special=False)#creates a mini world for the menu
backFill = random.randint(0,len(menBack.tilePics)-1)#chooses a random num from 0,1

menBack.fill(backFill)#fill with the block
physics =Physics.physics(menBack)

def toggle(mainVar):
    var = mainVar
    if var == True:
        var = False
    elif var == False:
        var = True
    return var
    
men = mainMenu(screen)#creates a menu
titleFont = pygame.font.Font(pygame.font.match_font('impact'), 55)#creates a tile font
titleFont.set_underline(True)#underlines the title
title = men.newTitle(titleFont,'Game 2',(screenSize[0]//2,(screenSize[1]//2) - 100))#creates a title
b = men.newButton(buttonFont,'Play',(screenSize[0]//2,(screenSize[1]//2) + 100), func='global play; play = True;')#creates a button that makes play true
b2 = men.newButton(buttonFont,'Controls',(screenSize[0]//2,(screenSize[1]//2) + 100 + buttonFont.get_height() + 10), func='global controls; controls = True;')
b3 = men.newButton(buttonFont,'Options',(screenSize[0]//2,(screenSize[1]//2) + 100 + buttonFont.get_height() + 10 + buttonFont.get_height()), func='global options; options = True;')


controlMen = mainMenu(screen)#menu for the controls
titleFont = pygame.font.Font(pygame.font.match_font('georgia'), 24)#creates a tile font
title = controlMen.newTitle(titleFont,'Controls',(screenSize[0]//2,(screenSize[1]//2) - 100))#creates the title
sizeDown = titleFont.get_height()#size down is how much to move down for the next sentence
l1 = controlMen.newTitle(titleFont,'Use A and D to move left and right, respectively.',(screenSize[0]//2,(screenSize[1]//2) -  sizeDown - 20))#creates more instructions
sizeDown = sizeDown - titleFont.get_height()
l2 = controlMen.newTitle(titleFont,'Left click to attack, right click to place a tile.',(screenSize[0]//2,(screenSize[1]//2) - sizeDown - 20))
sizeDown = sizeDown - titleFont.get_height()
l3 = controlMen.newTitle(titleFont,'Use Spacebar to jump.',(screenSize[0]//2,(screenSize[1]//2) - sizeDown - 20))
sizeDown = sizeDown - titleFont.get_height()
b3 = controlMen.newButton(buttonFont,'Back',(screenSize[0]//2,(screenSize[1]//2) + 50), func='global controls;controls = False;')#button that goes back to the menu

lightText = 'global activeLighting;activeLighting = toggle(activeLighting);optionMen.buttons[len(optionMen.buttons)-2].changeText("Lighting: "+str(activeLighting));'
optionMen = mainMenu(screen)
title= optionMen.newTitle(titleFont,'Options',(screenSize[0]//2,(screenSize[1]//2) - 100))
sizeDown = titleFont.get_height()
b1 = optionMen.newButton(buttonFont,'Lighting: '+str(activeLighting),(screenSize[0]//2,(screenSize[1]//2)), func=lightText)
sizeDown = sizeDown + buttonFont.get_height()
b2 = optionMen.newButton(buttonFont,'Back',(screenSize[0]//2,(screenSize[1]//2)+ sizeDown), func='global options;options = False;')

clicked = False#clicked is false
controls = False#not on controls screen
options = False
while play == False:
    mx = pygame.mouse.get_pos()#find mouse
    my = mx[1]
    mx = mx[0]

    for event in pygame.event.get():#finds events
        if event.type == pygame.QUIT:#if pressed red x
            quitGame()#exit
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:#if pressed escape
                quitGame()#quit
        elif event.type == MOUSEBUTTONDOWN:#if clicked
            if event.button == 1:
                clicked = True#ajust clik accordingly
        elif event.type == MOUSEBUTTONUP:#if released click
            if event.button == 1:
                clicked = False#not clicking
    
    screen.blit(background,(0,0))#draws background
    menBack.draw()#draws tiles
    if controls == False and options == False:#not on controls
        men.buttonHovers((mx,my),clicked)#checks for hovers
        men.draw()#draws menu
    elif controls == True:
        controlMen.buttonHovers((mx,my),clicked)#checks for hovers
        controlMen.draw()#draws controls
    elif options == True:
        optionMen.buttonHovers((mx,my),clicked)#checks for hovers
        optionMen.draw()#draws controls        
    pygame.display.flip()#refresh
    clock.tick(60)#set framerate

if play == True:
    background.fill((173, 216, 230))#sets background to sky color
    mainCamera = Camera.camera(screen,0,0,screenSize)#creates camera
    over = Overlay.overlay(screen,font,ItemList.itemList(loadPictures('data/images/Items/')))#creates overlay focussed on player
    worldBack = World.world((10000, 5000),mainCamera,loadPictures('data/images/tiles/'),itemList,tileCracks,weaponPics,armorPics,over,lighting=activeLighting)#creates a world
    worldBack.worldGen('Grassland')#generates the world
    AIOn = worldBack.AIOn#global variable controlling whether the AI is active
    charList = CharacterList.characterList(armorPics)

    player = worldBack.addCharacter(0,True)#creates the player on team player
    player.changeXY(500)#move him/her right 500px

    bottomRow = worldBack.size[1]//32#finds bottom row

    def displayFPS(font):#displays the frames per second
        fps = int(clock.get_fps())#gets fps
        fpsFont = font.render(str(fps), 1, (250, 250, 250))#font renders it
        fpsPos = fpsFont.get_rect()
        fpsPos.centerx = 50
        fpsPos.centery = 50
        screen.blit(fpsFont,fpsPos)

    def setNight():#sets time to night, unused
        background.fill((0,0,0))
        worldBack.baseLightLevel = 0
        worldBack.lighting.lightSection(0,worldBack.columns,0,worldBack.rows)

    ParticleEngine.setGravity(True)#turns on particle engine gravity
    projectiles = []#makes empty list of projectiles

    over.updateHealthbar()#update the healthbar
    #player.changeWeapon(weapons[0])#gives player a weapon
    player.inv.addToInventory(1,1)
    player.inv.addToInventory(3,1)
    player.inv.addToInventory(5,1)
    player.inv.addToInventory(0,80)
    player.inv.addToInventory(2,80)
    player.inv.addToInventory(10,1)
    player.inv.addToInventory(8,80)

    toFocus = 0#unused, kinda
    mouseInv = (None,None)
    clickDel = 0.5
    clickTime = time.time()
    while True:
        mx = pygame.mouse.get_pos()
        my = mx[1]
        mx = mx[0]

        relMX = mx + (mainCamera.centX - (mainCamera.fov[0]//2))#gets the mouse coordinates in the gameworld, not the screen
        relMY = my + (mainCamera.centY - (mainCamera.fov[1]//2))

        playerHover = False
        otherHover = False
        craftHover = False
        if over.fullInv == True and over.obj == player:
            for i in range(len(over.slots)):
                if physics.colliding((mx,my),(1,1),over.slots[i],over.slotSize) == True:
                    player.selectedSlot = i
                    playerHover = True

        if player.openInv != False and over.obj == player:
            for i in range(len(over.otherSlots)):
                if physics.colliding((mx,my),(1,1),over.otherSlots[i],over.slotSize) == True:
                    player.openInv.selectedSlot = i
                    otherHover = True

        if over.fullInv == True and player.openInv == False and over.obj == player:
            for i in range(len(over.craftSlots)):
                if physics.colliding((mx,my),(1,1),over.craftSlots[i],over.slotSize) == True:
                    over.craftHighlight = i
                    craftHover = True
                    
        if craftHover == False:
            over.craftHighlight = None

        pressedKeys = pygame.key.get_pressed()#makes a list of pressed keys
        for key in range(len(pressedKeys)):
            if pressedKeys[key] == True:
                if key == K_SPACE:#if space
                    if player.control == True:
                        player.jump()#jump
                elif key == K_a:#if a
                     if player.control == True:
                        player.addSpeed(-2)#move left
                elif key == K_d:# if d
                    if player.control == True:
                        player.addSpeed(2)#move right
                elif key == K_RETURN:#if enter
                    player.speak('Hello!',5)#say hello for 5 seconds
                elif key == K_o:#if o
                    AIOn = True#turn AI on
                elif key == K_f:#if f
                    AIOn = False#turn Ai off
                elif key == K_u:#if pressed u
                    player.setLevel(player.level+1)#level up player for testing of course
                elif key == K_n:#if pressed n
                    player.mining.addExp(500)
                elif key == K_g:
                    user32 = ctypes.windll.user32
                    screen = pygame.display.set_mode((user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)),FULLSCREEN)
                    screenSize = screen.get_size()
                    mainCamera.changeScreen(screen,(screenSize[0],screenSize[1]))
                    background = pygame.Surface(screen.get_size())#creates a background
                    background = background.convert()
                    background.fill((173, 216, 230))
                    over.changeScreen(screen,screenSize)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if over.fullInv == False:
                        quitGame()
                    else:
                        if over.fullInv == True:
                            if mouseInv[0] != None:
                                player.inv.addToInventory(mouseInv[0].ID,mouseInv[1])
                                mouseInv = (None,None)
                        over.toggleInv()
                elif event.key == K_i:
                    if over.fullInv == True:
                        if mouseInv[0] != None:
                            player.inv.addToInventory(mouseInv[0].ID,mouseInv[1])
                            mouseInv = (None,None)
                    over.toggleInv()
                elif event.key == K_UP:
                    if player.selectedSlot > 0:
                        player.selectedSlot -= 1
                elif event.key == K_DOWN:
                    if over.fullInv == False:
                        if player.selectedSlot < over.slotAmount:
                            player.selectedSlot += 1
                        if player.selectedSlot > over.slotAmount:
                            player.selectedSlot -= over.slotAmount
                    else:
                        if player.selectedSlot < player.inv.inventorySize:
                            player.selectedSlot += 1  
                    

            elif event.type == MOUSEBUTTONDOWN:#if click
                if event.button == 1:
                    if player.control == True:
                        #player.attack()#if left click attack
                        #player.castSpell('Fireblast')
                    #player.shootArrow(1,(mx,my),7)
                    #worldBack.removeTile(relMX//32,relMY//32,1)#remove any clicked on tiles
                        if over.fullInv == False:
                            player.activateHeldItem((relMX,relMY))
                        if time.time() - clickTime >= clickDel:
                            clickTime = time.time()
                            if playerHover == True:
                                if mouseInv[0] == None:
                                    if player.inv.inventory[player.selectedSlot][0] != None:
                                        mouseInv = player.inv.inventory[player.selectedSlot]
                                        player.inv.removeFromInventory(player.selectedSlot,player.inv.inventory[player.selectedSlot][1])
                                else:
                                    if player.inv.inventory[player.selectedSlot][0] == None:
                                        player.inv.inventory[player.selectedSlot] = mouseInv
                                        mouseInv = (None,None)
                                    elif player.inv.inventory[player.selectedSlot][0].ID == mouseInv[0].ID:
                                        player.inv.addToInventory(mouseInv[0].ID,mouseInv[1])
                                        mouseInv = (None,None)
                                        
                            elif otherHover == True:
                                if mouseInv[0] == None:
                                    if player.openInv.inv.inventory[player.openInv.selectedSlot][0] != None:
                                        mouseInv = player.openInv.inv.inventory[player.openInv.selectedSlot]
                                        player.openInv.inv.removeFromInventory(player.openInv.selectedSlot,player.openInv.inv.inventory[player.openInv.selectedSlot][1])
                                else:
                                    if player.openInv.inv.inventory[player.openInv.selectedSlot][0] == None:
                                        player.openInv.inv.inventory[player.openInv.selectedSlot] = mouseInv
                                        mouseInv = (None,None)
                                    elif player.openInv.inv.inventory[player.openInv.selectedSlot][0].ID == mouseInv[0].ID:
                                        player.openInv.inv.addToInventory(mouseInv[0].ID,mouseInv[1])
                                        mouseInv = (None,None)
                            elif craftHover == True:
                                player.crafting.craftItem(player.craftable[over.craftHighlight])
                                        
                            if over.fullInv == True and playerHover == False and otherHover == False:
                                mouseInv = (None,None)
                                
                elif event.button == 3:#if right click
                    col = relMX // 32
                    row = relMY // 32

                    if worldBack.tiles[col][row][1] != None:
                        worldBack.tiles[col][row][1].onClick(player)
                        if worldBack.tiles[col][row][1].inv != None:
                            player.openInv = worldBack.tiles[col][row][1]
                        #worldBack.addTile(relMX//32,relMY//32, 11, 1,lightLevel = 255, physical = False)#place torch
                        #worldBack.addTile(relMX//32,relMY//32, 0, 1)
                        #player.inv.removeFromInventory(0)
                    #worldBack.placeBlueprint('data/blueprints/House1.bprt',(relMX,relMY))
                    #worldBack.tree((relMX,relMY))
                elif event.button == 4:
                    if player.selectedSlot > 0:
                        player.selectedSlot -= 1
                elif event.button == 5:
                    if over.fullInv == False:
                        if player.selectedSlot < over.slotAmount:
                            player.selectedSlot += 1
                        if player.selectedSlot > over.slotAmount:
                            player.selectedSlot -= over.slotAmount
                    else:
                        if player.selectedSlot < player.inv.inventorySize:
                            player.selectedSlot += 1                        
                elif event.button == 2:
                    toFocus += 1
                    if toFocus == len(worldBack.entities):
                        toFocus = 0

        selectEnemy = False#if hovering an enemy
        for i in range(len(worldBack.entities)):
            xy = mainCamera.getRelative((worldBack.entities[i].x,worldBack.entities[i].y))#gets the relative postition of the characters on teh camera
            if worldBack.entities[i].ID != over.obj.ID:#not hovering self
                if physics.colliding((mx,my),(1,1),xy,worldBack.entities[i].size) == True:#and colliding
                    over.hoverEnemy(worldBack.entities[i])#print enemy info
                    selectEnemy = True

        if selectEnemy == False:
            over.unhover()#no enemy info if no hover
                    
        screen.blit(background, (0,0))#draw background

        worldBack.draw()

        mainCamera.focus((worldBack.entities[toFocus].x + (worldBack.entities[toFocus].size[0] // 2),worldBack.entities[toFocus].y + (worldBack.entities[toFocus].size[1]//2)))
        #mainCamera.focus((player.x + (player.size[0] // 2),player.y + (player.size[1]//2)))#focuses the camera on the player

        over.obj = worldBack.entities[toFocus]

        for i in range(len(worldBack.entities)):
            try:
                worldBack.entities[i].main()#runs entity main functions
            except:
                pass

        for i in range(len(projectiles)):
            try:
                projectiles[i].main()#runs projectile main functions
            except:
                pass
        if over.obj.dead == True:#if the overlay object is dead
            over.setMessage('You have died :(',100,(255,0,0))#show condolences

        for i in range(len(worldBack.spawners)):
            worldBack.spawners[i].main()#runs spawners

        for town in worldBack.towns:
            town.main()
            
        ParticleEngine.main(screen,mainCamera,worldBack.size)#runs particle engine
        over.updateHealthbar()#update healthbar
        over.draw()#draw overlay
        if mouseInv[0] != None:
            over.drawItem(mouseInv,(mx,my))
        displayFPS(font)#shows fps
        pygame.display.update((0,0,screenSize[0],screenSize[1]))#updates screen
        clock.tick(60)#constrain fps
