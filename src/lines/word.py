'''
Created on 20Nov.,2016

@author: fatdunky
'''

from lines.wordcategories.word_category import WordCategory
from lines.wordcategories.unmatched_word_category import UnmatchedWordCategory

class Word(object):
    '''
    This class defines a word object
    '''

    def __init__(self, text):
        '''
        Constructor
        '''
        self.__text = text
        self.__category = WordCategory.match_word_category(text)
        if self.__category is None:
            self.__category = UnmatchedWordCategory()

    def get_text(self):
        return self.__text


    def get_category(self):
        return self.__category


    def set_text(self, value):
        self.__text = value


    def set_category(self, value):
        self.__category = value


    def del_text(self):
        del self.__text
 

    def del_category(self):
        del self.__category

           
    def __repr__(self):
        return self.__text + ' (' + self.__category.__class__.__name__  +')' 
    
    text = property(get_text, set_text, del_text, "text's docstring")
    category = property(get_category, set_category, del_category, "category's docstring")
