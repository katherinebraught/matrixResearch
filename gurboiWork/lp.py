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

# Read and solve initial model
model = read(sys.argv[1])
model.write("eucbefore.lp")
model.optimize()
model.write("eucbefore.sol")



#consider removing reptitive columns
#good testing ones have lots of X's
#tool that allows you to remove a specific set of organisms
#remove row with the most dashes
#begin removing the row
row = sys.argv[2]
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
        if (constr.constrName == "cc(0," + row + ")"):
            model.remove(constr)
        #remove x(row,color) in each constraint
        else:
            for var in xvars:
                model.chgCoeff(constr,var, 0)
    model.write("after.lp")
    model.optimize()
    model.write("after.sol")
