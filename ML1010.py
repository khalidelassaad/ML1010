#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3 -u
#A python script that simulates and solves 1010 boards
from random import randint, seed
from move_1010 import *
from strategies_1010 import *

def set_moves_for_shape(shape, board): 
    #return a set of moves
    return_set = set()
    for x in range(10):
        for y in range(10):
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
        self.score = 0
        self.current_round = list()
        self.move_set = set()
        self.game_over = False

    def update_move_set(self):
        self.move_set = set()
        for shape in self.current_round:
            self.move_set = self.move_set.union(set_moves_for_shape(shape, self.board))

    def pick_move(self):#THE MONEY FUNCTION
        movedict = {}
        for move in self.move_set:
            movedict[move] = 0
            for movescore_func in STRATEGIES:
                movedict[move] = movedict[move] + movescore_func(self.board, move)
        bestmove = Move()
        bestscore = 0
        firstloop = True
        for move, score in movedict.items():
            if firstloop:
                firstloop = False
                bestmove = move
                bestscore = score
                continue
            if score > bestscore:
                bestmove = move
                bestscore = score
        if bestmove == Move():
            raise Exception("No move selected")
        return (bestmove, bestscore)

    def next_round(self):
        if len(self.current_round):
            raise Exception("Tried to start new round before all shapes used")
        for x in range(3):
            i = randint(0,18)
            self.current_round.append(SHAPES[i])

    def play(self):
        self.board.clear()
        self.score = 0
        self.current_round = list()
        self.next_round()
        while self.game_over == False:
            self.board.print()
            self.update_move_set()
            if len(self.move_set) == 0:
                self.game_over = True
                break
            result = self.pick_move()
            move = result[0]
            print(result[1])
            self.current_round.remove(move.shape)
            self.board.place((move.row,move.col),move.shape)
            #Score: blocks in shape, lines cleared * 10,20,30,etc...
            if self.current_round == list():
                self.next_round()
            self.score += len(move.shape.blocks) + self.board.clear10()
            print("--Current Score:"+str(self.score))
        print("Final Score:", self.score)
        self.board.print()
        return self.score
