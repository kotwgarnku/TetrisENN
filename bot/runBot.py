import multiprocessing
from bot.gist import TetrisApp
from evolution.generation import *
from evolution.connection_gene import *
from evolution.logger import *
from bot.tetrisPhenotypeHandler import TetrisPhenotypesHandlerFactory

def create_generation():
    Group._GROUP_ID = 0
    Generation._GENERATION_ID = 0
    specie = Group()
    for i in range(231):
        for j in range(232, 236):
            ConnectionGene(i + 1, j, enabled=True)

    connection_list = []
    z = 0
    for i in range(231):
        for j in range(232, 236):
            connection_list.append([i + 1, j, random.normalvariate(mu=0.0, sigma=1.0), True, z])
            z += 1

    for i in range(20):
        specie.add_genome(Genome(connection_list, 231, 4))

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
    gen = Generation([specie], mutation_coefficients=mutation_coefficients,
                     compatibility_coefficients=compatibility_coefficients, logger=log, phenotype_handler_factory=TetrisPhenotypesHandlerFactory())

    return gen

if __name__ == '__main__':
    gen = create_generation()
    for i in range(50):
        print(i)
        gen = gen.create_new_generation()
        i += 1