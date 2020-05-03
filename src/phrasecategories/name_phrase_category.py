'''
Created on 23Nov.,2016

@author: fatdunky
'''
from lines.phrasecategories.phrase_category import PhraseCategory

class NamePhraseCategory(PhraseCategory):
    '''
    This class catches all unmatched
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(NamePhraseCategory,self).__init__()
        
    

    def heuristic_match(self):
        pass
        