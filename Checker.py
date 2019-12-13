import numpy as np

# Difference between the scores of each player
# Returns positive max possible score if player +1 has won
# Returns negative max possible score if player -1 has won
def mancalaCheckWin(mancala_game):
    if(mancala_game.isTerminal):
        if mancala_game.winner == 1:
            return mancala_game.scores.max()
        elif mancala_game.winner == -1:
            return -1*mancala_game.scores.max()
        else:

            return 0
# default return the evaluation of the players score
    else:
        return mancala_game.scores[0] - mancala_game.scores[1]

# Check number of move without searching
def mancalaBetterCheckWin(mancala_game):
	marblesSide1 = sum(mancala_game.bins[0])
	marblesSide2 = sum(mancala_game.bins[1])
	marblesDifference = marblesSide1 - marblesSide2
	player1 = 0
	player2 = 0
	for i in range(len(mancala_game.bins[0])):
		if(mancala_game.bins[0][i]%(len(mancala_game.bins[0])*2+2)<=i):
			if(mancala_game.bins[1][i]!=0 and mancala_game.bins[0][i]!=0):
				player1+=mancala_game.bins[1][i]+1
		if(mancala_game.bins[1][i]%(len(mancala_game.bins[0])*2+2)<len(mancala_game.bins[0])-i):
			if(mancala_game.bins[1][i]!=0 and mancala_game.bins[0][i]!=0):
				player2+=mancala_game.bins[0][i]+1
		if mancala_game.bins[0][i] == i+1:
			player1 += 2
		if mancala_game.bins[1][i] == len(mancala_game.bins[0]) -  i:
			player2 += 2
		if(mancala_game.isTerminal):
			if mancala_game.winner == 1:
				return mancala_game.scores.max() + marblesSide1 + player1
			elif mancala_game.winner == -1:
				return -1*(mancala_game.scores.max()+marblesSide2 + player2)
			else:
				return 0
		else:
			return (mancala_game.scores[0] - mancala_game.scores[1] + player1 - player2 + marblesDifference)