import game2
import othello
import minimax
from ntuplesystematic import nTuplesSystematic
from bench import benchPlayer
from standardWPC import standardWPCPlayer

def evaluate():
	wins = [0, 0]
	for i in range(100):
		nTuplesSystematicObject = nTuplesSystematic()
		benchPlayerObject = standardWPCPlayer()
		winner = game2.play(othello.game(), game2.player_epsilon(lambda x: benchPlayerObject.play_next_move(x)),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), False)
		if winner == 1:
			wins[0] += 1
		elif winner == 2:
			wins[1] += 1
		winner = game2.play(othello.game(),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player_epsilon(lambda x: benchPlayerObject.play_next_move(x)), False)
		if winner == 2:
			wins[0] += 1
		elif winner == 1:
			wins[1] += 1

	print wins

evaluate()