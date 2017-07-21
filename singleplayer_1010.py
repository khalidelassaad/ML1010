from player_1010 import *
from random import randint

def run_x_times(x, weights, show_board=False, show_round=False, step_by_step=False):
	print("Running with weights",weights)
	P = Player()
	P.show_board = show_board
	P.show_round = show_round
	P.step_by_step = step_by_step
	P.adopt_weights(weights)
	scores = []
	for i in range(x):
		P.seed = randint(0,100000000)
		score = P.play()
		scores.append(score)
		print("    Run {}    Score {}    Hi {}    Avg {}    Seed {}".format(
			i,score,max(scores),round(sum(scores)/len(scores),1),P.seed))
	return scores

run_x_times(1000, [14.2, 0.6, 0.2, 1.5, 5.1, -0.3], True, True, True)