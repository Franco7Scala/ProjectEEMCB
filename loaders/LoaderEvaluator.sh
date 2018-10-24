#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -eq 2 ]; then
    pathNeuralNetwork=$1;
    input=$2;
elif [ "$#" -eq 1 ] && [ $1 = "help" ]; then
    printf "Parameters:\n\t-path neural network;\n\t-input to evaluate.\n";
    exit 0;
else
    echo "Using default parameters!";
    pathNeuralNetwork="/Users/francesco/Software/Python/ProjectEEMCB/data/output/test_little";
    input="1 2 1 2 1 2 1 2 1 2 1 2";
fi

################################         EVALUATING           ################################
python -W ignore ../src/MainEvaluator.py $pathNeuralNetwork "$input"

################################          CLEANING            ################################
rm ../src/Engine.pyc
rm ../src/NeuralNetwork.pyc
rm ../src/Parser.pyc
rm ../src/Support.pyc

echo "Done!";
