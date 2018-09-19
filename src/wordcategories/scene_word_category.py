'''
Created on 23Nov.,2016

@author: fatdunky
'''
from .word_category import WordCategory

class SceneWordCategory(WordCategory):
    '''
    This class defines a word as a common word i.e "a, the, because"
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(SceneWordCategory,self).__init__()
    

    def heuristic_match(self):
        pass
        