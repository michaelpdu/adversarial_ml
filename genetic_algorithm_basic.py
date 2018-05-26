"""
Visualize Genetic Algorithm to find a maximum point in a function.
Visit my tutorial website for more: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
from logging import *
# from calc_trendx_prediction import *

class GeneticAlgorithmHelper:

    def __init__(self, config):
        self.DNA_SIZE = config["dna_size"]                 # DNA length
        self.POP_SIZE = config["population_size"]          # population size
        self.CROSS_RATE = config["mating_prob"]            # mating probability (DNA crossover)
        self.MUTATION_RATE = config["mutation_prob"]       # mutation probability
        self.N_GENERATIONS = config["generations"]         # number of generations

        self.adv = None
        self.calc_callback_ = None
        self.msg_callback_ = None

    def set_adv(self, adv):
        self.adv = adv

    def set_calc_callback(self, callback):
        self.calc_callback_ = callback

    def set_msg_callback(self, callback):
        self.msg_callback_ = callback

    # def F(x): return np.sin(10*x)*x + np.cos(2*x)*x     # to find the maximum of this function
    def F(self, x):
        # return self.adv.calc_trendx_prediction(x)
        return self.calc_callback_(x)

    # find non-zero fitness for selection
    def get_fitness(self, pred):
        return pred + 1e-3 - np.min(pred)

    def select(self, pop, fitness):    # nature selection wrt pop's fitness
        idx = np.random.choice(np.arange(self.POP_SIZE), size=self.POP_SIZE, replace=True,
                               p=fitness/fitness.sum())
        return pop[idx]

    def crossover(self, parent, pop):     # mating process (genes crossover)
        if np.random.rand() < self.CROSS_RATE:
            i_ = np.random.randint(0, self.POP_SIZE, size=1)                             # select another individual from pop
            cross_points = np.random.randint(0, 2, size=self.DNA_SIZE).astype(np.bool)   # choose crossover points
            parent[cross_points] = pop[i_, cross_points]                                 # mating and produce one child
        return parent

    def mutate(self, child):
        for point in range(self.DNA_SIZE):
            if np.random.rand() < self.MUTATION_RATE:
                child[point] = 1 if child[point] == 0 else 0
        return child

    def evolution(self):
        # generate random DNA
        pop = np.random.randint(2, size=(self.POP_SIZE, self.DNA_SIZE))   # initialize the pop DNA

        max_value = 0
        most_dna = []

        for _ in range(self.N_GENERATIONS):
            F_values = self.F(pop)

            # GA part (evolution)
            fitness = self.get_fitness(F_values)
            dna = pop[np.argmax(fitness), :]
            value = F_values[np.argmax(fitness)]
            # print(type(dna))
            # dump message
            self.msg_callback_(_, dna.tolist(), value)

            if max_value < value:
                max_value = value
                most_dna = dna.tolist()
            pop = self.select(pop, fitness)
            pop_copy = pop.copy()
            for parent in pop:
                child = self.crossover(parent, pop_copy)
                child = self.mutate(child)
                parent[:] = child       # parent is replaced by its child
        return (most_dna,max_value)
