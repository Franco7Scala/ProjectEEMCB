#!/bin/bash

################################   CONFIGURATION PARAMETERS   ################################
if [ "$#" -ne 2 ]; then
    echo "using default parameters!";
    pathNeuralNetwork="/Users/francesco/Desktop/prj/output";
    input="1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2";
else
    pathNeuralNetwork=$0;
    input=$1;
fi

################################         EVALUATING           ################################
python ../src/MainEvaluator.py $pathNeuralNetwork $input

################################          CLEANING            ################################
rm ../src/Engine.pyc
rm ../src/MainEvaluator.pyc
rm ../src/MainTrainer.pyc
rm ../src/NeuralNetwork.pyc
rm ../src/Parser.pyc
rm ../src/Support.pyc

echo "Done!";
