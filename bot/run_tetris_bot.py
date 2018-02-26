from evolution.generation import *
from evolution.logger import *
from bot.tetris_phenotype_handler import TetrisPhenotypesHandler

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

    gen = Generation.create_starting_generation(231, 4, 10, TetrisPhenotypesHandler, mutation_coefficients, compatibility_coefficients, population_size=40)
    for i in range(50):
        print(i)
        gen = gen.create_new_generation()
        i += 1