'''
Created on 23Nov.,2016

@author: fatdunky
'''
from .word_category import WordCategory

class CommonWordCategory(WordCategory):
    '''
    This class defines a word as a common word i.e "a, the, because"
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(CommonWordCategory,self).__init__()
    

    def heuristic_match(self):
        pass
        