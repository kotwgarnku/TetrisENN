from random import shuffle
from functools import reduce
from threading import Thread
import random
from nn import NeuralNetwork
from evolution import Genome


class Evaluate(Thread):
    def __init__(self, nn):
        Thread.__init__(self)
        self._neural_network = nn
        self._fitness = None

    def run(self):
        self._neural_network.forward()

    def join(self):
        Thread.join(self)
        return self._fitness


class Generation:
    def __init__(self):
        self.species = {}
        self.fitness = None

    def create_new_generation(self):
        """
        Creates and returns new Generation of species based on current generation.
        """

        # get phenotype for each genome
        phenotypes = [phenotype for specie in self.species for phenotype in specie.get_phenotypes()]

        # create thread to calculate fitness for each neural network
        threads = [Evaluate(phenotype) for phenotype in phenotypes]

        for thread in threads:
            thread.start()

        # wait for all networks to end their tasks
        phenotypes_fitness = [thread.join() for thread in threads]

        # each genome gets fitness of it's phenotype
        for (phenotype, fitness) in zip(phenotypes, phenotypes_fitness):
            phenotypes.get_genome().fitness = fitness

        # divide each fitness in specie by specie size
        for specie in self.species:
            specie.adjust_fitness()

        # calculate mean generation fitness
        generation_fitness = sum(phenotypes_fitness) / float(len(phenotypes_fitness))

        # TODO: make 'coefficients' parameters
        reproduce_coefficients = {
            'add_connection': 0.3,
            'split_connection': 0.2,
            'change_weight': 0.5,
            'new_connection_abs_max_weight': 5.0,
            'max_weight_mutation': 2.5
        }

        compatibility_coefficients = {
            'excess_factor': 2.0,
            'disjoint_factor': 2.0,
            'weight_difference_factor': 1.0
        }

        for specie in self.species:
            specie_offspring_len = int(specie.get_fitness() / generation_fitness)
            # TODO: make 'r' a parameter
            parents = specie.get_parents(0.2)
            specie_parents = specie.genomes.keys()

            for i in range(specie_offspring_len):
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)

                offspring = Genome.reproduce(parent1, parent2)

                offspring.mutate(reproduce_coefficients)

                compatibility = offspring.compatibility_distance(specie.get_representative(), compatibility_coefficients)
                
                specie_found = False
                # favor parents' specie
                # TODO: add compatibility_threshold
                if compatibility < compatibility_threshold:
                    specie.add_genome(offspring)
                    specie_found = True
                else:
                    for sp in self.species:
                        compatibility = offspring.compatibility_distance(sp.get_representative(), compatibility_coefficients)
                        if compatibility < compatibility_threshold:
                            sp.add_genome(offspring)
                            specie_found = True
                            break
                if not specie_found:
                    # create new specie with offspring as it's representative
                    new_specie = Specie()
                    new_specie.add_genome(offspring)
                    self.species[len(self.species)] = new_specie

            # remove parents leaving only children in new specie
            for i in range(specie_parents):
                del specie[i]


class Specie:
    def __init__(self):
        self.genomes = {}
    
    def add_genome(self, genome):
        self.genomes[len(self.genomes)] = genome

    def adjust_fitness(self):
        """
        Adjusts fitness score of every genome in the species.
        """
        for genome in self.genomes:
            genome.fitness /= float(len(self.genomes))

    def get_fitness(self):
        return reduce(lambda x, y: x.fitness + y.fitness, self.genomes)

    def get_phenotypes(self):
        return [NeuralNetwork(genome) for genome in self.genomes]

    def get_representative(self):
        return random.choice(self.genomes)

    def get_parents(self, r):
        """
        Returns parents that will reproduce.
        """
        # sort genomes by fitness
        genomes = sorted([genome for genome in self.genomes], lambda x, y: x.fitness > y.fitness)
        # get r% of best-performing genomes
        genomes = genomes[:int(r*len(genomes))]
        shuffle(genomes)
        return genomes
