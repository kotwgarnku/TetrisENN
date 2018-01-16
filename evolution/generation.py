from random import shuffle
from functools import reduce
from threading import Thread
import random
from nn.neuralnetwork import NeuralNetwork
from evolution.genome import Genome
import math


class Generation:
    _GENERATION_ID = 0

    def __init__(self, groups=None, mutation_coefficients=None, compatibility_coefficients=None, compatibility_threshold=6.0, logger=None):

        self.groups = {}
        self.phenotypes = []
        self.logger = None
        self.mutation_coefficients = None
        self.compatibility_coefficients = None
        self.mutation_coefficients = None
        self.r_factor = None
        self.id = self.get_unique_generation_id()

        self._initialize_groups(groups)
        self._initialize_coefficients(mutation_coefficients, compatibility_coefficients, compatibility_threshold)
        self._initialize_logger(logger)

    def _initialize_groups(self, groups):
        if groups is not None:
            for group in groups:
                self.groups[group.get_id()] = group

    def _initialize_logger(self, logger):
        if logger is not None:
            self.logger = logger
            logger.log_coefficients(self.id, self.mutation_coefficients, self.compatibility_coefficients,
                                self.compatibility_threshold, self.r_factor)
            logger.log_groups(self.id, self.groups)

    def _initialize_coefficients(self, mutation_coefficients, compatibility_coefficients, compatibility_threshold):
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
        self.logger.log_phenotypes(self.id, self.phenotypes)
        self.run_phenotypes()

        phenotypes_fitness = self.get_phenotypes_fitness()
        self.update_genomes_fitness_scores(phenotypes_fitness)
        # TODO make love and reproduce below


    def create_phenotypes(self):
        for group in self.groups.values():
            for genome in group.genomes:
                self.phenotypes.append(NeuralNetwork(genome))

    def run_phenotypes(self):
        pass

    def get_phenotypes_fitness(self):
        pass

    def update_genomes_fitness_scores(self, phenotypes_fitness):
        pass

    @staticmethod
    def get_unique_generation_id():
        Generation._GENERATION_ID += 1
        return Generation._GENERATION_ID - 1


class Group:
    _GROUP_ID = 0

    def __init__(self):
        self.genomes = []
        self.group_fitness = None
        self.group_adjusted_fitness = None
        self.id = self.get_unique_group_id()

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

    def get_id(self):
        return self.id

    @staticmethod
    def get_unique_group_id():
        Group._GROUP_ID += 1
        return (Group._GROUP_ID - 1)