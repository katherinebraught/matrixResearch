from pysat.solvers import Lingeling, Solver

import time

import sys

def get_power_set(s):
  power_set=[[]]
  for elem in s:
    # iterate over the sub sets so far
    for sub_set in power_set:
      # add a new subset consisting of the subset at hand added elem
      power_set=power_set+[list(sub_set)+[elem]]
  return power_set

#takes in a set of values and checks if there are any opositites, 1 and -1
def tautology(values):
    for value in values:
        for oValue in values:
            if value == (-1 * oValue):
                return True
    return False

def formulaToString(a,b,c,d):
    return (str(a) + " " + str(b)+ " " + str(c) + " " + str(d) + " ")

def threeFormulaToString(a,b,c):
    return (str(a) + " " + str(b)+ " " + str(c) + " ")

def twoFormulaToString(a,b):
    return (str(a) + " " + str(b)+ " ")

def oneFormulaToString(a):
    return (str(a) + " ")

#converts p <-> (q OR r) to cnf
def IffOr(p, q, r, CNF_forms):
    CNF_forms.append([-1*p, q,r])
    CNF_forms.append([p, -1*q])
    CNF_forms.append([p, -1*r])
    return CNF_forms

#converts p <-> (q AND r) to cnf
def IffAnd(p, q, r, CNF_forms):
    CNF_forms.append([p, -1*q,-1*r])
    CNF_forms.append([-1*p, q])
    CNF_forms.append([-1*p, r])
    return CNF_forms

def convertAnds(formula, formulaName, nextVariableName, CNF_forms):
    for f in formula:
        IffAnd(formulaName, f, nextVariableName, CNF_forms)
        formulaName = nextVariableName
        nextVariableName +=1
    return [nextVariableName, CNF_forms]
 
def isSatisfiable(matrix):
    n = len(matrix)     # Require n >= 1
    k = len(matrix[0])  # Require k > =1

    #fill in vars
    var_val = 1;
    xvarmatrix = []
    for i in range(0,n):
        xvarmatrix.append([])
        for r in range (0,4):
            xvarmatrix[i].append(var_val)
            var_val += 1

    CNF_forms = []

    # Constraints to ensure each node gets only one color
    #print("equation 1:")
    for i in range(0,n):
        formula = []
        #xor of xi0, xi1,xi2, xi3
        a = xvarmatrix[i][0]
        b = xvarmatrix[i][1]
        c = xvarmatrix[i][2]
        d = xvarmatrix[i][3]
    
        formula.append([a,b,c,d])
        formula.append([a,b,-1*c,-1*d])
        formula.append([a,-1*b,c,-1*d])
        formula.append([a,-1*b,-1*c,d])
        formula.append([a,-1*b,-1*c,-1*d])

        formula.append([-1*a,b,c,-1*d])
        formula.append([-1*a,b,-1*c,d])
        formula.append([-1*a,b,-1*c,-1*d])

        formula.append([-1*a,-1*b,c,d])
        formula.append([-1*a,-1*b,c,-1*d])
        formula.append([-1*a,-1*b,-1*c,d])
        formula.append([-1*a,-1*b,-1*c,-1*d])
    
        for form in formula:
            CNF_forms.append(form)

                       
        # "Surjective" constraints: Ensure each color is used at least once.
    for r in range(0,4):
        eq = []
        for i in range(0,n):
            eq.append(xvarmatrix[i][r])
        CNF_forms.append(eq)

    # Ensure no hyperedge is rainbow-colored: topology-dependant constraints
    #for every column
    for c in range(0,k):
        c0 = []
        c1 = []
        c2 = []
        c3 = []
        #build our DNF formula to turn into CNF with Tseitin Transformation
        for i in range(0,n):
            if (matrix[i][c] == 'X'):
                c0.append(-1* xvarmatrix[i][0])
                c1.append(-1*xvarmatrix[i][1])
                c2.append(-1*xvarmatrix[i][2])
                c3.append(-1*xvarmatrix[i][3])

        #begining the tseitin transformation
        #add name of entire formula
        rainbowColorFormula = var_val
        var_val += 1
        #name the two subformulas
        leftSub = var_val
        var_val += 1
        rightSub = var_val
        var_val += 1
        #name the conjunctive formulas
        c0Name = var_val
        var_val += 1
        c1Name = var_val
        var_val += 1
        c2Name = var_val
        var_val += 1
        c3Name = var_val
        var_val += 1
        #generate our CNF formula for the outer formula
        CNF_forms.append([rainbowColorFormula])
        #rainbowColorFormula <-> leftSub OR rightSub
        CNF_forms = IffOr(rainbowColorFormula, leftSub, rightSub, CNF_forms)
        #leftSub <-> c0Name OR c1Name
        CNF_forms = IffOr(leftSub, c0Name, c1Name, CNF_forms)
        #rightSub <-> c2Name OR c3Name
        CNF_forms = IffOr(rightSub, c2Name, c3Name, CNF_forms)
        #now formulate the inner formulas (collecions of Ands)
        c0Res = convertAnds(c0, c0Name, var_val, CNF_forms)
        CNF_forms = c0Res[1]
        var_val = c0Res[0]

        c1Res = convertAnds(c1, c1Name, var_val, CNF_forms)
        CNF_forms = c1Res[1]
        var_val = c1Res[0]

        c2Res = convertAnds(c2, c2Name, var_val, CNF_forms)
        CNF_forms = c2Res[1]
        var_val = c2Res[0]

        c3Res = convertAnds(c3, c3Name, var_val, CNF_forms)
        CNF_forms = c3Res[1]
        var_val = c3Res[0]


    s = Lingeling() #Solver(name='Lingeling')
    for form in CNF_forms:
        s.add_clause(form)

    return(s.solve())


#arg1 = sys.argv[1]

#INFILE = open(arg1, "r")  # open the file specified by the value of arg1, to read from the file.

# Read data matrix, stripping away empty lines
#matrix = INFILE.read().splitlines()
#INFILE.close()

#while("" in matrix) :
#    matrix.remove("")

#print(isSatisfiable(matrix))

###############################################
def stripAndAdd():
	prog_start_time = time.time()
	if len(sys.argv) < 2:
		print('Usage: lp.py lp')
		quit()

	print("starting program")
	remove_ct = 0
	remove_time = 0
	add_ct = 0
	add_time = 0
	solve_ct = 0
	solve_time = 0
	timeResults = open(sys.argv[1] + "timeResults", "w")


	#generate initial model
	matrixFile = open(sys.argv[1], "r")
	matrix = matrixFile.read().splitlines()
	while("" in matrix) :
		matrix.remove("")  
	n = len(matrix)     # Require n >= 1
	k = len(matrix[0])  # Require k > =1
	matrixFile.close()
	matrixCopy = matrix[:]

	# Read and solve initial model
	#tempILPFile =  sys.argv[1] + "tempILP.lp"
	#updateILP(matrix, tempILPFile)

	#model = read(tempILPFile)

	solve_ct += 1
	start_time = time.time()
	sat_value = isSatisfiable(matrix)
	solve_time += (time.time() - start_time)
	print("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct))
	timeResults.write("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct) + "\n")
	#model.write("irusbefore.sol")
	print("found initial solution")

	#surpress output
	#model.setParam(GRB.Param.OutputFlag, 0)

	#

	removalCount = n
	removedRows = []

	#find column with the most x's
	maxColumn = 0
	maxX = 0
	for i in range(0,k):
		xCount = 0
		for j in range(0,n):
			if matrix[j][i] == "X":
				xCount=xCount+1
		if (xCount > maxX):
			maxX = xCount
			maxColumn = i

	print("Found max column")

	#remove all the rows missing the max x
	i = 0
	#for i in range(0, len(matrix)):
	#while i < len(matrix): #for i in range(0,len(matrix)):
	for row in matrix:
		#if matrix[i][maxColumn] != "X":
		if row[maxColumn] != 'X':
			print(matrix[i])
			remove_ct += 1
			#matrix.pop(i)
			#matrix.remove(row)
			#removedRows.append(matrix[i])
			removedRows.append(row)
		#else:
			#i+=1
	start_time = time.time()
	for row in removedRows:
		matrix.remove(row)
	#updateILP(matrix, tempILPFile)
	#model = read(tempILPFile)
	remove_time += (time.time() - start_time)
	#print("Total remove time: " + str(remove_time) + " Count: " + str(remove_ct))
	#timeResults.write("Total remove time: " + str(remove_time) + " Count: " + str(remove_ct) + "\n")
	#print(matrix)
	print("Removed rows")

	#now we have an infeasible solution        
	solve_ct += 1
	start_time = time.time()
	sat_value = isSatisfiable(matrix)
	solve_time += (time.time() - start_time)
	print("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct))
	timeResults.write("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct) + "\n")
	print(removedRows)

	#check all subsets
	power_sets = get_power_set(removedRows)

	#could probably be made more efficient by adding and removing rows only as needed to get the powersets
	lengthOfOptSolution=0
	optSolution = []
	solutionCount = 1
	print("checking powersets for more optimal solution")
	print_cnt = 0
	for row_set in power_sets:
		print(solutionCount)
		solutionCount += 1
		#add all the rows

		start_time = time.time()
		for row in row_set:
			matrix.append(row)
			add_ct += 1
		#updateILP(matrix, tempILPFile)
		#model = read(tempILPFile)
		#add_time += (time.time() - start_time)
		#print("Total add time: " + str(add_time) + " Count: " + str(add_ct))
		#timeResults.write("Total add time: " + str(add_time) + " Count: " + str(add_ct) + "\n")
		
		#check if its infeasible
		solve_ct += 1
		start_time = time.time()
		#model.optimize()
		sat_value = isSatisfiable(matrix)
		solve_time += (time.time() - start_time)
		print("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct))
		timeResults.write("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct) + "\n")
		infeasCount = 0
		if sat_value == False:
			#if it is, set that as opt solution
			print("found infeasible")
			print(row_set)
			if lengthOfOptSolution < len(row_set):
				lengthOfOptSolution = len(row_set)
				optSolution = row_set[:]


		start_time = time.time()
		#important: assumes no rows are the same... will be the case if we use a reduce matrix
		for row in row_set:
			matrix.remove(row)
			remove_ct += 1
		#updateILP(matrix, tempILPFile)
		#model = read(tempILPFile)    
		#remove_time += (time.time() - start_time)
		#print("Total remove time: " + str(remove_time) + " Count: " + str(remove_ct))
		#timeResults.write("Total remove time: " + str(remove_time) + " Count: " + str(remove_ct) + "\n")
		print_cnt += 1

	print("Optimal Solution adds back in: ")
	print(optSolution)
	start_time = time.time()
	for row in optSolution:
		add_ct += 1
		matrix.append(row)
	#updateILP(matrix, tempILPFile)
	#model = read(tempILPFile)
	#add_time += (time.time() - start_time)
	#print("Total add time: " + str(add_time) + " Count: " + str(add_ct))
	#timeResults.write("Total add time: " + str(add_time) + " Count: " + str(add_ct) + "\n")

	for row in optSolution:
		removedRows.remove(row)

	#unsurpress output and save last matrix
	#model.setParam(GRB.Param.OutputFlag, 1)
	solve_ct += 1
	start_time = time.time()
	#model.optimize()
	sat_value = isSatisfiable(matrix)
	solve_time += (time.time() - start_time)
	print("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct))
	timeResults.write("Total solve time: " + str(solve_time) + " Count: " + str(solve_ct) + "\n")

	#prog_start_time = time.time()
	#model.write("opt.lp")

	#outMatrix = open(sys.argv[2]+ "stripAndAddMatrix" ,'w')
	#for i in range (0,n):
	#    if (i in removedRows):
	#        outMatrix.write(matrix[i])
	#outMatrix.close()
	print("End program")
	timeResults.write("Total program time: " + str(time.time() - prog_start_time) +  "\n")

	#print matrix
	outMatrix = open(sys.argv[1] + "Results", 'w')
	for i in range(0,len(matrix)):
		print(matrix[i])
		outMatrix.write(matrix[i]+ '\n')
	#addRow(model, 133, removedConstr)
	#model.optimize()

def remove():	
	#read in matrix
	start_time = time.time()
	matrixFile = open(sys.argv[1], "r")
	matrix = matrixFile.read().splitlines()
	while("" in matrix) :
		matrix.remove("")  
	n = len(matrix)     # Require n >= 1
	k = len(matrix[0])  # Require k > =1
	matrixFile.close()
	matrixCopy = matrix[:]

	removalCount = n
	
	sat_value = isSatisfiable(matrix)

	#while model is not infeasible
	while removalCount > 1 and sat_value == True:
		removalCount = removalCount - 1
	#consider removing reptitive columns
	#good testing ones have lots of X's
	#tool that allows you to remove a specific set of organisms
	#remove row with the most dashes
	#begin removing the row
		minRow = n+1
		minXs = k+1
		for i in range (0, n):
			if matrix[i].count('X') < minXs:
				minXs = matrix[i].count('X')
				minRow = matrix[i]

		row = minRow
		matrix.remove(row)
		n-=1
		sat_value = isSatisfiable(matrix)
		print(matrix)

	print("Remaining rows:"  + str(len(matrix)))
	f = open(sys.argv[1] + "Results", "w")
	#print matrix:
	for i in range(0,n):
		f.write(matrix[i] + "\n")
		print(matrix[i])
	f.close()

	end_time = time.time()
	print("Execution time: %d", end_time-start_time);
	
if sys.argv[2] == "-a":
	stripAndAdd()
if sys.argv[2] == "-r":
	remove()
	