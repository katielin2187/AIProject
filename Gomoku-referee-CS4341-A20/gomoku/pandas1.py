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

def makeGameTree(whatTurn, all_moves):

    #get oponent's last move and add it to array of moves
    #if len(all_moves) >= 3:
    lastMove = readMoveFile()
    if lastMove not in all_moves:
        print(lastMove)
        all_moves.append(lastMove)
        if whatTurn == 2: #check opponent hasn't overwritten your turn after second turn
            if all_moves[0][-3:] == all_moves[1][-3:]:
                all_moves.pop(0)
            
        print("all moves:")
        print(all_moves)

    
   

    print("all moves:")
    print(all_moves)
    #make board from previous moves

    #if first move choose middle of board
    if(all_moves[0]=='None -1 -1'):
        all_moves.pop()
        line = 'pandas1.py H 8'
        whatTurn += 2
    elif len(all_moves) == 1 and whatTurn == 0: #if it's your first move but you're the second player
        print("overwriting first play")
        line = 'pandas1.py H 8'

        #print(all_moves[0][-3:])

        if(all_moves[0][-3:]=='7 7'):
            all_moves.pop(0) # gets rid of the previous 7 7 position since we don't want two things in the same spot
        whatTurn +=2
    else:
        print("create game board")
        whatTurn +=2
        #create game board
        level= []#will include the 15x15 options
        board= []
        for i in range(15):
            for j in range(15):
                move = 'pandas1.py ' + str(i) + ' '+ str(j)
                #print (move)
                if move not in all_moves:
                    board = all_moves.copy()
                    board.append(move)
                    if board not in level:
                        level.append(board)
        #print(level)

        #randomly choosing which move for now
        #getting last board in the level and taking out the move to be added
        tempBoard = level[len(level)-1]
        howManyTurnsSoFar = len(tempBoard)
        line = tempBoard[howManyTurnsSoFar-1]
        line = getLetterNumberMove(line)

    #add move to array 
    
    all_moves.append(getMove(line))

    print("all moves 2:")
    print(all_moves)

    #write move to file 
    writeMoveFile(line)

    if __name__ == "__main__":
        removeTeamGoFile()
        while not os.path.exists('pandas1.py.go'):   
            time.sleep(1)
        if os.path.isfile('pandas1.py.go'):  
            if not path.exists('end_game'): #team file exists and end game does not
                makeGameTree(whatTurn, all_moves)
            if path.exists('end_game'):
                print("ending")
                sys.exit()
'''
utility function is the higher the options left the lower the cost
- how many empty spaces around player
- how many of your pieces you have and location of pieces that match winning position
- position and amount of opponent player (how close is it to winning )
'''

def removeTeamGoFile():
    team_go_file = 'pandas1.py.go'
    try:
        os.remove(team_go_file)
    except OSError:
        pass
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


def getLetterNumberMove(line):
    line_parts = line.split()
    try:
        team_name = line_parts[0]
        move_x = chr(ord('@')+ int(line_parts[1])+1)
        move_y = int(line_parts[2]) + 1 
    except IndexError:
        logging.debug("Problems with the move")
        shutil.copyfile(move_file, "%s.bkup" % move_file)
        team_name = None
        move_x = -1
        move_y = -1

    move = team_name + ' ' + str(move_x) + ' ' + str(move_y)

    return move

#given a string, it will decipher into a move
def getMove(line, move_file="move_file"):
    line_parts = line.split()
    try:
        team_name = line_parts[0]
        move_x = ord(line_parts[1].lower()) - ord('a')
        move_y = int(line_parts[2], 10)-1
    except IndexError:
        logging.debug("Problems reading the move file")
        shutil.copyfile(move_file, "%s.bkup" % move_file)
        team_name = None
        move_x = -1
        move_y = -1
    except TypeError:
        logging.debug("cannot convert negative numbers to letters")
        team_name = line_parts[0]
        move_x = -1
        move_y = -1

    move = str(team_name)+ ' ' +  str(move_x) + ' ' + str(move_y)

    # in future add a addToBoard(move, team)
    #which using the parsed move and the team (X or O) will create a board for us

    return move

if __name__ == "__main__":
    while not os.path.exists('pandas1.py.go'):   
        time.sleep(1)
    if os.path.isfile('pandas1.py.go'):  
        if not path.exists('end_game'): #team file exists and end game does not
            whatTurn = 0
            all_moves = []
            makeGameTree(whatTurn, all_moves)
        if path.exists('end_game'):
            print("ending")
            sys.exit()

