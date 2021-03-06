from random import Random
from move_1010 import *
from strategies_1010 import *
from hashlib import md5
from logfile_1010 import LogFile

def my_hash(string):
    m = md5()
    m.update(string.encode())
    return m.hexdigest()

def move_to_hash(move):
    return my_hash(str(move.col)+str(move.row)+move.shape.namestring)

def set_moves_for_shape(shape, board): 
    #return a set of moves
    return_set = set()
    for x in range(10):
        for y in range(10):
            if not board.grid[y][x]:
                if board.check_place((y,x), shape):
                    move = Move()
                    move.col = x
                    move.row = y
                    move.shape = shape
                    return_set.add(move)
    return return_set

def get_move_set(board, current_round):
    move_set = set()
    for shape in current_round:
        move_set = move_set.union(set_moves_for_shape(shape, board))
    return move_set

class Player():
    def __init__(self):
        self.board = Board()
        self.name = ""
        self.score = 0
        self.current_round = list()
        self.move_set = set()
        self.weights = [0]*len(STRATEGIES)
        self.random = Random()
        self.seed = 0
        self.show_board = False
        self.show_round = False
        self.step_by_step = False
        self.last_move = Move()
        self.logfilename = ""
        self.show_score = False

    def adopt_weights(self, weights):
        i = 0
        for i in range(len(weights)):
            self.weights[i] = weights[i]
        return

    def __str__(self):
        return "Player Object: {} {}".format(self.name,self.weights)

    def update_move_set(self):
        self.move_set = set()
        for shape in self.current_round:
            self.move_set = self.move_set.union(set_moves_for_shape(shape, self.board))
        return

    def pick_move(self):#THE MONEY FUNCTION
        movedict = {}
        for move in self.move_set:
            movedict[move] = 0
            for x in range(len(STRATEGIES)):
                if self.weights[x] == 0:
                    continue
                movescore_func = STRATEGIES[x]
                movedict[move] = movedict[move] + (movescore_func(self.board, move)*self.weights[x])
        bestmoves = []
        bestscore = 0
        firstloop = True
        for move, score in movedict.items():
            if firstloop:
                firstloop = False
                bestmoves = [move]
                bestscore = score
                continue
            if score == bestscore:
                bestmoves.append(move)
            if score > bestscore:
                bestmoves = [move]
                bestscore = score
        if bestmoves == []:
            print(movedict)
            raise Exception("No move selected")
        bestmove = max(bestmoves, key = lambda x: move_to_hash(x))
        x = bestmove
        return (bestmove, bestscore)

    def next_round(self):
        if len(self.current_round):
            raise Exception("Tried to start new round before all shapes used")
        for x in range(3):
            i = self.random.randint(0,18)
            self.current_round.append(SHAPES[i])
        return

    def draw_from_bools(self):
        if self.show_board:
            self.board.draw(self.last_move)
        if self.show_score:
            print("Score:",self.score)
        if self.show_round:
            print()
            print_round(self.current_round)
        if self.step_by_step:
            input()
        if (self.show_round or self.show_board) and not self.step_by_step:
            print()
        return

    def play(self):
        if self.logfilename:
            self.log = LogFile(self.logfilename)
        self.random.seed(self.seed)
        self.board.clear()
        self.draw_from_bools
        self.score = 0
        self.current_round = list()
        self.next_round()
        while True:
            if self.logfilename:
                self.log.print_to_file("Score: {} {} Hash: {}".format(str(self.score), str(self.last_move), move_to_hash(self.last_move)))
            self.update_move_set()
            if len(self.move_set) == 0:
                break
            result = self.pick_move()
            move = result[0]
            self.last_move = move
            self.current_round.remove(move.shape)
            self.board.place((move.row,move.col),move.shape)
            #Score: blocks in shape, lines cleared * 10,20,30,etc...
            if self.current_round == list():
                self.next_round()
            self.score += len(move.shape.blocks) + self.board.clear10()
            #Draw the board
            self.draw_from_bools()
        #print("        ",self.name,"Final Score:", self.score, "Seed:",self.seed)
        if self.logfilename:
            self.log.close()
        return self.score
