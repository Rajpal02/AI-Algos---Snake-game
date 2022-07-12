
import argparse
from snake_game import run_snake_game_dijkstras, run_snake_game_baseline
from constants import *
import Astar_Algo.run_snake as AstarSnake
import Genetic_Algo.train_snake_genetic as GeneticAlgo
import Reinforcement_Learning_Algo.snake_run_RL as RLAlgo
from Baseline_Model.baseline import baseline_path_generator


def get_algo_from_args():
    parser = argparse.ArgumentParser(
        description='Pass the name of the algorithm to be used for snake traversal')
    parser.add_argument(
        "-a", "--algorithm", help="Algorithm name defaults to ASTAR", default=ASTAR)
    parser.add_argument(
        "-t", "--train", help="Training envriroment defaults to False", default=False)
    parser.add_argument(
        "-i", "--itertation", help="Iteration count for training, For Genetic it will be generation count (defaults to 100)", default=100)
    args = parser.parse_args()
    return args.algorithm, args.train, int(args.itertation)


def main():
    # Get runtime arguments
    algo, train, itertation = get_algo_from_args()
    print("Algorithm used is...", algo)
    print("Training env is ...", train)
    if train:
        print("Training count is ...", itertation)

    if(algo == DIJKSTRAS):
        direction = "RIGHT"
        run_snake_game_dijkstras(direction, direction)
    elif(algo == ASTAR):
        AstarSnake.run_snake()
    elif(algo == GENETIC):
        # Support for training genetic
        if train:
            GeneticAlgo.run_genetic_algo(itertation)
        else:
            GeneticAlgo.run_genetic_algo(1)
    elif(algo == RL):
        if train:
            RLAlgo.run_rl_algo(itertation)
        else:
            RLAlgo.run_rl_algo()
    elif(algo == BASELINE):
        direction = "RIGHT"
        run_snake_game_baseline(direction, direction)


if __name__ == "__main__":
    main()
