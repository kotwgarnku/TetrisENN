from evolution.generation import Generation, Group

class Logger:
    def __init__(self):
        self.log = {}

    def log_coefficients(self, id, mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor, population_size):
        self._check_if_record_exists(id)
        self.log[id].add_coefficients_to_log(mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor, population_size)

    def log_groups(self, id, groups):
        self._check_if_record_exists(id)
        self.log[id].add_groups_to_log(groups)

    def log_phenotypes(self, id, phenotypes):
        self._check_if_record_exists(id)
        self.log[id].add_phenotypes_to_log(phenotypes)

    def log_phenotypes_fitness_scores(self, id):
        self.log[id].fetch_and_log_phenotypes_fitness_scores()

    def log_groups_fitness_scores(self, id):
        self.log[id].fetch_and_log_groups_fitness_scores()

    def _check_if_record_exists(self, id):
        if id not in self.log:
            self.log[id] = Generation_Log(id)

class Generation_Log:
    def __init__(self, id):
        self.id = id
        self.coefficients_log = []
        self.groups_log = {}
        self.groups_fitness_scores_log = {}
        self.phenotypes_log = []
        self.phenotypes_fitness_scores = []

    def add_coefficients_to_log(self, mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor, population_size):
        self.coefficients_log.append((mutation_coefficients, compatibility_coefficients,
                                      compatibility_threshold, r_factor, population_size))

    def add_groups_to_log(self, groups):
        for group in groups.values():
            self.groups_log[group.id] = group

    def add_phenotypes_to_log(self, phenotypes):
        for phenotype in phenotypes:
            self.phenotypes_log.append(phenotype)

    def fetch_and_log_phenotypes_fitness_scores(self):
        for nn in self.phenotypes_log:
            self.phenotypes_fitness_scores.append(nn._genome.fitness)

    def fetch_and_log_groups_fitness_scores(self):
        for group in self.groups_log.values():
            self.groups_fitness_scores_log[group.id] = []
            for genome in group.genomes:
                self.groups_fitness_scores_log[group.id].append((genome.fitness, genome.adjusted_fitness, group.group_adjusted_fitness))