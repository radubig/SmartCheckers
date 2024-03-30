import copy


class TerminalColors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Table:
    def __init__(self, player1_sym, player1king_sym, player2_sym, player2king_sym, empty_sym, config=None):
        self.player1_sym = str(player1_sym)
        self.player1king_sym = str(player1king_sym)
        self.player2_sym = str(player2_sym)
        self.player2king_sym = str(player2king_sym)
        self.empty_sym = str(empty_sym)
        if config is None:
            self.config = [
                [empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym],
                [player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym],
                [empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym, empty_sym, player2_sym],
                [empty_sym for _ in range(8)],
                [empty_sym for _ in range(8)],
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
                match cell:
                    case self.player1_sym:
                        p1 += 1
                    case self.player1king_sym:
                        p1 += 2
                    case self.player2_sym:
                        p2 += 1
                    case self.player2king_sym:
                        p2 += 2
        if p1 == 0:
            return -1000
        elif p2 == 0:
            return 1000
        return p1 - p2

    def printTable(self):
        content = str(self)
        for c in content:
            if c in [self.player1_sym, self.player1king_sym]:
                print(TerminalColors.GREEN + c + TerminalColors.END, end='')
            elif c in [self.player2_sym, self.player2king_sym]:
                print(TerminalColors.RED + c + TerminalColors.END, end='')
            else:
                print(c, end='')


class Move:
    @staticmethod
    def checkKing(table: Table):
        for i in range(8):
            if table.config[0][i] == table.player1_sym:
                table.config[0][i] = table.player1king_sym
            if table.config[7][i] == table.player2_sym:
                table.config[7][i] = table.player2king_sym

    @staticmethod
    def moveUpperLeft(table: Table, i: int, j: int):
        if i - 1 < 0 or j - 1 < 0:
            return None
        if table.config[i - 1][j - 1] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i - 1][j - 1] = table.config[i][j]
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def jumpUpperLeft(table: Table, i: int, j: int, opponent: list):
        if i - 2 < 0 or j - 2 < 0:
            return None
        if table.config[i - 1][j - 1] in opponent and table.config[i - 2][j - 2] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i - 2][j - 2] = table.config[i][j]
            new_table.config[i - 1][j - 1] = table.empty_sym
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def moveUpperRight(table: Table, i: int, j: int):
        if i - 1 < 0 or j + 1 > 7:
            return None
        if table.config[i - 1][j + 1] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i - 1][j + 1] = table.config[i][j]
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def jumpUpperRight(table: Table, i: int, j: int, opponent):
        if i - 2 < 0 or j + 2 > 7:
            return None
        if table.config[i - 1][j + 1] in opponent and table.config[i - 2][j + 2] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i - 2][j + 2] = table.config[i][j]
            new_table.config[i - 1][j + 1] = table.empty_sym
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def moveLowerLeft(table: Table, i: int, j: int):
        if i + 1 > 7 or j - 1 < 0:
            return None
        if table.config[i + 1][j - 1] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i + 1][j - 1] = table.config[i][j]
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def jumpLowerLeft(table: Table, i: int, j: int, opponent):
        if i + 2 > 7 or j - 2 < 0:
            return None
        if table.config[i + 1][j - 1] in opponent and table.config[i + 2][j - 2] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i + 2][j - 2] = table.config[i][j]
            new_table.config[i + 1][j - 1] = table.empty_sym
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def moveLowerRight(table: Table, i: int, j: int):
        if i + 1 > 7 or j + 1 > 7:
            return None
        if table.config[i + 1][j + 1] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i + 1][j + 1] = table.config[i][j]
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None

    @staticmethod
    def jumpLowerRight(table: Table, i: int, j: int, opponent):
        if i + 2 > 7 or j + 2 > 7:
            return None
        if table.config[i + 1][j + 1] in opponent and table.config[i + 2][j + 2] == table.empty_sym:
            new_table = copy.deepcopy(table)
            new_table.config[i + 2][j + 2] = table.config[i][j]
            new_table.config[i + 1][j + 1] = table.empty_sym
            new_table.config[i][j] = table.empty_sym
            Move.checkKing(new_table)
            return new_table
        return None


class GameGraph:
    def __init__(self, player1_sym, player1king_sym, player2_sym, player2king_sym, empty_sym, starting_config=None):
        self.starting_table = Table(player1_sym, player1king_sym, player2_sym, player2king_sym, empty_sym, starting_config)

    @staticmethod
    def getJumpSuccessors(table: Table, player: int):
        succ = list[Table]()
        for i in range(8):
            for j in range(8):
                if player == 1:
                    if table.config[i][j] in [table.player1_sym, table.player1king_sym]:
                        if Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                            succ.append(Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]))
                        if Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                            succ.append(Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]))
                        if table.config[i][j] == table.player1king_sym:
                            if Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                succ.append(Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]))
                            if Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                succ.append(Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]))

                elif player == 2:
                    if table.config[i][j] in [table.player2_sym, table.player2king_sym]:
                        if Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                            succ.append(Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]))
                        if Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                            succ.append(Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]))
                        if table.config[i][j] == table.player2king_sym:
                            if Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                succ.append(Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]))
                            if Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                succ.append(Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]))
        return succ

    @staticmethod
    def getMoveSuccessors(table: Table, player: int):
        succ = list[Table]()
        for i in range(8):
            for j in range(8):
                if player == 1:
                    if table.config[i][j] in [table.player1_sym, table.player1king_sym]:
                        if Move.moveUpperLeft(table, i, j) is not None:
                            succ.append(Move.moveUpperLeft(table, i, j))
                        if Move.moveUpperRight(table, i, j) is not None:
                            succ.append(Move.moveUpperRight(table, i, j))
                        if table.config[i][j] == table.player1king_sym:
                            if Move.moveLowerLeft(table, i, j) is not None:
                                succ.append(Move.moveLowerLeft(table, i, j))
                            if Move.moveLowerRight(table, i, j) is not None:
                                succ.append(Move.moveLowerRight(table, i, j))

                elif player == 2:
                    if table.config[i][j] in [table.player2_sym, table.player2king_sym]:
                        if Move.moveLowerLeft(table, i, j) is not None:
                            succ.append(Move.moveLowerLeft(table, i, j))
                        if Move.moveLowerRight(table, i, j) is not None:
                            succ.append(Move.moveLowerRight(table, i, j))
                        if table.config[i][j] == table.player2king_sym:
                            if Move.moveUpperLeft(table, i, j) is not None:
                                succ.append(Move.moveUpperLeft(table, i, j))
                            if Move.moveUpperRight(table, i, j) is not None:
                                succ.append(Move.moveUpperRight(table, i, j))
        return succ

    @staticmethod
    def getSuccessors(table: Table, player: int):
        succ = GameGraph.getJumpSuccessors(table, player)
        if len(succ) == 0:
            succ = GameGraph.getMoveSuccessors(table, player)
            if len(succ) == 0:
                emptyTable = copy.deepcopy(table)
                emptyTable.config = [['#' for _ in range(8)] for _ in range(8)]
                return [emptyTable]
        else:
            foundCapture = True
            while foundCapture:
                newsucc = list[Table]()
                for s in succ:
                    n = GameGraph.getJumpSuccessors(s, player)
                    if len(n) != 0:
                        newsucc.extend(n)
                if len(newsucc) == 0:
                    foundCapture = False
                else:
                    succ = newsucc
        return succ


def minimax(node: Table, depth: int, player: int):
    playerAdvantage = node.evaluatePlayerAdvantage()
    if depth == 0 or playerAdvantage == 1000 or playerAdvantage == -1000:
        return playerAdvantage
    if player == 1:
        value = -1005
        for child in GameGraph.getSuccessors(node, player):
            evaluation = minimax(child, depth - 1, 2)
            if evaluation > value:
                value = evaluation
        return value
    else:
        value = 1005
        for child in GameGraph.getSuccessors(node, player):
            evaluation = minimax(child, depth - 1, 1)
            if evaluation < value:
                value = evaluation
        return value


if __name__ == '__main__':
    starting_config = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', 'b', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'b', '#', 'b', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'b', '#', '#', '#', '#', '#', '#'],
        ['a', '#', 'a', '#', '#', '#', '#', '#']
        ]

    game = GameGraph('a', 'A', 'b', 'B', '#')
    currentState = game.starting_table
    currentState.printTable()
    print()
    for i in range(50):
        value = -1005
        newState = None
        for child in GameGraph.getSuccessors(currentState, 1):
            evaluation = minimax(child, 6, 2)
            if evaluation > value:
                value = evaluation
                newState = child
        currentState = newState
        currentState.printTable()
        print(value)
        if currentState.evaluatePlayerAdvantage() in [1000, -1000]:
            break
        print('------------------')

        value = 1005
        newState = None
        for child in GameGraph.getSuccessors(currentState, 2):
            evaluation = minimax(child, 6, 1)
            if evaluation < value:
                value = evaluation
                newState = child
        currentState = newState
        currentState.printTable()
        print(value)
        if currentState.evaluatePlayerAdvantage() in [1000, -1000]:
            break
        print('------------------')


