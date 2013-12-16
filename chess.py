#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys

board = [
					["r","h","b","q","k","b","h","r"],
					["p","p","p","p","p","p","p","p"],
					["","","","","","","",""],
					["","","","","","","",""],
					["","","","","","","",""],
					["","","","","","","",""],
					["p","p","p","p","p","p","p","p"],
					["r","h","b","k","q","b","h","r"]
				]

#Convert letter to Index (eg. 'a5' to 0 or 'e3' to 5)
def convert(pair):
	print "Checking pair: " + pair
	new_int = ord(pair[0]) - 97 # in ascii lower case a is 97
	print "Letter is " + str(pair[0]) + " -> " + str(new_int)
	return new_int, int(pair[1])

def take_input():
	print ' Enter piece to move. Example: e2 e4 '
	r = raw_input()
	move = r.split()
	return move[0:1], move[1:]

def printBoard(board):
	for row in board[:]:
		for piece in row[:]:
			print piece,
		print #next row
	print #new line

	

while 1:
	print 'White\'s turn. Enter row'
	start,end = take_input()
	print start
	print end
	start = convert(start[0])
	print start
	end = convert(end[0])
	print end
	printBoard(board)

	board[end[0]][end[1]] = board[start[0]][start[1]]
	board[start[0]][start[1]] = ""
	printBoard(board)
