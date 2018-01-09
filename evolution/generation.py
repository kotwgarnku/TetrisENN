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
    def __init__(self):
        self.species = {}
        self.fitness = None

    def create_new_generation(self, mutation_coefficients=None, compatibility_coefficients=None, compatibility_threshold=6.0):
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

        # calculate mean generation fitness
        self.fitness = sum(phenotypes_fitness) / float(len(phenotypes_fitness)**2)

        # TODO: make 'coefficients' parameters
        if mutation_coefficients is None:
            mutation_coefficients = {
                'add_connection': 0.3,
                'split_connection': 0.2,
                'change_weight': 0.5,
                'new_connection_abs_max_weight': 1.0,
                'max_weight_mutation': 0.5
            }
        if compatibility_coefficients is None:
            compatibility_coefficients = {
                'excess_factor': 2.0,
                'disjoint_factor': 2.0,
                'weight_difference_factor': 1.0
            }

        new_species = []
        for specie in self.species.values():
            specie_offspring_len = round(specie.get_fitness() / self.fitness)
            # TODO: make 'r' a parameter
            parents = specie.get_parents(0.2)
            if len(parents) == 0:
                continue
            specie_parents = list(specie.genomes.keys())

            for i in range(specie_offspring_len):
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)

                offspring = Genome.reproduce(parent1, parent2)

                offspring.mutate(mutation_coefficients)

                compatibility_distance = offspring.compatibility_distance(specie.get_representative(), compatibility_coefficients)
                
                specie_found = False
                # favor parents' specie
                # TODO: add compatibility_threshold
                if compatibility_distance < compatibility_threshold:
                    specie.add_genome(offspring)
                    specie_found = True
                else:
                    for sp in self.species.values():
                        if len(sp.genomes) == 0:
                            continue
                        compatibility_distance = offspring.compatibility_distance(sp.get_representative(), compatibility_coefficients)
                        if compatibility_distance < compatibility_threshold:
                            sp.add_genome(offspring)
                            specie_found = True
                            break
                if not specie_found:
                    for sp in new_species:
                        compatibility_distance = offspring.compatibility_distance(sp.get_representative(),
                                                                                  compatibility_coefficients)
                        if compatibility_distance < compatibility_threshold:
                            sp.add_genome(offspring)
                            specie_found = True
                            break
                    if specie_found:
                        continue
                    # create new specie with offspring as it's representative
                    new_specie = Specie()
                    new_specie.add_genome(offspring)
                    new_species.append(new_specie)

            # remove parents leaving only children in new specie
            for i in specie_parents:
                del specie.genomes[i]
        for specie in new_species:
            self.species[len(self.species)] = specie

class Specie:
    def __init__(self):
        self.genomes = {}
    
    def add_genome(self, genome):
        self.genomes[len(self.genomes)] = genome

    def adjust_fitness(self):
        """
        Adjusts fitness score of every genome in the species.
        """
        for genome in self.genomes.values():
            genome.fitness /= float(len(self.genomes))

    def get_fitness(self):
        return sum(genome.fitness for genome in self.genomes.values())

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
        # get r% of best-performing genomes
        genomes = genomes[:round(r*len(genomes))]
        shuffle(genomes)
        return genomes
