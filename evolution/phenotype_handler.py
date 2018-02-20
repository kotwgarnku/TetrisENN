from abc import ABCMeta

class PhenotypesHandler:
    '''
    General class that should be (for convenience) inherited
    '''
    def __init__(self, phenotypes):
        self._input = input
        self._neural_networks = phenotypes
        self._signal_provider = None

    def run_all_phenotypes(self):
        #Implementation below is just for mocking
        raise Exception("Custom run phenotype handler method was not implemented.")


    def get_phenotypes_fitness_scores(self):
        phenotypes_fitnesses = []
        for nn in self._neural_networks:
            phenotypes_fitnesses.append(nn._genome.fitness)
        return phenotypes_fitnesses