##parse through original matrix and new matrix to see family coverage
##output as CSV so we can make pretty graphs

#usage python getData.py originalMatrix newMatrix outputFile.csv
import sys

fullSum = 0
newSum = 0

#parse original file wtih _ between families and more speicific organisms
families = dict()
matrixFile = open(sys.argv[1], "r")
matrix = matrixFile.readlines()
for row in matrix:
    fullSum = 1 + fullSum
    words = row.split()
    family = words[0].split("_")[0]
    if (family in families):
        families[family] = [1 + families[family][0], 0]
    else:
       families[family] = [1, 0] 
matrixFile.close()

print(families)


newMatrixFile = open(sys.argv[2], "r")
newMatrix = newMatrixFile.readlines()
for row in newMatrix:
    newSum = 1 + newSum
    words = row.split()
    family = words[0].split("_")[0]
    families[family] = [families[family][0], 1 + families[family][1]]
matrixFile.close()

print(families)

resultsFile = open(sys.argv[3], "a")
resultsFile.write("Family,Number in Original Matrix,Number in New Matrix,Percent Represented")
for family in families:
    resultsFile.write("\n" + family + "," + str(families[family][0]) + "," + str(families[family][1]) + "," + str((families[family][1] / families[family][0])* 100))
resultsFile.write("\nTotal," + str(fullSum) + "," + str(newSum) + "," + str((newSum/fullSum) * 100))
resultsFile.close()
