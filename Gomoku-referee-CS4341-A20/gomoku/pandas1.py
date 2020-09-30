import logging
import sys
import os
import random
import time
import hashlib
import shutil
import copy
import os.path
from os import path


move_file_name = "move_file"
all_moves = []
whatTurn = 0

'''
pass in state of board and move history to help start the algorithm
'''
def makeGameTree():
    '''
    utility function needed to help algorithm determine which move is best 
    '''
    lastMove = readMoveFile()
    all_moves.append(lastMove)
    print "all moves:"
    print(all_moves)
    #make board from previous moves
    if(all_moves[0] ==  '-1-1'):
        all_moves.remove('-1-1')
        line = 'pandas1.py H 8'
    elif len(all_moves) == 1 and whatTurn == 0:
        line = 'pandas1.py H 8'
    else:
        #calculate what move should be 
        line = 'pandas1.py A 1'

    move = getMove(line)
    all_moves.append(move)

    print "all moves 2:"
    print(all_moves)

    writeMoveFile(line)

'''
utility function is the higher the options left the lower the cost
- how many empty spaces around player
- how many of your pieces you have and location of pieces that match winning position
- position and amount of opponent player (how close is it to winning )
'''
def writeMoveFile(move, move_file="move_file"):
    with open(move_file, 'w') as move_fid:
        move_text = str(move)
        logging.debug("Writing move text \"%s\" to %s" % (move_text, move_file))
        move_fid.write(move_text)
        move_fid.write("\n")
        move_fid.flush()
    return os.stat(move_file_name).st_mtime

def readMoveFile(move_file="move_file", purge=True):
    with open(move_file) as move_fid:
        line = move_fid.readline()
    if line is None:
        logging.error("Move file empty!")

    logging.debug("Read from %s: \"%s\"" % (move_file, line))

    move = getMove(line)

    return move

def getMove(line, move_file="move_file"):
    line_parts = line.split()
    try:
        team_name = line_parts[0]
        move_x = ord(line_parts[1].lower()) - ord('a')
        move_y = int(line_parts[2], 10) - 1
    except IndexError:
        logging.debug("Problems reading the move file")
        shutil.copyfile(move_file, "%s.bkup" % move_file)
        team_name = None
        move_x = -1
        move_y = -1

    move = str(move_x) + str(move_y)

    return move

if __name__ == "__main__":
    while not os.path.exists('pandas1.py.go'):   
        time.sleep(1)
    if os.path.isfile('pandas1.py.go'):  
        if not path.exists('end_game'): 
            makeGameTree()
        if path.exists('end_game'):
            print("ending")
            sys.exit()

