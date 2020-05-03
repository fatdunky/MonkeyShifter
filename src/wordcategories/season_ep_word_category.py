'''
Created on 23Nov.,2016

@author: fatdunky
'''
from .word_category import WordCategory

class SeasonEpisodeWordCategory(WordCategory):
    '''
    This class defines a tv season an episode i.e "S02E01"
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(SeasonEpisodeWordCategory,self).__init__()
    

    def heuristic_match(self):
        pass
        