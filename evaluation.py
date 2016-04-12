import game2
import othello
import minimax
from ntuplesystematic import nTuplesSystematic
from bench import benchPlayer
from standardWPC import standardWPCPlayer
from randPlayer import randomPlayer

def evaluate():
	wins = [0, 0]
	for i in range(100):
		player1 = randomPlayer()
		player2 = nTuplesSystematic()
		winner = game2.play(othello.game(), game2.player_epsilon(lambda x: player1.play_next_move(x)),game2.player_epsilon(lambda x: player2.play_next_move(x)), False)
		if winner == 1:
			wins[0] += 1
		elif winner == 2:
			wins[1] += 1
		winner = game2.play(othello.game(),game2.player_epsilon(lambda x: player2.play_next_move(x)), game2.player_epsilon(lambda x: player1.play_next_move(x)), False)
		if winner == 2:
			wins[0] += 1
		elif winner == 1:
			wins[1] += 1

	print wins

evaluate()