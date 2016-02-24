# SYSTEMATIC N-TUPLE NETWORKS FOR OTHELLO POSITION EVALUATION
# http://www.cs.put.poznan.pl/wjaskowski/pub/papers/jaskowski2014ICGAsystematic.pdf
# Weights have been taken from https://github.com/wjaskowski/TCIAIG-2015-Co-CMA-ES/blob/master/cevo-games/src/main/resources/put/ci/cevo/games/othello/players/published/Jaskowski2014All2.player
import pickle
import othello
import minimax
import game2

class nTuplesSystematic(object):
	def __init__(self):
		"""
		Creates nTuplesSystematic Player using values from nTuplesSystematic.values
		"""
		f = open('ntuplesystematic.values', 'r')
		lut_index = {}
		lut_values = {}
		num_tuples = int(f.readline().strip())
		for i in range(num_tuples):
			tuple_size = int(f.readline().strip())
			similar_tuples = int(f.readline().strip())
			for j in range(similar_tuples):
				a1 = int(f.readline().strip())
				a2 = int(f.readline().strip())
				a = (a1,a2)
				lut_index[a] = i
			lut_values_elem = []
			for j in range(3**tuple_size):
				lut_values_elem.append(float(f.readline().strip()))
			lut_values[i] = lut_values_elem

		self.lut_index = lut_index
		self.lut_values = lut_values

	def get_evaluation_score(self,game):
		"""
		We use board inversion to calculate score
		Score is calculated such as to maximize black advantage
		"""
		evaluation_score = 0

		# If next player is white then I am black, hence inversion value is 1, otherwise -1
		inversion_val = 1 if game.player==1 else -1
		for key in self.lut_index.keys():
			lut_values_index = get_board_pos_value(inversion_val*game.board[key[0]/othello.size][key[0]%othello.size])
			lut_values_index += 3*get_board_pos_value(inversion_val*game.board[key[1]/othello.size][key[1]%othello.size])
			evaluation_score += self.lut_values[self.lut_index[key]][lut_values_index]
		return evaluation_score

	def play_next_move(self, game):
		"""
		Since we are using board inversion, we will return the move with best score
		"""
		best = None
		# try each move
		print game.generate_moves()
		for move in game.generate_moves():
			g = game.copy()
			g.play_move(move)
			# evaluate the position and choose the best move
			val = self.get_evaluation_score(g)
			print move,val
			# update the best operator so far
			if best is None or val > best[0]:
				best = (val, move)
		print best
		return best

def get_board_pos_value(game_elem):
	"""
	Returns 0 if piece is white
	Returns 1 if piece is empty
	Returns 2 if piece is black
	"""
	if game_elem==-1:
		return 2
	elif game_elem==1:
		return 0
	else:
		return 1


if __name__ == "__main__":
	"""
	Creates a main player
	"""
	nTuplesSystematicObject = nTuplesSystematic()

	# nTuplesSystematic - Black
	# Minimax - White
	# game2.play(othello.game(),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player(lambda x: minimax.minimax(x, 0)), False)

	# Minimax - Black
	# nTuplesSystematic - White
	# game2.play(othello.game(), game2.player(lambda x: minimax.minimax(x, 0)),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)),False)

	# nTuplesSystematic - Black
	# Minimax Edge Eval - White
	# game2.play(othello.game(),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player(lambda x: minimax.minimax(x, 0,othello.edge_eval)), True)
	
	# Minimax Edge Eval - Black
	# nTuplesSystematic - White
	game2.play(othello.game(), game2.player(lambda x: minimax.minimax(x, 0,othello.edge_eval)),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), True)
