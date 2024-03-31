import copy
from datetime import datetime


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

    def __eq__(self, other):
        return self.config == other.config

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
    def getJumpSuccessors(table: Table, player: int, capturingPiece=None):
        succ = []
        if capturingPiece is None:
            for i in range(8):
                for j in range(8):
                    if player == 1:
                        if table.config[i][j] in [table.player1_sym, table.player1king_sym]:
                            if Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                succ.append((Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]), (i-2, j-2)))
                            if Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                succ.append((Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]), (i-2, j+2)))
                            if table.config[i][j] == table.player1king_sym:
                                if Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                    succ.append((Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]), (i+2, j-2)))
                                if Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                                    succ.append((Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]), (i+2, j+2)))
                    elif player == 2:
                        if table.config[i][j] in [table.player2_sym, table.player2king_sym]:
                            if Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                succ.append((Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]), (i+2, j-2)))
                            if Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                succ.append((Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]), (i+2, j+2)))
                            if table.config[i][j] == table.player2king_sym:
                                if Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                    succ.append((Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]), (i-2, j-2)))
                                if Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                                    succ.append((Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]), (i-2, j+2)))

        else:
            i = capturingPiece[0]
            j = capturingPiece[1]
            if player == 1:
                if table.config[i][j] in [table.player1_sym, table.player1king_sym]:
                    if Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                        succ.append((Move.jumpUpperLeft(table, i, j, [table.player2_sym, table.player2king_sym]), (i-2, j-2)))
                    if Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                        succ.append((Move.jumpUpperRight(table, i, j, [table.player2_sym, table.player2king_sym]), (i-2, j+2)))
                    if table.config[i][j] == table.player1king_sym:
                        if Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                            succ.append((Move.jumpLowerLeft(table, i, j, [table.player2_sym, table.player2king_sym]), (i+2, j-2)))
                        if Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]) is not None:
                            succ.append((Move.jumpLowerRight(table, i, j, [table.player2_sym, table.player2king_sym]), (i+2, j+2)))
            elif player == 2:
                if table.config[i][j] in [table.player2_sym, table.player2king_sym]:
                    if Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                        succ.append((Move.jumpLowerLeft(table, i, j, [table.player1_sym, table.player1king_sym]), (i+2, j-2)))
                    if Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                        succ.append((Move.jumpLowerRight(table, i, j, [table.player1_sym, table.player1king_sym]), (i+2, j+2)))
                    if table.config[i][j] == table.player2king_sym:
                        if Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                            succ.append((Move.jumpUpperLeft(table, i, j, [table.player1_sym, table.player1king_sym]), (i-2, j-2)))
                        if Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]) is not None:
                            succ.append((Move.jumpUpperRight(table, i, j, [table.player1_sym, table.player1king_sym]), (i-2, j+2)))
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
        else:
            foundCapture = True
            while foundCapture:
                newsucc = []
                for s, piece in succ:
                    n = GameGraph.getJumpSuccessors(s, player, piece)
                    if len(n) != 0:
                        newsucc.extend(n)
                if len(newsucc) == 0:
                    foundCapture = False
                else:
                    succ = newsucc

            newsucc = []
            for s, _ in succ:
                newsucc.append(s)
            succ = newsucc
        return succ


def minimax(node: Table, depth: int, player: int):
    playerAdvantage = node.evaluatePlayerAdvantage()
    if depth == 0 or playerAdvantage == 1000 or playerAdvantage == -1000:
        return playerAdvantage
    if player == 1:
        value = -1005
        successors = GameGraph.getSuccessors(node, player)
        if len(successors) == 0:
            return -1000
        for child in successors:
            evaluation = minimax(child, depth - 1, 2)
            if evaluation > value:
                value = evaluation
        return value
    else:
        value = 1005
        successors = GameGraph.getSuccessors(node, player)
        if len(successors) == 0:
            return 1000
        for child in successors:
            evaluation = minimax(child, depth - 1, 1)
            if evaluation < value:
                value = evaluation
        return value


def PlayerMove(table: Table, player: int):
    mutareInvalida = True
    while mutareInvalida:
        mutareInvalida = False
        str_moves = input('Introdu mutarea (ex: 22->33[->42...]):')
        moves = str_moves.split('->')
        si = sj = -1
        new_table = copy.deepcopy(table)
        for move in moves:
            if len(move) != 2:
                mutareInvalida = True
                break
            ei = int(move[0]) - 1
            ej = int(move[1]) - 1
            if ei < 0 or ei > 7 or ej < 0 or ej > 7:
                mutareInvalida = True
                break
            if si == -1 or sj == -1:
                si = ei
                sj = ej
                continue
            if ((player == 1 and new_table.config[si][sj] in [new_table.player1_sym, new_table.player1king_sym]) or
               (player == 2 and new_table.config[si][sj] in [new_table.player2_sym, new_table.player2king_sym])) and \
               new_table.config[ei][ej] == new_table.empty_sym:
                    if abs(si - ei) == 1 and abs(sj - ej) == 1:
                        new_table.config[ei][ej] = new_table.config[si][sj]
                        new_table.config[si][sj] = new_table.empty_sym
                    elif abs(si - ei) == 2 and abs(sj - ej) == 2:
                        if player == 1 and new_table.config[(si + ei) // 2][(sj + ej) // 2] in [new_table.player2_sym, new_table.player2king_sym]:
                                new_table.config[ei][ej] = new_table.config[si][sj]
                                new_table.config[si][sj] = new_table.empty_sym
                                new_table.config[(si + ei) // 2][(sj + ej) // 2] = new_table.empty_sym
                        elif player == 2 and new_table.config[(si + ei) // 2][(sj + ej) // 2] in [new_table.player1_sym, new_table.player1king_sym]:
                                new_table.config[ei][ej] = new_table.config[si][sj]
                                new_table.config[si][sj] = new_table.empty_sym
                                new_table.config[(si + ei) // 2][(sj + ej) // 2] = new_table.empty_sym
                        else:
                            mutareInvalida = True
                            break
                    else:
                        mutareInvalida = True
                        break
            else:
                mutareInvalida = True
                break
            si = ei
            sj = ej
            Move.checkKing(new_table)

        # Verificare daca mutarea este valida
        if mutareInvalida:
            mutareInvalida = True
            print('Mutare invalida!')
            continue
        if new_table in GameGraph.getSuccessors(table, player):
            return new_table
        print('Mutare invalida!')
        mutareInvalida = True


if __name__ == '__main__':
    gamemode = 0
    while True:
        gamemode = int(input('Selecteaza modul de joc:\n1. Player vs Computer\n2. Player vs Player\n3. Computer vs Computer\n'))
        if gamemode in [1, 2, 3]:
            break
        print('Input invalid!')

    selected_algorithm = 0
    while True:
        selected_algorithm = int(input('Selecteaza algoritmul:\n1. Min-Max\n'))
        if selected_algorithm in [1]:
            break
        print('Input invalid!')

    depth = 0
    if gamemode in [1, 3]:
        while True:
            depth = int(input('Selecteaza dificultatea (adancimea arborelui de decizie) 1...10: '))
            if depth > 10:
                print('Adancimea este prea mare! Daca ai un calculator puternic probabil poti sa scoti aceasta limitare din cod, dar realistic vorbind o sa iti ia calculatorul foc pana se termina de calculat urmatoarea mutare a calculatorului.')
            elif depth < 1:
                print('Input invalid!')
            else:
                break

    personIsPlayer = 0
    if gamemode == 1:
        while True:
            personIsPlayer = int(input('Selecteaza cu ce joci:\n1. Verde (Player 1)\n2. Rosu (Player 2)\n'))
            if personIsPlayer in [1, 2]:
                break
            print('Input invalid!')

    # starting_config nu este validat!
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

    sc = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'b', '#', 'b', '#', 'b', '#', 'b'],
        ['b', '#', 'b', '#', 'b', '#', 'b', '#'],
        ['#', 'a', '#', 'a', '#', 'a', '#', 'a'],
        ['a', '#', 'a', '#', 'a', '#', 'a', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['a', '#', '#', '#', '#', '#', '#', '#']
    ]

    sc2 = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'b', '#', 'b', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['a', '#', '#', '#', '#', '#', '#', '#']
    ]

    custom_config = [
        ['#', '#', '#', '#', '#', '#', '#', 'b'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'a', '#', '#', '#', '#', '#', 'b'],
        ['#', '#', 'b', '#', 'b', '#', '#', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['b', '#', 'a', '#', '#', '#', '#', '#'],
        ['#', '#', '#', 'a', '#', '#', '#', '#'],
        ['a', '#', 'a', '#', 'B', '#', '#', '#']
    ]

    game = GameGraph('a', 'A', 'b', 'B', '#')
    currentState = game.starting_table
    currentState.printTable()
    print()

    start_clock = datetime.now()
    while True:
        print(TerminalColors.CYAN + 'Player 1 Turn' + TerminalColors.END)

        newState = None
        value = -1005
        if (gamemode == 1 and personIsPlayer == 1) or gamemode == 2:
            newState = PlayerMove(currentState, 1)
        else:
            for child in GameGraph.getSuccessors(currentState, 1):
                evaluation = minimax(child, depth, 2)
                if evaluation > value:
                    value = evaluation
                    newState = child

        currentState = newState
        currentState.printTable()
        if value != -1005:
            print('Evaluare pozitie: ', value)
        if (currentState.evaluatePlayerAdvantage() in [1000, -1000]
                or len(GameGraph.getSuccessors(currentState, 2)) == 0):
            print(TerminalColors.CYAN + 'Player 1 a castigat!' + TerminalColors.END)
            break

        print('------------------')
        print(TerminalColors.CYAN + 'Player 2 Turn' + TerminalColors.END)

        newState = None
        value = 1005
        if (gamemode == 1 and personIsPlayer == 2) or gamemode == 2:
            newState = PlayerMove(currentState, 2)
        else:
            for child in GameGraph.getSuccessors(currentState, 2):
                evaluation = minimax(child, depth, 1)
                if evaluation < value:
                    value = evaluation
                    newState = child

        currentState = newState
        currentState.printTable()
        if value != 1005:
            print('Evaluare pozitie: ', value)
        if (currentState.evaluatePlayerAdvantage() in [1000, -1000]
                or len(GameGraph.getSuccessors(currentState, 1)) == 0):
            print(TerminalColors.CYAN + 'Player 2 a castigat!' + TerminalColors.END)
            break
        print('------------------')

    end_clock = datetime.now()
    print('Timp joc: ', end_clock - start_clock)
