#Imports math module for sqrt function
import math
#Function to times each value in matrix by scalor
def mult_scalar(matrix, scale,operation):
	#Creates 2 list for row and everything together
	newlist = []
	row = []
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			#Will go to each value in matrix and multiply it by scalor
			if operation == "*":
				int = scale * matrix[i][j]
			elif operation == "+":
				int = scale + matrix[i][j]
			#Will add to row list
			row.append(int)
		#End of for loop, will add row to newlist(Everything)
		newlist.append(row)
		#Reset row to avoid previous values
		row = []
	return newlist

def mult_matrix(a, b):
	#Similar way of function above
	newlist = []
	row = []
	sum = 0
	#3 for loops for matric calculation
	for i in range(len(a)):
		for z in range(len(b[0])):
			for j in range(len(a[i])):
				#Sum is solved and added to row
				sum += (a[i][j]*b[j][z])
			row.append(sum)
			sum = 0
		#Row is added to newlist
		newlist.append(row)
		row = []
	return newlist

def euclidean_dist(a,b):
	total = 0
	sum = 0
	#Makes sure if only 1 row is given for each matrix
	if len(a)==1 and len(b) == 1:
		for j in range(len(a[0])):
			#Does formula calculation
			sum = (a[0][j]-b[0][j])**2
			total += sum
		return math.sqrt(total)
	#If more than 1 row, returns -1
	else:
		return -1
