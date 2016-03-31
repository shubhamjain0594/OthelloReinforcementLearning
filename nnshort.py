
import neurolab as nl
import game2
import othello
import ntuplesystematic as nts
import time
import random

class nn:
	def __init__(self):
		self.x = [[-1,1] for x in range(64)]
		self.net = nl.net.newff(self.x,[1])
		#self.net.trainf = nl.train.train_gd
		self.move = [0]*2
		self.last_v = [0]*2
		self.fin_v = []
		self.fin_val = []

	def play_move(self,game,epsilon=0):
		moves = game.generate_moves()
		player = -game.player
		v=[]
		best_move = None
		if(moves[0]==None):
			for k in range(8):
				for l in range(8):
					#print temp.get_color([k,l])
					v.append(game.get_color([k,l]))
		else:
			bmove = 0
			num = random.uniform(0,1)
			if(num <= epsilon):
				bmove = random.choice(moves)
			else:
				j=0
				max1 = 0
				best_v = 0
				for move in moves:
					temp = game.copy()
					temp.play_move(move)
					v3 = []
					for k in range(8):
						for l in range(8):
							#print temp.get_color([k,l])
							v3.append(temp.get_color([k,l]))
					#print v
					v2 = [v3]
					v1 = self.net.sim(v2)
					if((j==0) or ((player*v1[0][0])>max1)):
						max1 = v1[0][0]
						bmove = move
					j = j+1
			best_move = bmove
			temp = game.copy()
			temp.play_move(bmove)
			for k in range(8):
				for l in range(8):
					#print temp.get_color([k,l])
					v.append(temp.get_color([k,l]))
		temp = game.copy()
		temp.play_move(best_move)
		reward = 0
		if(temp.terminal_test()):
			if(temp.score()>0):
				reward=-1
			elif(temp.score()<0):
				reward = 1

		v2 = [v]
		v1 = self.net.sim(v2)
		v1 = v1[0][0]
		v1 = reward + v1
		v1 = [v1]
		player = -player
		if(self.move[(player+1)/2]==0):
			self.move[(player+1)/2] = 1 + self.move[(player+1)/2]
			self.last_v[(player+1)/2]=v
		else:
			self.fin_v.append(self.last_v[(player+1)/2])
			self.fin_val.append(v1)
			self.last_v[(player+1)/2] = v
		return (v1[0],best_move)

	def reset(self):
		#print self.fin_v
		#print self.fin_val
		error = self.net.train(self.fin_v,self.fin_val,show=1,epochs=1)
		self.move = [0]*2
		self.last_v = [0]*2
		self.fin_v = []
		self.fin_val = []

	def reset_without_train(self):
		self.move = [0]*2
		self.last_v = [0]*2
		self.fin_v = []
		self.fin_val = []
		
if __name__ == "__main__":
	"""
	Creates a main player
	"""
	playernew = nn()
	nTuplesSystematicObject = nts.nTuplesSystematic()
	game2.play(othello.game(), game2.player(lambda x: playernew.play_move(x)),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), True)
	time.sleep(3)
	playernew.reset_without_train()
	game2.play(othello.game(),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player(lambda x: playernew.play_move(x)), True)
	time.sleep(3)
	playernew.reset_without_train()
	k = 200000
	for i in range(k):
		print(i)
		game2.play(othello.game(), game2.player(lambda x: playernew.play_move(x,0.1)),game2.player(lambda x: playernew.play_move(x,0.1)), False)
		playernew.reset()

	wins = [0, 0]
	for i in range(100):
		winner = game2.play(othello.game(), game2.player_epsilon(lambda x: playernew.play_move(x)),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), False)
		if winner == 1:
			wins[0] += 1
		elif winner == 2:
			wins[1] += 1
		winner = game2.play(othello.game(),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player_epsilon(lambda x: playernew.play_move(x)), False)
		if winner == 2:
			wins[0] += 1
		elif winner == 1:
			wins[1] += 1

	print(wins)
	#f = open('results','a')
	#val = (k,0.001,'epsilon',wins)
	#val = str(val)
	#f.write(val)




	













