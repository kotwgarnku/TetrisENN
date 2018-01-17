from random import shuffle
from functools import reduce
from threading import Thread
import random
from nn.neuralnetwork import NeuralNetwork
from evolution.genome import Genome
import math
import numpy as np


class PhenotypesHandler:
    def __init__(self, phenotypes):
        self._input = input
        self._neural_networks = phenotypes
        self._signal_provider = None

        self._connect_to_signals_provider()

    def run_all_phenotypes(self):
        #Implementation below is just for mocking
        for nn in self._neural_networks:
            nn.forward(np.ones(len(nn._input_neurons)))

        for nn in self._neural_networks:
            nn._genome.fitness = 1

    def run_all_phenotypes2(self):
        for nn in self._neural_networks:
            nn.forward(np.ones(len(nn._input_neurons)))

        for nn in self._neural_networks:
            nn._genome.fitness = random.uniform(0.1, 8)

    def get_phenotypes_fitness_scores(self):
        phenotypes_fitnesses = []
        for nn in self._neural_networks:
            phenotypes_fitnesses.append(nn._genome.fitness)
        return phenotypes_fitnesses

    def _connect_to_signals_provider(self):
        """
        This method connects PhenotypesHandler to some object that will provide it with inputs and that will handle
        neural networks outputs
        :return:
        """
        #self._signal_provider = Game()
        pass


class Generation:
    #ID for logging purpose
    _GENERATION_ID = 0

    def __init__(self, groups=None, mutation_coefficients=None, compatibility_coefficients=None, compatibility_threshold=6.0, logger=None):

        self.groups = {}
        self.phenotypes = []
        self.logger = None
        self.handler = None

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
                                self.compatibility_threshold, self.r_factor, self.population_size)
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
        else:
            self.mutation_coefficients = mutation_coefficients

        if compatibility_coefficients is None:
            self.compatibility_coefficients = {
                'excess_factor': 2.0,
                'disjoint_factor': 2.0,
                'weight_difference_factor': 1.0
            }
        else:
            self.compatibility_coefficients = compatibility_coefficients

        self.compatibility_threshold = compatibility_threshold
        self.r_factor = 0.2
        self.population_size = 100

    def create_new_generation(self):
        self.create_phenotypes()
        if self.logger is not None:
            self.logger.log_phenotypes(self.id, self.phenotypes)
        self.run_phenotypes2()

        if self.logger is not None:
            self.logger.log_phenotypes_fitness_scores(self.id)
        phenotypes_fitness = self.get_phenotypes_fitness_scores()
        self.update_genomes_fitness_scores(phenotypes_fitness)

        # After running all phenotypes and getting their fitness scores we can start reproducing
        self.adjust_genomes_fitness_scores()
        group_scores = self.calculate_groups_adjusted_fitness_scores()
        total_generation_score = sum(group_scores.values())
        if self.logger is not None:
            self.logger.log_groups_fitness_scores(self.id)

        # After calculating all groups fitness scores we calculate the amount of offsprings in each group
        offspring_count = self.calculate_groups_offsprings(group_scores, total_generation_score)
        if len(offspring_count) != len(self.groups):
            raise Exception("Length of offspring amount list nad length of groups doesn't match.")

        # And now we create offsprings for every group
        new_groups = []
        for (group_key, group_offspring_amount) in offspring_count.items():
            if group_key not in self.groups:
                raise Exception("There is no group with such a ID in generation")
            new_groups.append(Group(group_key, self.get_offsprings_from_group(group_key, group_offspring_amount)))

        # And return new generation
        return Generation(new_groups, self.mutation_coefficients, self.compatibility_coefficients,
                          36.0, self.logger)


    def create_phenotypes(self):
        for group in self.groups.values():
            for genome in group.genomes:
                self.phenotypes.append(NeuralNetwork(genome))

    def run_phenotypes(self):
        self.handler = PhenotypesHandler(self.phenotypes)
        self.handler.run_all_phenotypes()

    def run_phenotypes2(self):
        self.handler = PhenotypesHandler(self.phenotypes)
        self.handler.run_all_phenotypes2()

    def get_phenotypes_fitness_scores(self):
        return self.handler.get_phenotypes_fitness_scores()

    def update_genomes_fitness_scores(self, phenotypes_fitness_scores):
        for phenotype, phenotype_score in zip(self.phenotypes, phenotypes_fitness_scores):
            if phenotype_score is None:
                raise Exception("Fitness score is none")
            phenotype._genome.fitness = phenotype_score

    def adjust_genomes_fitness_scores(self):
        for group in self.groups.values():
            group.adjust_genomes_fitness()

    def calculate_groups_adjusted_fitness_scores(self):
        groups_adjusted_fitness_scores = {}
        for group in self.groups.values():
            groups_adjusted_fitness_scores[group.id] = group.calculate_group_adjusted_fitness_score()
        return groups_adjusted_fitness_scores

    def calculate_groups_offsprings(self, group_scores, total_generation_score):
        offspring_count = {}
        for group_id, group_score in group_scores.items():
            offspring_count[group_id] = round((float(group_score)/float(total_generation_score)) * self.population_size)

        if(sum(offspring_count.values()) != self.population_size):
            raise Exception(("Amount of offsprings does not sum up to population size.[Sum = " + str(offspring_count) +
                            " | Population size: " + str(self.population_size)))
        return offspring_count

    def get_offsprings_from_group(self, group_key, group_offspring_amount):
        group_to_reproduce = self.groups[group_key]
        parents = group_to_reproduce.get_parents(self.r_factor)
        offsprings = []

        while(len(offsprings) != group_offspring_amount):
            first_parent = random.choice(parents)
            second_parent = random.choice(parents)
            # Make a child
            offspring = Genome.reproduce(first_parent, second_parent)
            # Mutate it
            offspring.mutate(self.mutation_coefficients)
            # Now try to fit it into this group
            offsprings.append(offspring)

        return offsprings

    @staticmethod
    def get_unique_generation_id():
        Generation._GENERATION_ID += 1
        return Generation._GENERATION_ID - 1


class Group:
    #ID for logging purpose
    _GROUP_ID = 0

    def __init__(self, id=None, genomes=None):
        if id is not None and genomes is not None:
            self.id = id
            self.genomes = genomes
            self.group_adjusted_fitness = None
        else:
            self.genomes = []
            self.group_adjusted_fitness = None
            self.id = self.get_unique_group_id()

    def add_genome(self, genome):
        self.genomes.append(genome)

    def remove_all_genomes(self):
        self.genomes.clear()

    def adjust_genomes_fitness(self):
        """
        Adjusts fitness score of every genome in the species.
        """
        for genome in self.genomes:
            genome.adjusted_fitness = genome.fitness/float(len(self.genomes))

    def calculate_group_adjusted_fitness_score(self):
        """
        Sum all of genomes adjusted fitnesses
        :return:
        """
        total = 0
        for genome in self.genomes:
            total += genome.adjusted_fitness
        self.group_adjusted_fitness = total
        return total

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