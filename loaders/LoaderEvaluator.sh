#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -ne 2 ]; then
    echo "using default parameters!";
    pathNeuralNetwork="/Users/francesco/Desktop/prj/output";
    input="1,2,1,2,3,2,1,1,1,1,2,3,1,2,3,4,2";
else
    pathNeuralNetwork=$0;
    input=$1;
fi

################################         EVALUATING           ################################
python ../MainEvaluator.py pathNeuralNetwork input

################################          CLEANING            ################################
rm ../Engine.pyc
rm ../MainEvaluator.pyc
rm ../MainTrainer.pyc
rm ../NeuralNetwork.pyc
rm ../Parser.pyc
rm ../Support.pyc

echo "Done!";
