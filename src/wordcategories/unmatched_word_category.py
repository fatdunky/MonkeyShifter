'''
Created on 23Nov.,2016

@author: fatdunky
'''
from .word_category import WordCategory

class UnmatchedWordCategory(WordCategory):
    '''
    This class catches all unmatched
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(UnmatchedWordCategory,self).__init__()
        
    

    def heuristic_match(self):
        pass
        