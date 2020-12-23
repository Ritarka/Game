from PIL import Image
from timeit import default_timer as timer
import time
import os
import sys
import pygame
import Battle

pygame.init()
screen = pygame.display.set_mode((720,520))

#Load Title Screen Images
currDir = os.getcwd()
title = {}

os.chdir(currDir + '\\TitleScreen')
for file in os.listdir(os.getcwd()):
    newfile = file.replace('.png', '')
    title[newfile] = pygame.image.load(file)

screen.blit(title['Base'], (0, 0))
pygame.display.flip()
os.chdir(currDir)

def main():
    while True:
        if intro():
            f = open('Data.dat', 'w')
            f.close()
        world('New Map')

def intro():
    x = 'Start'
    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type is pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x = 'Start'
                    screen.blit(title[x], (0, 0))
                    pygame.display.flip()
                elif event.key == pygame.K_DOWN:
                    x = 'Continue'
                    screen.blit(title[x], (0, 0))
                    pygame.display.flip()
                elif event.key == pygame.K_RETURN:
                    if x is 'Start':
                        return True
                    else:
                        return False

def back():
    for j in range(0, 520, 1):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720, j))
        pygame.display.flip()

    for j in range(0, 520, 4):
        screen.blit(title['Base'], (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720, 520 - j))
        pygame.display.flip()

    screen.blit(title['Base'], (0, 0))
    pygame.display.flip()

def world(location):
    
    GAME_FONT = pygame.freetype.Font("font.otf", 32)
    Large = pygame.freetype.Font("font.otf", 48)

    def transition():
        for j in range(0, 520, 1):
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720, j))
            pygame.display.flip()


        for j in range(0, 520, 4):
            screen.blit(area[place], (-charX, -charY))
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720, 520 - j))
            pygame.display.flip()


    def save():

        x = [Battle.ply.HP, Battle.ply.Stam, charX, charY, charRXM, charRYM, Battle.ply.inv, Battle.ply.money,
             Battle.ply.armour, Battle.ply.weapon, Battle.ply.accessory, yCoor, xCoor]

        with open('Data.dat', 'w') as f:
            for data in x:
                f.write(str(data) + '\n')

            for i in encounters:
                for k in i:
                    for j in k:
                        f.write(str(j.alive) + '\n')
                        f.write(str(j.pos[0]) + '\n')
                        f.write(str(j.pos[1]) + '\n')

            for i in findings:
                for k in i:
                    for j in k:
                        f.write(str(j.active) + '\n')
        

    def load():
        nonlocal charX, charY, charRXM, charRYM, yCoor, xCoor, place

        enemies = 0
        for i in encounters:
            for j in i:
                for k in j:
                    enemies += 1

        stuff = 0
        for i in findings:
            for j in i:
                for k in j:
                    stuff += 1
        
        with open('Data.dat', 'r') as f:
            info = []
            for k in range(13 + enemies * 3 + stuff):
                info.append(f.readline())

        Battle.ply.HP = int(info[0])
        Battle.ply.Stam = int(info[1])
        charX = int(info[2])
        charY = int(info[3])
        charRXM = int(info[4])
        charRYM = int(info[5])
        
        battleArray = []
        word = ''
        for k in info[6]:
            if k in ',]':
                battleArray.append(word.strip())
                word = ''
            elif k not in '[\'':
                word = word + k

        Battle.ply.inv = battleArray
        Battle.ply.money = int(info[7])

        line = info[8]
        line = line.strip()
        Battle.ply.armour = line.replace('\'', '')

        line = info[9]
        line = line.strip()
        Battle.ply.weapon = line.replace('\'', '')

        line = info[10]
        line = line.strip()
        Battle.ply.accessory = line.replace('\'', '')

        yCoor = int(info[11])
        xCoor = int(info[12])

        place = location + str(3 * yCoor + xCoor + 1)
        
        x = 13
        for i in encounters:
            for j in i:
                for k in j:
                    k.alive = int(info[x])
                    k.pos[0] = int(info[x + 1])
                    k.pos[1] = int(info[x + 2])

                    x += 3

        for i in findings:
            for j in i:
                for k in j:
                    line = info[x]
                    line = line.strip()
                    k.active = line.replace('\'', '')

                    x += 1

    def death():
        deathScreen = pygame.Surface((720,520)).convert_alpha()
        deathScreen2 = pygame.Surface((720,520)).convert_alpha()
        
        Alpha = 0
        shift = 5
        while Alpha <= 255:
            screen.blit(area[place], (-charX,-charY))
            screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                
            deathScreen.fill((0,0,0,Alpha))
            screen.blit(deathScreen, (0,0))
            deathScreen2.fill((0,0,0,Alpha/2))
            screen.blit(deathScreen2, (0,0))

            pygame.display.flip()

            Alpha += 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
        load()
        Alpha = 0
        while Alpha <= 175:

            GAME_FONT.render_to(screen, (180, 250), 'You Won\'t Give Up Now Will You?', (Alpha, Alpha, Alpha, Alpha))
            time.sleep(.03)

            pygame.display.flip()

            Alpha += 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        time.sleep(1.2)

        Alpha = 255
        while Alpha > 0:
            screen.blit(area[place], (-charX,-charY))
            screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                
            deathScreen.fill((0,0,0,Alpha))
            screen.blit(deathScreen, (0,0))
            deathScreen2.fill((0,0,0,Alpha/2))
            screen.blit(deathScreen2, (0,0))

            pygame.display.flip()
            Alpha -= 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def item():
        xDist = 200
        yDist = 40
        
        xPos = 100
        yPos = 100
        for i in range(len(Battle.ply.inv)):
            GAME_FONT.render_to(screen, (xPos, yPos), Battle.ply.inv[i], (0, 0, 0))
            
            xPos += xDist
            if xPos > 520:
                xPos = 100
                yPos += yDist

        if len(Battle.ply.inv) == 0:
            Large.render_to(screen, (50, 250), 'YOU DO NOT HAVE ANY ITEMS TO USE')

        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x:
                        return 5
                    if event.key == pygame.K_RIGHT:
                        return 4
                    elif event.key == pygame.K_LEFT:
                        return 2
                    elif event.key == pygame.K_DOWN:


                        #----------------------Rest is Item Interaction Code---------------------#
                        xArPos = 70
                        yArPos = 100

                        smallArrow = pygame.image.load('SmallArrow.png')

                        running = True
                        while running:
                            screen.blit(smallArrow, (xArPos, yArPos))
                            pygame.display.flip()
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:

                                    pygame.draw.rect(screen, (255, 213, 79), (xArPos, yArPos, 20, 20))
                                    pygame.display.flip()

                                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x: return 5
                                    
                                    elif event.key == pygame.K_UP:
                                        if yArPos != 100: yArPos -= yDist
                                        else: return 3

                                    elif event.key == pygame.K_DOWN and yArPos != yPos and (xArPos <= 70 + 200 * ((len(Battle.ply.inv) % 3) - 1) or yArPos < yPos - 40):
                                        yArPos += yDist
                                    elif event.key == pygame.K_LEFT:
                                        if xArPos != 70: xArPos -= xDist
                                        else: return 2
                                        
                                    elif event.key == pygame.K_RIGHT:
                                        if xArPos != 470 and (xArPos + 30 != xPos - 200 or yArPos != yPos): xArPos += xDist
                                        else: return 4
                                        
                                    elif event.key == pygame.K_RETURN:
                                        i = int((xArPos - 70)/200 + 3 * (yArPos - 100)/40)
                                        running = False

                        if Battle.ply.inv[i] == 'Bomb':
                            Battle.text('You can\'t use that now')
                        else:
                            Battle.itemEffects(i)
                        
                        return 3


    def special():
        xDist = 200
        yDist = 40
        
        xPos = 100
        yPos = 100
        for i in range(len(Battle.ply.moves)):
            GAME_FONT.render_to(screen, (xPos, yPos), Battle.ply.moves[i], (0, 0, 0))
            
            xPos += xDist
            if xPos > 520:
                xPos = 100
                yPos += yDist

        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x:
                        return 5
                    if event.key == pygame.K_RIGHT:
                        return 3
                    elif event.key == pygame.K_LEFT:
                        return 1
                    elif event.key == pygame.K_DOWN:

                        #----------------------Rest is Special Description Code---------------------#
                        xArPos = 70
                        yArPos = 100

                        smallArrow = pygame.image.load('SmallArrow.png')

                        running = True
                        while running:
                            screen.blit(smallArrow, (xArPos, yArPos))
                            pygame.display.flip()
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:

                                    pygame.draw.rect(screen, (255, 213, 79), (xArPos, yArPos, 20, 20))
                                    pygame.display.flip()

                                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x: return 5
                                    
                                    elif event.key == pygame.K_UP:
                                        if yArPos != 100: yArPos -= yDist
                                        else: return 2

                                    elif event.key == pygame.K_DOWN and yArPos != yPos and (xArPos <= 70 + xDist * ((len(Battle.ply.moves) % 3) - 1) or yArPos < yPos - 40):
                                        yArPos += yDist
                                        
                                    elif event.key == pygame.K_LEFT:
                                        if xArPos != 70: xArPos -= xDist
                                        else: return 1
                                        
                                    elif event.key == pygame.K_RIGHT and (xArPos + 30 != xPos - xDist or yArPos != yPos):
                                        if xArPos != 470: xArPos += xDist
                                        else: return 3
                                        
                                    elif event.key == pygame.K_RETURN:
                                        i = int((xArPos - 70)/xDist + 3 * (yArPos - 100)/yDist)
                                        running = False

                        #---------------------Case By Case Descriptions of Specials---------------------#
                        special = Battle.ply.moves[i]
                        if special == 'Punch':
                            Battle.text('The classic')
                        elif special == 'Double Slash':
                            Battle.text('Two lightning fast strikes guaranteed to mortally damage your opponent')
                        elif special == 'Fireball':
                            Battle.text('A ball of fire that burns the enemy for the next three turns!')
                        
                        return 2

    def UI():
        pos = 1
        while True:
            screen.blit(mapUI[str(pos)], (0, 0))

            #-------------------------Tab Names----------------------------#
            GAME_FONT.render_to(screen, (65, 9), "STATS", (0, 0, 0))
            GAME_FONT.render_to(screen, (222, 9), "SPECIALS", (0, 0, 0))
            GAME_FONT.render_to(screen, (410, 9), "ITEMS", (0, 0, 0))
            GAME_FONT.render_to(screen, (558, 9), "EQUIPMENT", (0, 0, 0))

            #---------------------------Tab Specific Information-----------------------------------#
            if pos == 1:
                GAME_FONT.render_to(screen, (75, 100), "Strength - " + str(Battle.ply.st), (0, 0, 0))
                GAME_FONT.render_to(screen, (75, 200), "Dexterity - " + str(Battle.ply.dex), (0, 0, 0))
                GAME_FONT.render_to(screen, (75, 300), "Speed - " + str(Battle.ply.spd), (0, 0, 0))
                Large.render_to(screen, (375, 100), "HP - " + str(Battle.ply.HP) + '/' + str(Battle.ply.maxHP), (0, 0, 0))
                Large.render_to(screen, (375, 200), "Stamina - " + str(Battle.ply.Stam) + '/' + str(Battle.ply.maxStam), (0, 0, 0))
                GAME_FONT.render_to(screen, (75, 400), "Creds - " + str(Battle.ply.money), (0, 0, 0))
                GAME_FONT.render_to(screen, (375, 300), "Armour Bonus - " + str(Battle.ply.armourBonus), (0, 0, 0))
                GAME_FONT.render_to(screen, (375, 400), "Weapon Bonus - " + str(Battle.ply.weaponBonus), (0, 0, 0))

                
            elif pos == 2:
                pos = special()
            elif pos == 3:
                pos = item()
            else:
                GAME_FONT.render_to(screen, (80, 100), "Armor - " + Battle.ply.armour, (0, 0, 0))
                GAME_FONT.render_to(screen, (80, 200), "Weapon - " + Battle.ply.weapon, (0, 0, 0))
                GAME_FONT.render_to(screen, (80, 300), "Accessory - " + Battle.ply.accessory, (0, 0, 0))
                GAME_FONT.render_to(screen, (380, 100), "Armor Bonus - " + str(Battle.ply.armourBonus), (0, 0, 0))
                GAME_FONT.render_to(screen, (380, 200), "Weapon Bonus - " + str(Battle.ply.weaponBonus), (0, 0, 0))

                ac = Battle.ply.accessory

                if ac == 'Winged Shoes':
                    GAME_FONT.render_to(screen, (80, 370), 'Description:', (0, 0, 0))
                    GAME_FONT.render_to(screen, (80, 430), 'These shoes help you attack quicker', (0, 0, 0))
        

            pygame.display.flip()

            if pos == 5:
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_x:
                        return
                    elif event.key == pygame.K_RIGHT:
                        pos += 1
                        if pos == 5:
                            pos = 1
                    elif event.key == pygame.K_LEFT:
                        pos -= 1
                        if pos == 0:
                            pos = 4


    #The character's position on the map
    charX = 400
    charY = 1080


    class creature:

        alive = 1
        
        def __init__(self, stats, initialPos):
            #Strength, dexterity, speed, HP, Stamina, ID, Drop, Resistance, Vulnerablity
            self.stats = stats
            
            self.pos = [0, 0]
            self.initialPos = initialPos

            self.collision = None
            self.dim = None

    class still:

        active = True

        #Objects of the still class are hidden by default
        def __init__(self, ID, pos, hidden = True, stats = None):
            self.ID = ID

            self.pos = pos

            self.collision = pygame.Rect(pos[0], pos[1], 64, 64)
            
            self.hidden = hidden
            self.stats = stats

    #Reminder: Each creature object is unique, do not re-use the same object
    #Reminder:  1 - Up, 2 - Right, 3 - Down, 4 - Left
    if location == 'New Map':
        mapPos = [[0, '23', '4'],
                  [0, '123', '4'],
                  [0, '1', 0]]

        Tomato = creature((5, 9, 2, 10, 3, 'Tomato', 20, 'Fire', 'Bludgeoning'), (1000, 1000))
        Corn = creature((5, 9, 12, 25, 3, 'Corn', None, None, None), (500, 1000))
        Tomato1 = creature((5, 9, 2, 10, 3, 'Tomato', 20, None, None), (1000, 1000))
        Corn1 = creature((5, 9, 12, 25, 3, 'Corn', 'Potion', None, None), (500, 1000))
        
        encounters = [ [[], [Tomato1, Corn1], []],
                  [[], [Tomato, Corn], []],
                  [[], [], []] ]


        tomato = still('Tomato', (0, 0), False, (2, 6, Battle.ply.spd + 1, 8, 4, 'Tomato', 10, None, None))
        corn = still('Corn', (1536, 0), stats = (4, 10, Battle.ply.spd + 1, 14, 2, 'Corn', 'Potion', None, None))
        bomb = still('Bomb', (0, 1536))
        creds = still(20, (1536, 1536))

        findings = [[[], [creds, corn], []],
                   [[], [tomato, bomb], []],
                   [[], [], []] ]

    xCoor = 1
    yCoor = 1
    place = location + str(3 * yCoor + xCoor + 1)
    enemy = encounters[yCoor][xCoor]
    objects = findings[yCoor][xCoor]

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    charRX = 296
    charRY = 186

    #The character's position modifier (coming up on edges)
    charRXM = 0
    charRYM = 0

    #Initializing the character's and enemies' sprites
    charSprite = 'CharacterFront1'

    #The width and height of the player
    playerHeight = 0
    playerWidth = 0

    #The initial player collision rect
    playerCollision = pygame.Rect(charRX+charRXM,charRY+charRYM,playerWidth,playerHeight)

    #Accounting for the empty space of the character sprites
    emptyXModChar = 0
    emptyYModChar = 0

    #Uh... well, speed
    speed = 2

    walkTimerStart = 0


    currDir = os.getcwd()

    #Opening the sprites for use by pygame
    i = {}
    os.chdir(currDir + '\\Tony')
    for file in os.listdir(os.getcwd()):
        newFile = file.replace('.png', '')
        i[newFile] = pygame.image.load(file)

    #Reminder: Resizing the map takes a lot of time....this now takes 1.4 seconds...we should avoid resizing images
    area = {}
    os.chdir(currDir + '\\Maps' + '\\' + location)
    for file in os.listdir(os.getcwd()):
        newFile = file.replace('.png', '')
        area[newFile] = pygame.image.load(file)

    mapUI = {}
    os.chdir(currDir + '\\UI')
    for file in os.listdir(os.getcwd()):
        newFile = file.replace('.png','')
        mapUI[newFile] = pygame.image.load(file)

    os.chdir(currDir)

    #Resizing World Sprites
    def resize():
        nonlocal enemy, objects, enemyImg, objectImg
        
        enemy = encounters[yCoor][xCoor]
        objects = findings[yCoor][xCoor]
        enemyImg = {}
        objectImg = {}
        
        for k in range(len(enemy)):
            os.chdir(currDir + '\\MapSprites')
            img = Image.open(enemy[k].stats[5] + '.png')
            enemy[k].collision = pygame.Rect(enemy[k].initialPos[0], enemy[k].initialPos[1], img.size[0], img.size[1])
            enemy[k].dim = img.size
            enemyImg[enemy[k].stats[5]] = pygame.image.load(enemy[k].stats[5] + '.png')

            
        for k in range(len(objects)):
            if not objects[k].hidden:
                os.chdir(currDir + '\\Objects')
                img = Image.open(objects[k].stats[5] + '.png')
                objects[k].collision = pygame.Rect(objects[k].pos[0], objects[k].pos[1], img.size[0], img.size[1])
                objectImg[objects[k].ID] = pygame.image.load(objects[k].ID + '.png')
            

        os.chdir(currDir)

    #--/-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    enemyImg = {}
    objectImg = {}

    filestats = os.stat('Data.dat')
    if filestats.st_size != 0:
        load()
        place = location + str(3 * yCoor + xCoor + 1)
    
    resize()
    save()
    transition()

    running = True
    while running:
        
        #Initializing the map
        screen.blit(area[place], (-charX,-charY))

        #Sceen Transition Triggers, drawn for ease of testing
        pygame.draw.rect(screen, (255, 0, 0), (0 - charX, 760 - charY, 20, 80))
        left = pygame.Rect(0 - charX, 760 - charY, 20, 80)
        pygame.draw.rect(screen, (255, 0, 0), (1580 - charX, 760 - charY, 20, 80))
        right = pygame.Rect(1580 - charX, 760 - charY, 20, 80)
        pygame.draw.rect(screen, (255, 0, 0), (760 - charX, 0 - charY, 80, 20))
        up = pygame.Rect(760 - charX, 0 - charY, 80, 20)
        pygame.draw.rect(screen, (255, 0, 0), (760 - charX, 1580 - charY, 80, 20))
        down = pygame.Rect(760 - charX, 1580 - charY, 80, 20)

        #Keeps track of all keys that are currently held
        keys = pygame.key.get_pressed()


        boxCollision = []
        #Determining where collision boxes are
        if place == 'New Map5' or place == 'New Map8' or place == 'New Map6' or place == 'New Map2' or place == 'New Map3':
            boxCollision.append(pygame.Rect(100-charX,100-charY,200,200))
            boxCollision.append(pygame.Rect(200-charX,200-charY,200,200))
            boxCollision.append(pygame.Rect(1300-charX,100-charY,200,200))
            boxCollision.append(pygame.Rect(1200-charX,200-charY,200,200))
            boxCollision.append(pygame.Rect(700-charX,700-charY,200,200))
            boxCollision.append(pygame.Rect(200-charX,1200-charY,200,200))
            boxCollision.append(pygame.Rect(100-charX,1300-charY,200,200))
            boxCollision.append(pygame.Rect(1200-charX,1200-charY,200,200))
            boxCollision.append(pygame.Rect(1300-charX,1300-charY,200,200))
            

        #Walking animation
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            walkTimerEnd = timer()

            #Changing sprites while walking
            if walkTimerEnd - walkTimerStart > .25:
                if charSprite.endswith('1'):
                    charSprite = charSprite.replace('1','2')
                elif charSprite.endswith('2'):
                    if charSprite.endswith('Left',9,13) or charSprite.endswith('Right',9,14):
                        charSprite = charSprite.replace('2','1')
                    else:
                        charSprite = charSprite.replace('2','3')
                else:
                    charSprite = charSprite.replace('3','2')
                walkTimerStart = timer()

        #Changing the sprite to a standing position        
        elif not charSprite.endswith('1'):
            charSprite = charSprite.replace(charSprite[len(charSprite)-1],'1')


        
        #Drawing the Objects
        for k in range(len(objects)):
            #pygame.draw.rect(screen, (255, 255, 255), (objects[k].collision.x, objects[k].collision.y, 64, 64)) #Use this to check the hitboxes of the objects
            if objects[k].active and not objects[k].hidden:
                screen.blit(objectImg[objects[k].ID], (objects[k].pos[0] - charX, objects[k].pos[1] - charY))

        #Drawing the enemy
        for k in range(len(enemy)):
            if enemy[k].alive == 1:
                screen.blit(enemyImg[enemy[k].stats[5]],(enemy[k].initialPos[0] - charX - enemy[k].pos[0], enemy[k].initialPos[1] - charY - enemy[k].pos[1]))
                #pygame.draw.rect(screen,(255,255,255),(enemy[k].collision.x, enemy[k].collision.y, enemy[k].collision.w, enemy[k].collision.h))

        #Drawing the player
        screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))

        #Updating the player's collision rect
        playerCollision.x = charRX+charRXM+emptyXModChar
        playerCollision.y = charRY+charRYM+emptyYModChar
        playerCollision.w = playerWidth
        playerCollision.h = playerHeight

        #Updating the enemies' collision rects
        for k in range(len(enemy)):
            enemy[k].collision.x = enemy[k].initialPos[0] - charX - enemy[k].pos[0]
            enemy[k].collision.y = enemy[k].initialPos[1] - charY - enemy[k].pos[1]
            if enemy[k].alive == 1:
                enemy[k].collision.w = enemy[k].dim[0]
                enemy[k].collision.h = enemy[k].dim[1]
            else:
                enemy[k].collision.w = 0
                enemy[k].collision.h = 0

        for k in range(len(objects)):
            objects[k].collision.x = objects[k].pos[0] - charX
            objects[k].collision.y = objects[k].pos[1] - charY
        
        
        pygame.display.flip()




#------------------------------Key Strokes-------------------------------------------------------------------------------------------------------------------------------------------#




        #Sprinting
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            speed = 4
        else:
            speed = 2

        #Movement
        if keys[pygame.K_UP]:
            if charY > 0 and charRYM == 0:
                charY -= speed   
            elif playerCollision.y > 0: #Upper edge collision
                charRYM -= speed
            elif playerCollision.y > 260: #Moving away from lower edge (1/2 screen height)
                charRYM -= speed
            if (charSprite == 'CharacterFront1' or charSprite == 'CharacterFront2' or charSprite == 'CharacterFront3') and not keys[pygame.K_DOWN]:
                charSprite = 'CharacterBack2'
            if playerCollision.colliderect(up) and '1' in mapPos[yCoor][xCoor] and mapPos[yCoor - 1][xCoor] != 0:
                prev = place
                yCoor -= 1
                place = location + str(3 * yCoor + xCoor + 1)

                for k in range(0, 1600, 16):
                    screen.fill((0, 0, 0))
                    screen.blit(area[prev], (-charX, -charY + k))
                    screen.blit(area[place], (-charX, -charY - 1600 + k))
                    screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                    pygame.display.flip()

                    charY += 1080/100
                    charRYM += 410/100

                charY = int(charY)
                charRYM = int(charRYM)

                resize()
                    
        if keys[pygame.K_DOWN]:
            if charY < 1080 and charRYM == 0: #1080 -> Total Map Height - Screen Height
                charY += speed
            elif playerCollision.y < 520 - playerCollision.h: #Lower edge collision (Screen height minus collision box height)
                charRYM += speed
            elif playerCollision.y < 260 + playerCollision.h: #Moving away from upper edge (1/2 screen height plus collision box height)
                charRYM += speed
            if (charSprite == 'CharacterBack1' or charSprite == 'CharacterBack2' or charSprite == 'CharacterBack3') and not keys[pygame.K_UP]:
                charSprite = 'CharacterFront2'
            if playerCollision.colliderect(down) and '3' in mapPos[yCoor][xCoor] and mapPos[yCoor + 1][xCoor] != 0:
                prev = place
                yCoor += 1
                place = location + str(3 * yCoor + xCoor + 1)

                for k in range(0, 1600, 16):
                    screen.fill((0, 0, 0))
                    screen.blit(area[prev], (-charX, -charY - k))
                    screen.blit(area[place], (-charX, -charY + 1600 - k))
                    screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                    pygame.display.flip()

                    charY -= 1080/100
                    charRYM -= 410/100

                charY = int(charY)
                charRYM = int(charRYM)

                resize()
            
        if keys[pygame.K_LEFT]:
            if charX > 0 and charRXM == 0:
                charX -= speed
            elif playerCollision.x > 0: #Left edge collision
                charRXM -= speed
            elif playerCollision.x > 360: #Moving away from the right edge (1/2 screen width)
                charRXM -= speed
            if ((charSprite == 'CharacterBack1' or charSprite == 'CharacterBack2' or charSprite == 'CharacterBack3') and not keys[pygame.K_UP]) or ((charSprite == 'CharacterFront1' or charSprite == 'CharacterFront2' or charSprite == 'CharacterFront3') and not keys[pygame.K_DOWN]) or ((charSprite == 'CharacterRight1' or charSprite == 'CharacterRight2' or charSprite == 'CharacterRight3') and not keys[pygame.K_RIGHT]):
                charSprite = 'CharacterLeft2'
            if playerCollision.colliderect(left) and '4' in mapPos[yCoor][xCoor] and mapPos[yCoor][xCoor - 1] != 0:
                prev = place
                xCoor -= 1
                place = location + str(3 * yCoor + xCoor + 1)

                for k in range(0, 1600, 16):
                    screen.fill((0, 0, 0))
                    screen.blit(area[prev], (-charX + k, -charY))
                    screen.blit(area[place], (-charX - 1600 + k, -charY))
                    screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                    pygame.display.flip()

                    charX += 880/100
                    charRXM += 640/100

                charX = int(charX)
                charRXM = int(charRXM)

                resize()
                    
        if keys[pygame.K_RIGHT]:
            if charX < 880 and charRXM == 0:
                charX += speed
            elif playerCollision.x < 720 - playerCollision.w: #Right edge collision (Screen width minus collision box width)
                charRXM += speed
            elif playerCollision.x < 360 + playerCollision.w: #Moving away from the left edge (1/2 screen width plus collision box width)
                charRXM += speed
            if ((charSprite == 'CharacterBack1' or charSprite == 'CharacterBack2' or charSprite == 'CharacterBack3') and not keys[pygame.K_UP]) or ((charSprite == 'CharacterFront1' or charSprite == 'CharacterFront2' or charSprite == 'CharacterFront3') and not keys[pygame.K_DOWN]) or ((charSprite == 'CharacterLeft1' or charSprite == 'CharacterLeft2' or charSprite == 'CharacterLeft3') and not keys[pygame.K_LEFT]):
                charSprite = 'CharacterRight2'
            if playerCollision.colliderect(right) and '2' in mapPos[yCoor][xCoor] and mapPos[yCoor][xCoor + 1] != 0:
                prev = place
                xCoor += 1
                place = location + str(3 * yCoor + xCoor + 1)

                for k in range(0, 1600, 16):
                    screen.fill((0, 0, 0))
                    screen.blit(area[prev], (-charX - k, -charY))
                    screen.blit(area[place], (-charX + 1600 - k, -charY))
                    screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                    pygame.display.flip()

                    charX -= 880/100
                    charRXM -= 640/100

                charX = int(charX)
                charRXM = int(charRXM)

                resize()

        
        if keys[pygame.K_RETURN]:
            for k in range(len(objects)):
                if playerCollision.colliderect(objects[k].collision) and objects[k].active:
                    try:
                        Battle.ply.money += objects[k].ID

                        if objects[k].hidden:
                            Battle.text('You found ' + str(objects[k].ID) + ' creds buried in the ground!')
                        else:
                            Battle.text('You found ' + str(objects[k].ID) + ' creds')

                        objects[k].active = False
                    except:
                        if objects[k].hidden:
                            Battle.text('You find a ' + objects[k].ID + ' beneath the ground!')
                                
                        if objects[k].ID is 'Bomb':
                            Battle.ply.addInv('Bomb')
                            Battle.text('You slowly pick up the bomb and put it in your backpack')
                            objects[k].active = False
                        else:

                            Battle.text('You pick up and examine the ' + objects[k].ID + ', when it suddenly attacks you!')

                            os.chdir(currDir + '\\Music')
                            music = pygame.mixer.Sound('Tomato_Battle.wav')
                            os.chdir(currDir)

                            pygame.mixer.Channel(0).play(music, -1)                
                            value = Battle.battle(objects[k].stats)
                            pygame.mixer.Channel(0).fadeout(1000)

                            if value is 3:
                                for j in range(0, 720, 24):
                                    screen.blit(area[place], (-charX,-charY))
                                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720 - j, 520))
                                    pygame.display.flip()
                                
                                death()
                            else:
                                objects[k].active = False

                                for j in range(0, 720, 24):
                                    screen.blit(area[place], (-charX,-charY))
                                    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720 - j, 520))
                                    pygame.display.flip()

                


        #Misc collision checks (caused by the addition of sprinting) (becoming QPU missaligned)
        if playerCollision.y < 0: #Preventing the character from moving off the upper edge of the screen
            charRYM = -222
        if playerCollision.y > 520 - playerCollision.h: #Preventing the character from committing under screen
            charRYM = 224
        if playerCollision.x < 0: #Preventing the character from no clipping out of reality and off of the left edge of the map
            if emptyXModChar == 40: #For foward/back sprites
                charRXM = -336
            if emptyXModChar == 48: #For side sprites
                charRXM = -344
        if playerCollision.x > 720 - playerCollision.w: #Preventing the character from building up speed for 12 microseconds and entering a PU off of the right edge of the map
            if emptyXModChar == 40: #For foward/back sprites
                charRXM = 336
            if emptyXModChar == 48: #For side sprites
                charRXM = 344
        if charY < 0: #Preventing the screen from scrolling beyond the map's upper edge
            charY = 0
        elif charY > 1080: #Preventing the screen from scrolling beyond the map's lower edge
            charY = 1080
        if charX < 0: #Preventing the screen from scrolling beyond the map's left edge
            charX = 0
        if charX > 880: #Preventing the screen from scrolling beyond the map's right edge
            charX = 880
        if (charRXM > 0 and charX < 800) or (charRXM < 0 and charX > 800): #Preventing passing the trigger to start scrolling the screen while moving horizontally
            charRXM = 0
        if (charRYM > 0 and charY < 800) or (charRYM < 0 and charY > 800): #Preventing passing the trigger to start scrolling the screen while moving vertically
            charRYM = 0

        
        #Internal Collision
        for j in range(len(boxCollision)):
            if playerCollision.colliderect(boxCollision[j]):
                if playerCollision.x >= boxCollision[j].x + boxCollision[j].w - 16:
                    if charRXM == 0:
                        charX += boxCollision[j].x + boxCollision[j].w - playerCollision.x
                    else:
                        charRXM += boxCollision[j].x + boxCollision[j].w - playerCollision.x
                elif playerCollision.x + playerCollision.w <= boxCollision[j].x + 16:
                    if charRXM == 0:
                        charX -= playerCollision.x + playerCollision.w - boxCollision[j].x
                    else:
                        charRXM -= playerCollision.x + playerCollision.w - boxCollision[j].x
                elif playerCollision.y >= boxCollision[j].y + boxCollision[j].h - 16:
                    if charRYM == 0:
                        charY += boxCollision[j].y + boxCollision[j].h - playerCollision.y
                    else:
                        charRYM += boxCollision[j].y + boxCollision[j].h - playerCollision.y
                elif playerCollision.y + playerCollision.h <= boxCollision[j].y + 16:
                    if charRYM == 0:
                        charY -= playerCollision.y + playerCollision.h - boxCollision[j].y
                    else:
                        charRYM -= playerCollision.y + playerCollision.h - boxCollision[j].y
        

                

        #Updating sprite dimensions for collision
        if charSprite.endswith('Back',len(charSprite)-5,len(charSprite)-1) or charSprite.endswith('Front',len(charSprite)-6,len(charSprite)-1):
            playerWidth = 48
            playerHeight = 74
            emptyXModChar = 40
            emptyYModChar = 36
        else:
            playerWidth = 28
            playerHeight = 74
            emptyXModChar = 48
            emptyYModChar = 36



        


        #Enemy movement
        for k in range(len(enemy)):
            enDist = int(((playerCollision.center[0]-enemy[k].collision.center[0]) ** 2 + (playerCollision.center[1]-enemy[k].collision.center[1]) ** 2) ** .5)
            if enDist > 460 and enemy[k].alive == 2:
                enemy[k].alive = 1
            if enDist < 250 and enemy[k].alive == 1:
                enemyCollisionCheckLeft = True
                enemyCollisionCheckRight = True
                enemyCollisionCheckUp = True
                enemyCollisionCheckDown = True
                for j in range(0,9):
                    if enemy[k].collision.colliderect(boxCollision[j]):
                        if enemy[k].collision.x >= boxCollision[j].x + boxCollision[j].w - 16:
                            enemyCollisionCheckLeft = False
                        elif enemy[k].collision.x + enemy[k].collision.w <= boxCollision[j].x + 16:
                            enemyCollisionCheckRight = False
                        elif enemy[k].collision.y >= boxCollision[j].y + boxCollision[j].h - 16:
                            enemyCollisionCheckDown = False
                        elif enemy[k].collision.y + enemy[k].collision.h <= boxCollision[j].y + 16:
                            enemyCollisionCheckUp = False
                if playerCollision.x+.5*playerCollision.w < enemy[k].collision.x+.5*enemy[k].collision.w and enemyCollisionCheckLeft == True:
                    enemy[k].pos[0] += 2
                elif playerCollision.x+.5*playerCollision.w > enemy[k].collision.x+.5*enemy[k].collision.w and enemyCollisionCheckRight == True:
                    enemy[k].pos[0] -= 2
                if playerCollision.y+.5*playerCollision.h > enemy[k].collision.y+.5*enemy[k].collision.h and enemyCollisionCheckUp == True:
                    enemy[k].pos[1] -= 2
                elif playerCollision.y+.5*playerCollision.h < enemy[k].collision.y+.5*enemy[k].collision.h and enemyCollisionCheckDown == True:
                    enemy[k].pos[1] += 2

                    
        for k in range(len(enemy)):
            if playerCollision.colliderect(enemy[k].collision) and enemy[k].alive is 1:


                os.chdir(currDir + '\\Music')
                music = pygame.mixer.Sound('Tomato_Battle.wav')
                os.chdir(currDir)

                pygame.mixer.Channel(0).play(music, -1)
                value = Battle.battle(enemy[k].stats)
                pygame.mixer.Channel(0).fadeout(1000)
                        
                if value is 3:
                    for j in range(0, 720, 24):
                        screen.blit(area[place], (-charX,-charY))
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720 - j, 520))
                        pygame.display.flip()
                        
                    death()
                else:
                    enemy[k].alive = value

                    for j in range(0, 720, 24):
                        screen.blit(area[place], (-charX,-charY))
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 720 - j, 520))
                        pygame.display.flip()

        
        

                        
        
        
        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    walkTimerStart = timer()
                    charSprite = 'CharacterFront1'
                elif event.key == pygame.K_UP:
                    walkTimerStart = timer()
                    charSprite = 'CharacterBack1'
                elif event.key == pygame.K_LEFT and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    walkTimerStart = timer()
                    charSprite = 'CharacterLeft1'
                elif event.key == pygame.K_RIGHT and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                    walkTimerStart = timer()
                    charSprite = 'CharacterRight1'
                elif event.key == pygame.K_x:
                    UI()
                elif event.key == pygame.K_d:
                    death()
                elif event.key == pygame.K_z:
                    save()
                    back()
                    return
                elif event.key == pygame.K_s:
                    save()

                    #--------------------Saving Animation----------------------#
                    GAME_FONT.render_to(screen, (600, 480), 'Saving.', (0, 0, 0))
                    pygame.display.flip()
                    time.sleep(.3)
                    GAME_FONT.render_to(screen, (600, 480), 'Saving..', (0, 0, 0))
                    pygame.display.flip()
                    time.sleep(.3)
                    GAME_FONT.render_to(screen, (600, 480), 'Saving...', (0, 0, 0))
                    pygame.display.flip()
                    time.sleep(.3)
                    screen.blit(area[place], (-charX,-charY))

                    for k in range(len(objects)):
                        if objects[k].active and not objects[k].hidden:
                            screen.blit(objectImg[objects[k].ID], (objects[k].pos[0] - charX, objects[k].pos[1] - charY))

                    for k in range(len(enemy)):
                        if enemy[k].alive == 1:
                            screen.blit(enemyImg[enemy[k].stats[5]],(enemy[k].initialPos[0] - charX - enemy[k].pos[0], enemy[k].initialPos[1] - charY - enemy[k].pos[1]))

                    screen.blit(i[charSprite],(charRX+charRXM,charRY+charRYM))
                    
                    GAME_FONT.render_to(screen, (600, 480), 'Saved', (0, 0, 0))
                    pygame.display.flip()
                    time.sleep(.3)
                    


if __name__ == "__main__":
    main()
