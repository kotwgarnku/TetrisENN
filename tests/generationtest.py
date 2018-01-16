import unittest

from evolution.generation import Generation, Group
from evolution.genome import *
import math

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
        self.group.calculate_group_adjusted_fitness()

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

class TestGenerationCase(unittest.TestCase):

    # def test_next_generation_the_same(self):
    #     mutation_coefficients = {
    #         'add_connection': 1.0,
    #         'split_connection': 0.0,
    #         'change_weight': 0.0,
    #         'new_connection_abs_max_weight': 5.0,
    #         'max_weight_mutation': 2.5
    #     }
    #     compatibility_coefficients = {
    #         'excess_factor': 2.0,
    #         'disjoint_factor': 2.0,
    #         'weight_difference_factor': 1.0
    #     }
    #
    #     generation = Generation()
    #
    #     specie = Specie()
    #
    #     for i in range(10):
    #         specie.add_genome(Genome([[1, 2, 0, True, 0], [1, 3, 0, True, 1]], 1, 1))
    #
    #     generation.species[0] = specie
    #
    #     generation.create_new_generation(mutation_coefficients, compatibility_coefficients)
    #     print(generation.species[0].genomes)
    #     print(specie.genomes)
    #     #self.assertEqual(generation.species)

    @unittest.skip("skipping for now")
    def test_evolve_xor(self):

        generation = Generation()

        specie = Group()

        c1 = ConnectionGene(1, 3, enabled=True)
        c2 = ConnectionGene(2, 3, enabled=True)

        for i in range(100):
            specie.add_genome(Genome([[1, 3, random.random(), True, 0], [2, 3, random.random(), True, 1]], 2, 1))

        generation.species[0] = specie

        generation.create_new_generation()

        i = 1
        while i < 100:
            generation.create_new_generation()
            i += 1
        print(generation.fitness)


if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(TestSpecieCase)
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenerationCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)
