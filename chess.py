#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys

class Piece(object):
	def __init__(self,col):
		self.moved = 0
		self.col = col
		self.type="_"
		if (self.col=="white"):
			self.enemyCol="black"
			self.forwardDir=-1
		elif (self.col=="black"):
			self.enemyCol="white"
			self.forwardDir=+1

	def getMoveSet(self,pieceLocation):
		return []

class Pawn(Piece):
	def __init__(self,col):
		super(Pawn, self).__init__(col)
		self.type="p"

	def getMoveSet(self,pieceLocation):
		myMoveSet=[]
		if (checkLocation(pieceLocation[0]+self.forwardDir,pieceLocation[1])=="_"): #Is space directly forward from us free?
			myMoveSet.append([pieceLocation[0]+self.forwardDir,pieceLocation[1]])
			if ((checkLocation(pieceLocation[0]+self.forwardDir*2,pieceLocation[1])=="_") and self.moved==0): #If in addition space TWO forward from us free, and we haven't moved
				myMoveSet.append([pieceLocation[0]+self.forwardDir*2,pieceLocation[1]]) #Pawn jump
		if (checkLocation(pieceLocation[0]+self.forwardDir,pieceLocation[1]-1)==self.enemyCol): #Attack north west
			myMoveSet.append([pieceLocation[0]+self.forwardDir,pieceLocation[1]-1])
		if (checkLocation(pieceLocation[0]+self.forwardDir,pieceLocation[1]+1)==self.enemyCol): #Attack north east
			myMoveSet.append([pieceLocation[0]+self.forwardDir,pieceLocation[1]+1])
			
		return myMoveSet

def checkLocation(row,column):
	return board[row][column].type

def convert(pair):
	""" Converts chess coords to index (eg. 'a4' to [4,0] or 'e3' to [3,5]). Returns in [row,col], Assumes valid input (for now) """
	print "Checking pair: " + pair
	col = ord(pair[0]) - 97 # in ascii lower case a is 97
	print "Letter is " + str(pair[0]) + " -> " + str(col)
	row = 8 - int(pair[1]) # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
	return row,col

def take_input():
	print ' Select piece to move. Example: e2 '
	r = raw_input()
	move = r.split()
	return move[0:1]

def printBoard(board):
	for row in board[:]:
		for piece in row[:]:
			print piece.type + " ",
		print #next row
	print #new line

#Create board:
global board
board = []

piece = Piece("black") #test only
board.append([piece,piece,piece,piece,piece,piece,piece,piece])
board.append([]);
for i in range(0,8):
	p = Pawn("black")
	board[1].append(p);
piece = Piece("") #test only
for i in range(2,6):
	board.append([piece,piece,piece,piece,piece,piece,piece,piece])
board.append([]);
for i in range(0,8):
	p = Pawn("white")
	board[6].append(p);
piece = Piece("white") #test only
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
	legalSelection=0
	while (legalSelection==0):
		selected = take_input()
		print selected
		legalSelection=1 #No error checking for now
		if (legalSelection==0):
			print 'INVALID MOVE. Re-enter'

	selected = convert(selected[0])
	printBoard(board)
	selectedMoveSet=board[selected[0]][selected[1]].getMoveSet(selected)
	print selectedMoveSet
	print 'Please enter index of move choice to make:'
	indexOfChoice = int(raw_input())
	end = selectedMoveSet[indexOfChoice]
	
	print 'Chose:',
	print end


	board[end[0]][end[1]] = board[selected[0]][selected[1]]
	board[selected[0]][selected[1]] = piece
	printBoard(board)
