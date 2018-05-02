import re


# file =  "PacmanPos, 9, 1, Ghost0Pos, 8, 7, Ghost1Pos, 9, 7, Ghost2Pos, 10, 7, Ghost3Pos, 11, 7, "
# #m = re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', file)
# m = re.findall(r'\d', file)
# print(m[0])

filename = "guru99.csv"
file = open(filename, "r")
previous = ""

leftG0 = 0
rightG0 = 0
upG0 = 0
downG0 = 0
leftG1 = 0
rightG1 = 0
upG1 = 0
downG1 = 0
leftG2 = 0
rightG2 = 0
upG2 = 0
downG2 = 0
leftG3 = 0
rightG3 = 0
upG3 = 0
downG3 = 0

counter = 0

for line in file:
	if(line != previous):

		m = re.findall(r'\d', line)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', line)
		r = re.findall(r'\d', previous)#re.match(r'PacmanPos, (.*), (.*), Ghost0Pos (.*), (.*), Ghost1Pos (.*), (.*), Ghost2Pos (.*), (.*), Ghost3Pos (.*), (.*),', previous)
		m = map(int, m)
		r = map(int, r)
		#print('\n')
		#print ("previous %s \n current %s" % (previous, line))
		result = True;
		for i in range(0, len(m)):
			result = (m[i] >= -1 and m[i] <= 1 ) and result
		if((previous != "") and (m >= 0 )):
			'''PacmanPos
			m.group(1), m[0]'''
			'''Ghost0Pos'''
			#print(m[0], r[0] )
			if(m[0] != r[0]):
				if((m[0] - r[0]) == 1):
					rightG0 = rightG0 + 1
				elif((m[0] - r[0]) == -1):
					leftG0 = leftG0 + 1

			if(m[1] != r[1]):
				if((m[1] - r[1]) == 1):
					upG0 = upG0 + 1
				elif((m[1] - r[1]) == -1):
					downG0 = downG0 + 1


			'''Ghost1Pos'''
			if(m[2] != r[2]):
				if((m[2] - r[2]) == 1):
					rightG1 = rightG1 + 1
				elif((m[2] - r[2]) == -1):
					leftG1 = leftG1 + 1
			if(m[3] != r[3]):
				if((m[3] - r[3]) == 1):
					upG1 = upG1 + 1
				elif((m[3] - r[3]) == -1):
					downG1 = downG1 + 1
			'''Ghost2Pos'''
			if(m[4] != r[4]):
				if((m[4] - r[4]) == 1):
					rightG2 = rightG2 + 1
				elif((m[4] - r[4]) == -1):
					leftG2 = leftG2 + 1
			if(m[5] != r[5]):
				if((m[5] - r[5]) == 1):
					upG2 = upG2 + 1
				elif((m[5] - r[5]) == -1):
					downG2 = downG2 + 1
			'''//Ghost3Pos'''
			if(m[6] != r[6]):
				if((m[6] - r[6]) == 1):
					rightG3 = rightG3 + 1
				elif((m[6] - r[6]) == -1):
					leftG3 = leftG3 + 1
			if(m[7] != r[7]):
				if((m[7] - r[7]) == 1):
					upG3 = upG3 + 1
				elif((m[7] - r[7]) == -1):
					downG3 = downG3 + 1
		counter = counter + 1

	previous = line;
	#print ("previous %s \n current %s" % (previous, line))
	
   	#print line,

#fcounter = float(counter);
fcounter = float(upG0 + downG0 + leftG0 + rightG0)
print("Ghost 0 up %f down: %f left: %f right: %f\n" %((upG0/fcounter),(downG0/fcounter),(leftG0/fcounter), (rightG0/fcounter) ))
fcounter = float(upG1 + downG1 + leftG1 + rightG1)
print("Ghost 1 up %f down: %f left: %f right: %f\n" %((upG1/fcounter),(downG1/fcounter),(leftG1/fcounter), (rightG1/fcounter) ))
fcounter = float(upG2 + downG2 + leftG2 + rightG2)
print("Ghost 2 up %f down: %f left: %f right: %f\n" %((upG2/fcounter),(downG2/fcounter),(leftG2/fcounter), (rightG2/fcounter) ))
fcounter = float(upG3 + downG3 + leftG3 + rightG3)
print("Ghost 3 up %f down: %f left: %f right: %f\n" %((upG3/fcounter),(downG3/fcounter),(leftG3/fcounter), (rightG3/fcounter) ))