import sys
def reduce(matrixFile, outfile):
    matrix = open(matrixFile, 'r').read().splitlines()
    while("" in matrix):
        matrix.remove("")
    foundLines = []
    for line in matrix:
        if not line in foundLines:
            foundLines.append(line)
    out = open(outfile, 'w')
    i = len(foundLines)
    j = 0
    while i > 0:
        out.write(foundLines[j])
        if i != 1:
            out.write("\n")
        i= i-1
        j = j+1

#takes in original file with names and results and outputs unreduced matrix with names
#assume names are connected with _ so they are one word
def expandAndAddNames(originalFile, resultFile, finalResultsFile):
    matrix = open(resultFile, 'r').read().splitlines()
    while("" in matrix):
        matrix.remove("")
    names = open(originalFile, 'r').read().splitlines()
    while("" in names):
        names.remove("")
    results = []
    for line in names:
        if line != '\n':
            wordList = line.split()
            matrixPortion = wordList[len(wordList) -1 ]
            if matrixPortion in matrix:
                results.append(line)
    out = open(finalResultsFile, 'w')
    i = len(results)
    j = 0
    while i > 0:
        out.write(results[j])
        #if i != 1:
        out.write("\n")
        i= i-1
        j = j+1

def strip(originalFile, outfile):
    names = open(originalFile, 'r').read().splitlines()
    while("" in names):
        names.remove("")
    out = open(outfile, 'w')
    for line in names:
        if line != '\n':
            wordList = line.split()
            matrixPortion = wordList[len(wordList) -1 ]
            out.write(matrixPortion + '\n')

arg1 = sys.argv[1]
if arg1 == '-o':
    if len(sys.argv) < 5:
        print("Usage: reduce.py -o originalMatrixFile resultFile outputFile")
        quit()
    expandAndAddNames(sys.argv[2], sys.argv[3], sys.argv[4])

if arg1 == '-i':
    if len(sys.argv) < 4:
        print("Usage: reduce.py -o strippedMatrixFile outputFile")
        quit()
    reduce(sys.argv[2], sys.argv[3])

if arg1 == '-s':
    if len(sys.argv) < 4:
        print("Usage: reduce.py -s matrixfile outname")
        quit()
    strip(sys.argv[2], sys.argv[3])

#reduce("AlliumStripped", "out.txt")
#expandAndAddNames("Allium", "out.txt", "results")

#reduce.py -i plainMatrix reduced.txt
#reduce.py -o namedMatrix resultsFile FinalOut
