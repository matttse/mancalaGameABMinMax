import numpy as np
## Mancala as defined http://boardgames.about.com/cs/mancala/ht/play_mancala.htm
class Mancala:
    def __init__(self, bins_per_player=6, stones_per_bin=4, game=None):
        if game is None: # create new game
            self.bins = np.empty([2, bins_per_player], dtype=int)
            self.bins.fill(stones_per_bin)
            self.scores = np.zeros(2, dtype=int)
            self.turn = 1
        else: # copy existing game
            self.bins = game.bins.copy()
            self.scores = game.scores.copy()
            self.turn = game.turn
        self._moves = None
        self._terminal = None
        self._repr = None

    def _print_char(self, i):
        return i

    def __repr__(self):
        # An console representation of the board state.
        if self._repr is None:
            # Player 0 scoring area
            if self.turn == 1:
                rows = [" --", ">| ", " | ", " | ", " --"]
            else:
                rows = [" --", " | ", " | ", ">| ", " --"]
            rows[2] += str(self.scores[0]) + " |"
            for r in [0,4]:
                rows[r] += "-"*(len(str(self.scores[0])) + 2)
            for r in [1,3]:
                rows[r] += " "*len(str(self.scores[0])) + " |"
            # bins
            for h in range(self.bins.shape[1]):
                width = len(str(self.bins[:,h].max()))
                for r in [1,3]:
                    rows[r] += " " + str(self.bins[r//2,h])
                    rows[r] += " "*(width - len(str(self.bins[r//2,h]))) +" |"
                for r in [0,2,4]:
                    rows[r] += "-"*(width + 3)
            rows[2] = rows[2][:-1] + "|"
            # player 1 scoring area
            rows[2] += " " + str(self.scores[1]) + " |\n"
            for r in [0,4]:
                rows[r] += "-"*(len(str(self.scores[1])) + 2) + "\n"
            for r in [1,3]:
                rows[r] += " "*len(str(self.scores[1])) + "  |"
            if self.turn == 1:
                rows[1] += "<\n"
                rows[3] += "\n"
            else:
                rows[1] += "\n"
                rows[3] += "<\n"
        self._repr = "".join(rows)
        return self._repr

    def makeMove(self, move):
        # Returns a new Mancala instance in which move has been play

        # A valid move is the index (column) of a bin in which the current
        # player has stones. stones in that bin are sown counter-clockwise
        # il they run out, at which point a capture may occur.
        new_game = Mancala(game=self)
        new_game.bins = self.bins.copy()
        side = 0 if self.turn == 1 else 1 # start sowing in row 0 or row 1
        start_side = side
        bin = move

        # grab stones
        stones = self.bins[side, move]
        size = self.bins.shape[1]
        new_game.bins[side, move] = 0

        while stones > 0: # sow
            if side == 0:
                bin -= 1
            else:
                bin += 1
            if (bin == -1) or (bin == size): # reached end of side
                if side == start_side: # sow in the scoring pile
                    new_game.scores[side] += 1
                    stones -= 1
                    if stones == 0:
                        break
                side = (side + 1) % 2
                if side == 1:
                    bin += 1
                else:
                    bin -= 1
            new_game.bins[(side, bin)] += 1
            stones -= 1

        if (bin == -1) or (bin == size):
            new_game.turn = self.turn # take another turn
        else:
            new_game.turn = -self.turn
            # check for capture
            if side == start_side and new_game.bins[(side, bin)] == 1:
                captured_bin = ((side + 1) % 2, bin)
                if new_game.bins[captured_bin] != 0:
                    new_game.scores[side] += new_game.bins[captured_bin] + 1
                    new_game.bins[(side, bin)] = 0
                    new_game.bins[captured_bin] = 0

        # check for empty sides
        if new_game.bins[0].sum() == 0:
            new_game.scores[1] += new_game.bins[1].sum()
            new_game.bins[1] = 0
            new_game._terminal = True
        elif new_game.bins[1].sum() == 0:
            new_game.scores[0] += new_game.bins[0].sum()
            new_game.bins[0] = 0
            new_game._terminal = True

        return new_game

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        # List of legal moves for the current player.
        if self._moves is None:
            side = 0 if self.turn == 1 else 1
            self._moves = [int(m) for m in np.nonzero(self.bins[side])[0]]
        return self._moves

    @property
    def isTerminal(self):
        # Boolean indicating whether the game has ended.
        if self._terminal is None:
            if self.scores.max() > (self.bins.sum() + self.scores.sum()) // 2:
                self._terminal = True
            elif self.bins.sum() == 0:
                self._terminal = True
            else:
                self._terminal = False
        return self._terminal

    @property
    def winner(self):
        ##+1 if the first player (maximizer) has won. -1 if the second player
        # (minimizer) has won. 0 if the game is a draw. Raises an AttributeError
        # if accessed on a non-terminal state
        if not self.isTerminal:
            raise AttributeError("Non-terminal states have no winner.")
        if self.scores[0] > self.scores[1]:
            return 1
        elif self.scores[1] > self.scores[0]:
            return -1
        return 0
