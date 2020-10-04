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
        # level= [] #will include the 15x15 options
        # board= []
        # for i in range(15):
        #     for j in range(15):

        #         move = 'pandas.py ' + str(i) + ' '+ str(j)
        #         #print (move)
        #         if move not in all_moves:
        #             board = all_moves.copy()
        #             board.append(move)
        #             if board not in level:
        #                 level.append(board)
        #print(level)

        #with level get the utlity value for each board in level
        evalBoard(all_moves)

        #randomly choosing which move for now
        #getting last board in the level and taking out the move to be added
        
        
        line = 'pandas.py 6 7'
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
        shutil.copyfile(move_file_name, "%s.bkup" % move_file_name)
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
    # surrMoves = getSurr(board,nextPossibleMove,boardSoFar, team, blocking2)
    # if len(surrMoves) == 0:
    #    return 0
    return True
    

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

def evalBoard(board):
    #if your opponent surrounds your possible move, then append it to 
    #the array and return surrounding moves
    sendUtility = []
    # = [utility = 0 until evaluated, ourTeam = t/f, first pos, last pos, number in a row, array of empty that continues row]
    ourMoves = []
    opponentMoves = []
    currentArray = []
    emptySpaces = []
    emptyCounter = 0

    checkOurTurn = board[len(board) - 1]
    if 'pandas' in checkOurTurn:
        ourTurn = False
    else:
        ourTurn = True

    for i in range(len(board) - 1):
        position = [board[i][-3],board[i][-1]]
        # [column, row]

        if 'pandas' in board[i]:
            ourMoves.append(position)
        else:
            opponentMoves.append(position)
    for i in range(len(ourMoves) - 1): 
        currentMove = ourMoves[i]
        surroundings = getSurr(currentMove)
        currMoveBeginner = isBeginner(currentMove,j, board, ourMoves, opponentMoves, ourTurn)
        # returns true if finds a beginner node
        for j in surroundings:
            if j in ourMoves and currMoveBeginner:
                # get further investigations find where it is compared to currentMove
                posRelative = getPosition(currentMove, j, ourMoves, opponentMoves, ourTeam = True)
                # = [utility = 0 until evaluated, ourTeam = t/f, first pos, last pos, number 
                # in a row, array of empty that continues row]
                endingPositon = posRelative[0]
                numRow = posRelative[1]
                emptySpaces = posRelative[2]
                currentArray = [0, ourTurn, currentMove, endingPositon, numRow, emptySpaces] 
                sendUtility.append(currentArray) 
            elif isEmpty(j, ourMoves, opponentMoves) and currMoveBeginner:
                # when move is single and nothing surrounding
                emptySpaces = checkEmptyBothSides(currentMove, j, ourMoves, opponentMoves)
                currentArray = [0, ourTurn, currentMove, currentMove, 1, emptySpaces]
                emptyCounter = emptyCounter + 1
                # idk if we'll need counter yet
                sendUtility.append(currentArray)
        
    for i in range(len(opponentMoves) - 1): 
        currentMove = ourMoves[i]
        surroundings = getSurr(currentMove)
        currMoveBeginner = isBeginner(currentMove,j, board, ourMoves, opponentMoves, ourTurn)
        # returns true if finds a beginner node
        for j in surroundings:
            if j in opponentMoves and currMoveBeginner:
                # get further investigations find where it is compared to currentMove
                posRelative = getPosition(currentMove, j, ourMoves, opponentMoves, ourTeam = False)
                # = [utility = 0 until evaluated, ourTeam = t/f, first pos, last pos, number 
                # in a row, array of empty that continues row]
                endingPositon = posRelative[0]
                numRow = posRelative[1]
                emptySpaces = posRelative[2]
                currentArray = [0, ourTurn, currentMove, endingPositon, numRow, emptySpaces] 
                sendUtility.append(currentArray)
            elif isEmpty(j, ourMoves, opponentMoves) and currMoveBeginner:
                # when move is single and nothing surrounding
                emptySpaces = checkEmptyBothSides(currentMove, j, ourMoves, opponentMoves)
                currentArray = [0, ourTurn, currentMove, currentMove, 1, emptySpaces]
                emptyCounter = emptyCounter + 1
                # idk if we'll need counter yet
                sendUtility.append(currentArray) 

    return sendUtility 
    # send this to a utlity function which will return same array but with first value filled in 
    # sort array by that value depending on whether or not it is our turn 
    # add position to board that this function returns or make copy of a "fake" board and keep going 
    # recursion until the end of the board or until depth limited
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
            -- outside of if statement to sort both and start depth limited with first move off of array
        add own player to board based off of what was picked and opponents turn -- recursion from above again
        if board full or limit of depth limited search
            put board back to how it was and add second move from array of sorted utilites
            recursion again from the top make it drop WAP
        
        return next move 
    
    '''
def checkEmptyBothSides(move, emptyMove, ourMoves, opponentMoves):
    #checks if empty on both side
    #return array of empties
    currCol = int(move[0])
    currRow = int(move[1])
    empties = [emptyMove]
    if whereSurrMove(move, emptyMove) == 'top right' and isEmpty([str(currCol - 1), str(currRow + 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol - 1), str(currRow + 1)]]
    elif whereSurrMove(move, emptyMove) == 'top left' and isEmpty([str(currCol + 1), str(currRow + 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol + 1), str(currRow + 1)]]
    elif whereSurrMove(move, emptyMove) == 'bottom left' and isEmpty([str(currCol + 1), str(currRow - 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol + 1), str(currRow - 1)]]
    elif whereSurrMove(move, emptyMove) == 'bottom right' and isEmpty([str(currCol - 1), str(currRow - 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol - 1), str(currRow - 1)]]
    elif whereSurrMove(move, emptyMove) == 'top' and isEmpty([str(currCol), str(currRow + 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol), str(currRow + 1)]]
    elif whereSurrMove(move, emptyMove) == 'bottom' and isEmpty([str(currCol), str(currRow - 1)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol), str(currRow + 1)]]
    elif whereSurrMove(move, emptyMove) == 'left' and isEmpty([str(currCol + 1), str(currRow)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol + 1), str(currRow)]]
    elif whereSurrMove(move, emptyMove) == 'right' and isEmpty([str(currCol - 1), str(currRow)], ourMoves, opponentMoves) :
        empties = [emptyMove, [str(currCol - 1), str(currRow)]]
    return empties


def whereSurrMove(currentMove, surrMove):

    currCol = int(currentMove[0])
    currRow = int(currentMove[1])
    surrCol = int(surrMove[0])
    surrRow = int(surrMove[1])
    #where is surrounding move
    location = ''
    # if top right: surrCol - currCol > 0 and surrRow - currRow < 0
    if surrCol - currCol > 0 and surrRow - currRow < 0:
        # check empty bottom left if counter == 2
        if ((surrCol + 1 <= 14) and (surrRow - 1 >= 0)):
            location = 'top right'

    # if top left: surrCol - currCol < 0 and surrRow - currRow < 0
    elif surrCol - currCol < 0 and surrRow - currRow < 0:
            # check empty bottom right
        if ((surrCol - 1 >= 0) and (surrRow - 1 >= 0)):
            location = 'top left'

    # if bottom left: surrCol - currCol < 0 and surrRow - currRow > 0
    elif surrCol - currCol < 0 and surrRow - currRow > 0:
        if ((surrCol - 1 >= 0) and (surrRow + 1 <= 14)):
            location = 'bottom left'

    # if bottom right: surrCol - currCol > 0 and surrRow - currRow > 0
    elif surrCol - currCol > 0 and surrRow - currRow > 0:
        if ((surrCol + 1 <= 14) and (surrRow + 1 <= 14)):
            location = 'bottom right'

    # if top: surrRow - currRow < 0
    elif surrRow - currRow < 0:
        if surrRow - 1 >= 0:
            location = 'top'

    # if bottom: surrRow - currRow > 0
    elif surrRow - currRow > 0:
        if surrRow + 1 <= 14:
            location = 'bottom'

    # if left: surrCol - currCol < 0 
    elif surrCol - currCol < 0:
        if surrCol - 1 >= 0:
            location = 'left'

    # if right: surrCol - currCol > 0 
    elif surrCol - currCol > 0:
        if surrCol + 1 <= 14:
            location = 'right'
    else:
        location = 'out of board'
    return location

def checkEdge(move):
# check if is on outer edges of board
    colMove = move[0]
    rowMove = move[1]
    edge = ''

    # if top right corner
    if(colMove == '14' and rowMove == '0'):
        edge = 'top right'
    # if bottom right corner
    elif(colMove == '14' and rowMove == '14'):
        edge = 'bottom right'
    # if top left corner 
    elif(colMove == '0' and rowMove == '0'):
        edge = 'top left'
    # if bottom left corner
    elif(colMove == '0' and rowMove == '14'):
        edge = 'bottom left'
    # if top 
    elif(rowMove == '0'):
        edge = 'top right'
    # if bottom
    elif(rowMove == '14'):
        edge = 'bottom'
    # if left 
    elif(colMove == '0'):
        edge = 'left'
    # if right 
    elif(colMove == '14'):
        edge = 'right'

    return edge

def isEmpty(move, ourMoves, opponentMoves):
# return true if not in opponent or ourmoves
    moveCol = int(move[0])
    moveRow = int(move[1])
    if ((move not in opponentMoves or move not in ourMoves) and moveCol >= 0 and moveCol <= 14 and moveRow <= 14 and moveRow >= 0):
        return True
    else:
        return False

def isBeginner(move, nextMove, board, ourMoves, opponentMoves, ourTeam):
    # return true if the beginning move is empty before, is in a corner or has an opponent before
    colStart = move[0]
    rowStart = move[1]
    colEnd = nextMove[0]
    rowEnd = nextMove[1]
    isAvailable = False
    if ourTeam:
        # if rows are same then horizontal
        # check if start is most left and check conditions above
        if rowStart == rowEnd:
            if ( (checkEdge(move) == 'left') or (checkEdge(move) == 'right') ):
                isAvailable = True
            elif ( ([str(int(colStart - 1)),rowStart] in opponentMoves) or ([str(int(colStart + 1)),rowStart] in opponentMoves) ):
                isAvailable = True
            elif ( (isEmpty([str(int(colStart - 1)),rowStart], ourMoves, opponentMoves)) )or (isEmpty([str(int(colStart + 1)),rowStart], ourMoves, opponentMoves)):
                isAvailable = True
                # if on edge or opponent or empty   
        # if columns are same then vertical
        elif colStart == colEnd:
            if ((checkEdge(move) == 'bottom') or (checkEdge(move) == 'top')):
                isAvailable = True 
            elif ( ([colStart,str(int(rowStart - 1))] in opponentMoves) or ([colStart,str(int(rowStart + 1))] in opponentMoves) ):
                isAvailable = True
            elif ( (isEmpty([colStart,str(int(rowStart - 1))], ourMoves, opponentMoves)) or (isEmpty([colStart,str(int(rowStart + 1))], ourMoves, opponentMoves))):
                isAvailable = True
        # if top right diag
        elif ((int(colStart) > int(colEnd) and int(rowStart) < int(rowEnd)) or (int(colEnd) > int(colStart) and int(rowEnd) < int(rowStart))):
            if ( (checkEdge(move) == 'top right') or (checkEdge(move) == 'bottom left') ):
                    # if on edge or opponent or empty
                return True
            elif ( ([str(int(colStart + 1)), str(int(rowStart - 1))] in opponentMoves) or ([str(int(colStart - 1)), str(int(rowStart + 1))] in opponentMoves) ):
                return True
            elif ( isEmpty([str(int(colStart + 1)), str(int(rowStart - 1))], ourMoves, opponentMoves) or isEmpty([str(int(colStart - 1)), str(int(rowStart + 1))], ourMoves, opponentMoves) ):
                return True
        # if top left diag
        elif ((int(colStart) < int(colEnd) and int(rowStart) > int(rowEnd)) or (int(colEnd) < int(colStart) and int(rowEnd) > int(rowStart))):
            if ( (checkEdge(move) == 'top left') or (checkEdge(move) == 'bottom right') ):
                    # if on edge or opponent or empty
                return True
            elif ( ([str(int(colStart - 1)), str(int(rowStart - 1))] in opponentMoves) or ([str(int(colStart + 1)), str(int(rowStart + 1))] in opponentMoves) ):
                return True
            elif ( isEmpty([str(int(colStart - 1)), str(int(rowStart - 1))], ourMoves, opponentMoves) or isEmpty([str(int(colStart + 1)), str(int(rowStart + 1))], ourMoves, opponentMoves) ):
                return True
          
    elif not ourTeam:
        if rowStart == rowEnd:
            if ( (checkEdge(move) == 'left') or (checkEdge(move) == 'right') ):
                isAvailable = True
            elif ( ([str(int(colStart - 1)),rowStart] in ourMoves) or ([str(int(colStart + 1)),rowStart] in ourMoves) ):
                isAvailable = True
            elif ( (isEmpty([str(int(colStart - 1)),rowStart], ourMoves, opponentMoves)) )or (isEmpty([str(int(colStart + 1)),rowStart], ourMoves, opponentMoves)):
                isAvailable = True
                # if on edge or opponent or empty   
        # if columns are same then vertical
        elif colStart == colEnd:
            if ((checkEdge(move) == 'bottom') or (checkEdge(move) == 'top')):
                isAvailable = True 
            elif ( ([colStart,str(int(rowStart - 1))] in ourMoves) or ([colStart,str(int(rowStart + 1))] in ourMoves) ):
                isAvailable = True
            elif ( (isEmpty([colStart,str(int(rowStart - 1))], ourMoves, opponentMoves)) or (isEmpty([colStart,str(int(rowStart + 1))], ourMoves, opponentMoves))):
                isAvailable = True
        # if top right diag
        elif ((int(colStart) > int(colEnd) and int(rowStart) < int(rowEnd)) or (int(colEnd) > int(colStart) and int(rowEnd) < int(rowStart))):
            if ( (checkEdge(move) == 'top right') or (checkEdge(move) == 'bottom left') ):
                    # if on edge or opponent or empty
                return True
            elif ( ([str(int(colStart + 1)), str(int(rowStart - 1))] in ourMoves) or ([str(int(colStart - 1)), str(int(rowStart + 1))] in ourMoves) ):
                return True
            elif ( isEmpty([str(int(colStart + 1)), str(int(rowStart - 1))], ourMoves, opponentMoves) or isEmpty([str(int(colStart - 1)), str(int(rowStart + 1))], ourMoves, opponentMoves) ):
                return True
        # if top left diag
        elif ((int(colStart) < int(colEnd) and int(rowStart) > int(rowEnd)) or (int(colEnd) < int(colStart) and int(rowEnd) > int(rowStart))):
            if ( (checkEdge(move) == 'top left') or (checkEdge(move) == 'bottom right') ):
                    # if on edge or opponent or empty
                return True
            elif ( ([str(int(colStart - 1)), str(int(rowStart - 1))] in ourMoves) or ([str(int(colStart + 1)), str(int(rowStart + 1))] in ourMoves) ):
                return True
            elif ( isEmpty([str(int(colStart - 1)), str(int(rowStart - 1))], ourMoves, opponentMoves) or isEmpty([str(int(colStart + 1)), str(int(rowStart + 1))], ourMoves, opponentMoves) ):
                return True

    return isAvailable

def getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = 2, loop = True):
    # returns endingPosition, number of in a row 
    surrCol = int(surrMove[0])
    surrRow = int(surrMove[1])
    if counter == 2:
        startingMove = currentMove
    while loop == True:
        # if top right: surrCol - currCol > 0 and surrRow - currRow < 0
        if whereSurrMove(currentMove, surrMove) == 'top right':
            # check empty bottom left if counter == 2
            currentMove = surrMove
            surrMove = [str(surrRow - 1), str(surrCol + 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False

        # if top left: surrCol - currCol < 0 and surrRow - currRow < 0
        elif whereSurrMove(currentMove, surrMove) == 'top left':
            currentMove = surrMove
            surrMove = [str(surrRow - 1), str(surrCol - 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False

        # if bottom left: surrCol - currentMove < 0 and surrRow - currRow > 0
        elif whereSurrMove(currentMove, surrMove) == 'bottom left':
            currentMove = surrMove
            surrMove = [str(surrRow - 1), str(surrCol + 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False

        # if bottom right: surrCol - currentMove > 0 and surrRow - currRow > 0
        elif whereSurrMove(currentMove, surrMove) == 'bottom right':
            currentMove = surrMove
            surrMove = [str(surrRow + 1), str(surrCol + 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False
                
        # if top: surrRow - currRow < 0
        elif whereSurrMove(currentMove, surrMove) == 'top':
            currentMove = surrMove
            surrMove = [str(surrRow - 1), str(surrCol)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False
                
        # if bottom: surrRow - currRow > 0
        elif whereSurrMove(currentMove, surrMove) == 'bottom':
            currentMove = surrMove
            surrMove = [str(surrRow + 1), str(surrCol)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False

        # if left: surrCol - currCol < 0 
        elif whereSurrMove(currentMove, surrMove) == 'left':
            currentMove = surrMove
            surrMove = [str(surrRow), str(surrCol - 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False

        # if right: surrCol - currCol > 0 
        elif whereSurrMove(currentMove, surrMove) == 'right':
            currentMove = surrMove
            surrMove = [str(surrRow), str(surrCol + 1)]
            if ((ourTeam and surrMove in ourMoves) or (not ourTeam and surrMove in opponentMoves)):
                getPosition(currentMove, surrMove, ourMoves, opponentMoves, ourTeam, counter = counter + 1)
            else:
                loop = False
    endingMove = currentMove
    emptySpaces = checkEmpties(startingMove, endingMove, ourMoves, opponentMoves)
    return [endingMove, counter, emptySpaces]

def checkEmpties(startingMove, endingMove, ourMoves, opponentMoves):
# checks empty spaces around starting and ending moves
    colStart = startingMove[0]
    rowStart = startingMove[1]
    colEnd = endingMove[0]
    rowEnd = endingMove[1]
    empty = []
    # if rows are same then horizontal
    if rowStart == rowEnd:
        leftMove = min(int(colStart), int(colEnd))
        rightMove = max(int(colStart), int(colEnd))
        if leftMove - 1 >= 0:
            emptyMove = [str(leftMove - 1), rowStart]
            if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                empty.append(emptyMove)
        if rightMove + 1 <= 14:
            emptyMove = [str(leftMove + 1), rowStart]
            if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                empty.append(emptyMove)
    # if columns are same then vertical
    elif colStart == colEnd:
        bottomMove = max(int(rowStart), int(rowEnd))
        topMove = min(int(rowStart), int(rowEnd))
        if bottomMove + 1 <= 14:
            emptyMove = [colStart, str(bottomMove + 1)]
            if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                empty.append(emptyMove)
        if rightMove - 1 >= 0:
            emptyMove = [colStart, str(topMove - 1)]
            if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                empty.append(emptyMove)
    # else theyre diagonal
    else:
        # if top right diag
        if ((int(colStart) > int(colEnd) and int(rowStart) < int(rowEnd)) or (int(colEnd) > int(colStart) and int(rowEnd) < int(rowStart))):
            bottomLeft = [min(int(colStart),int(colEnd)),max(int(rowEnd),int(rowStart))]
            bottomLeftCol = bottomLeft[0]
            bottomLeftRow = bottomLeft[1]
            topRight = [max(int(colStart),int(colEnd)),min(int(rowEnd),int(rowStart))]
            topRightCol = topRight[0]
            topRightRow = topRight[1]
            if bottomLeftCol - 1 >= 0 and bottomLeftRow + 1 <= 14:
                emptyMove = [str(bottomLeftCol - 1), str(bottomLeftRow + 1)]
                if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                    empty.append(emptyMove)
            if topRightCol + 1 <= 14 and topRightRow - 1 <= 0:
                emptyMove = [str(topRightCol + 1), str(topRightRow - 1)]
                if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                    empty.append(emptyMove)
        # if top left diag
        if ((int(colStart) < int(colEnd) and int(rowStart) > int(rowEnd)) or (int(colEnd) < int(colStart) and int(rowEnd) > int(rowStart))):
            bottomRight = [max(int(colStart),int(colEnd)),min(int(rowEnd),int(rowStart))]
            bottomRightCol = bottomRight[0]
            bottomRightRow = bottomRight[1]
            topLeft = [min(int(colStart),int(colEnd)),max(int(rowEnd),int(rowStart))]
            topLeftCol = topLeft[0]
            topLeftRow = topLeft[1]
            if bottomRightCol + 1 <= 14 and bottomRightRow + 1 <= 14:
                emptyMove = [str(bottomRightCol + 1), str(bottomRightRow + 1)]
                if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                    empty.append(emptyMove)
            if topLeftCol - 1 >= 0 and topLeftRow - 1 >= 0:
                emptyMove = [str(topRightCol - 1), str(topRightRow - 1)]
                if emptyMove not in ourMoves and emptyMove not in opponentMoves:
                    empty.append(emptyMove)

    return empty


def getSurr(position):
    surrounding = []
    column = position[0]
    row = position[1]
    addCol = str(int(column) + 1)
    subCol = str(int(column) - 1)
    addRow = str(int(row) + 1)
    subRow = str(int(row) - 1)
    # if top right corner
    if(column == '14' and row == '0'):
        surrounding = [['13','0'],['13','1'], ['14','1']]
    # if bottom right corner
    elif(column == '14' and row == '14'):
        surrounding = [['14','13'],['13','13'], ['13','14']]
    # if top left corner 
    elif(column == '0' and row == '0'):
        surrounding = [['1','0'],['1','1'], ['0','1']]
    # if bottom left corner
    elif(column == '0' and row == '14'):
        surrounding = [['0','13'],['1','13'], ['1','14']]
    # if top 
    elif(row == '0'):
        surrounding = [[subCol,row],[addCol,row], [subCol,addRow], [column,addRow], [addCol,addRow]]
    # if bottom
    elif(row == '14'):
        surrounding = [[subCol,row], [subCol,subRow], [column, subRow], [addCol, subRow], [addCol, row]] 
    # if left 
    elif(column == '0'):
        surrounding = [[column,subRow], [addCol,subRow], [addCol, row], [addCol, addRow], [column, addRow]]
    # if right 
    elif(column == '14'):
        surrounding = [[column,subRow], [subCol,subRow], [subCol, row], [subCol, addRow], [column, addRow]]
    else:
        surrounding = [[column,subRow], [subCol,subRow], [subCol, row], [subCol, addRow], [column, addRow], [addCol, row], [addCol, addRow], [column, addRow]]
    
    return surrounding
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

