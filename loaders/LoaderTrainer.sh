#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -ne 5 ]; then
    echo "using default parameters!";
    pathTrainingSet="/Users/francesco/Desktop/prj/training_set.txt";
    pathTestSet="/Users/francesco/Desktop/prj/test_set.txt";
    pathOutput="/Users/francesco/Desktop/prj/output";
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
python ../MainTrainer.py pathTrainingSet pathTestSet pathOutput epoques batchSize

################################          CLEANING            ################################
rm ../Engine.pyc
rm ../MainEvaluator.pyc
rm ../MainTrainer.pyc
rm ../NeuralNetwork.pyc
rm ../Parser.pyc
rm ../Support.pyc

echo "Done!";