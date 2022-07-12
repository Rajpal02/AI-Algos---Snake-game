# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 13:30:43 2022

@author: shriya
"""

from .run_snake_game import run_snake_with_genetic
import numpy as np
from random import randint, uniform


def get_crossover(parent, child_num):
    children = np.empty(child_num)
    for i in range(child_num[0]): 
        while True:
            p1_id = randint(0, parent.shape[0] - 1)
            p2_id = randint(0, parent.shape[0] - 1)
            # check for different parent1 and parent2
            if p1_id != p2_id:
                for j in range(child_num[1]):
                    #random generation of child
                    if uniform(0, 1) < 0.5:
                        children[i, j] = parent[p1_id, j]
                    else:
                        children[i, j] = parent[p2_id, j]
                break
    return children

def get_mutation(children):
    #random mutations in population of children
    for i in range(children.shape[0]):
        for _ in range(25):
            j = randint(0,children.shape[1]-1)

        rand = np.random.choice(np.arange(-1,1,step=0.001),size=(1),replace=False)
        children[i, j] = children[i, j] + rand
    return children

def fitness_calc(population):
    # calculation of fitness for population
    pop_fitness = []
    # fitness for chromosome calculated by running game for each
    pop_len = population.shape[0]
    for i in range(pop_len):
        #running game
        fit_val = run_snake_with_genetic(population[i])
        #print fitness for each
        print('Fitness (Chromosome no. '+ str(i) +') :  ', fit_val)
        pop_fitness.append(fit_val)
    return np.array(pop_fitness)

def mate_selection(population, fit_val, parent_count):
    #Survival of the fittest
    # Mating partners selected on the basis of fitness
    parent = np.empty((parent_count, population.shape[1]))
    for parent_id in range(parent_count):
        fitness_max = np.where(fit_val == np.max(fit_val))
        fitness_max = fitness_max[0][0]
        parent[parent_id, :] = population[fitness_max, :]
        fit_val[fitness_max] = -99999999
    return parent