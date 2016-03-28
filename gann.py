import neurolab as nl
import game2
import othello
import ntuplesystematic as nts
import time
import random
import numpy
import nn

populationsize=10
goodpopulationsize=5
generations=5
parent = []
child = [0]*populationsize

for i in range(populationsize):
		playermaxx = nn.nn()
		for j in range(200):
			game2.play(othello.game(), game2.player(lambda x: playermaxx.play_move(x,0.3)),game2.player(lambda x: playermaxx.play_move(x,0.3)), False)
			playermaxx.reset()
		parent.append(playermaxx)


for z in range(generations):
	win = []
	for i in range(populationsize):
		winsfori=0
		for j in range(100):
			winner = game2.play(othello.game(), game2.player_epsilon(lambda x: parent[i].play_move(x)),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), False)
			if winner == 1:
				winsfori += 1
			winner = game2.play(othello.game(),game2.player_epsilon(lambda x: nTuplesSystematicObject.play_next_move(x)), game2.player_epsilon(lambda x: parent[i].play_move(x)), False)
			if winner == 2:
				winsfori += 1
		win.append(winsfori)	

	sortedwin = sorted(range(len(win)), key=lambda k: -1*win[k])
	
	goodparents = []
	for i in range(goodpopulationsize):
		a1 = parent[sortedwin[i]].layers[0].np['w']
		a2 = parent[sortedwin[i]].layers[1].np['w']

		a3 = []
		for j in range(50):
			for k in range(64):
				a3.append(a1[j][k])
		for j in range(50):
			a3.append(a2[1][j])

		goodparents.append(a3)

	#sampling
	goodMean = np.mean(goodparents)
	goodCov = np.cov(goodparents)

	for i in range(populationsize):
		child[i] = 	np.random.multivariate_normal(goodMean, goodCov).T

	#parent[i] from child[i]
	for i in range(populationsize):
		for j in range(50):
			for k in range(64):
				parent[i].layers[0].np['w'][j][k] = child[i][j*64 + k]

		for j in range(50):
			parent[i].layers[1].np['w'][1][j] = child[i][50*64 + j]

	#backpropagation in parent[i]
	for i in range(populationsize):
		for j in range(200):
			game2.play(othello.game(), game2.player(lambda x: parent[i].play_move(x,0.3)),game2.player(lambda x: parent[i].play_move(x,0.3)), False)
			parent[i].reset()






