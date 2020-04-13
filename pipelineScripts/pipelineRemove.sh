#!/bin/bash

pythonInstall=C\:/Users/Katherine/gurobi811/win64/python27/bin/python.exe
gurobiInstall=C\:/Users/Katherine/gurobi811/win64/bin/gurobi.bat

matrixFile="$1"
strippedFile="$matrixFile"Stripped
reducedFile="$matrixFile"Reduced
ilpFile="$matrixFile".lp

outputfile="$reducedFile"Results
resultsFile="$matrixFile"FinalResults
summaryFile="$matrixFile"Summary.txt

start=`date +%s%N`

$pythonInstall  reduce.py -s $matrixFile $strippedFile

$pythonInstall  reduce.py -i $strippedFile $reducedFile

$pythonInstall DecisiveILPGen.py $reducedFile $ilpFile

$gurobiInstall  lp.py $ilpFile $reducedFile

$pythonInstall  reduce.py -o $matrixFile $outputfile $resultsFile

end=`date +%s%N`

#summary file
$pythonInstall summary.py $summaryFile $matrixFile $strippedFile $reducedFile $outputfile $resultsFile $0 $((end-start))

#echo Veryify Final Matrix is decisive
