import re
import numpy as np


# file =  "PacmanPos, 9, 1, Ghost0Pos, 8, 7, Ghost1Pos, 9, 7, Ghost2Pos, 10, 7, Ghost3Pos, 11, 7, "
# #m = re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', file)
# m = re.findall(r'\d', file)
# print(m[0])

NUMBER_OF_GHOSTS = 4;
NUMBER_OF_GAMES = 150;
TRAINING_SESSIONS = 50;
FIELD_OF_VIEW = 9;
ARRAY_FIELD_SIZE = FIELD_OF_VIEW*2 +1
POSSIBLE_MOVEMENTS_IN_A_2DIMENSIONAL_WORLD = 4;

filename = "ghost_movements.csv"
file = open(filename, "r")
previous = ""

#ArrayWithGhostCounters = np.zeros(shape = (NUMBER_OF_GHOSTS,4))

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
                    for p in range(0, ARRAY_FIELD_SIZE):
                        for q in range(0,ARRAY_FIELD_SIZE):
                        
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

                #for i in range(1, NUMBER_OF_GHOSTS+1):
                        #xdistance = r[0] - r[i*2] + FIELD_OF_VIEW;
                        #ydistance = r[1] - r[1 + i*2] + FIELD_OF_VIEW;
                        #print(xdistance,'(',r[0], r[i*2],')', ydistance, '(', r[1], r[1 + i*2], ')')
                        #result = ((xdistance >= 0 and xdistance <= FIELD_OF_VIEW) and (ydistance >= 0 and ydistance <= FIELD_OF_VIEW)) and result
                        #print(result)
                        
                #print('off')
                if(result):
                    for i in range (1, NUMBER_OF_GHOSTS+1):
                        
                        locX = r[0] - r[i*2] + FIELD_OF_VIEW;
                        locY = r[1] - r[1 + i*2] + FIELD_OF_VIEW;
                        #print(locX,'(',r[0], r[i*2],')', locY, '(', r[1], r[1 + i*2], ')')
                        if(((locX < ARRAY_FIELD_SIZE and locX >= 0) and (locY < ARRAY_FIELD_SIZE and locY >= 0))):

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
allPositionsFromGhostsUp = np.zeros(shape=(ARRAY_FIELD_SIZE,ARRAY_FIELD_SIZE,4,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsDown = np.zeros(shape=(ARRAY_FIELD_SIZE,ARRAY_FIELD_SIZE, 4,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsLeft = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4,NUMBER_OF_GAMES - TRAINING_SESSIONS))
allPositionsFromGhostsRight = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4,NUMBER_OF_GAMES - TRAINING_SESSIONS))
print('counter', counter)
for i in range (0, NUMBER_OF_GAMES - TRAINING_SESSIONS):
    for j in range (0, NUMBER_OF_GHOSTS):
        for p in range(0, ARRAY_FIELD_SIZE):
            for q in range(0,ARRAY_FIELD_SIZE):
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
averagesGhostsUp = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4), dtype=float)
averagesGhostsDown = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4), dtype=float)
averagesGhostsLeft = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4), dtype=float)
averagesGhostsRight = np.zeros(shape=(ARRAY_FIELD_SIZE, ARRAY_FIELD_SIZE,4), dtype=float)
for j in range (0, NUMBER_OF_GHOSTS):
    for p in range(0, ARRAY_FIELD_SIZE):
            for q in range(0,ARRAY_FIELD_SIZE):
                print (j, 'up', np.sum(allPositionsFromGhostsUp[p][q][j]))
                print (j, 'down', np.sum(allPositionsFromGhostsDown[p][q][j]))
                print (j, 'left',np.sum(allPositionsFromGhostsLeft[p][q][j]))
                print (j, 'right', np.sum(allPositionsFromGhostsRight[p][q][j]))
                total = float(np.sum(allPositionsFromGhostsUp[p][q][j]) + np.sum(allPositionsFromGhostsDown[p][q][j])+np.sum(allPositionsFromGhostsLeft[p][q][j])+np.sum(allPositionsFromGhostsRight[p][q][j]))
                if(np.sum(allPositionsFromGhostsUp[p][q][j]) > 0):
                    averagesGhostsUp[p][q][j] = np.sum(allPositionsFromGhostsUp[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsDown[p][q][j]) > 0):
                    averagesGhostsDown[p][q][j] = np.sum(allPositionsFromGhostsDown[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsLeft[p][q][j]) > 0):
                    averagesGhostsLeft[p][q][j] = np.sum(allPositionsFromGhostsLeft[p][q][j])/float(total)
                if(np.sum(allPositionsFromGhostsRight[p][q][j]) > 0):
                    averagesGhostsRight[p][q][j] =  np.sum(allPositionsFromGhostsRight[p][q][j])/float(total)
                print('total', total)

print("finishedrecorded")

for j in range (0, NUMBER_OF_GHOSTS):
    for p in range(0, ARRAY_FIELD_SIZE):
            for q in range(0,ARRAY_FIELD_SIZE):
                print ('up', 'ghost', j, p, q, averagesGhostsUp[p][q][j])
                print ('down', 'ghost',j, p, q, averagesGhostsDown[p][q][j])
                print ('left', 'ghost',j, p, q, averagesGhostsLeft[p][q][j])
                print ('right', 'ghost',j, p, q, averagesGhostsRight[p][q][j])

#for j in range (0, NUMBER_OF_GHOSTS):
#	print("Ghost[%d] up: %f | down: %f | left: %f | right: %f" %(j, averagesGhostsUp[j], averagesGhostsDown[j],averagesGhostsLeft[j],averagesGhostsRight[j]))

#----------------------------------ENDS HERE






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




			


