from evolution.logger import Logger
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class LoggerVisualiser:
    @staticmethod
    def plot_max_generation_fitness_scores(logger, path = None):
        scores = logger.get_fitness_scores()
        x = list(scores.keys())
        y = [max(generation_scores) for generation_scores in scores.values()]
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(x, y)
        plt.scatter(x, y)

        plt.xlabel("Generation")
        plt.ylabel("Max Fitness score")
        plt.title("Fitness score progression")
        if not path:
            path = "Max fitness scores"
        plt.savefig(path)
        plt.cla()
        plt.clf()

    @staticmethod
    def plot_groups_number(logger, path = None):
        groups_count = [len(generation_log.groups_log) for generation_log in logger.log.values()]
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.scatter(list(logger.log.keys()), groups_count)
        plt.xlabel("Generation")
        plt.ylabel("Number of groups")
        plt.title("Groups amount change over evolution")
        if not path:
            path = "Groups number"
        plt.savefig(path)
        plt.clf()
        plt.cla()

    @staticmethod
    def plot_last_generation_adjusted_fitness_scores(logger, path = None):
        last_gen_groups_fitness = []
        last_generation_id = max(logger.log.keys())
        for fit in logger.log[last_generation_id].groups_fitness_scores_log.values():
            last_gen_groups_fitness.append(fit[0][2])
        x = list(logger.log[last_generation_id].groups_log.keys())
        y = last_gen_groups_fitness
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.plot(x, y, 'ro')
        plt.xlabel("Group")
        plt.ylabel("Group adjusted fitness")
        plt.title("Adjusted fitness of groups in last generation")
        if not path:
            path= "Last generation adjusted fitness scores"
        plt.savefig(path)
        plt.clf()
        plt.cla()