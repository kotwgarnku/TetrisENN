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

    def _check_if_record_exists(self, id):
        if id not in self.log:
            self.log[id] = Generation_Log()

class Generation_Log:
    def __init__(self, id):
        self.id = id
        self.coefficients_log = []
        self.groups_log = {}
        self.phenotypes_log = []

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