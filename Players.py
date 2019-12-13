from random import choice
from sys import stdin
from math import inf

class HumanPlayer:
    ##Player that gets moves from command line input
    def __init__(self, *args):
        self.name = "Human"

    def getNextMove(self, game):
        move = None
        while move not in game.availableMoves:
            print([move for move in game.availableMoves])
            if all(isinstance(move, int) for move in game.availableMoves):
                print("select a move from", game.availableMoves)
                try:
                    move = int(stdin.readline())
                except ValueError:
                    print("invalid move")
                if move not in game.availableMoves:
                    print("invalid move")
            else:
                print("select a move from:")
                for i,move in enumerate(game.availableMoves):
                    print(i, ":", move)
                try:
                    move = game.availableMoves[int(stdin.readline())]
                except (ValueError, IndexError):
                    print("invalid move")
        return move


class RandomPlayer:
    ##Player that selects a random legal move
    def __init__(self, *args):
        self.name = "Random"

    def getNextMove(self, game):
        return choice(game.availableMoves)

class MiniMaxPlayer:
    ##Gets moves by depth min-max search.
    def __init__(self, boardEval, depthBound):
        self.name = "MiniMax"
        self.boardEval = boardEval
        self.depthBound = depthBound
    def getNextMove(self, game_state):
        best_value, best_move = self.limited_mini_max(game_state, 0)
        return best_move


    def limited_mini_max(self, state, depth):
        if(state.isTerminal or self.depthBound == depth):
            return self.boardEval(state), None
        # best_value = self.boardEval(state)
        if(state.turn==1):
            best_value = -1*inf
        else:
            best_value = inf
        best_move = None
        for move in state.availableMoves:
            next_state = state.makeMove(move)
            value, boundedMove = self.limited_mini_max(next_state, depth+1)
            # if(value == None):
            #     continue
            if(state.turn==1):
                if(value > best_value):
                    best_value = value
                    best_move = move
            else:
                if(value < best_value):
                    best_value = value
                    best_move = move
        return best_value, best_move

##Get moves by depth search with alpha beta pruning
class AlphaBetaPruningPlayer:    
    def __init__(self, boardEval, depthBound):
        self.name = "AlphaBetaPruning"
        self.boardEval = boardEval
        self.depthBound = depthBound
    def getNextMove(self, game_state):
        best_value, best_move = self.alpha_beta(game_state, inf, -1*inf, 0)
        return best_move

    def alpha_beta(self, state, UB, LB, depth):
        if(state.isTerminal or self.depthBound == depth):
            return self.boardEval(state), None
        if(state.turn==1):
            best_value = -1*inf
        else:
            best_value = inf
        best_move = None
        for move in state.availableMoves:
            next_state = state.makeMove(move)
            value, boundedMove = self.alpha_beta(next_state, UB, LB, depth+1)
            if(state.turn==1):
                if(value >= UB):
                    return value, boundedMove
                if(value > LB):
                    LB = value
                if(value > best_value):
                    best_value = value
                    best_move = move
            else:
                if(value <= LB):
                    return value, boundedMove
                if(value < UB):
                    UB = value
                if(value < best_value):
                    best_value = value
                    best_move = move
        return best_value, best_move