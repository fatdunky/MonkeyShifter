'''
Created on 20Nov.,2016

@author: fatdunky
'''
from lines.word import Word
import re, logging
from lines.wordcategories.unmatched_word_category import UnmatchedWordCategory

class Line(object):
    '''
    Class representing a line of text. It will be made of of word classes.
    '''


    def __init__(self):
        '''
        Constructor for an empty line
        '''
        self.__words = []
        self.__origional_line = ""
    

    def get_words(self):
        return self.__words


    def set_words(self, value):
        self.__words = value


    def del_words(self):
        del self.__words

    
    def add_word(self, Word):
        '''
        Add a word to the line
        '''
        self.words.append(Word)
    
    #def update_word_category(self):
        
    
    
    def split_line(self, line, delimeters):
        '''
        Splits the given string into words
        Return a list of any unmatched words
        '''
        unmatched_words = []
        self.__origional_line = line
        line_to_split = self.get_line_with_out_filename()
        for wordString in re.split("["+delimeters+"]+", line_to_split):
            currentWord = Word(wordString.rstrip())
            self.add_word(currentWord)
            if (isinstance(currentWord.get_category(),UnmatchedWordCategory)):
                unmatched_words.append(currentWord)
        
        return unmatched_words
            
    def get_last_right_of_dot_in_line(self):
        '''
        Return the string right of the . 
        '''
        strings = self.__origional_line.split(".")
        return self.__origional_line[self.__origional_line.rfind(".")+1:]

    def get_line_with_out_filename(self):
        filename = self.get_last_right_of_dot_in_line()
        if (self.__origional_line.endswith(filename)):
            retval = self.__origional_line[:self.__origional_line.rfind(".")]
        else:
            retval = self.__origional_line
        return retval
                   
    words = property(get_words, set_words, del_words, "words's docstring")
        
        