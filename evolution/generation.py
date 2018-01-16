from random import shuffle
from functools import reduce
from threading import Thread
import random
from nn.neuralnetwork import NeuralNetwork
from evolution.genome import Genome
import math

class Generation:

    def __init__(self, mutation_coefficients=None, compatibility_coefficients=None, compatibility_threshold=6.0):

        if mutation_coefficients is None:
            self.mutation_coefficients = {
                'add_connection': 0.1,
                'split_connection': 0.3,
                'change_weight': 0.5,
                'new_connection_abs_max_weight': 1.0,
                'max_weight_mutation': 0.5
            }
        if compatibility_coefficients is None:
            self.compatibility_coefficients = {
                'excess_factor': 2.0,
                'disjoint_factor': 2.0,
                'weight_difference_factor': 1.0
            }
        self.compatibility_threshold = compatibility_threshold
        self.r_factor = 0.2

    def create_new_generation(self):
        self.create_phenotypes()
        self.run_phenotypes()
        phenotypes_fitness = self.get_phenotypes_fitness()
        self.update_genomes_fitness_scores(phenotypes_fitness)
        # TODO make love and reproduce below


    def create_phenotypes(self):
        pass

    def run_phenotypes(self):
        pass

    def get_phenotypes_fitness(self):
        pass

    def update_genomes_fitness_scores(self, phenotypes_fitness):
        pass


class Group:

    def __init__(self):
        self.genomes = []
        self.group_fitness = None
        self.group_adjusted_fitness = None

    def add_genome(self, genome):
        self.genomes.append(genome)


    def adjust_genomes_fitness(self):
        """
        Adjusts fitness score of every genome in the species.
        """
        for genome in self.genomes:
            genome.adjusted_fitness = genome.fitness/float(len(self.genomes))

    def calculate_group_adjusted_fitness(self):
        """
        Sum all of genomes adjusted fitnesses
        :return:
        """
        total = 0
        for genome in self.genomes:
            total += genome.adjusted_fitness
        self.group_adjusted_fitness = total

    def get_representative(self):
        if not self.genomes:
            raise Exception("Cannot return representative, because the genome list is empty!")

        return random.choice(self.genomes)

    def get_parents(self, r):
        number_of_parents = math.ceil(r*len(self.genomes))
        sorted_genomes = sorted(self.genomes, key = lambda x: x.adjusted_fitness, reverse=True)

        return sorted_genomes[:number_of_parents]