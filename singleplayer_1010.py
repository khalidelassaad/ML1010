from player_1010 import *
from random import randint
import cProfile

def run_x_times(x, weights, show_board=False, show_round=False, show_score=False, step_by_step=False, seed=None, printfile=None):
	P = Player()
	P.logfilename = printfile
	P.show_board = show_board
	P.show_round = show_round
	P.show_score = show_score
	P.step_by_step = step_by_step
	P.adopt_weights(weights)
	scores = []
	print("Running with weights",P.weights)
	for i in range(x):
		if seed != None:
			current_seed = seed + i
		else:
			current_seed = randint(0,x*10000)
		P.seed = current_seed
		score = P.play()
		scores.append(score)
		print("    Run {}    Score {}    Hi {}    Avg {}    Seed {}".format(
			i,score,max(scores),round(sum(scores)/len(scores),1),P.seed))
	return scores

#cProfile.run("run_x_times(1, [14.2, 0.6, 0.2, 1.5, 5.1, -0.3, 0], show_board = True, show_round = False, seed = 55)")
#cProfile.run("run_x_times(1, [-1.3, -3.8, 8.1, -4.0, 6.2, -6.2, -1.0], show_board = True, show_round = False, seed = 55)")
#run_x_times(1, [14.2, 0.6, 0.2, 1.5, 5.1, -0.3, 0], 
#	show_board = True, show_round = True, show_score=True, step_by_step = False)
cProfile.run("run_x_times(1, [14.2, 0.6, 0.2, 1.5, 5.1, -0.3, 0], seed = 2)")
