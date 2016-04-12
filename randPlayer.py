# random player
# plays random moves

import game2
import othello
import random

class randomPlayer():
	def __init__(self):
		pass

	def play_next_move(self, game):
		"""
		Plays a move in random
		"""
		moves = game.generate_moves()
		return (0,random.choice(moves))
