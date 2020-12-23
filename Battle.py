from PIL import Image
import os
import pygame
import pygame.freetype
import random
import sys
import time
pygame.init()

def changePos():
    global position
    if en.ID is 'Tomato':
        position = (200, 20)
    if en.ID is 'Corn':
        position = (240, 20)

class enemy:
    def __init__(self, st, dex, spd, maxHP, maxStam, ID, drop, resistance, vulnerability):
        self.st = st
        self.dex = dex
        self.spd = spd
        self.maxHP = maxHP
        self.maxStam = maxStam
        self.HP = maxHP
        self.Stam = maxStam
        self.ID = ID
        self.effect = ''
        self.time = 0
        self.check = 0
        self.state = 1
        
        self.drop = drop
        self.resist = resistance
        self.vulner = vulnerability


i = {}

#----Comment This Out If Using The Map Movement Script----#
en = enemy(5, 9, 2, 20, 3, 'Tomato', 20, None, 'Bludgeoning')

original = os.getcwd() + '\\Assets'
os.chdir(original + '\\' + en.ID)

for file in os.listdir(os.getcwd()):
    newFile = file.replace('.png', '')
    i[newFile] = pygame.image.load(file)

os.chdir(original)

position = (200, 20)
changePos()
#-------Make Sure That en.ID is set to the Enemy You Want----#

screen = pygame.display.set_mode((720,520))
GAME_FONT = pygame.freetype.Font("font.otf", 32)
textBox = pygame.image.load('NewTextBox.png')
arrow = pygame.image.load('Arrow.png')
smallArrow = pygame.image.load('SmallArrow.png')
Boxtext = pygame.image.load('NewBoxText.png')

def battle(x):
    global en
    global i

    en = enemy(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
    
    original = os.getcwd()
    os.chdir('.\\' + en.ID)

    for file in os.listdir(os.getcwd()):
        newFile = file.replace('.png', '')
        i[newFile] = pygame.image.load(file)

    os.chdir(original)
    changePos()

    pygame.event.clear()

    value = main()
    exitAnim()
    
    ply.battle = False
    pygame.event.clear()
    
    return value
    
class player:
    def __init__(self):
        self.name = 'Ritogan'
        
        self.st = 5
        self.dex = 10
        self.spd = 10
        self.maxHP = 25
        self.maxStam = 2
        self.HP = self.maxHP
        self.Stam = self.maxStam
        
        self.inv = ['Bomb', 'Potion', 'Light Armour', 'Shortsword', 'Winged Shoes']
        self.moves = ['Punch', 'Double Slash', 'Fireball']
        
        self.exp = 0
        self.lvl = 1
        
        self.armour = 'None'
        self.weapon = 'None'
        self.accessory = 'None'
        self.armourBonus = 0
        self.weaponBonus = 0

        self.money = 0
        self.battle = False
        
        
    def addInv(self, obj):
        self.inv.append(obj)
    
    def addMove(self, obj):
        self.moves.append(obj)


ply = player()

def text(x):
    xPos = 95
    yPos = 375
    sleepTime = .0325

    screen.blit(textBox, (10, 295))

    letters = x.upper()

    for i in range(len(letters)):

        #Calculates Projected Width For A Word
        if letters[i] == ' ':
            n = 1
            xProj = 0
            Font = pygame.font.Font('font.otf', 32)
            while i + n < len(letters) and letters[i + n] != ' ':
                    width = Font.size(letters[i + n])[0]
                    xProj += width
                    n += 1

            #Checks To See If New Line Is Needed
            if xProj + xPos >= 580:
                xPos = 95
                yPos += 35

        #yPos Shifts
        slide = 0
        if letters[i] == ',' or letters[i] == '.':
            slide = 20
        elif  letters[i] == '-':
            slide = 12

        #---------------------Renders Each Letter Individually------------------------#
        GAME_FONT.render_to(screen, (xPos ,yPos + slide), letters[i], (255, 255, 255))
        pygame.display.flip()

        #----------------In Case You Want To Skip The Animation---------------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for i in range(len(letters)):
                    sleepTime = 0

        
        #---------------xPos Shifts----------------------#
        shift = 0
        if i + 1 < len(letters):
            if letters[i] == 'I':
                shift = 7
            if letters[i] == 'W':
                shift = -3
            elif letters[i] == '\'':
                shift = 5
            elif letters[i] == 'A' and letters[i + 1] == 'T':
                shift = 3
            elif letters[i] == 'M' and letters[i + 1] == 'E':
                shift = -3

        xPos += 14 - shift


        #Wait and Type Another Letter
        time.sleep(sleepTime)

    #-----------------Take Input to Return---------------#
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main():
    
    ply.battle = True
    introAnim()

    if en.spd > ply.spd:
        baseScreen()
        enTurn()
        if ply.HP <= 0:
            text('A wise man once said,\"Dying is bad\"')
            return 3

    #-------------------------------Main Loop-------------------------------#
    pos = 0
    running = True
    while running:
        pygame.event.pump()

        if round(time.time(), 2) % .25 == 0:
            if en.state == 1:
                en.state = 2
            elif en.state == 2:
                en.state = 1
            elif en.state == 3:
                en.state = 4
            elif en.state == 4:
                en.state = 3

        baseScreen()
        
        #Menu
        GAME_FONT.render_to(screen, (150, 380), "FIGHT", (255, 255, 255))
        GAME_FONT.render_to(screen, (450, 380), "SPECIAL", (255, 255, 255))
        GAME_FONT.render_to(screen, (150, 450), "ITEM", (255, 255, 255))
        GAME_FONT.render_to(screen, (450, 450), "RUN", (255, 255, 255))

        #Moving on the menu
        if pos == 0:
            screen.blit(arrow, (85, 373))
        elif pos == 1:
            screen.blit(arrow, (385,373))
        elif pos == 2:
            screen.blit(arrow, (85, 443))
        elif pos == 3:
            screen.blit(arrow, (385, 443))

        pygame.display.flip()

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if pos == 2:
                        pos = 0
                    elif pos == 3:
                        pos = 1
                elif event.key == pygame.K_DOWN:
                    if pos == 0:
                        pos = 2
                    elif pos == 1:
                        pos = 3
                elif event.key == pygame.K_LEFT:
                    if pos == 1:
                        pos = 0
                    elif pos == 3:
                        pos = 2
                elif event.key == pygame.K_RIGHT:
                    if pos == 0:
                        pos = 1
                    elif pos == 2:
                        pos = 3
                elif event.key == pygame.K_RETURN:
                    if pos == 0:
                        fight()
                    elif pos == 1:
                        if special():
                            continue
                    elif pos == 2:
                        if item():
                            continue
                    else:
                        if run():
                            return 2

                    if en.HP <= 0:
                        text('You Have emerged victorious!')
                        reward()
                        return 0

                    baseScreen()

                    #Enemy's Turn And Checks To See If Player Is Dead
                    enTurn()
                    if ply.HP <= 0:
                        text('A wise man once said,\"Dying is bad\"')
                        return 3
                        
                    effect()

                    #A Second Check To See If The Enemy Died from an Efect
                    if en.HP <= 0:
                        text('You Have emerged victorious!')
                        reward()
                        return 0

#----------------------Code TO Update The Visuals Of Enemy and Player Stats----------------------#
def plyUpdate():
    #Erase Existing Stats And Rewrite Them
    pygame.draw.rect(screen, (255, 255, 255), (600, 150, 700, 50))
    GAME_FONT.render_to(screen, (600, 150), "HP: "+str(ply.HP)+"/"+str(ply.maxHP), (0, 0, 0))
    GAME_FONT.render_to(screen, (600, 190), "Stam: "+str(ply.Stam)+"/"+str(ply.maxStam), (0, 0, 0))

def enUpdate(x, y):
    if en.HP < 0:
        en.HP = 0
    elif en.HP <= .5 * en.maxHP and en.state != 4:
        en.state = 3
    
    #Changes The Enemy Health Bar
    pygame.draw.rect(screen, (0, 0, 0), (25, 75, 54, 190))
    pygame.draw.rect(screen, (99, 199, 77), (30, 80, 44, 180))
    
    for i in range(0, 4 * x):
        en.HP -= 1/4
        if en.HP < 0:
            en.HP = 0
        pygame.draw.rect(screen, (162, 38, 51), (30, 80, 44, int(180 * (1 - en.HP/en.maxHP))))
        pygame.draw.rect(screen, (0, 0, 0), (30, int(180 * (1 - en.HP/en.maxHP)) + 80, 44, 5))
        time.sleep(.03/x)
        pygame.display.flip()

    if en.HP < en.maxHP:
        pygame.draw.rect(screen, (162, 38, 51), (30, 80, 44, int(180 * (1 - en.HP/en.maxHP))))
        pygame.draw.rect(screen, (0, 0, 0), (30, int(180 * (1 - en.HP/en.maxHP)) + 80, 44, 5))
    
    GAME_FONT.render_to(screen, (40, 270), "HP", (0, 0, 0))

    #Changes Enemy Stamina Bar
    pygame.draw.rect(screen, (0, 0, 0), (85, 75, 54, 190))
    pygame.draw.rect(screen, (0, 153, 219), (90, 80, 44, 180))

    for i in range(0, 4 * y):
        en.Stam -= 1/4
        pygame.draw.rect(screen, (162, 38, 51), (90, 80, 44, int(180 * (1 - en.Stam/en.maxStam))))
        pygame.draw.rect(screen, (0, 0, 0), (90, int(180 * (1 - en.Stam/en.maxStam)) + 80, 44, 5))
        time.sleep(.03/y)
        pygame.display.flip()
    
    if en.Stam < en.maxStam:
        pygame.draw.rect(screen, (162, 38, 51), (90, 80, 44, int(180 * (1 - en.Stam/en.maxStam))))
        pygame.draw.rect(screen, (0, 0, 0), (90, int(180 * (1 - en.Stam/en.maxStam)) + 80, 44, 5))

    
    GAME_FONT.render_to(screen, (90, 270), "Stam", (0, 0, 0))

def baseScreen():
    screen.fill((255, 255, 255))
    screen.blit(textBox, (10, 295))
    plyUpdate()
    enUpdate(0, 0)
    screen.blit(i[en.ID + str(en.state)], position)

#------------------All Battle Related Functions Are Below This Line-----------------#
def fight():
    screen.blit(textBox, (10, 295))
    text(ply.name+' attacks!')
    if ply.dex + random.randint(3,5) < en.dex + random.randint(1,3):
        text(en.ID+' dodges your attack!')
    else:
        enHPDec(ply.st + ply.weaponBonus, 'Bludgeoning')

def special():
    if ply.Stam <= 0:
        text('You have zero stamina')
        return

    #Arrow Coordinates
    xArPos = 70
    yArPos = 120

    running = True
    while running:
        pygame.event.pump()

        screen.blit(Boxtext, (10, 10))
        GAME_FONT.render_to(screen, (300, 80), 'SPECIALS', (255, 255, 255))

        '''img = Image.open('Arrow.png')
        img = img.resize((20, 20))
        img.save('SmallArrow.png')'''
        
        screen.blit(smallArrow, (xArPos, yArPos))

        #------------------Render Special Moves Onto the Screen---------------------#
        xPos = 100
        yPos = 120
        for i in range(len(ply.moves)):
            GAME_FONT.render_to(screen, (xPos, yPos), ply.moves[i], (255, 255, 255))
            
            xPos += 200
            if xPos > 520:
                xPos = 100
                yPos += 40
        
        pygame.display.flip()
        
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and yArPos != 120:
                    yArPos -= 40
                elif event.key == pygame.K_DOWN and yArPos != yPos and (xArPos <= 90 + 200 * ((len(ply.moves) % 3) - 1) or yArPos < yPos - 40):
                    yArPos += 40
                elif event.key == pygame.K_LEFT and xArPos != 90:
                    xArPos -= 200
                elif event.key == pygame.K_RIGHT and xArPos != 490 and (xArPos + 30 != xPos - 200 or yArPos != yPos):
                    xArPos += 200
                elif event.key == pygame.K_RETURN:
                    i = int((xArPos - 70)/200 + 3 * (yArPos - 120)/40)
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    return True

    ply.Stam -= 1
    baseScreen()

    move = ply.moves[i]
    #--------------------------Effects and Texts Of Each Special------------------------------#
    if move == 'Punch':
        text('You spring towards the '+en.ID+' and land a solid blow')
        enHPDec(3*ply.st, 'Bludgeoning')
        text(en.ID+' is knocked back a few meters!')        
        
    elif move == 'Double Slash':
        text('You draw your blade and hit not three times, not four times, but two times')
        enHPDec(2*ply.st + 2*ply.weaponBonus, 'Slashing')
        text(en.ID+' now knows how it feels to be slashed twice in a row')
        
    elif move == 'Fireball':
        text('You form a small ball of fire between your hands and throw it towards the enemy')
        
        enHPDec(round(1.5*ply.st), 'Fire')
        
        text(en.ID+' hardly seems to notice until his entire body is engulfed in flames')
        en.effect = 'Burn'

def item():

    if len(ply.inv) == 0:
        text('You Dont have any left items to use')
        return

    #Arrow Coordinates
    xArPos = 70
    yArPos = 120
    
    running = True
    while running:
        pygame.event.pump()

        screen.blit(Boxtext, (10, 10))
        GAME_FONT.render_to(screen, (300, 80), 'ITEMS', (255, 255, 255))

        screen.blit(smallArrow, (xArPos, yArPos))

        #------------------Render Items Onto the Screen---------------------#
        xPos = 100
        yPos = 120
        for i in range(len(ply.inv)):
            GAME_FONT.render_to(screen, (xPos, yPos), ply.inv[i], (255, 255, 255))
            
            xPos += 200
            if xPos > 520:
                xPos = 100
                yPos += 40
        
        pygame.display.flip()
        
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and yArPos != 120:
                    yArPos -= 40
                elif event.key == pygame.K_DOWN and yArPos != yPos and (xArPos <= 70 + 200 * ((len(ply.inv) % 3) - 1) or yArPos < yPos - 40):
                    yArPos += 40
                elif event.key == pygame.K_LEFT and xArPos != 70:
                    xArPos -= 200
                elif event.key == pygame.K_RIGHT and xArPos != 470 and (xArPos + 30 != xPos - 200 or yArPos != yPos):
                    xArPos += 200
                elif event.key == pygame.K_RETURN:
                    i = int((xArPos - 70)/200 + 3 * (yArPos - 120)/40)
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    return True

    baseScreen()
    itemEffects(i)

    
def run():  
    x = random.randint(1,2)
    if x == 1:
        text('You successfully escape the '+en.ID+'!')
        return True
    else:
        text('What A Loser')

def enTurn():
    if en.HP <= int(0.5*en.maxHP) and en.Stam > 0:
        if en.ID == 'Tomato':
            if en.check == 0:
                text('Red liqiud oozes out of the Tomato\'s body') 
                text('You are unsure if it is tomato juice or blood')
                en.check = 1

            text('The Tomato puffs out its cheeks and sends a barrage of seeds in your direction!')

        elif en.ID == 'Corn':
            if en.check == 0:
                text('The corns starts to fall apart')
                text('Shucks, that\'s not something you would want on your plate')
                en.check = 1

            text('A few kernels start to expand in a declicious but deadly attack!')
            pass

        enUpdate(0, 1)
        enSpecAnim()
        HPinc(int(-2 * en.st * (1 - ply.armourBonus/10)))
        text(ply.name+' takes '+str(int(2 * en.st * (1 - ply.armourBonus/10)))+' damage!')
            
    else:    
        text(en.ID+' attacks!')
        if en.dex + random.randint(3,5) < ply.dex + random.randint(1,3):
            text(en.ID+' misses!')
        else:
            HPinc(int(-en.st * (1 - ply.armourBonus/10)))
            text(ply.name+' takes '+str(int(en.st * (1 - ply.armourBonus/10)))+' damage!')

def effect():
    x = en.effect
    
    if x == 'Burn':
        text(en.ID + ' is slowly becoming charred')
        enHPDec(3, 'Fire')
        text(en.ID + ' takes 3 damage!')
        effectTime(3)

def effectTime(x):
    if en.time == 0:
        en.time = x
        
    en.time -= 1
    if en.time == 0:
        en.effect = ''

def HPinc(x):
    ply.HP += x
    
    if ply.HP >= ply.maxHP:
        ply.HP = ply.maxHP
    elif ply.HP < 0:
        ply.HP = 0

    if ply.battle == True:
        plyUpdate()

def damageAnim():

    baseScreen()
    
    for j in range(2):
        for j in range(2):
            screen.blit(i[en.ID + str(en.state) + '-Black'], position)
            pygame.display.flip()
            time.sleep(.0325)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        for j in range(2):
            screen.blit(i[en.ID + str(en.state) + '-White'], position)
            pygame.display.flip()
            time.sleep(.0325)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    screen.blit(i[en.ID + str(en.state)], position)

def enSpecAnim():
    start = time.time()

    screen.blit(i[en.ID + str(en.state) + '-Spec1'], position)
    pygame.display.flip()

    while True:

        end = time.time()

        if end - start >= .30:
            baseScreen()
            break
        elif end - start >= .20:
            screen.blit(i[en.ID + str(en.state) + '-Spec3'], position)
        elif end - start >= .10:
            screen.blit(i[en.ID + str(en.state) + '-Spec2'], position)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                baseScreen()
                return

def enHPDec(x, sort):
    
    if str(en.resist) is sort:
        x /= 2
        text('It\'s not very effective')
    elif str(en.vulner) is sort:
        x *= 2
        text('It\'s extremely effective!')

    x = int(x)
    
    text(en.ID+' takes '+str(x)+' damage!')
    enUpdate(x, 0)
    damageAnim()

def introAnim():
    for j in range(0, 720, 3):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, j, 520))
        pygame.display.flip()
    
    for j in range(0, 720, 15):
        screen.fill((255, 255, 255))
        screen.blit(textBox, (10, 295))
        screen.blit(i[en.ID + str(en.state)], position)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720 - j, 520))
        pygame.display.flip()

def exitAnim():
    for j in range(0, 720, 3):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, j, 520))
        pygame.display.flip()

def reward():
    if en.drop is None:
        return
    elif en.drop is 'Potion':
        ply.addInv('Potion')
        text(en.ID + ' dropped a potion!')
    else:
        ply.money += en.drop
        text(en.ID + ' dropped ' + str(en.drop) + ' creds!')

def itemEffects(i):
    item = ply.inv[i]
    #--------------------------Effects and Texts Of Each Item------------------------------#
    if item == 'Bomb':
        text('You throw a grenade at the ' + en.ID)
        SFX('Item_Bomb')
        enHPDec(15, 'Force')
        
    elif item == 'Potion':
        text('You take a sip of the blood-red potion and the wounds on your body begin closing up')
        SFX('Item_Potion')
        text('You regain 8 hitpoints!')
        HPinc(8)

    elif item == 'Light Armour':
        if ply.armour == 'None':
            text('You put on the light leather armour')
        else:
            ply.addInv(ply.armour)
            text('You take off the ' + ply.armour + ' and put on the light leather armour')

        ply.armour = item
        ply.armourBonus = 2


    elif item == 'Shortsword':
        if ply.weapon == 'None':
            text('You bring out your sword in its leather scabbard, ready to attack at a moment\'s notice')
        else:
            ply.addInv(ply.weapon)
            text('You stow away your ' + ply.weapon + ' and bring out your shortsword')

        ply.weapon = item
        ply.weaponBonus = 2

    elif item == 'Winged Shoes':
        if ply.accessory == 'None':
            text('You wear the shoes, and the wings start flapping, making you lighter and faster')
        else:
            ply.addInv(ply.accessory)
            text('You stow away your ' + ply.accessory + ' and bring out your shortsword')

        ply.accessory = item
        ply.spd += 6

    ply.inv.remove(item)

def SFX(x):
    os.chdir(original + '\\Music')
    pygame.mixer.music.load(x + '.wav')
    pygame.mixer.music.play()
    os.chdir(original)

    
if __name__ == '__main__':
    main()
