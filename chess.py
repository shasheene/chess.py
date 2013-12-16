#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys

class Piece():
	def __init__(self):
		self.moved = 0
		self.type="_"
	def moveValid(self,start,end):
		return 1

class Pawn(Piece):
	def __init__(self,col):
		self.col = col
		self.moved = 0
		self.type="p"
		if (col=="white"):
			self.forward_dir=1
		else:
			self.forward_dir=-1

	def moveValid(self,start,end):
		#FORWARD
		if (start[1]==end[1]): #If columns are same (ie Pawn moving forward)
			if (board[start[0]+1][end[1]].type!="_"): #if piece in front of us
				print 'ERROR: THERE IS A PIECE BLOCKING'
				return 0
			if (end[0]==start[0]+2): #If jumping two spaces:
				if (self.moved==1):
					print 'ERROR: CANNOT DO PAWN HOP AFTER FIRST MOVE'
					return 0
				if ((board[start[0]+1][end[1]].type!="_") or (board[start[0]+2][end[1]].type!="_")):
					print 'ERROR: THERE IS A PIECE BLOCKING'
					return 0
			if (abs(start[0]-end[0])>2):
				print 'ERROR: PAWN JUMPING TOO FAR'
				return 0
		#		if ((end[1]==start[1]) and board[end[0],end[1]].type==""):
		self.moved=1
		return 1
		

def convert(pair):
	""" Converts chess coords to index (eg. 'a4' to [4,0] or 'e3' to [3,5]). Returns in [row,col], Assumes valid input (for now) """
	print "Checking pair: " + pair
	col = ord(pair[0]) - 97 # in ascii lower case a is 97
	print "Letter is " + str(pair[0]) + " -> " + str(col)
	row = 8 - int(pair[1]) # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
	return row,col

def take_input():
	print ' Enter piece to move. Example: e2 e4 '
	r = raw_input()
	move = r.split()
	return move[0:1], move[1:]

def printBoard(board):
	for row in board[:]:
		for piece in row[:]:
			print piece.type + " ",
		print #next row
	print #new line

#Create board:
global board
board = []

piece = Piece() #test only
board.append([piece,piece,piece,piece,piece,piece,piece,piece])
board.append([]);
for i in range(0,8):
	p = Pawn("black")
	board[1].append(p);
for i in range(2,6):
	board.append([piece,piece,piece,piece,piece,piece,piece,piece])
board.append([]);
for i in range(0,8):
	p = Pawn("white")
	board[6].append(p);
piece = Piece() #test only
board.append([piece,piece,piece,piece,piece,piece,piece,piece])


"""board = [
					["r","h","b","q","k","b","h","r"],
					["p","p","p","p","p","p","p","p"],
					["","","","","","","",""],
					["","","","","","","",""],
					["","","","","","","",""],
					["","","","","","","",""],
					["p","p","p","p","p","p","p","p"],
					["r","h","b","k","q","b","h","r"]
				]"""

print 'WELCOME TO TEXT BASED CHESS'
printBoard(board)

while 1:
	print 'White\'s turn. Enter row'
	legalMove=0
	while (legalMove==0):
		start,end = take_input()
		print start
		print end
		start = convert(start[0])
		print start
		end = convert(end[0])
		print end
		printBoard(board)

		legalMove = board[start[0]][start[1]].moveValid(start,end)
		if (legalMove==0):
			print 'INVALID MOVE. Re-enter'
	board[end[0]][end[1]] = board[start[0]][start[1]]
	board[start[0]][start[1]] = piece
	printBoard(board)
