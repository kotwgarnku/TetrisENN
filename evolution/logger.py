from evolution.generation import Generation, Group

class Logger:
    def __init__(self):
        self.log = {}

    def log_coefficients(self, id, mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor):
        self._check_if_record_exists(id)
        self.log[id].add_coefficients_to_log(mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor)

    def log_groups(self, id, groups):
        self._check_if_record_exists(id)
        self.log[id].add_groups_to_log(groups)

    def log_phenotypes(self, id, phenotypes):
        self._check_if_record_exists(id)
        self.log[id].add_phenotypes_to_log(phenotypes)

    def log_phenotypes_fitness_scores(self, id):
        self.log[id].fetch_and_log_fitness_scores()

    def _check_if_record_exists(self, id):
        if id not in self.log:
            self.log[id] = Generation_Log(id)

class Generation_Log:
    def __init__(self, id):
        self.id = id
        self.coefficients_log = []
        self.groups_log = {}
        self.phenotypes_log = []
        self.fitness_scores = []

    def add_coefficients_to_log(self, mutation_coefficients, compatibility_coefficients,
                                compatibility_threshold, r_factor):
        self.coefficients_log.append((mutation_coefficients, compatibility_coefficients,
                                      compatibility_threshold, r_factor))

    def add_groups_to_log(self, groups):
        for group in groups.values():
            self.groups_log[group.id] = group

    def add_phenotypes_to_log(self, phenotypes):
        for phenotype in phenotypes:
            self.phenotypes_log.append(phenotype)

    def fetch_and_log_fitness_scores(self):
        for nn in self.phenotypes_log:
            self.fitness_scores.append(nn._genome.fitness)