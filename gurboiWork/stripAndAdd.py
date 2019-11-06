#!/usr/bin/python

# Copyright 2019, Gurobi Optimization, LLC

# This example reads an LP model from a file and solves it.
# If the model is infeasible or unbounded, the example turns off
# presolve and solves the model again. If the model is infeasible,
# the example computes an Irreducible Inconsistent Subsystem (IIS),
# and writes it to a file

## command : gurobi.bat lp.py "C:/Users/Katherine/gurobiWorking/irus/irus.lp" "C:/Users/Katherine/gurobiWorking/irus/irusStripped.txt"

import sys
from gurobipy import *

def removeRow(model, row, removedConstr):
    #print("removing row " + str(row))
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
            lhs, sense, rhs, name = model.getRow(constr), constr.Sense, constr.RHS, constr.ConstrName
            #print(lhs)
            constrList = (lhs, sense, rhs, name)
            removedConstr["cc(0," + str(row) + ")"] = constrList
            model.remove(constr)
        #remove x(row,color) in each constraint
        else:
            for var in xvars:
                model.chgCoeff(constr,var, 0)

def addRow(model, row, removedConstr):
    constraints = model.getConstrs()
    vars = model.getVars()
    #find the variables that corresponds with row
    xvars = []
    for var in vars:
        for i in range(0,4):
            if (var.varname == "x(" + str(row) + "," + str(i) + ")"):
                xvars.append(var)
    for constr in constraints:
        for var in xvars:
            model.chgCoeff(constr,var, 1)
    #model.addConstr(removedConstr["cc(0," + str(row) + ")"])
    constrInfo = removedConstr["cc(0," + str(row) + ")"]
    model.addConstr(constrInfo[0], constrInfo[1], constrInfo[2], constrInfo[3])
    #undo addition to first set:
    

def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 0:
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

def get_power_set(s):
  power_set=[[]]
  for elem in s:
    # iterate over the sub sets so far
    for sub_set in power_set:
      # add a new subset consisting of the subset at hand added elem
      power_set=power_set+[list(sub_set)+[elem]]
  return power_set


if len(sys.argv) < 3:
    print('Usage: lp.py lp matrix')
    quit()

# Read and solve initial model
model = read(sys.argv[1])
model.write("irusbefore.lp")
model.optimize()
model.write("irusbefore.sol")

#surpress output
model.setParam(GRB.Param.OutputFlag, 0)

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
removedConstr = {}
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

#remove all the rows missing the max x
for i in range(0,n):
    if matrix[i][maxColumn] != "X":
        removeRow(model, i, removedConstr)
        removedRows.append(i)
#now we have an infeasible solution        
model.optimize()

#check all subsets
power_sets = get_power_set(removedRows)

#could probably be made more efficient by adding and removing rows only as needed to get the powersets
lengthOfOptSolution=0
optSolution = []
for row_set in power_sets:
    #add all the rows
    for row in row_set:
        addRow(model, row, removedConstr)
    #check if its infeasible
    model.optimize()
    infeasCount = 0
    if model.status == GRB.INFEASIBLE:
        #print("???")
        #infeasCount=infeasCount+1
        #if it is, set that as opt solution
        if lengthOfOptSolution < len(row_set):
            lengthOfOptSolution = len(row_set)
            optSolution = row_set[:]
    else:
        print(row_set)
    #remove all the rows
    for row in row_set:
        removeRow(model, row, removedConstr)

print(infeasCount)
print(removedRows)
print(optSolution)
print(lengthOfOptSolution)
for row in optSolution:
    addRow(model, row, removedConstr)
model.optimize()
model.write("opt.lp")

###while model is not infeasible
##while removalCount > 1 and model.status != GRB.INFEASIBLE:
##    removalCount = removalCount - 1
##
##    minRow = n+1
##    minXs = k+1
##    for i in range (0, n):
##        #print(matrix[i])
##        #print("foo")
##        if matrix[i] != ".":
##            if matrix[i].count('X') < minXs:
##                minXs = matrix[i].count('X')
##                minRow = i
##
##    row = minRow
##    matrix[row] = "."
##    #print("removing row" + str(row))
##    if (row != "n"):
##        removeRow(model, row, removedConstr)
##        model.write("after" + str(row) +".lp")
##        model.optimize()
##        if model.status != GRB.INFEASIBLE: 
##            model.write("after" + str(row) +".sol")

#check all subsets

#pick the subset that has the most
            
#print("Removed rows:")
#for i in range (0, n):
#    if matrix[i] ==".":
#        print(str(i) + "    " + matrixCopy[i])
print("---------------------------------------")
#print("Remaining rows:"  + str(removalCount))
#print matrix:
#for i in range(0,n):
#    if matrix[i]  != ".":
#        print(str(i) + "    " + matrix[i])
#addRow(model, 133, removedConstr)
#model.optimize()



