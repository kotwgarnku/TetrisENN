from evolution.generation import *
from evolution.logger import *
from bot.tetris_phenotype_handler import TetrisPhenotypesHandler
from evolution.genome_serialization import genome_to_json
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    mutation_coefficients = {
        'add_connection': 0.5,
        'split_connection': 0.2,
        'change_weight': 0.8,
        'new_connection_abs_max_weight': 2.0,
        'max_weight_mutation': 0.5
    }

    compatibility_coefficients = {
        'excess_factor': 1.5,
        'disjoint_factor': 1.5,
        'weight_difference_factor': 2.0
    }
    log = Logger()

    gen = Generation.create_starting_generation(10, 4, 1, TetrisPhenotypesHandler, mutation_coefficients, compatibility_coefficients, population_size=1)
    for i in range(4):
        print(i)
        time.sleep(5)
        gen = gen.create_new_generation()
        i += 1
    best_genome = gen.best_genome

    groups_count = []
    for generation_log in gen.logger.log.values():
        groups_count.append(len(generation_log.groups_log))

    plt.plot(list(gen.logger.log.keys()), groups_count)
    plt.xlabel("Generation")
    plt.ylabel("Number of groups")
    plt.title("Groups amount change over evolution")
    plt.savefig("plot of gen count_tetris")
    plt.clf()

    last_gen_groups_fitness = []
    for fit in gen.logger.log[gen.id - 1].groups_fitness_scores_log.values():
        last_gen_groups_fitness.append(fit[0][2])
    plt.plot(list(gen.logger.log[gen.id - 1].groups_log.keys()), last_gen_groups_fitness, 'ro')
    plt.xlabel("Group")
    plt.ylabel("Group adjusted fitness")
    plt.title("Adjusted fitness of groups in last generation")
    plt.savefig("plot of last gen fitness_tetris")
    plt.clf()

    plt.plot(list(Generation.best_fitnesses.keys()), list(Generation.best_fitnesses.values()))
    plt.xlabel("Generation")
    plt.ylabel("Fitness score")
    plt.title("Fitness score progression")
    plt.savefig("plot of fitness_tetris")

    f = open('best_genome', mode='w')
    f.write(genome_to_json(best_genome))
    f.close()