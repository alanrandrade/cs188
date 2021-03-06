from __future__ import print_function
import re
import math
import numpy as np
import string

# file =  "PacmanPos, 9, 1, Ghost0Pos, 8, 7, Ghost1Pos, 9, 7, Ghost2Pos, 10, 7, Ghost3Pos, 11, 7, "
# #m = re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', file)
# m = re.findall(r'\d', file)
# print(m[0])

pacMap = np.array([
['%','%','%','%','%','%','%','%','%','%','%'],
['%','.','.','.','.',' ','.','.',' ','.','%'],
['%','.','%','%','.','%','.','%','%','.','%'],
['%','.','%','.','.','.','.','.','.','.','%'],
['%','.','%','%','.','%','.','%','%','.','%'],
['%','.','.','.','.','.','.','.','.',' ','%'],
['%','%','%','%','%','%','%','%','%','%','%']])

yMap = pacMap.shape[0]
xMap = pacMap.shape[1]

ARRAY_FIELD_SIZE_X = ((xMap-2)*2)-1
ARRAY_FIELD_SIZE_Y = ((yMap-2)*2)-1
#print(ARRAY_FIELD_SIZE_Y)


outcomeRules = ''

NUMBER_OF_GHOSTS = 1;
NUMBER_OF_GAMES = 2010;
TRAINING_SESSIONS = 10;
POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD = 4;

#filename = "ghost_movements_micro - Copy.csv"
filename = "ghost_movements.csv"
file = open(filename, "r")
previous = ""

NEWArrayWithGhostCounters = np.zeros(shape=(ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

PercentagesOfGames = np.zeros(shape=(NUMBER_OF_GAMES - TRAINING_SESSIONS, ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

counter = 0
training_counter = 0;


for line in file:
    if(line != previous):

        m = re.findall(r'\d+(?:,\d+)?', line)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', line)
        r = re.findall(r'\d+(?:,\d+)?', previous)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', previous)
        m = map(int, m)
        r = map(int, r)
        if("End of game" in line):
            training_counter = training_counter + 1
        
            if(training_counter > TRAINING_SESSIONS):
                
                for p in range(0, ARRAY_FIELD_SIZE_X):
                    for q in range(0,ARRAY_FIELD_SIZE_Y):
                        
                        total = NEWArrayWithGhostCounters[p][q][0][0] + NEWArrayWithGhostCounters[p][q][0][1] + NEWArrayWithGhostCounters[p][q][0][2] + NEWArrayWithGhostCounters[p][q][0][3]
                        PercentagesOfGames[counter][p][q][0] = NEWArrayWithGhostCounters[p][q][0] 

                        for k in range (0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
                            if(NEWArrayWithGhostCounters[p][q][0][k] > 0):
                                PercentagesOfGames[counter][p][q][0][k] = NEWArrayWithGhostCounters[p][q][0][k]/float(total)
                    
                            NEWArrayWithGhostCounters[p][q][0][k] = 0;
                        
                counter = counter +1

        #print ("previous %s \n current %s" % (previous, line))
        if(training_counter >= TRAINING_SESSIONS):
            if((len(r) and len(m) >0 and len(m) == len(r)) and (len(m) >= 0 )):

                result = True;
                for i in range(0, len(m)-1):
                        result = ((m[i] -r[i] >= -1) and (m[i] -r[i]<= 1) ) and result

                if(result):
                    for i in range (1, NUMBER_OF_GHOSTS+1):
                        
                        locX = ((r[i*2] - r[0]) + (xMap - 3));
                        #Y orientation is counted backwards, therefore it needs adjustments
                        #locY = ((r[1 + i*2] - r[1]) + (yMap - 3));
                        locY =  ((((yMap-1)-r[1 + i*2]) - ((yMap-1)-r[1])) + (yMap - 3));
                        
                        if(((locX < ARRAY_FIELD_SIZE_X and locX >= 0) and (locY < ARRAY_FIELD_SIZE_Y and locY >= 0))):
                            
                            if(m[i*2] != r[i*2]):
                                if((m[i*2] - r[i*2]) == 1):

                                    #0 is right
                                    NEWArrayWithGhostCounters[locX][locY][i-1][0] = NEWArrayWithGhostCounters[locX][locY][i-1][0] + 1
                                elif((m[i*2] - r[i*2]) == -1):
                                    
                                    #1 is left
                                    NEWArrayWithGhostCounters[locX][locY][i-1][1] = NEWArrayWithGhostCounters[locX][locY][i-1][1] + 1
                        
                            if(m[i*2 -1] != r[i*2 -1]):
                                if((m[i*2 -1] - r[i*2 -1]) == 1):
                                    #2 is up
                                    NEWArrayWithGhostCounters[locX][locY][i-1][2] = NEWArrayWithGhostCounters[locX][locY][i-1][2] + 1
                                elif((m[i*2 -1] - r[i*2 -1]) == -1):
                                    #3 is down
                                    NEWArrayWithGhostCounters[locX][locY][i-1][3] = NEWArrayWithGhostCounters[locX][locY][i-1][3] + 1

    previous = line;
	
   	#print line,
allPositionsFromGhostsUp = np.zeros(shape=(ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y,NUMBER_OF_GHOSTS,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsDown = np.zeros(shape=(ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsLeft = np.zeros(shape=(ARRAY_FIELD_SIZE_X, ARRAY_FIELD_SIZE_Y,NUMBER_OF_GHOSTS,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsRight = np.zeros(shape=(ARRAY_FIELD_SIZE_X, ARRAY_FIELD_SIZE_Y,NUMBER_OF_GHOSTS,NUMBER_OF_GAMES - TRAINING_SESSIONS))
#print('counter', counter)
for i in range (0, NUMBER_OF_GAMES - TRAINING_SESSIONS):
    for j in range (0, NUMBER_OF_GHOSTS):
        for p in range(0, ARRAY_FIELD_SIZE_X):
            for q in range(0,ARRAY_FIELD_SIZE_Y):
                allPositionsFromGhostsUp[p][q][j][i] = PercentagesOfGames[i][p][q][j][2]
                allPositionsFromGhostsDown[p][q][j][i] = PercentagesOfGames[i][p][q][j][3]
                allPositionsFromGhostsLeft[p][q][j][i] = PercentagesOfGames[i][p][q][j][1]
                allPositionsFromGhostsRight[p][q][j][i] = PercentagesOfGames[i][p][q][j][0]

total = 0.0;
averagesGhosts = np.zeros(shape=(POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD, ARRAY_FIELD_SIZE_X, ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS), dtype=float)
for j in range (0, NUMBER_OF_GHOSTS):
    for p in range(0, ARRAY_FIELD_SIZE_X):
            for q in range(0,ARRAY_FIELD_SIZE_Y):
                total = float(np.sum(allPositionsFromGhostsUp[p][q][j]) + np.sum(allPositionsFromGhostsDown[p][q][j])+np.sum(allPositionsFromGhostsLeft[p][q][j])+np.sum(allPositionsFromGhostsRight[p][q][j]))
                if(np.sum(allPositionsFromGhostsUp[p][q][j]) > 0):
                    averagesGhosts[0][p][q][j] = np.sum(allPositionsFromGhostsUp[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsDown[p][q][j])   > 0):
                    averagesGhosts[1][p][q][j] = np.sum(allPositionsFromGhostsDown[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsLeft[p][q][j]) > 0):
                    averagesGhosts[2][p][q][j] = np.sum(allPositionsFromGhostsLeft[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsRight[p][q][j]) > 0):
                    averagesGhosts[3][p][q][j] =  np.sum(allPositionsFromGhostsRight[p][q][j])/float(total)

def getIdPartly(currentValueX, currentValueY):
    result = ''
    if(currentValueX < 10):
        result = '0'+ str(currentValueX)
    else:
        result = str(currentValueX)
    if(currentValueY < 10):
        result = result + '0' + str(currentValueY)
    else:
        result = result + str(currentValueY)
    return result

def getId(ghost1x, ghost1y, ghost2x, ghost2y):
    full_string = getIdPartly(ghost1x, ghost1y) + getIdPartly(ghost2x, ghost2y)
    busy = True
    while (busy):
        if (len(full_string) > 1):
            if (full_string[0] == '0'):
                full_string = full_string[1:]
            else:
                busy = False
        else: 
            busy = False
    return full_string

def getMovement(pacmanAction, ghostAction, ghostNumber, ghostx, ghosty):
    #print(str(getSign((ghostx-(ARRAY_FIELD_SIZE_X/2)))), str(getSign((ghosty-(ARRAY_FIELD_SIZE_Y/2)))) , ghostAction)
    result = ''
    if(ghostNumber == 0):
        if (pacmanAction == 0):  # UP
            if(str(getSign((ghosty-(ARRAY_FIELD_SIZE_Y/2)))) == ' -1' 
                and str(getSign((ghostx-(ARRAY_FIELD_SIZE_X/2)))) == '' and ghostAction == 1):
                result += '(yP\' = yP) & '
            else:
                result += '(yP\' = yP-1) & '
        elif (pacmanAction == 1): #DOWN
            if(str(getSign((ghosty-(ARRAY_FIELD_SIZE_Y/2)))) == ' + 1' 
                and str(getSign((ghostx-(ARRAY_FIELD_SIZE_X/2)))) == '' 
                and ghostAction == 0):
                result += '(yP\' = yP) & '
            else:
                result += '(yP\' = yP+1) & '

        elif (pacmanAction == 2): #LEFT
            if(str(getSign((ghosty-(ARRAY_FIELD_SIZE_Y/2)))) == '' 
                and str(getSign((ghostx-(ARRAY_FIELD_SIZE_X/2)))) == ' -1' 
                and ghostAction == 3):
                result += '(xP\' = xP) & '
            else:
                result += '(xP\' = xP-1) & '
        elif (pacmanAction == 3): #RIGHT
            if(str(getSign((ghosty-(ARRAY_FIELD_SIZE_Y/2)))) == '' 
                and str(getSign((ghostx-(ARRAY_FIELD_SIZE_X/2)))) == ' + 1' 
                and ghostAction == 2):
                result += '(xP\' = xP) & '
            else:
                result += '(xP\' = xP+1) & '
   
    if(ghostAction == 0): #UP
        result += '(yG'+ str(ghostNumber)+'\' = yG'+str(ghostNumber)+'-1) & '  
    elif(ghostAction == 1): #down
        result += '(yG'+ str(ghostNumber)+'\' = yG'+str(ghostNumber)+'+1) & '   
    elif(ghostAction == 2): #left
        result += '(xG'+ str(ghostNumber)+'\' = xG'+str(ghostNumber)+'-1) & '
    elif(ghostAction == 3): #right
        result += '(xG'+ str(ghostNumber)+'\' = xG'+str(ghostNumber)+'+1) & '

    return result[:-3]


def getAction(act):
    if(act == 0):
        return 'up'        
    elif(act == 1):
        return 'down'
    elif(act == 2):
        return 'left'
    elif(act == 3):
        return 'right'
        
print('mdp')
print('')
print('const xSize ='+ str(xMap)+';')
print('const ySize ='+ str(yMap)+';')
print('')
print('module pacman')
print('')
print('\txG0 : [0..xSize] init 7; // x position of Ghost0')
print('\tyG0 : [0..ySize] init 1; // y position of Ghost0')
print('\txP : [0..xSize] init 2; // x position of Pacman')
print('\tyP : [0..ySize] init 1; // y position of Pacman')
print('')

def getSign(i):
	if(i > 0):
		return ' + '+ str(i)
	elif(i < 0):
		return ' ' + str(i)
	else:
		return ''
    
def rond(i):
    modded = (1000000 * i) % 1;
    if(modded < 0.5):
        return math.floor(i * 1000000) / 1000000;
    elif(modded >= 0.5):
        return math.ceil(i * 1000000) / 1000000;



for ghost1X in range(0, ARRAY_FIELD_SIZE_X):
    for ghost1Y in range(0, ARRAY_FIELD_SIZE_Y):
        for action in range(0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
            minX = ''
            maxX = ''
            minY = ''
            maxY = ''
        
            first_part = '[' + getAction(action) + '] '
            if(getAction(action) == 'left'):
                    minX = 'xP > 1 &'
            elif(getAction(action) == 'right'):
                    maxX = 'xP < '+str(xMap-2) + ' & '
            elif(getAction(action) == 'up'):
                    minX = 'yP > 1 &'
            elif(getAction(action) == 'down'):
                    maxX = 'yP < '+str(yMap-2) + ' & '
            first_part += '('+minX+maxX+minY+maxY+' xG0= (xP' + str(getSign((ghost1X-(ARRAY_FIELD_SIZE_X/2)))) +') & yG0= (yP'+ str(getSign((ghost1Y-(ARRAY_FIELD_SIZE_Y/2)))) +')'
            first_part += ' & (xP > 0) & (xP < ' + str(xMap) + ') & (yP > 0) & (yP < ' + str(yMap) + ')'
            first_part += ' & (xG0 > 0) & (xG0 < ' + str(xMap) + ') & (yG0 > 0) & (yG0 < ' + str(yMap) + ')'
            first_part_end = ") -> "
            line = "";
            for g1 in range(0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
                prob = str(rond(float(averagesGhosts[g1][ghost1X][ghost1Y][0])))
                if (prob != "0.0"):
                    line += prob +': ' + str(getMovement(action, g1, 0, ghost1X, ghost1Y))
                    line += " + "
            if (len(line) > 0):
                print(first_part, end='')
                print(first_part_end, end='')
                print(line[:-3], end='')
                print(";")




print("")
print("endmodule")
			
