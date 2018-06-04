from __future__ import print_function
import re
import numpy as np



# file =  "PacmanPos, 9, 1, Ghost0Pos, 8, 7, Ghost1Pos, 9, 7, Ghost2Pos, 10, 7, Ghost3Pos, 11, 7, "
# #m = re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', file)
# m = re.findall(r'\d', file)
# print(m[0])

pacMap = np.array(

['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%'],
['%','.','.','.','.','.','.','%',' ',' ',' ',' ','%','.','.','.','.','.','.','%'],
['%','.','%','%','.','.','.','%','%',' ',' ','%','%','.','.','.','%','%','.','%'],
['%','.','%','.','.','%','.','.','.','.','.','.','.','.','%','.','.','%','.','%'],
['%','.','%','%','.','%','.','%','%','%','%','%','%','.','%','.','%','%','.','%'],
['%','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.','%'],
['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%'])

yMap = pacMac.shape[0]
xMap = pacMac.shape[1]

ARRAY_FIELD_SIZE_X = ((xMap-2)*2)-1
ARRAY_FIELD_SIZE_Y = ((yMap-2)*2)-1


NUM_GHOSTS = 2

outcomeRules = ''

NUMBER_OF_GHOSTS = 2;
NUMBER_OF_GAMES = 500;
TRAINING_SESSIONS = 480;
POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD = 4;

filename = "ghost_movements.csv"
file = open(filename, "r")
previous = ""

#ArrayWithGhostCounters = np.zeros(shape = (NUMBER_OF_GHOSTS,4))

NEWArrayWithGhostCounters = np.zeros(shape=(ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

PercentagesOfGames = np.zeros(shape=(NUMBER_OF_GAMES - TRAINING_SESSIONS, ARRAY_FIELD_SIZE_X,ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

counter = 0
training_counter = 0;


for line in file:
    if(line != previous):

		# if(line == "End of game"):
		# 	/float(upG0 + downG0 + leftG0 + rightG0)
		# 	/float(upG1 + downG1 + leftG1 + rightG1)
		# 	/float(upG2 + downG2 + leftG2 + rightG2)
		# 	/float(upG3 + downG3 + leftG3 + rightG3)


        m = re.findall(r'\d+(?:,\d+)?', line)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', line)
        r = re.findall(r'\d+(?:,\d+)?', previous)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', previous)
        m = map(int, m)
        r = map(int, r)
        if("End of game" in line):
            training_counter = training_counter + 1
        
            if(training_counter > TRAINING_SESSIONS):
                for j in range (0, NUMBER_OF_GHOSTS):
                    for p in range(0, ARRAY_FIELD_SIZE_X):
                        for q in range(0,ARRAY_FIELD_SIZE_Y):
                        
                            total = NEWArrayWithGhostCounters[p][q][j][0] + NEWArrayWithGhostCounters[p][q][j][1] + NEWArrayWithGhostCounters[p][q][j][2] + NEWArrayWithGhostCounters[p][q][j][3]

                            #print('total', training_counter, p, q, j, total, NEWArrayWithGhostCounters[p][q][j][0], NEWArrayWithGhostCounters[p][q][j][0]/float(total))
                            
                            PercentagesOfGames[counter][p][q][j] = NEWArrayWithGhostCounters[p][q][j] 
                            #PercentagesOfGames[counter][j] = ArrayWithGhostCounters[j]
                            for k in range (0, 4):
                                if(NEWArrayWithGhostCounters[p][q][j][k] > 0):
                                    PercentagesOfGames[counter][p][q][j][k] = NEWArrayWithGhostCounters[p][q][j][k]/float(total)
                                #print(PercentagesOfGames[counter][p][q][j][k])
                                #PercentagesOfGames[counter][j][k] = ArrayWithGhostCounters[j][k]/float(total)
                                
                                
                                #print('here')

                                NEWArrayWithGhostCounters[p][q][j][k] = 0;
                            #for k in range (0, 4):
                                #print('first',PercentagesOfGames[counter][p][q][j][k], NEWArrayWithGhostCounters[p][q][j][k]/float(total))

                counter = counter +1
            #training_counter = training_counter + 1
            #print(training_counter)

        #print ("previous %s \n current %s" % (previous, line))
        if(training_counter > TRAINING_SESSIONS):
            if((len(r) and len(m) >0 and len(m) == len(r)) and (len(m) >= 0 )):

                result = True;
                for i in range(0, len(m)-1):
                        result = ((m[i] -r[i] >= -1) and (m[i] -r[i]<= 1) ) and result

                if(result):
                    for i in range (1, NUMBER_OF_GHOSTS+1):
                        
                        locX = r[0] - r[i*2] + xMap;
                        locY = r[1] - r[1 + i*2] + yMap;
                        #print(locX,'(',r[0], r[i*2],')', locY, '(', r[1], r[1 + i*2], ')')
                        if(((locX < ARRAY_FIELD_SIZE_X and locX >= 0) and (locY < ARRAY_FIELD_SIZE_Y and locY >= 0))):

                            #print(locX,'(',r[0], r[i*2],')', locY, '(', r[1], r[1 + i*2], ')')
                            if(m[i*2] != r[i*2]):
                                if((m[i*2] - r[i*2]) == 1):

                                    #0 is right
                                    NEWArrayWithGhostCounters[locX][locY][i-1][0] = NEWArrayWithGhostCounters[locX][locY][i-1][0] +1
                                    #print('right',NEWArrayWithGhostCounters[locX][locY][i-1][0])
                                    #rightG0 = rightG0 + 1
                                elif((m[i*2] - r[i*2]) == -1):
                                    #1 is left

                                    NEWArrayWithGhostCounters[locX][locY][i-1][1] = NEWArrayWithGhostCounters[locX][locY][i-1][1] +1
                                    #print('left',NEWArrayWithGhostCounters[locX][locY][i-1][1])
                                    #leftG0 = leftG0 + 1

                            if(m[i*2 -1] != r[i*2 -1]):
                                if((m[i*2 -1] - r[i*2 -1]) == 1):
                                    #2 is up
                                    NEWArrayWithGhostCounters[locX][locY][i-1][2] = NEWArrayWithGhostCounters[locX][locY][i-1][2] +1
                                    #print('up',NEWArrayWithGhostCounters[locX][locY][i-1][2])
                                    #upG0 = upG0 + 1
                                elif((m[i*2 -1] - r[i*2 -1]) == -1):
                                    #3 is down
                                    NEWArrayWithGhostCounters[locX][locY][i-1][3] = NEWArrayWithGhostCounters[locX][locY][i-1][3] +1
                                    #print('down',NEWArrayWithGhostCounters[locX][locY][i-1][3])
                                    #downG0 = downG0 + 1

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
                allPositionsFromGhostsLeft[p][q][j][i] = PercentagesOfGames[i][p][q][j][0]
                allPositionsFromGhostsRight[p][q][j][i] = PercentagesOfGames[i][p][q][j][1]
                

'''print("recorded")
for i in range (0, NUMBER_OF_GAMES - TRAINING_SESSIONS):
    for j in range (0, NUMBER_OF_GHOSTS):
        for p in range(0, ARRAY_FIELD_SIZE):
            for q in range(0,ARRAY_FIELD_SIZE):
                #if allPositionsFromGhostsUp[p][q][j][i] > 0 :
                print (i, j, allPositionsFromGhostsUp[p][q][j][i])
                print (i, j, allPositionsFromGhostsDown[p][q][j][i])
                print (i, j, allPositionsFromGhostsLeft[p][q][j][i])
                print (i, j, allPositionsFromGhostsRight[p][q][j][i])
'''

total = 0.0;
averagesGhosts = np.zeros(shape=(POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD, ARRAY_FIELD_SIZE_X, ARRAY_FIELD_SIZE_Y, NUMBER_OF_GHOSTS), dtype=float)
for j in range (0, NUMBER_OF_GHOSTS):
    for p in range(0, ARRAY_FIELD_SIZE_X):
            for q in range(0,ARRAY_FIELD_SIZE_Y):
                # print (j, 'up', np.sum(allPositionsFromGhostsUp[p][q][j]))
                # print (j, 'down', np.sum(allPositionsFromGhostsDown[p][q][j]))
                # print (j, 'left',np.sum(allPositionsFromGhostsLeft[p][q][j]))
                # print (j, 'right', np.sum(allPositionsFromGhostsRight[p][q][j]))
                total = float(np.sum(allPositionsFromGhostsUp[p][q][j]) + np.sum(allPositionsFromGhostsDown[p][q][j])+np.sum(allPositionsFromGhostsLeft[p][q][j])+np.sum(allPositionsFromGhostsRight[p][q][j]))
                if(np.sum(allPositionsFromGhostsUp[p][q][j]) > 0):
                    averagesGhosts[0][p][q][j] = np.sum(allPositionsFromGhostsUp[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsDown[p][q][j])   > 0):
                    averagesGhosts[1][p][q][j] = np.sum(allPositionsFromGhostsDown[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsLeft[p][q][j]) > 0):
                    averagesGhosts[2][p][q][j] = np.sum(allPositionsFromGhostsLeft[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsRight[p][q][j]) > 0):
                    averagesGhosts[3][p][q][j] =  np.sum(allPositionsFromGhostsRight[p][q][j])/float(total)
                # print('total', total)

# print("finishedrecorded")

for j in range (0, NUMBER_OF_GHOSTS):
    for p in range(0, ARRAY_FIELD_SIZE_X):
            for q in range(0,ARRAY_FIELD_SIZE_Y):
                print ('up', 'ghost', j, p - xMap, q- yMap, averagesGhosts[0][p][q][j])
                print ('down', 'ghost',j, p- xMap, q- yMap, averagesGhosts[1][p][q][j])
                print ('left', 'ghost',j, p- xMap, q- yMap, averagesGhosts[2][p][q][j])
                print ('right', 'ghost',j, p- xMap, q- yMap, averagesGhosts[3][p][q][j])


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

def getGhostMovement(pacmanAction, ghostAction, ghostx, ghosty):
    if (pacmanAction == 0):                 # UP
        if(ghostAction == 0): #up
            return ghostx, ghosty
        if(ghostAction == 1): #down
            return ghostx, (ghosty-2)
        if(ghostAction == 2): #left
            return (ghostx -1), (ghosty-1)
        if(ghostAction == 3): #right
            return (ghostx + 1), (ghosty-1)
    elif (pacmanAction == 1):               #DOWN
        if(ghostAction == 0): #up
            return ghostx, (ghosty + 2)
        if(ghostAction == 1): #down
            return ghostx, ghosty
        if(ghostAction == 2): #left
            return (ghostx -1), (ghosty + 1)
        if(ghostAction == 3): #right
            return (ghostx + 1), (ghosty + 1)
    elif (pacmanAction == 2):               #LEFT
        if(ghostAction == 0): #up
            return (ghostx + 1), (ghosty + 1)
        if(ghostAction == 1): #down
            return (ghostx + 1), (ghosty - 1)
        if(ghostAction == 2): #left
            return ghostx, ghosty
        if(ghostAction == 3): #right
            return (ghostx + 2), ghosty
    elif (pacmanAction == 3):               #RIGHT
        if(ghostAction == 0): #up
            return (ghostx - 1), (ghosty + 1)
        if(ghostAction == 1): #down
            return (ghostx - 1), (ghosty - 1)
        if(ghostAction == 2): #left
            return (ghostx - 2), ghosty
        if(ghostAction == 3): #right
            return ghostx, ghosty

        
        
print('mdp')
print('')
print('const xSize ='+ xMap+';')
print('const ySize ='+ yMap+';')
print('')
print('module pacman')
print('')
print('\txG0 : [0..xSize] init 8; // x position of Ghost')
print('\tyG0 : [0..ySize] init 1; // y position of Ghost')
print('\txG1 : [0..xSize] init 11; // x position of Ghost')
print('\tyG1 : [0..ySize] init 1; // y position of Ghost')
print('')



for ghost1X in range(0, ARRAY_FIELD_SIZE_X):
    for ghost1Y in range(0, ARRAY_FIELD_SIZE_Y):
        for ghost2X in range(0, ARRAY_FIELD_SIZE_X):
            for ghost2Y in range(0, ARRAY_FIELD_SIZE_Y):
                for action in range(0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
                    first_part = '[' + str(action) + '] s='
                    first_part += getId(ghost1X, ghost1Y, ghost2X, ghost2Y)
                    first_part += " -> "
                    line = "";
                    for g1 in range(0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
                        for g2 in range(0, POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD):
                            prob = str(averagesGhosts[g1][ghost1X][ghost1Y][0] * averagesGhosts[g2][ghost1X][ghost1Y][1])
                            if (prob != "0.0"):
                                line += prob + " (s'="
                                g1resultX, g1resultY  = getGhostMovement(action, g1, ghost1X, ghost1Y)
                                g2resultX, g2resultY = getGhostMovement(action, g2, ghost2X, ghost2Y)
                                line += getId(g1resultX, g1resultY, g2resultX, g2resultY)
                                line += ")"
                                line += " + "
                    if (len(line) > 0):
                        print(first_part, end='')
                        print(line[:-3], end='')
                        print(";")

print("")
print("endmodule")
			



for g in range(0, NUM_GHOSTS):
    for x in range(0, xMap):
        for y in range(0, yMap):
            if(pacMap[x][y] == ' ' || pacMap[x][y] == '.'):
                #left
                if(pacMap[x-1][y] != '%'):
                    outcomeRules += '[g'+str(g)+ '] (y ='+str(y) + '& x'+ str(x)+') -> 1:(x\' = x-1)' +'\n'
                #right    
                if(pacMap[x+1][y] != '%'):
                    outcomeRules += '[g'+str(g)+ '] (y ='+str(y) + '& x'+ str(x)+') -> 1:(x\' = x+1)' +'\n'
                #up
                if(pacMap[x][y-1] != '%'):
                    outcomeRules += '[g'+str(g)+ '] (y ='+str(y) + '& x'+ str(x)+') -> 1:(y\' = y-1)' +'\n'

                if(pacMap[x][y+1] != '%'):
                    outcomeRules += '[g'+str(g)+ '] (y ='+str(y) + '& x'+ str(x)+') -> 1:(y\' = y+1)' +'\n'