#!/usr/bin/python

# Copyright 2019, Gurobi Optimization, LLC

# This example reads an LP model from a file and solves it.
# If the model is infeasible or unbounded, the example turns off
# presolve and solves the model again. If the model is infeasible,
# the example computes an Irreducible Inconsistent Subsystem (IIS),
# and writes it to a file

## command : gurobi.bat lp.py "C:/Users/Katherine/gurobiWorking/irus/irus.lp" "C:/Users/Katherine/gurobiWorking/irus/irusStripped.txt"

import sys
import time
from gurobipy import *

#if len(sys.argv) < 3:
#    print('Usage: lp.py lp matrix')
#    quit()

#start_time = time.time()

# Read and solve initial model
model = read(sys.argv[1])
#model.write("eucbefore.lp")
start_time = time.time()
model.optimize()
first_pass = time.time()
#model.write("eucbefore.sol")

#first_pass = time.time()
print("Initial Solving of " + sys.argv[1] + ": " + str(first_pass -start_time));
#exit()

#read in matrix
matrixFile = open(sys.argv[2], "r")
matrix = matrixFile.read().splitlines()
while("" in matrix) :
    matrix.remove("")  
n = len(matrix)     # Require n >= 1
k = len(matrix[0])  # Require k > =1
matrixFile.close()
matrixCopy = matrix[:]

removalCount = n

#while model is not infeasible
while removalCount > 1 and model.status != GRB.INFEASIBLE:
    removalCount = removalCount - 1
#consider removing reptitive columns
#good testing ones have lots of X's
#tool that allows you to remove a specific set of organisms
#remove row with the most dashes
#begin removing the row
    minRow = n+1
    minXs = k+1
    for i in range (0, n):
        #print(matrix[i])
        #print("foo")
        if matrix[i] != ".":
            if matrix[i].count('X') < minXs:
                minXs = matrix[i].count('X')
                minRow = i

    row = minRow
    matrix[row] = "."
    print("removing row" + str(row))
    if (row != "n"):
        constraints = model.getConstrs()
        vars = model.getVars()
        #find the variables that corresponds with row
        xvars = []
        for var in vars:
            for i in range(0,4):
                if (var.varname == "x(" + str(row) + "," + str(i) + ")"):
                    xvars.append(var)
        for constr in constraints:
            #remove entire constraint for cc(0,row)
            if (constr.constrName == "cc(0," + str(row) + ")"):
                model.remove(constr)
            #remove x(row,color) in each constraint
            else:
                for var in xvars:
                    model.chgCoeff(constr,var, 0)
        #model.write("after" + str(row) +".lp")
        model.optimize()
        #if model.status != GRB.INFEASIBLE: 
            #model.write("after" + str(row) +".sol")
print("Removed rows:")
for i in range (0, n):
    if matrix[i] ==".":
        print(str(i) + "    " + matrixCopy[i])
print("---------------------------------------")
print("Remaining rows:"  + str(removalCount))
f = open(sys.argv[2] + "Results", "w")
#print matrix:
for i in range(0,n):
    if matrix[i]  != ".":
        print(str(i) + "    " + matrix[i])
        f.write(matrix[i] + "\n")
f.close()

end_time = time.time()
print("Execution time: %d", end_time-start_time);




        

