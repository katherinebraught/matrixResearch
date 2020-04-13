# Given a file containing a data availability matrix in text fomat, generates
# a Gurobi-format ILP that is feasible if and only if the given matrix is
# non-decisive.
#
# Call this program on a command line in a terminal window as:
#     python DecisiveILPGen input_matrix.txt ILP_file.lp

import sys

arg1 = sys.argv[1]
arg2 = sys.argv[2]

INFILE = open(arg1, "r")  # open the file specified by the value of arg1, to read from the file.
OUT = open(arg2, "w")     # open the file specified by the value of arg2, to write to the file.

# Read data matrix, stripping away empty lines
matrix = INFILE.read().splitlines()
while("" in matrix) :
    matrix.remove("")
 
n = len(matrix)     # Require n >= 1
k = len(matrix[0])  # Require k > =1
INFILE.close()

# Constraints to ensure each node gets only one color
oneColorConstrs = ""
for i in xrange(0,n):
    oneColorConstrs = oneColorConstrs + "cc(0,"+ str(i) + "): x(" + str(i) + ",0)"
    for r in xrange (1,4):
        oneColorConstrs = oneColorConstrs + " + x(" + str(i) + "," + str(r) + ")"

    oneColorConstrs = oneColorConstrs + " = 1\n"

# "Surjective" constraints: Ensure each color is used at least once.
surjColorConstrs = ""
for r in xrange(0,4):
    surjColorConstrs = surjColorConstrs + "cc(1," + str(r) +"): x(0," + str(r) + ")"
    for i in xrange(1,n):
        surjColorConstrs = surjColorConstrs + " + x(" + str(i) + "," + str(r) + ")"
    surjColorConstrs = surjColorConstrs + " >= 1\n"

# Ensure no hyperedge is rainbow-colored: topology-independent constraints
noRainbowConstrs = ""
for j in xrange(0,k):
    noRainbowConstrs = noRainbowConstrs + "cc(2," + str(j) +"): z(" + str(j) + ",0)"
    for r in xrange(1,4):
        noRainbowConstrs = noRainbowConstrs + " + z(" + str(j) + "," + str(r) + ")"

    noRainbowConstrs = noRainbowConstrs + " >= 1\n"

# Ensure no hyperedge is rainbow-colored: topology-dependant constraints
topolDepConstrs = ""
for j in xrange(0,k):
    for r in xrange(0,4):
        sumXIR = ""
        i = 0
        while i < n and matrix[i][j] != "X":
            i = i + 1

        sumXIR = sumXIR + "x(" + str(i) + "," + str(r) + ")"
        for q in xrange(i+1,n):
            if matrix[q][j] == "X":
                sumXIR = sumXIR + " + x(" + str(q) + "," + str(r) + ")"

        topolDepConstrs = topolDepConstrs + "cc(3," + str(j) + "," + str(r) +"): " + sumXIR + " + z(" + str(j) + "," + str(r) + ") >= 1" + "\n"
        topolDepConstrs = topolDepConstrs + "cc(4," + str(j) + "," + str(r) + "): " + sumXIR + " + " + str(n) + " z(" + str(j) + "," + str(r) + ") <= " + str(n) + "\n"

# List of (binary) variables.
binaryVars = "binary \n"
for i in xrange(0,n):
    for r in xrange (0,4):
        binaryVars = binaryVars + "x(" + str(i) + "," + str(r) + ") "

for j in xrange(0,k):
    for r in xrange(0,4):
        binaryVars = binaryVars + "z(" + str(j) + "," + str(r) + ") "

# Generate ILP file.
OUT.write("subject to \n")
OUT.write(oneColorConstrs + " \n\n")
OUT.write(surjColorConstrs + " \n\n")
OUT.write(noRainbowConstrs + " \n\n")
OUT.write(topolDepConstrs + " \n\n")
OUT.write(binaryVars + " \n")  # write to file the value of the variable 'binaries'
OUT.write("end")  # write to file the string (word) 'end'
OUT.close()
print ("The ILP file is %s \n" %  arg2)
