#!/usr/bin/python

# Copyright 2019, Gurobi Optimization, LLC

# This example reads an LP model from a file and solves it.
# If the model is infeasible or unbounded, the example turns off
# presolve and solves the model again. If the model is infeasible,
# the example computes an Irreducible Inconsistent Subsystem (IIS),
# and writes it to a file

import sys
from gurobipy import *

if len(sys.argv) < 3:
    print('Usage: lp.py filename row')
    quit()

# Read and solve model

model = read(sys.argv[1])
model.write("before.lp")
model.optimize()

print("now we can remove a row")

row = sys.argv[2]

#print(model.Vars())
constraints = model.getConstrs()
vars = model.getVars()
#step one: find the variables that corresponds with row
xvars = []
for var in vars:
    for i in range(0,4):
        if (var.varname == "x(" + str(row) + "," + str(i) + ")"):
            xvars.append(var)
print(xvars)
for constr in constraints:
    #remove entire constraint for cc(0,row)
    if (constr.constrName == "cc(0," + row + ")"):
        print(constr.constrName) #prints cc(0,1)
        model.remove(constr)
    #remove x(row,color) in each constraint
    else:
        for var in xvars:
            model.chgCoeff(constr,var, 0)
model.write("after.lp")

