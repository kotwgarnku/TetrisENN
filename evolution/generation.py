class Generation():
    def __init__(self):
        self.species = {}

    def create_new_generation(self):
        '''
        Creates and returns new Generation of species based on current generation.
        '''
        pass

    def adjust_fitnesses(self):
        '''
        Adjust fitness scores of every genome in every species.
        '''
        pass

    def compute_children_number(self):
        '''
        Computes and returns list of children that every species should have.
        :return:
        '''
        pass


class Species():
    def adjust_genomes_fitnesses(self, generationFitnessScore):
        '''
        Adjusts fitness score of every genome in the species.
        '''
        pass

    def get_parents(self):
        '''
        Returns parents that will reproduce.
        '''
        pass