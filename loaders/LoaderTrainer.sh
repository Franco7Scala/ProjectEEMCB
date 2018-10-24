#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -eq 6 ]; then
    pathTrainingSet=$1;
    pathTestSet=$2;
    pathOutput=$3;
    epoques=$4;
    batchSize=$5;
    load=$6;
elif [ "$#" -eq 1 ] && [ $1 = "help" ]; then
    printf "Parameters:\n\t-path training set;\n\t-path test set;\n\t-path output and eventually loading;\n\t-epoques;\n\t-batch size;\n\t-load network.\n";
    exit 0;
else
    echo "Using default parameters!";
    pathTrainingSet="/Users/francesco/Software/Python/ProjectEEMCB/data/little_training_set.txt";
    pathTestSet="/Users/francesco/Software/Python/ProjectEEMCB/data/little_test_set.txt";
    pathOutput="/Users/francesco/Software/Python/ProjectEEMCB/data/output/test_little";
    epoques=10;
    batchSize=32;
    load=0;
fi

################################          TRAINING            ################################
python -W ignore ../src/MainTrainer.py $pathTrainingSet $pathTestSet $pathOutput $epoques $batchSize $load

################################          CLEANING            ################################
rm ../src/Engine.pyc
rm ../src/NeuralNetwork.pyc
rm ../src/Parser.pyc
rm ../src/Support.pyc

echo "Done!";