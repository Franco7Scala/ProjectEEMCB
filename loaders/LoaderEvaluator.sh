#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -ne 2 ]; then
    echo "Using default parameters!";
    pathNeuralNetwork="/Users/francesco/Software/Python/ProjectEEMCB/data/output/test_little";
    input="1 2 1 2 1 2 1 2 1 2 1 2";
    inputSize=12;
else
    pathNeuralNetwork=$0;
    input=$1;
fi

################################         EVALUATING           ################################
python -W ignore ../src/MainEvaluator.py $pathNeuralNetwork "$input" $inputSize

################################          CLEANING            ################################
rm ../src/Engine.pyc
rm ../src/NeuralNetwork.pyc
rm ../src/Parser.pyc
rm ../src/Support.pyc

echo "Done!";
