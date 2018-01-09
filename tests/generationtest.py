import unittest

from evolution.generation import Specie, Generation
from evolution.genome import *

class TestSpecieCase(unittest.TestCase):

    def test_genome_added(self):
        specie = Specie()
        specie.add_genome(Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1))
        specie.add_genome(Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1))
        specie.add_genome(Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1))
        self.assertEqual(len(specie.genomes), 3)

    # def test_genomes_fitness_adjusted(self):
    #     specie = Specie()
    #
    #     g1 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
    #     g1.fitness = 9
    #     g2 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
    #     g2.fitness = 1
    #     g3 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
    #     g3.fitness = 3
    #
    #     specie.add_genome(g1)
    #     specie.add_genome(g2)
    #     specie.add_genome(g3)
    #
    #     specie.adjust_fitness()
    #
    #     for (key, genome) in specie.genomes.items():
    #         self.assertAlmostEqual(genome.fitness)
    #
    #     self.assertEqual(specie.genomes[0].fitness, 3)
    #     self.assertAlmostEqual(specie.genomes[1].fitness, 0.333333, 6)
    #     self.assertEqual(specie.genomes[2].fitness, 1)

    def test_specie_fitness(self):
        specie = Specie()

        g1 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g1.fitness = 8
        g2 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g2.fitness = 1
        g3 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g3.fitness = 3

        specie.add_genome(g1)
        specie.add_genome(g2)
        specie.add_genome(g3)

        specie.adjust_fitness()

        self.assertEqual(specie.get_fitness(), 4)

    def test_get_parents(self):
        specie = Specie()

        g1 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g1.fitness = 9
        g2 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g2.fitness = 1
        g3 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g3.fitness = 3
        g4 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g4.fitness = 7
        g5 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g5.fitness = 8
        g6 = Genome([[1, 2, 0, True], [1, 3, 0, True]], 1, 1)
        g6.fitness = 5

        specie.add_genome(g1)
        specie.add_genome(g2)
        specie.add_genome(g3)
        specie.add_genome(g4)
        specie.add_genome(g5)
        specie.add_genome(g6)

        self.assertEqual(sorted([sp.fitness for sp in specie.get_parents(0.5)]), [7, 8, 9])


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

    def test_evolve_xor(self):

        generation = Generation()

        specie = Specie()

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
        print(generation.species[0].get_representative())
        print(generation.fitness)


if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(TestSpecieCase)
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenerationCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)
