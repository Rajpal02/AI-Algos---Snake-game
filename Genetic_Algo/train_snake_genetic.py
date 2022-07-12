import numpy as np
import os
from .genetic_algo import *
from .genetic_neural_net import *

def run_genetic_algo(count_generations = 100):

    # n1 -> number of input units
    # n2 -> number of units in hidden layer 1
    # n3 -> number of units in hidden layer 2
    # n4 -> number of output units

    # The entire population will obtain "sol_per_population" chromosome.
    sol_per_population = 50
    num_weights = n1*n2 + n2*n3 + n3*n4

    # Population size for the pool.
    population_size = (sol_per_population ,num_weights)
    prev_file = None

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    save_file = curr_dir + "/temp.npz"

    if os.path.exists(save_file):
        prev_file = np.load(save_file)
    prev_gen = 0

    #  Defining the initial population.
    if prev_file:
        population = prev_file['arr_0']
        prev_gen = prev_file['arr_1']
    else:
        population = np.random.choice(np.arange(-1,1,step=0.01),size=population_size,replace=True)

    print("Generations retrieved from prev run ",prev_gen)
    print("Count Generation  ", count_generations)
    count_generations = count_generations - prev_gen

    if(count_generations<=0):
        count_generations=1

    count_parents_mating = 12
    for current_generation in range(count_generations ):
        print('##########        GENERATION COUNT' + str(current_generation)+ '  ############' )
        # Measuring the fitness of each chromosome in the population.
        fitness = fitness_calc(population)
        print('#######  chromosome with highest fitness in gneneration ' + str(current_generation) +'with value:  ', np.max(fitness))
        # Deriving the best parents in the population for mating.
        parents = mate_selection(population, fitness, count_parents_mating)

        # Generating next generation of population using crossover.
        offspring_crossover = get_crossover(parents, child_num=(population_size[0] - parents.shape[0], num_weights))

        # Introducing the variations to the offspring using mutation.
        offspring_mutation = get_mutation(offspring_crossover)

        # Generating new population based on parents and offspring
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = offspring_mutation

        prev_gen=prev_gen+1

    np.savez(save_file, population, prev_gen)
