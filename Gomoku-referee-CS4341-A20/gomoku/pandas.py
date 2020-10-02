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
    team = 'pandas.py'

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
        line = 'pandas.py H 8'
        whatTurn += 2
    elif len(all_moves) == 1 and whatTurn == 0: #if it's your first move but you're the second player
        print("overwriting first play")
        line = 'pandas.py H 8'

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

                move = 'pandas.py ' + str(i) + ' '+ str(j)
                #print (move)
                if move not in all_moves:
                    board = all_moves.copy()
                    board.append(move)
                    if board not in level:
                        level.append(board)
        #print(level)

        #with level get the utlity value for each board in level
        sendToUtlity(level, team)

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
        while not os.path.exists('pandas.py.go'):   
            time.sleep(1)
        if os.path.isfile('pandas.py.go'):  
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
    team_go_file = 'pandas.py.go'
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

def sendToUtlity(level, team):
    for board in level:
        utilityOfBoard = Utility(board, team)

def Utility(board, team):
    '''
    winning => 10
    blocking opponent's 5th => 9
    making 4th connection => 8
    blocking opponent's 4th => 7
    making 3th connection => 6
    blocking opponent's 3th => 5
    making 2th connection => 4
    making 1st connection => 3
    blocking opponent's 2th => 2
    blocking opponent's 1th => 1   don't need this, cannot block a move if they have nothing on the board
    empty surrounding spaces => 1  checks diagonals
    '''

    winning =10
    blocking5 = 9
    making4 = 8
    blocking4 = 7
    making3 = 6
    blocking3 = 5
    making2 = 4
    making1 = 3
    blocking2 = 2
    #blocking1 = 1
    emptySpaces = 1

    utilityVal = 0
    nextPossibleMove= board[len(board)-1]
    boardSoFar = [x for i, x in enumerate(board) if i !=len(board)-1]

   
    if Winning(board,nextPossibleMove,boardSoFar, team):
        utilityVal += winning
    if callBlockingFive(board,nextPossibleMove,boardSoFar, team):
        utilityVal += blocking5   
    if callMakingFour(board,nextPossibleMove,boardSoFar, team):
        utilityVal += making4
    if callBlockingFour(board,nextPossibleMove,boardSoFar, team):
        utilityVal += blocking4   
    if callMakingThree(board,nextPossibleMove,boardSoFar, team):
        utilityVal += making3  
    if callBlockingThree(board,nextPossibleMove,boardSoFar, team):
        utilityVal += blocking3  
    if callMakingTwo(board,nextPossibleMove,boardSoFar, team):
        utilityVal += making2

    numOfTwo = callBlockingTwo(board,nextPossibleMove,boardSoFar, team,blocking2)
    utilityVal += numOfTwo * blocking2 

    if callMakingOne(board,nextPossibleMove,boardSoFar,team):
        utilityVal += making1
    if len(board) ==2: #if opponent erases your move, pick spot with most empty spaces
        numOfEmpty = callEmptySpaces(board,nextPossibleMove,boardSoFar, team)
        utilityVal += numOfEmpty

    return utilityVal


def Winning(board,nextPossibleMove,boardSoFar, team):
    return True
def callBlockingFive(board,nextPossibleMove,boardSoFar, team):
    return True   
def callMakingFour(board,nextPossibleMove,boardSoFar, team):
    return True
def callBlockingFour(board,nextPossibleMove,boardSoFar, team):
    return True  
def callMakingThree(board,nextPossibleMove,boardSoFar, team):
    return True
def callBlockingThree(board,nextPossibleMove,boardSoFar, team):
    return True
def callMakingTwo(board,nextPossibleMove,boardSoFar, team):
    return True
def callBlockingTwo(board,nextPossibleMove,boardSoFar, team, blocking2):
    #take next possible move and compare it to 
    surrMoves = getSurr(board,nextPossibleMove,boardSoFar, team, blocking2)
    if len(surrMoves) == 0:
        return 0
    

    return 0
def callMakingOne(board,nextPossibleMove,boardSoFar, team):
    #not sure if this will work
    #check if team has had a move yet
    if team in board:
        #not first move
        return False
    else:
        #first move
        return True
def callEmptySpaces(board,nextPossibleMove,boardSoFar, team):
    return 0 

def getSurr(board,nextPossibleMove,boardSoFar, team):
    #if your opponent surrounds your possible move, then append it to 
    #the array and return surrounding moves
    surroundingMoves = []
    '''
        go through every level in board and construct picture of opponent
        if opponent 
            start counter/match board combos we hard code, if opponent has all [number ex: 3 areas in graph]
            then give starting, ending, number of opponent in a row, and if it is able to continue on
            either end (array of those locations)
            return array of (startingPos, endingPos, number in a row, array of position next to starting or ending if available)
            utilityFunction(array[2], len(positionArray))
                this gets the utility based of off number in a row and if it has spaces on both sides
                tuple = (utility,array)
                totalUtilities.append(tuple)
        if player
            start counter and only look for own spots in graph dont worry about opponent because utlity will 
            give what to do based off of returned info
            also give starting, ending, number of own player in a row, and if 
            it is able to continue on either end (array of those locations)
            return tuple of (startingPos, endingPos, number in a row, array of position next to starting or ending if available)
            utilityFunction(array[2], len(positionArray))
                this gets the utility based of off number in a row and if it has spaces on both sides
                tuple = (utility,array)
                totalUtilities.append(tuple)
        totalUtilities.sort() 
            -- out of if statement to sort both and start depth limited with first move off of array
        if starting and ending of either player is the same -> thats 1
        construct possible boards based off of these first move of array but alpha beta pruning while
        constructing tree(?)
        if can continue (either one)
            pass through utility function and determine what next move
            if utilityFunction
                add to either starting or ending location based off of what is available in array
            somekind of recursion action in here, making sure to add cost
                loop through every potential next position, sorted by initial highest 
                utility given with depth limited in mind
            is board full?
                totalCosts.append(str(moveLocation) + str(cost))
            find lowest cost and choose that move

        return next move 
    
    '''
    return surroundingMoves


if __name__ == "__main__":
    while not os.path.exists('pandas.py.go'):   
        time.sleep(1)
    if os.path.isfile('pandas.py.go'):  
        if not path.exists('end_game'): #team file exists and end game does not
            whatTurn = 0
            all_moves = []
            makeGameTree(whatTurn, all_moves)
        if path.exists('end_game'):
            print("ending")
            sys.exit()

