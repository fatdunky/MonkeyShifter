'''
Created on 23Nov.,2016

@author: fatdunky
'''
from lines.wordcategories.word_category import WordCategory

class TechnicalWordCategory(WordCategory):
    '''
    This class defines a word as a common word i.e "a, the, because"
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(TechnicalWordCategory,self).__init__()
        
    

    def heuristic_match(self):
        pass
        