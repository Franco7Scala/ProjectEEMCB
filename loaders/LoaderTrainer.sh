#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -ne 5 ]; then
    echo "Using default parameters!";
    pathTrainingSet="/Users/francesco/Software/Python/ProjectEEMCB/data/little_training_set.txt";
    pathTestSet="/Users/francesco/Software/Python/ProjectEEMCB/data/little_test_set.txt";
    pathOutput="/Users/francesco/Software/Python/ProjectEEMCB/data/output/test_little";
    epoques=10;
    batchSize=32;
else
    pathTrainingSet=$0;
    pathTestSet=$1;
    pathOutput=$2;
    epoques=$3;
    batchSize=$4;
fi

################################          TRAINING            ################################
python -W ignore ../src/MainTrainer.py $pathTrainingSet $pathTestSet $pathOutput $epoques $batchSize

################################          CLEANING            ################################
rm ../src/Engine.pyc
rm ../src/NeuralNetwork.pyc
rm ../src/Parser.pyc
rm ../src/Support.pyc

echo "Done!";