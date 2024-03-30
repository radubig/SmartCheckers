import copy


class GameGraph:
    def __init__(self, player1_sym, player2_sym, empty_sym, starting_config=None):
        self.starting_table = Table(player1_sym, player2_sym, empty_sym, starting_config)


class Table:
    def __init__(self, player1_sym, player2_sym, empty_sym, config=None):
        self.player1_sym = str(player1_sym)
        self.player2_sym = str(player2_sym)
        self.empty_sym = str(empty_sym)
        if config is None:
            self.config = [
                [empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym],
                [player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym],
                [empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym],
                [player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym],
                [empty_sym for _ in range(8)],
                [empty_sym for _ in range(8)],
                [empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym],
                [player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym],
                [empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym],
                [player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym, player1_sym, empty_sym]
            ]
        else:
            self.config = copy.deepcopy(config)

    def __str__(self):
        prt = ""
        for row in self.config:
            for cell in row:
                prt += cell + ' '
            prt += '\n'
        return prt

    # Calculate the advantage of pieces of player 1
    def evaluatePlayerAdvantage(self):
        p1 = p2 = 0
        for row in self.config:
            for cell in row:
                if cell == self.player1_sym:
                    p1 += 1
                elif cell == self.player2_sym:
                    p2 += 1
        return p1 - p2


if __name__ == '__main__':
    game = GameGraph('O', '@', '#')
    print(game.starting_table)
