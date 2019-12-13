from argparse import ArgumentParser
from Mancala import Mancala
from Players import HumanPlayer, RandomPlayer, MiniMaxPlayer, AlphaBetaPruningPlayer
from Checker import normalCheck, betterCheck

# Game Type Class object
games = {"mancala":Mancala}
# Evaluation Options
check_options = ["normal", "better"]
check_functions = {"mancala":{"normal":normalCheck, "better":betterCheck}}

# Player Options
players = {"random":RandomPlayer,
           "human":HumanPlayer,
           "minimax":MiniMaxPlayer,
           "alphabeta":AlphaBetaPruningPlayer}

# Run the game
def main():
    args = parse_args()
    if args.p1 == "minimax" or args.p1 == "alphabeta":
        e1 = check_functions[args.game][args.e1]
        p1 = players[args.p1](e1, args.d1)
    else:
        p1 = players[args.p1]()
    if args.p2 == "minimax" or args.p2 == "alphabeta":
        e2 = check_functions[args.game][args.e2]
        p2 = players[args.p2](e2, args.d2)
    else:
        p2 = players[args.p2]()
    game = games[args.game](*args.game_args)

    if args.games == 1:
        GameBoard(game, p1, p2, args.show)
    else:
        p1_wins = 0
        p2_wins = 0
        draws = 0
        for i in range(args.games):
            if i % 2:
                result = GameBoard(game, p1, p2, args.show)
                if result.winner == 1:
                    p1_wins += 1
                elif result.winner == -1:
                    p2_wins += 1
                else:
                    draws += 1
            else:
                result = GameBoard(game, p2, p1, args.show)
                if result.winner == -1:
                    p1_wins += 1
                elif result.winner == 1:
                    p2_wins += 1
                else:
                    draws += 1
        print("results after", args.games, "games:")
        print(p1_wins, "wins for player 1 (" + p1.name + ")")
        print(p2_wins, "wins for player 2 (" + p2.name + ")")
        if draws > 0:
            print(draws, "draws")

# Display args to change game type
def parse_args():
    p = ArgumentParser()
    p.add_argument("game", type=str, choices=list(games.keys()), help="Type mancala")
    p.add_argument("p1", type=str, choices=list(players.keys()), help="Select Player 1 Type")
    p.add_argument("p2", type=str, choices=list(players.keys()), help="Select Player 2 Type")
    p.add_argument("-games", type=int, default=1, help="Number of games to play.")
    p.add_argument("--show", action="store_true", help="Set this flag to print the board every round.")
    p.add_argument("-game_args", type=int, nargs="*", default=[], help="Optional arguments to type to the game, must be typed in order.")
    p.add_argument("-e1", type=str, choices=check_options, default="normal", help="Board eval function for player 1.")
    p.add_argument("-e2", type=str, choices=check_options, default="normal", help="Board eval function for player 2.")
    p.add_argument("-d1", type=int, default=4, help="Search depth for player 1.")
    p.add_argument("-d2", type=int, default=4, help="Search depth for player 2.")
    return p.parse_args()

##Plays a game then returns the final state
def GameBoard(game, player1, player2, show=False):
    # while game has not ended
    while not game.isTerminal:
        if show:
            print(game)
        if game.turn == 1:
            m = player1.getNextMove(game)
        else:
            m = player2.getNextMove(game)
        if m not in game.availableMoves:
            raise Exception("pick another move, invalid move: " + str(m))
        game = game.makeMove(m)
    if show:
        print(game, "\n")
        if game.winner != 0:
            print("player", game._print_char(game.winner), "wins")
        else:
            print("it's a draw")
    return game

if __name__ == "__main__":
    main()
