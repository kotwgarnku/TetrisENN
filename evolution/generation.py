from random import shuffle
from functools import reduce
from threading import Thread
import random
from nn.neuralnetwork import NeuralNetwork
from evolution.genome import Genome
import math


class Evaluate(Thread):
    def __init__(self, nn):
        Thread.__init__(self)
        self._neural_network = nn
        self._fitness = None

    def run(self):
        self._fitness = 0
        self._fitness += 5*math.exp(-(self._neural_network.forward([1, 1])[0] - 0)**2)
        self._fitness += 5*math.exp(-(self._neural_network.forward([1, 0])[0] - 1)**2)
        self._fitness += 5*math.exp(-(self._neural_network.forward([0, 0])[0] - 0)**2)
        self._fitness += 5*math.exp(-(self._neural_network.forward([0, 1])[0] - 1)**2)

    def join(self):
        Thread.join(self)
        return self._fitness


class Generation:
    _specie_number = 0

    def __init__(self, mutation_coefficients=None, compatibility_coefficients=None, compatibility_threshold=6.0):
        self.species = {}
        self.fitness = None

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
        """
        Creates and returns new Generation of species based on current generation.
        """

        # get phenotype for each genome
        phenotypes = [phenotype for specie in self.species.values() for phenotype in specie.get_phenotypes()]

        # create thread to calculate fitness for each neural network
        threads = [Evaluate(phenotype) for phenotype in phenotypes]

        for thread in threads:
            thread.start()

        # wait for all networks to end their tasks
        phenotypes_fitness = []

        for thread in threads:
            phenotypes_fitness.append(thread.join())

        print(phenotypes_fitness)

        # each genome gets fitness of it's phenotype
        for (phenotype, fitness) in zip(phenotypes, phenotypes_fitness):
            phenotype.get_genome().fitness = fitness

        # divide each fitness in specie by specie size
        for specie in self.species.values():
            specie.adjust_fitness()

        # calculate mean adjusted generation fitness
        self.fitness = sum(phenotypes_fitness) / float(len(phenotypes_fitness)**2)

        # create place for new species
        new_species = {k: Specie() for k in self.species.keys()}

        for (key, specie) in self.species.items():
            specie_offspring_len = round(specie.get_fitness() / self.fitness)
            parents = specie.get_parents(self.r_factor)

            # create specie_offspring_len children
            for i in range(specie_offspring_len):
                # create child
                offspring = Specie.get_offspring(parents)
                # mutate it
                offspring.mutate(self.mutation_coefficients)

                # select specie for the child

                # favor parents' specie
                if self._is_specie_fitting_for_offspring(specie, offspring):
                    new_species[key].add_genome(offspring)
                    continue
                # child does not fit in parents' specie
                # check if it does in some other specie
                else:
                    fitting_specie_found = False
                    for (key, specie) in self.species.items():
                        if self._is_specie_fitting_for_offspring(specie, offspring):
                            new_species[key].add_genome(offspring)
                            fitting_specie_found = True
                            break
                # child does not fit in any of the current species
                # create new species and add child as it's representative
                if not fitting_specie_found:
                    # create new specie with offspring as it's representative
                    new_specie = Specie()
                    new_specie.add_genome(offspring)
                    new_species[Generation._get_new_specie_number()] = new_specie

        self.species = new_species

    def _is_specie_fitting_for_offspring(self, specie, offspring):
        is_fitting = False
        compatibility_distance = offspring.compatibility_distance(specie.get_representative(), self.compatibility_coefficients)

        if compatibility_distance < self.compatibility_threshold:
            specie.add_genome(offspring)
            is_fitting = True

        return is_fitting

    @staticmethod
    def _get_new_specie_number():
        Generation._specie_number += 1
        return Generation._specie_number - 1

class Specie:
    _genome_number = 0

    def __init__(self):
        self.genomes = {}
        self.fitness = None

    def add_genome(self, genome):
        self.genome_number = Specie._get_new_genome_number()
        self.genomes[self.genome_number] = genome

    def adjust_fitness(self):
        """
        Adjusts fitness score of every genome in the species.
        """
        for genome in self.genomes.values():
            genome.fitness /= float(len(self.genomes))

        self.fitness = sum(genome.fitness for genome in self.genomes.values())

    def get_fitness(self):
        return self.fitness

    def get_phenotypes(self):
        return [NeuralNetwork(genome) for genome in self.genomes.values()]

    def get_representative(self):
        return random.choice(list(self.genomes.values()))

    def get_parents(self, r):
        """
        Returns parents that will reproduce.
        """
        # sort genomes by fitness
        genomes = sorted([genome for genome in self.genomes.values()], key=lambda x: x.fitness, reverse=True)
        # get r% of best-performing genomes ( minimum 2 )
        count_to_return = max(round(r*len(genomes)), 2)
        genomes = genomes[:count_to_return]
        shuffle(genomes)
        return genomes

    @staticmethod
    def get_offspring(parents):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        offspring = Genome.reproduce(parent1, parent2)

        return offspring

    @staticmethod
    def _get_new_genome_number():
        Specie._genome_number += 1
        return Specie._genome_number - 1