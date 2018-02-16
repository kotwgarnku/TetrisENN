import multiprocessing
import multiprocessing.managers
from bot.gist import TetrisApp
from evolution.generation import *
from evolution.logger import *
import boardUtils


class TetrisPhenotypeHandlerFactory:
    def get_phenotype_handler(self, phenotypes):
        return TetrisPhenotypeHandler(phenotypes)


class TetrisPhenotypeHandler(PhenotypesHandler):
    def run_all_phenotypes(self):
        resource_manager = multiprocessing.Manager()
        fitnesses = resource_manager.dict()
        games_subprocesses = []
        nn_subprocesses = []
        for nn, ind in zip(self._neural_networks, range(len(self._neural_networks))):
            #create pipe
            tetris_connection, neural_network_connection = multiprocessing.Pipe()
            #create tetris game process
            game = multiprocessing.Process(name="game", target=self.create_tetris_subprocess, args=(tetris_connection,))
            games_subprocesses.append(game)
            #create nn subprocess
            neural_network = multiprocessing.Process(name="nn", target=self.create_nn_subprocess, args=(neural_network_connection, fitnesses, ind, nn))
            nn_subprocesses.append(neural_network)

        for game, nn in zip(games_subprocesses, nn_subprocesses):
            game.start()
            nn.start()

        for game, nn in zip(games_subprocesses, nn_subprocesses):
            game.join()
            nn.join()

        if Generation.best_genome is None:
            Generation.best_genome = self._neural_networks[0]._genome

        for nn, ind in zip(self._neural_networks, range(len(self._neural_networks))):
            nn._genome.fitness = fitnesses[ind]
            if fitnesses[ind] > Generation.best_genome.fitness:
                Generation.best_genome = nn._genome
                Generation.best_fitnesses[Generation._GENERATION_ID - 1] = fitnesses[ind]

    def create_tetris_subprocess(self, connection):
        game = TetrisApp(connection)
        game.run()
        connection.close()

    def create_nn_subprocess(self, neural_network_connection, fitnesses, ind, nn):

        while (True):
            score, board = neural_network_connection.recv()
            if (score == 'quit'):
                break
            else:
                nn_input = []
                for row in board:
                    for block in row:
                        nn_input.append(block)

                if (len(nn_input) != nn._input_size):
                    raise ("Input to the network has wrong size")

                y = nn.forward(nn_input)

                if (len(y) != 4):
                    raise ("Wrong output size")

                max_y = max(y)
                if (y.index(max_y) == 0):
                    neural_network_connection.send('w')
                elif (y.index(max_y) == 1):
                    neural_network_connection.send('a')
                elif (y.index(max_y) == 2):
                    neural_network_connection.send('s')
                elif (y.index(max_y) == 3):
                    neural_network_connection.send('d')

                num_gaps = boardUtils.num_gaps(board)
                num_holes = boardUtils.num_holes(board)
                num_blocks_above = boardUtils.num_blocks_above_holes(board)

                fitnesses[ind] = max((1000 + 100 * score - 5 * num_gaps - 10 * num_holes - 4 * num_blocks_above), 1)
                print("Score:{} ; num_gaps: {} ; num_holes: {} ; num_blocks: {}".format(fitnesses[ind], num_gaps, num_holes, num_blocks_above))

        neural_network_connection.close()