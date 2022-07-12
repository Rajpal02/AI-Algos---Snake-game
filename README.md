# AIGroupProject
Artificial Intelligence group project repository

## Pre-requisites

If you have conda installed:

- Run ```conda env create -f environment.yml``` 

This will create an environment with the dependencies installed. Also note, the dev version is for mac compatibility, we can also use 1.9.6 for windows

- Run ```conda activate snake``` 

Otherwise you can install the following packages using pip

- pygame==2.0.0.dev6
- dataclasses==0.8
- sympy==1.9
- mpmath==1.2.1
- psutil==5.9.0
- numpy==1.19.5

## How to run

Run ```python main.py -a [ALGO_NAME]```

Default algo is ASTAR. ALGO_NAME can be ASTAR, GENETIC, RL, DIJKSTRAS and BASELINE 

For example, for GENETIC
Run ```python main.py -a "GENETIC"```

ASTAR and RL will run for one iteration only as the goal state doesn't depend on any evaluated population/q values set.

GENETIC will run for 1 generation having 50 as the default population and will determine the best possible score from it.

Reinforcement Learning (RL) will run for 120 iterations and will determine the best score based on it.

## How to train (Genetic and RL)

### Genetic Algotithm

GENETIC uses **temp.npz** file to get the existing list of population set and use them for moves generations. Every generation for which genetic is used for gets appended in the file. 

To train genetic specifically navigate inside Genetic Algo and run ```python main.py -a "GENETIC" -t True -i [ITERATION_COUNT]```

In the above command iteration count will be used for number of generations to be added. 

If you have to start training from scratch(Not recommended), delete the file **temp.npz** and then run the above command.

### Reinforcement Learning Algotithm

RL uses **qvalues.json** file to get the existing list of qvalues set and use them for moves generations. Q values set for each game is appended in this json file

To train genetic specifically navigate inside Genetic Algo and run ```python main.py -a "RL" -t True -i [ITERATION_COUNT]```

In the above command ITERATION_COUNT relates to the number of games to be used for training. 

If you have to start training from scratch(Not recommended), delete the file **qvalues.json** and then run the above command.






