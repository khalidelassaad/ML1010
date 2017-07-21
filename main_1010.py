from player_1010 import *

NUM_CANDIDATES = 20# DO NOT SET LESS THAN 3, only evolves well with 10 or more (see mutate_all)
NUM_GENERATIONS = 20

#The main random number generator
#used to mutate candidates
main_rand = Random()

#The board_seeds table decides how many games will be played
#with its length, the seeds are arbitrary
board_seeds = [8,9,99,999,9999,9997]

#Sets player names and appends each player to the players list
def rename(players):
	for x in range(len(players)):
		players[x].name = "Candidate " + str(x + 1)

def randomize_weights(player):
	"""Totally scrambles the weights of a player's strategy functions to a
	value from -10 to 10 step by 0.1"""
	for x in range(len(player.weights)):
		player.weights[x] = main_rand.randrange(-100,101)/10
	return player

def avg(*args):
	return(sum(args)/len(args))

def avg_l(l):
	return(sum(l)/len(l))

def avg_w(*players):
	P = Player()
	weights = []
	for x in P.weights:
		weights.append([])
	for player in players:
		for x in range(len(player.weights)):
			weights[x].append(player.weights[x])
	for x in range(len(P.weights)):
		P.weights[x]=avg_l(weights[x])
	return P

def gene_mix(*players):
	P = Player()
	weights = []
	for x in P.weights:
		weights.append([])
	for player in players:
		for x in range(len(player.weights)):
			weights[x].append(player.weights[x])
	for x in range(len(P.weights)):
		P.weights[x]=main_rand.choice(weights[x])
	return P

def breed(*players):
	P = gene_mix(*players)
	return mutate_shift(P)

def mutate_shift(player):
	"""creates a copy of the given player, with slight mutations"""
	P = Player()
	for x in range(len(player.weights)):
		P.weights[x]=player.weights[x]+main_rand.randrange(-20,21)/10
	return P

def mutate_all(old_players, scores):
	"""mutates the players table (see diagram for details)"""
	ziplist = list(zip(old_players, scores))
	ziplist.sort(reverse=True, key = lambda x: avg_l(x[1]))
	c1 = ziplist[0][0]
	c2 = ziplist[1][0]
	c3 = ziplist[2][0]
	c4 = breed(c1, c2)
	c5 = breed(c2, c3)
	c6 = breed(c1, c3)
	c7 = breed(c1, c2, c3)
	c8 = mutate_shift(c1)
	c9 = mutate_shift(c7)
	c10 = randomize_weights(Player())
	players = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
	if NUM_CANDIDATES < 10:
		return players[:NUM_CANDIDATES]
	elif NUM_CANDIDATES == 10:
		return players
	else:
		for x in range(NUM_CANDIDATES-10):
			players.append(randomize_weights(Player()))
		return players




def run_sim(player, seed, scorehistory):
	player.seed = seed
	key = (tuple(player.weights),seed)
	if key in scorehistory:
		return scorehistory[key]
	else:
		score = player.play()
		scorehistory[key] = score
		return score

#The players table contains the candidates
players = []

for x in range(NUM_CANDIDATES):
	P = Player()
	players.append(P)
rename(players)

SCOREDICT = dict()
player_scores = []

#The initial scrambling of all the candidates
for player in players:
	randomize_weights(player)

#known impressive weights
#players[0].weights = [8.7, -6.9, 6.1, 0.5, 6.2, -1.5]
#players[1].weights = [6.0, -5.2, 9.0, -9.6, 9.5, -4.3]

#Run the evolution for the desired number of generations
for x in range(NUM_GENERATIONS):
	print("Starting Generation",x)
	player_scores = []
	for player in players:
		scores = []
		print("    "+player.name+" Weights:"+str(player.weights))
		for seed in board_seeds:
			score = run_sim(player, seed, SCOREDICT)
			scores.append(score)
		average = avg_l(scores)
		hiscore = max(scores)
		print("    AVERAGE =",average)
		print("    HISCORE =",hiscore)
		print()
		player_scores.append((average,hiscore))
	print("Top performer of Generation",x)
	top_player_score = max(player_scores, key=lambda x: avg(x[0],x[1]))
	i = player_scores.index(top_player_score)
	top = players[i]
	print("NAME:",top.name)
	print("WEIGHTS:",top.weights)
	print("HISCORE:",player_scores[i][1])
	print("AVERAGE:",player_scores[i][0])
	print()
	players = mutate_all(players, player_scores)
	for player in players:
		for x in range(len(player.weights)):
			player.weights[x] = round(player.weights[x],1)
	rename(players)

