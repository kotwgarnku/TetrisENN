from evolution.generation import *
from bot.tetris_phenotype_handler import TetrisPhenotypesHandler
import bot.gist
from evolution.genome_serialization import genome_from_json

if __name__ == '__main__':
    try:
        f = open('best_genome')
        genome = genome_from_json(f.read())
        bot.gist.DROP_TIME = 300
        TetrisPhenotypesHandler([NeuralNetwork(genome)]).run_all_phenotypes()
        bot.gist.DROP_TIME = 20

    except OSError:
        print("Couldn't find the file with the best genome")
