from evolution.generation import *
from evolution.logger import *
from evolution.logger_visualiser import LoggerVisualiser
from bot.tetris_phenotype_handler import TetrisPhenotypesHandler
from evolution.genome_serialization import genome_to_json
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
    mutation_coefficients = {
        'add_connection': 0.3,
        'split_connection': 0.4,
        'change_weight': 0.8,
        'new_connection_abs_max_weight': 1.5,
        'max_weight_mutation': 0.5
    }

    compatibility_coefficients = {
        'excess_factor': 1.5,
        'disjoint_factor': 1.5,
        'weight_difference_factor': 2.0
    }

    log = Logger()
    gen = Generation.create_starting_generation(13, 4, 4, TetrisPhenotypesHandler, mutation_coefficients,
                                                compatibility_coefficients, population_size=100, logger=log,
                                                compatibility_threshold=0.12)
    for i in range(250):
        print(i)
        time.sleep(5)
        gen = gen.create_new_generation()
        i += 1

        best_genome = gen.best_genome
        f = open('best_genome', mode='w')
        f.write(genome_to_json(best_genome))
        f.close()

    # Remove last generation log(it was created when second to last generation returned new Generation object)
    del log.log[max(log.log.keys())]
    LoggerVisualiser.plot_max_generation_fitness_scores(log)
    LoggerVisualiser.plot_groups_number(log)
    LoggerVisualiser.plot_last_generation_adjusted_fitness_scores(log)

    f = open('best_genome', mode='w')
    f.write(genome_to_json(best_genome))
    f.close()