import math
import unittest

import matplotlib.pyplot as plt

from evolution.generation import Generation, Group
from evolution.phenotype_handler import PhenotypesHandler
from evolution.genome import *
from evolution.logger import Logger
from nn.neuralnetwork import NeuralNetwork


class TestGroupCase(unittest.TestCase):
    def setUp(self):
        self.genome1 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome2 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome3 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome4 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome5 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome6 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome7 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome1.fitness = 2
        self.genome2.fitness = 0
        self.genome3.fitness = 22
        self.genome4.fitness = 13
        self.genome5.fitness = 2
        self.genome6.fitness = 6
        self.genome7.fitness = 8
        self.group = Group()
        self.group.add_genome(self.genome1)
        self.group.add_genome(self.genome2)
        self.group.add_genome(self.genome3)
        self.group.add_genome(self.genome4)
        self.group.add_genome(self.genome5)
        self.group.add_genome(self.genome6)
        self.group.add_genome(self.genome7)
        self.group.adjust_genomes_fitness()
        self.group.calculate_group_adjusted_fitness_score()

    def test_adjust_genome_fitnesses(self):
        self.assertAlmostEqual(self.genome1.adjusted_fitness, 0.28571428, 5)
        self.assertAlmostEqual(self.genome2.adjusted_fitness, 0)
        self.assertAlmostEqual(self.genome3.adjusted_fitness, 3.14285714, 5)
        self.assertAlmostEqual(self.genome4.adjusted_fitness, 1.8571428, 5)
        self.assertAlmostEqual(self.genome5.adjusted_fitness, 0.28571428, 5)
        self.assertAlmostEqual(self.genome6.adjusted_fitness, 0.85714285, 5)
        self.assertAlmostEqual(self.genome7.adjusted_fitness, 1.14285714, 5)
        self.assertAlmostEqual(self.group.group_adjusted_fitness, sum([self.genome1.adjusted_fitness,
                                               self.genome2.adjusted_fitness,
                                               self.genome3.adjusted_fitness,
                                               self.genome4.adjusted_fitness,
                                               self.genome5.adjusted_fitness,
                                               self.genome6.adjusted_fitness,
                                               self.genome7.adjusted_fitness]))

    def test_get_representative(self):
        for i in range(1000000):
            gen = self.group.get_representative()

    def test_ceil(self):
        self.assertEqual(math.ceil(0.1*1), 1)
        self.assertEqual(math.ceil(0.1*2), 1)
        self.assertEqual(math.ceil(0.1*3), 1)
        self.assertEqual(math.ceil(0.5*1), 1)
        self.assertEqual(math.ceil(0.5*3), 2)
        self.assertEqual(math.ceil(0.1*1), 1)
        self.assertEqual(math.ceil(0.9*12), 11)
        self.assertEqual(math.ceil(0.1*0), 0)
        self.assertEqual(math.ceil(0*11), 0)

    def test_get_parents(self):
        parents = self.group.get_parents(0.3)
        self.assertIs(parents[0], self.genome3)
        self.assertIs(parents[1], self.genome4)
        self.assertIs(parents[2], self.genome7)

    def test_create_phenotypes(self):
        generation = Generation()
        generation.groups[0] = self.group
        generation.create_phenotypes()
        first_phenotype = generation.phenotypes[0]
        self.assertEqual(1 in first_phenotype._neurons, True)
        self.assertEqual(2 in first_phenotype._neurons, True)
        self.assertEqual(3 in first_phenotype._neurons, True)
        self.assertEqual(4 in first_phenotype._neurons, True)
        self.assertEqual(5 in first_phenotype._neurons, False)
        self.assertEqual(1 in first_phenotype._input_neurons, True)
        self.assertEqual(2 in first_phenotype._input_neurons, True)
        self.assertEqual(3 in first_phenotype._input_neurons, False)
        self.assertEqual(4 in first_phenotype._input_neurons, False)
        self.assertEqual(5 in first_phenotype._input_neurons, False)
        self.assertEqual(1 in first_phenotype._output_neurons, False)
        self.assertEqual(2 in first_phenotype._output_neurons, False)
        self.assertEqual(3 in first_phenotype._output_neurons, True)
        self.assertEqual(4 in first_phenotype._output_neurons, False)
        self.assertEqual(5 in first_phenotype._output_neurons, False)
        self.assertIs(first_phenotype._genome, self.genome1)


class TestGenerationSecondCase(unittest.TestCase):
    @unittest.skip("skipping")
    def test_calculating_offsprings(self):
        Group._GROUP_ID = 0
        Generation._GENERATION_ID = 0
        genome1 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome2 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome3 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome4 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome5 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome6 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome7 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        group1 = Group()
        group2 = Group()
        group1.add_genome(genome1)
        group1.add_genome(genome2)
        group1.add_genome(genome3)
        group1.add_genome(genome4)
        group2.add_genome(genome5)
        group2.add_genome(genome6)
        group2.add_genome(genome7)
        generation = Generation([group1, group2])
        generation.create_phenotypes()
        generation.run_phenotypes()
        generation.update_genomes_fitness_scores(generation.get_phenotypes_fitness_scores())
        generation.adjust_genomes_fitness_scores()
        a = generation.calculate_groups_adjusted_fitness_scores()
        offspring_count = generation.calculate_groups_offsprings(a, sum(a.values()))
        self.assertEqual(offspring_count[0], 50)
        self.assertEqual(offspring_count[1], 50)
        genome1.adjusted_fitness = 1
        a = generation.calculate_groups_adjusted_fitness_scores()
        offspring_count = generation.calculate_groups_offsprings(a, sum(a.values()))
        self.assertEqual(offspring_count[0], 64)
        self.assertEqual(offspring_count[1], 36)

    def test_making_new_generation(self):
        Group._GROUP_ID = 0
        Generation._GENERATION_ID = 0
        genome1 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome2 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome3 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome4 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome5 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome6 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        genome7 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        group1 = Group()
        group2 = Group()
        group1.add_genome(genome1)
        group1.add_genome(genome2)
        group1.add_genome(genome3)
        group1.add_genome(genome4)
        group2.add_genome(genome5)
        group2.add_genome(genome6)
        group2.add_genome(genome7)
        generation = Generation([group1, group2])

class TestLoggerCase(unittest.TestCase):
    def setUp(self):
        Group._GROUP_ID = 0
        Generation._GENERATION_ID = 0
        self.genome1 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome2 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome3 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome4 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome5 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome6 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome7 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome1.fitness = 2
        self.genome2.fitness = 0
        self.genome3.fitness = 22
        self.genome4.fitness = 13
        self.genome5.fitness = 2
        self.genome6.fitness = 6
        self.genome7.fitness = 8
        self.group = Group()
        self.group.add_genome(self.genome1)
        self.group.add_genome(self.genome2)
        self.group.add_genome(self.genome3)
        self.group.add_genome(self.genome4)
        self.group.add_genome(self.genome5)
        self.group.add_genome(self.genome6)
        self.group.add_genome(self.genome7)
        self.logger = Logger()
        self.generation = Generation([self.group], logger=self.logger)

    def test_logging(self):
        self.assertIs(self.logger.log[0].groups_log[0], self.group)


    #TODO test logging fitness scores and other things

class TestGenerationCase(unittest.TestCase):

    def test_simple_xor(self):
        print("testing simple xor")
        Group._GROUP_ID = 0
        Generation._GENERATION_ID = 0
        specie = Group()
        for i in range(16):
            for j in range(17, 21):
                ConnectionGene(i + 1, j,enabled=True)

        connection_list = []
        z = 0
        for i in range(16):
            for j in range(17, 21):
                connection_list.append([i + 1, j, random.normalvariate(mu=0.0, sigma=1.0), True, z])
                z += 1
        print(connection_list)
        for i in range(10):
            specie.add_genome(Genome([[1, 3, random.normalvariate(mu=0.0, sigma=1.0), True, 0],
                                     [2, 3, random.normalvariate(mu=0.0, sigma=1.0), True, 1]], 2, 1))


        mutation_coefficients = {
            'add_connection': 0.5,
            'split_connection': 0.2,
            'change_weight': 0.8,
            'new_connection_abs_max_weight': 1.0,
            'max_weight_mutation': 0.5
        }
        compatibility_coefficients = {
            'excess_factor': 1.0,
            'disjoint_factor': 1.0,
            'weight_difference_factor': 2.0
        }
        log = Logger()

        class XorPhenotypesHandler(PhenotypesHandler):
            def run_all_phenotypes(self):
                if Generation.best_genome is None:
                    Generation.best_genome = self._neural_networks[0]._genome

                for nn in self._neural_networks:
                    fitness = 4.0

                    Y1 = nn.forward([0.0, 0.0])
                    fitness -= ((Y1[0] - 0) ** 2)

                    Y2 = nn.forward([0.0, 1.0])
                    fitness -= ((Y2[0] - 1) ** 2)

                    Y3 = nn.forward([1.0, 0.0])
                    fitness -= ((Y3[0] - 1) ** 2)

                    Y4 = nn.forward([1.0, 1.0])
                    fitness -= ((Y4[0] - 0) ** 2)

                    nn._genome.fitness = (fitness)
                    if fitness > Generation.best_genome.fitness:
                        Generation.best_genome = nn._genome
                        Generation.best_fitnesses[Generation._GENERATION_ID - 1] = fitness


        gen = Generation([specie], mutation_coefficients=mutation_coefficients,
                         compatibility_coefficients=compatibility_coefficients, logger=log,
                         phenotype_handler=XorPhenotypesHandler)

        i = 1
        while i < 50:
            print(i)
            gen = gen.create_new_generation()
            i += 1

        best_nn = NeuralNetwork(Generation.best_genome)
        a = (best_nn.forward([0.0, 0.0]))
        b = (best_nn.forward([0.0, 1.0]))
        c = (best_nn.forward([1.0, 0.0]))
        d = (best_nn.forward([1.0, 1.0]))
        print(a)
        print(b)
        print(c)
        print(d)


        print(4.0 - (a[0]-0)**2 - (b[0]-1)**2 - (c[0]-1)**2 - (d[0]-0)**2)
        print(best_nn._genome.fitness)

        groups_count = []
        for generation_log in gen.logger.log.values():
            groups_count.append(len(generation_log.groups_log))

        plt.plot(list(gen.logger.log.keys()), groups_count)
        plt.xlabel("Generation")
        plt.ylabel("Number of groups")
        plt.title("Groups amount change over evolution")
        plt.savefig("plot of gen count")
        plt.clf()

        last_gen_groups_fitness = []
        for fit in gen.logger.log[gen.id-1].groups_fitness_scores_log.values():
            last_gen_groups_fitness.append(fit[0][2])
        plt.plot(list(gen.logger.log[gen.id-1].groups_log.keys()), last_gen_groups_fitness, 'ro')
        plt.xlabel("Group")
        plt.ylabel("Group adjusted fitness")
        plt.title("Adjusted fitness of groups in last generation")
        plt.savefig("plot of last gen fitness")
        plt.clf()


        plt.plot(list(Generation.best_fitnesses.keys()), list(Generation.best_fitnesses.values()))
        plt.xlabel("Generation")
        plt.ylabel("Fitness score")
        plt.title("Fitness score progression")
        plt.savefig("plot of fitness")

if __name__ == '__main__':
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenerationCase)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)
