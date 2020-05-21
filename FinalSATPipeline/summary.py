import sys

def getDimensions(filename, out, width):
	matrixFile = open(filename, "r")
	matrix = matrixFile.read().splitlines()
	while("" in matrix) :
		matrix.remove("")  
	n = len(matrix)
	k = len(matrix[0])  # Require k > =1
	if width == 1:
		out.write("Matrices contain  " + str(k) +  " columns. \n")
	out.write("Dimension of " + filename  + ": " + str(n) + " rows.\n")
	matrixFile.close()

originalMatrix = sys.argv[2];
strippedFile = sys.argv[3];
reducedFile = sys.argv[4];
pre_unreducedFile = sys.argv[5];
finalDecisiveMatrix = sys.argv[6];
pipelineName = sys.argv[7];
runtime = sys.argv[8];

out = open(sys.argv[1] , 'w')
out.write("Summary file for " + originalMatrix + ' after running' + pipelineName +'\n')
out.write("Original Matrix: " +  originalMatrix +"\n")
out.write("Stripped Matrix (matrix missing taxa names): " +  strippedFile +"\n")
out.write("Reduced Matrix (matrix containing only unique rows): " +  reducedFile +"\n")
out.write("Reduced Decicisive Matrix (decisive matrix containing only unique rows): " +  pre_unreducedFile +"\n")
out.write("Full Decicisive Matrix with Taxa Names: " +  finalDecisiveMatrix +"\n\n")

getDimensions(strippedFile, out, 1)
getDimensions(reducedFile, out, 0)
getDimensions(pre_unreducedFile, out, 0)
getDimensions(finalDecisiveMatrix, out, 0)

#timing data:
out.write("\n Runtime of entire script execution: " + str(runtime) + " nanoseconds." )

out.close()
