import re
import numpy as np


# file =  "PacmanPos, 9, 1, Ghost0Pos, 8, 7, Ghost1Pos, 9, 7, Ghost2Pos, 10, 7, Ghost3Pos, 11, 7, "
# #m = re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', file)
# m = re.findall(r'\d', file)
# print(m[0])

NUMBER_OF_GHOSTS = 4;
NUMBER_OF_GAMES = 201;
TRAINING_SESSIONS = 99;
FIELD_OF_VIEW = 9;
ARRAY_FIELD_SIZE = FIELD_OF_VIEW*2 +1
POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD = 4;

filename = "ghost_movements.csv"
file = open(filename, "r")
previous = ""

ArrayWithGhostCounters = np.zeros(shape = (NUMBER_OF_GHOSTS,4))

NEWArrayWithGhostCounters = np.zeros(shape=(ARRAY_FIELD_SIZE,ARRAY_FIELD_SIZE, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

PercentagesOfGames = np.zeros(shape=(NUMBER_OF_GAMES - TRAINING_SESSIONS, ARRAY_FIELD_SIZE,ARRAY_FIELD_SIZE, NUMBER_OF_GHOSTS,POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD))

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
                    total = ArrayWithGhostCounters[j][0] + ArrayWithGhostCounters[j][1] + ArrayWithGhostCounters[j][2] + ArrayWithGhostCounters[j][3]
                    
                    PercentagesOfGames[counter][j] = ArrayWithGhostCounters[j]
                    for k in range (0, 4):
                        PercentagesOfGames[counter][j][k] = ArrayWithGhostCounters[j][k]/float(total)
                        print(PercentagesOfGames[counter][j][k])
                        
                        #print('here')

                        ArrayWithGhostCounters[j][k] = 0;
                    for k in range (0, 4):
                        print('first',PercentagesOfGames[counter][j][k], ArrayWithGhostCounters[j][k]/float(total))

                counter = counter + 1

        #print ("previous %s \n current %s" % (previous, line))
        if(training_counter > TRAINING_SESSIONS):
            if((len(r) and len(m) >0 and len(m) == len(r)) and (len(m) >= 0 )):

                result = True;
                for i in range(0, len(m)-1):
                        result = ((m[i] -r[i] >= -1) and (m[i] -r[i]<= 1) ) and result
                        
                if(result):
                    for i in range (1, NUMBER_OF_GHOSTS+1):
                        
                        locX = r[0] - r[i*2] + FIELD_OF_VIEW;
                        locY = r[1] - r[1 + i*2] + FIELD_OF_VIEW;
                        
                        if(m[i*2] != r[i*2]):
                            if((m[i*2] - r[i*2]) == 1):
                                #0 is right
                                ArrayWithGhostCounters[locX][locY][i][0] = ArrayWithGhostCounters[locX][locY][i][0] +1
                                #rightG0 = rightG0 + 1
                            elif((m[i*2] - r[i*2]) == -1):
                                #1 is left
                                ArrayWithGhostCounters[locX][locY][i][1] = ArrayWithGhostCounters[locX][locY][i][1] +1
                                #leftG0 = leftG0 + 1

                        if(m[i*2 -1] != r[i*2 -1]):
                            if((m[i*2 -1] - r[i*2 -1]) == 1):
                                #2 is up
                                ArrayWithGhostCounters[locX][locY][i][2] = ArrayWithGhostCounters[locX][locY][i][2] +1
                                #upG0 = upG0 + 1
                            elif((m[i*2 -1] - r[i*2 -1]) == -1):
                                #3 is down
                                ArrayWithGhostCounters[locX][locY][i][3] = ArrayWithGhostCounters[locX][locY][i][3] +1
                                #downG0 = downG0 + 1

    previous = line;
	
   	#print line,
allPositionsFromGhostsUp = np.zeros(shape=(4,211))
allPositionsFromGhostsDown = np.zeros(shape=(4,211))
allPositionsFromGhostsLeft = np.zeros(shape=(4,211))
allPositionsFromGhostsRight = np.zeros(shape=(4,211))
print('counter', counter)
for i in range (0, NUMBER_OF_GAMES):
    for j in range (0, NUMBER_OF_GHOSTS):
		# for k in range (0, 4):
		# 	print(i, j, k, PercentagesOfGames[i][j][k])
        allPositionsFromGhostsUp[j][i] = PercentagesOfGames[i][j][2]
        allPositionsFromGhostsDown[j][i] = PercentagesOfGames[i][j][3]
        allPositionsFromGhostsLeft[j][i] = PercentagesOfGames[i][j][0]
        allPositionsFromGhostsRight[j][i] = PercentagesOfGames[i][j][1]
#fcounter = float(counter);

print("recorded")
for i in range (0, NUMBER_OF_GAMES):
    for j in range (0, NUMBER_OF_GHOSTS):
        print (i, j, allPositionsFromGhostsUp[j][i])
        print (i, j, allPositionsFromGhostsDown[j][i])
        print (i, j, allPositionsFromGhostsLeft[j][i])
        print (i, j, allPositionsFromGhostsRight[j][i])


total = 0.0;
averagesGhostsUp = np.zeros(4, dtype=float)
averagesGhostsDown = np.zeros(4, dtype=float)
averagesGhostsLeft = np.zeros(4, dtype=float)
averagesGhostsRight = np.zeros(4, dtype=float)
for j in range (0, NUMBER_OF_GHOSTS):
    print (j, 'up', np.sum(allPositionsFromGhostsUp[j]))
    print (j, 'down', np.sum(allPositionsFromGhostsDown[j]))
    print (j, 'left',np.sum(allPositionsFromGhostsLeft[j]))
    print (j, 'right', np.sum(allPositionsFromGhostsRight[j]))
    total = float(np.sum(allPositionsFromGhostsUp[j]) + np.sum(allPositionsFromGhostsDown[j])+np.sum(allPositionsFromGhostsLeft[j])+np.sum(allPositionsFromGhostsRight[j]))
    averagesGhostsUp[j] = np.sum(allPositionsFromGhostsUp[j])/float(total)
    averagesGhostsDown[j] = np.sum(allPositionsFromGhostsDown[j])/float(total)
    averagesGhostsLeft[j] = np.sum(allPositionsFromGhostsLeft[j])/float(total)
    averagesGhostsRight[j] =  np.sum(allPositionsFromGhostsRight[j])/float(total)
    print('total', total)

print("finishedrecorded")

for j in range (0, NUMBER_OF_GHOSTS):
    print (j, averagesGhostsUp[j])
    print (j, averagesGhostsDown[j])
    print (j, averagesGhostsLeft[j])
    print (j, averagesGhostsRight[j])

for j in range (0, NUMBER_OF_GHOSTS):
	print("Ghost[%d] up: %f | down: %f | left: %f | right: %f" %(j, averagesGhostsUp[j], averagesGhostsDown[j],averagesGhostsLeft[j],averagesGhostsRight[j]))

#print("shape of allPositionsFromGhostOneUp", allPositionsFromGhostOneUp.shape)


# for i in range (0, NUMBER_OF_GHOSTS):
# 	total = float(ArrayWithGhostCounters[i][0] + ArrayWithGhostCounters[i][1] + ArrayWithGhostCounters[i][2] + ArrayWithGhostCounters[i][3])
# 	print("Ghost %d up %f down: %f left: %f right: %f\n" %(i,(ArrayWithGhostCounters[i][2]/total),(ArrayWithGhostCounters[i][3]/total),(ArrayWithGhostCounters[i][0]/total), (ArrayWithGhostCounters[i][1]/total) ))
# 	print("Ghost %d up %d down: %d left: %d right: %d\n" %(i,(ArrayWithGhostCounters[i][2]),(ArrayWithGhostCounters[i][3]),(ArrayWithGhostCounters[i][0]), (ArrayWithGhostCounters[i][1]) ))



# print('here')
# print(upPercentage[0], upPercentage[1], upPercentage[2], upPercentage[3])

# #PercentagesOfGames[N_GAME][GHOST][PERCENTAGES]

# for j in range (0, NUMBER_OF_GHOSTS):
# 	for i in range (0, NUMBER_OF_GAMES):
# 		#print('this',j, i, upPercentage[j], PercentagesOfGames[i][j][2])
# 		upPercentage[j][i] =  float(PercentagesOfGames[i][j][2])
# 		downPercentage[j][i] = float(PercentagesOfGames[i][j][3])
# 		leftPercentage[j][i] =  float(PercentagesOfGames[i][j][0])
# 		rightPercentage[j][i] = float(PercentagesOfGames[i][j][1])
		# print("\n")
		# print(i, j, PercentagesOfGames[i][j][2] ,upPercentage[j][i])
		# print('\n')
		# print(PercentagesOfGames[i][j][3],downPercentage[j][i])
		# print('\n')
		# print(PercentagesOfGames[i][j][0], leftPercentage[j][i])
		# print('\n')
		# print(PercentagesOfGames[i][j][1], rightPercentage[j][i])
		# print('here')
		#print(upPercentage[0], upPercentage[1], upPercentage[2], upPercentage[3])
		#print("%d up %f down %f left %f right %f" % (j, upPercentage[j], downPercentage[j], leftPercentage[j], rightPercentage[j]))
		#print(np.sum(PercentagesOfGames[i][j][k], axis = 0))
	#print("%d up %f down %f left %f right %f" % (j, upPercentage[j], downPercentage[j], leftPercentage[j], rightPercentage[j]))


# print('shape of upPercentage ', upPercentage.shape)

# for i in range (0, NUMBER_OF_GAMES):
# 	for J in range (0, NUMBER_OF_GHOSTS):
# 		print('upPercentage[%d]: %f' % (i, (PercentagesOfGames[i][j][2])))
# 		print('downPercentage[%d]: %f' %(i, (PercentagesOfGames[i][j][3])))
# 		print('leftPercentage[%d]: %f' %(i, (PercentagesOfGames[i][j][0])))
# 		print('rightPercentage[%d]: %f' %(i, (PercentagesOfGames[i][j][1])))



# average = np.zeros(shape = (4,4) )
# for i in range (0, NUMBER_OF_GHOSTS):
# 	mysum = np.sum(upPercentage[i]) + np.sum(downPercentage[i]) + np.sum(leftPercentage[i]) + np.sum(rightPercentage[i]);

# 	average[i][0] = np.sum(upPercentage[i])/ float(mysum)
# 	average[i][1] = np.sum(downPercentage[i])/float(mysum)
# 	average[i][2] = np.sum(downPercentage[i])/float(mysum)
# 	average[i][3] = np.sum(downPercentage[i])/float(mysum)


# for i in range (0, NUMBER_OF_GHOSTS):
# 	print("Ghost %d up %f down: %f left: %f right: %f\n" %(i,average[i][0],average[i][1],average[i][2], average[i][3] ))




			


