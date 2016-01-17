import ParticleEngine

def getSpell(name):#returns a spell dictionary by name
    for i in range(len(spellList)):
        if spellList[i]['Name'] == name:
            return spellList[i]
    return None

def fireBlast (mage,target = None):#this function shoots a fireball, mage is a character that shoots the spell and target the targeted character
    damage = 20#base damage is 20
    damage = damage + (damage * (mage.level // 10))#modifies the damge according to the mage's level
    mage.armLeft.setRotation(90, -mage.attackSpeed)#rotates the mage's arm

    if mage.faceRight == False:#x range is the x speed
        xRange = -20
    else:
        xRange = 20
    
    mage.shootProject(0,(xRange, 0),damage,mage)#shoots a projectile
    ParticleEngine.createPoint(10,mage.x,mage.y,(-10,10),(-10,10),(255,100,0),'Circle Rand',grav = True)#create an explosion of particles
    return damage#returns the damage done


spellList = []#list of all spells
spellList.append({'Name':'Fireblast','Spell':fireBlast, 'Cooldown':100})#adds fireball, cooldown is delay between spellcasts
