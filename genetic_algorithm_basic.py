"""
Visualize Genetic Algorithm to find a maximum point in a function.
Visit my tutorial website for more: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
from calc_trendx_prediction import *

class GeneticAlgorithmHelper:

    def __init__(self, adv):
        self.DNA_SIZE = 32            # DNA length
        self.POP_SIZE = 100           # population size
        self.CROSS_RATE = 0.8         # mating probability (DNA crossover)
        self.MUTATION_RATE = 0.003    # mutation probability
        self.N_GENERATIONS = 100

        self.adv = adv

    def set_dna_size(self, size):
        self.DNA_SIZE = size

    # def F(x): return np.sin(10*x)*x + np.cos(2*x)*x     # to find the maximum of this function
    def F(self, x):
        return self.adv.calc_trendx_prediction(x)

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
            parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
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
            msg = "G{}: Most fitted DNA: {}, and value: {}".format(_, dna, value)
            info(msg)
            print(msg)
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
