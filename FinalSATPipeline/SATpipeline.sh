#!/bin/bash

matrixFile="$1"
typearg="$2"
strippedFile="$matrixFile"Stripped
reducedFile="$matrixFile"Reduced

outputfile="$reducedFile"Results
resultsFile="$matrixFile"FinalResults
summaryFile="$matrixFile"Summary.txt

start=`date +%s%N`

python reduce.py -s $matrixFile $strippedFile

python reduce.py -i $strippedFile $reducedFile

python SATreducer.py $reducedFile $typearg


python reduce.py -o $matrixFile $outputfile $resultsFile

end=`date +%s%N`

#summary file
python summary.py $summaryFile $matrixFile $strippedFile $reducedFile $outputfile $resultsFile $0$2 $((end-start))
