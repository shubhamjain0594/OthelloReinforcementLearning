
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
		self.moveb = 0
		self.movew = 0
		self.last_vb = 0
		self.last_vw = 0
		self.fin_v = []
		self.fin_val = []

	def play_move(self,game,epsilon = 0):
		moves = game.generate_moves()
		num = random.uniform(0,1)
		if(num <= epsilon):
			temp = game.copy()
			if(game.player==-1):
				if(self.moveb == 0):
					move = random.choice(moves)
					temp.play_move(move)
					v=[]
					for k in range(8):
							for l in range(8):
								v.append(temp.get_color([k,l]))
					v2 = [v]
					v1 = self.net.sim(v2)
					self.moveb = self.moveb+1
					self.last_vb = v
					return (v1[0][0], move)
				else:
					if(moves[0]==None):
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(game.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = [v1]
						#print 0
						#print self.last_vb
						self.fin_v.append(self.last_vb)
						self.fin_val.append(v1)
						self.last_vb = v
						return (0,None)
					else:
						move = random.choice(moves)
						reward = 0
						temp.play_move(move)
						if(temp.terminal_test()):
							if(temp.score()>0):
								reward=-1
							elif(temp.score()<0):
								reward = 1
						v=[]
						for k in range(8):
							for l in range(8):
								v.append(temp.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = reward + v1
						v1 = [v1]
						#print 1
						#print self.last_vb
						self.fin_v.append(self.last_vb)
						self.fin_val.append(v1)
						self.last_vb = v
						return (v1[0],move)
			else:
				if(self.movew == 0):
					move = random.choice(moves)
					temp.play_move(move)
					v=[]
					for k in range(8):
							for l in range(8):
								v.append(temp.get_color([k,l]))
					v2 = [v]
					v1 = self.net.sim(v2)
					self.movew = self.movew+1
					self.last_vw = v
					return (v1[0][0], move)
				else:
					if(moves[0]==None):
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(game.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = [v1]
						#print 2
						#print self.last_vw
						self.fin_v.append(self.last_vw)
						self.fin_val.append(v1)
						self.last_vw = v
						return (0,None)
					else:
						move = random.choice(moves)
						reward = 0
						temp.play_move(move)
						if(temp.terminal_test()):
							if(temp.score()>0):
								reward=-1
							elif(temp.score()<0):
								reward = 1
						v=[]
						for k in range(8):
							for l in range(8):
								v.append(temp.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = reward + v1
						v1 = [v1]
						#print 3
						#print self.last_vw
						self.fin_v.append(self.last_vw)
						self.fin_val.append(v1)
						self.last_vw = v
						return (v1[0],move)
		else:
			if(game.player == -1):
				if(self.moveb==0):
					j=0
					max1 = 0
					best_v = 0
					best_move = None
					for move in moves:
						temp = game.copy()
						temp.play_move(move)
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(temp.get_color([k,l]))
						#print v
						v2 = [v]
						v1 = self.net.sim(v2)
						if(j==0):
							max1 = v1[0][0]
							best_v = v
							best_move = move
						elif(v1[0][0]>max1):
							max1 = v1[0][0]
							best_move = move
							best_v =v
						j = j+1
					self.moveb = self.moveb+1
					self.last_vb = best_v
					return (max1, best_move)
				else:
					if(moves[0]==None):
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(game.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = [v1]
						#print 4
						#print self.last_vb
						self.fin_v.append(self.last_vb)
						self.fin_val.append(v1)
						self.last_vb = v
						return (0,None)
					else:
						j=0
						max1 = 0
						best_v = 0
						best_move = 0
						for move in moves:
							temp = game.copy()
							temp.play_move(move)
							v = []
							for k in range(8):
								for l in range(8):
									#print temp.get_color([k,l])
									v.append(temp.get_color([k,l]))
							#print v
							v2 = [v]
							v1 = self.net.sim(v2)
							if(j==0):
								max1 = v1[0][0]
								best_v = v
								best_move = move
							elif(v1[0][0]>max1):
								max1 = v1[0][0]
								best_move = move
								best_v =v
							j = j+1
						temp = game.copy()
						reward = 0
						temp.play_move(best_move)
						if(temp.terminal_test()):
							if(temp.score()>0):
								reward=-1
							elif(temp.score()<0):
								reward = 1
						v2 = [best_v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = reward + v1
						v1 = [v1]
						#print 5
						#print self.last_vw
						self.fin_v.append(self.last_vb)
						self.fin_val.append(v1)
						self.last_vb = best_v
						return (max1,best_move)
				
			else:
				if(self.movew==0):
					j=0
					max1 = 0
					best_v = 0
					best_move = 0
					for move in moves:
						temp = game.copy()
						temp.play_move(move)
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(temp.get_color([k,l]))
						#print v
						v2 = [v]
						v1 = self.net.sim(v2)
						if(j==0):
							max1 = v1[0][0]
							best_v = v
							best_move = move
						elif(v1[0][0]<max1):
							max1 = v1[0][0]
							best_move = move
							best_v =v
						j = j+1
					self.movew = self.movew+1
					self.last_vw = best_v
					return (max1,best_move)
				else:
					if(moves[0]==None):
						v = []
						for k in range(8):
							for l in range(8):
								#print temp.get_color([k,l])
								v.append(game.get_color([k,l]))
						v2 = [v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = [v1]
						#print 6
						#print self.last_vw
						self.fin_v.append(self.last_vw)
						self.fin_val.append(v1)
						self.last_vw = v
						return (0,None)
					else:
						j=0
						max1 = 0
						best_v = 0
						best_move = 0
						for move in moves:
							temp = game.copy()
							temp.play_move(move)
							v = []
							for k in range(8):
								for l in range(8):
									#print temp.get_color([k,l])
									v.append(temp.get_color([k,l]))
							#print v
							v2 = [v]
							v1 = self.net.sim(v2)
							if(j==0):
								max1 = v1[0][0]
								best_v = v
								best_move = move
							elif(v1[0][0]<max1):
								max1 = v1[0][0]
								best_move = move
								best_v =v
							j = j+1
						temp = game.copy()
						reward = 0
						temp.play_move(best_move)
						if(temp.terminal_test()):
							if(temp.score()>0):
								reward=-1
							elif(temp.score()<0):
								reward = 1
						v2 = [best_v]
						v1 = self.net.sim(v2)
						v1 = v1[0][0]
						v1 = reward + v1
						v1 = [v1]
						#print 7
						#print self.last_vw
						self.fin_v.append(self.last_vw)
						self.fin_val.append(v1)
						self.last_vw = best_v
						return (max1,best_move)

	def reset(self):
		#print self.fin_v
		#print self.fin_val
		error = self.net.train(self.fin_v,self.fin_val,epochs=5,show=1)
		self.moveb = 0
		self.movew = 0
		self.last_vb = 0
		self.last_vw = 0
		self.fin_v = []
		self.fin_val = []

	def reset_without_train(self):
		self.moveb = 0
		self.movew = 0
		self.last_vb = 0
		self.last_vw = 0
		self.fin_v = []
		self.fin_val = []

if __name__ == "__main__":
	"""
	Creates a main player
	"""
	playernew = nn()
	nTuplesSystematicObject = nts.nTuplesSystematic()
	game2.play(othello.game(), game2.player(lambda x: playernew.play_move(x)),game2.player(lambda x: nTuplesSystematicObject.play_next_move(x)), True)
	playernew.reset_without_train()
	time.sleep(5)
	k = 100
	for i in range(k):
		print(i)
		game2.play(othello.game(), game2.player(lambda x: playernew.play_move(x,0.3)),game2.player(lambda x: playernew.play_move(x,0.3)), False)
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

	print wins
	f = open('results','a')
	val = (k,0.001,'epsilon',wins)
	val = str(val)





