from player_1010 import *

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
	num_candidates = len(old_players)
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
	if num_candidates < 10:
		return players[:num_candidates]
	elif num_candidates == 10:
		return players
	else:
		for x in range(num_candidates-10):
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

#The initial scrambling of all the candidates
def initial_scramble(players):
	for player in players:
		randomize_weights(player)
	return 

#The players table contains the candidates
def intialize_players_list(num_candidates):
	players = []
	for x in range(num_candidates):
		P = Player()
		players.append(P)
	rename(players)
	return players

#Run the evolution for the desired number of generations
def run_evolution(num_generations, num_candidates, board_seeds, *starting_weights):
	#initialize everything
	scoredict = dict()
	players = intialize_players_list(num_candidates)
	initial_scramble(players)
	player_scores = []
	#set given starting weights
	player_index = 0
	for weight_list in starting_weights:
		players[player_index].adopt_weights(weight_list)
		player_index += 1
	#Generation loop
	top_hiscore = 0
	top_average = 0
	top_weights = []
	for x in range(num_generations):
		print("Starting Generation",x)
		player_scores = []
		for player in players:
			scores = []
			print("    "+player.name+" Weights:"+str(player.weights))
			for seed in board_seeds:
				score = run_sim(player, seed, scoredict)
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
		top_weights = top.weights
		top_hiscore = player_scores[i][1]
		top_average = player_scores[i][0]
		print("NAME:",top.name)
		print("WEIGHTS:",top_weights)
		print("HISCORE:",top_hiscore)
		print("AVERAGE:",top_average)
		print()
		players = mutate_all(players, player_scores)
		for player in players:
			for x in range(len(player.weights)):
				player.weights[x] = round(player.weights[x],1)
		rename(players)
	#print and return results
	print("""Most effective weights: {}
		Highest Score: {}
		Average Score: {}""".format(top_weights, top_hiscore, top_average))
	return top_weights


# BEST WEIGHTS YET [13.4, 0.2, -0.7, 5.8, 5.1, -1.0]
def main():
	known_good_weights = [
	[13.4, 0.2, -0.7, 5.8, 5.1, -1.0],
	[8.7, -6.9, 6.1, 0.5, 6.2, -1.5],
	[6.0, -5.2, 9.0, -9.6, 9.5, -4.3]]
	weights = run_evolution(20, 20, list(range(10)) *known_good_weights)

if __name__ == "__main__":
	main_rand = Random()
	main()

