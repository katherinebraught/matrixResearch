#!/bin/bash

#usage: ./stripAll.sh <directoryWithFilesToStrip>
#creates a new directory in the working directory stripped<directoryWithFilesToStrip> containing the stripped files
#script must be executable: run "chmod u+x stripAll.sh" to allow excution
#limitations:
#      error is thrown if a stripped directory already exists, but script will still execute
#      all files in <directoryWithFilesToStrip> will be processes. The script assumes that they can be processed.

directory=$1
newDirectory="stripped$directory"
mkdir $newDirectory
cd $directory

for f in ./*
do
    echo "Processing $f"
    outputFile="../$newDirectory/$f"
    less $f | awk '{print $2}' > $outputFile
    head -5 $f
    echo "ooooooooooooooooooooooooooooooooooooooooooooooooo"
    head -5 $outputFile
done
