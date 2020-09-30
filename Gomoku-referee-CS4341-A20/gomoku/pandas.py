import logging
import sys
import os
import random
import time
import hashlib
import shutil
import copy

'''
pass in state of board and move history to help start the algorithm
'''
def makeGameTree():
    '''
    utility function needed to help algorithm determine which move is best 
    '''
    
    temp = 'pandas.py A 1'
    writeMoveFile(temp)

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

if __name__ == "__main__":
    while not os.path.exists(pandas.py.go):   
        time.sleep(1)
    if os.path.isfile(file_path):  
        makeGameTree()

