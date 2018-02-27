import multiprocessing
import multiprocessing.managers

from bot import boardUtils
from bot.gist import TetrisApp
from evolution.generation import Generation
from evolution.phenotype_handler import PhenotypesHandler


class TetrisPhenotypesHandler(PhenotypesHandler):
    def run_all_phenotypes(self):
        resource_manager = multiprocessing.Manager()
        fitnesses = resource_manager.dict()
        games_subprocesses = []
        nn_subprocesses = []
        for nn, ind in zip(self._neural_networks, range(len(self._neural_networks))):
            # create pipe
            tetris_connection, neural_network_connection = multiprocessing.Pipe()
            # create tetris game process
            game = multiprocessing.Process(name="game", target=self.create_tetris_subprocess,
                                           args=(tetris_connection,))
            games_subprocesses.append(game)
            # create nn subprocess
            neural_network = multiprocessing.Process(name="nn", target=self.create_nn_subprocess,
                                                     args=(neural_network_connection, fitnesses, ind, nn))
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
            score, board, current_stone, stone_x, stone_y, next_stone = neural_network_connection.recv()
            if (score == 'quit'):
                break
            else:
                nn_input = []
                # for row in board:
                #     for block in row:
                #         nn_input.append(block)

                columns_heights = boardUtils.get_columns_heights(board)

                for column_height in columns_heights:
                    nn_input.append(column_height)

                nn_input.append(boardUtils.get_stone_number(current_stone))
                nn_input.append(stone_x)
                nn_input.append(stone_y)

                if (len(nn_input) != nn._input_size):
                    neural_network_connection.close()
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

                fitnesses[ind] = self.calculate_fitness(score, columns_heights)
                print("Score:{0}".format(fitnesses[ind]))

        neural_network_connection.close()


    def calculate_fitness(self, score, columns_heights):
        differences = self.calculate_max_height_difference(columns_heights)
        fitness = 11000 + score * 500 - self.calculate_penalty_for_height_differences(differences)
        return fitness


    def calculate_max_height_difference(self, columns_heights):
        return [abs(a - b) for ind, a in enumerate(columns_heights) for b in columns_heights[ind+1 :]]


    def calculate_penalty_for_height_differences(self, differences):
        # Max penalty is 10164(22^2 * 21)
        sum = 0
        for difference in differences:
            sum += (difference**2)
        return sum